from dataclasses import dataclass, field
from os import PathLike

from PIL import Image
from typing_extensions import Union, IO, Any, Optional, Literal

from archerdfu.reticle2 import rle
from archerdfu.reticle2._containers import FixedSizeList, RestrictedDict
from archerdfu.reticle2.typedefs import (Reticle2Type, PXL4ID, PXL8ID, PXL4_ZOOM_COUNT, PXL8_ZOOM_COUNT,
                                         SMALL_RETICLES_COUNT, HOLD_RETICLES_COUNT,
                                         TReticle2FileHeaderSize, TReticle2Index, TReticle2Build, TReticle2Parse)


@dataclass(unsafe_hash=True)
class Reticle2Frame:
    _rle: bytes = field(init=False, default=b'', compare=True, repr=False)
    _img: Optional[Image.Image] = field(init=False, default=None, compare=False)

    def __init__(self, __o: Union[bytes, Image.Image, None] = None):
        if __o is not None:
            if isinstance(__o, bytes):
                self.rle = __o
            elif isinstance(__o, Image.Image):
                self.img = __o
            else:
                raise TypeError('__o must be bytes or Image.Image')

    def __len__(self) -> int:
        return len(self._rle)

    @property
    def rle(self) -> bytes:
        return self._rle

    @property
    def img(self) -> Image.Image:
        return self._img

    @rle.setter
    def rle(self, buffer: bytes):
        self._rle = buffer
        self._img = rle.decode(buffer)

    @img.setter
    def img(self, img: Image.Image):
        self._img = img
        self._rle = rle.encode(img)

    def save(self, fp: str | bytes | PathLike[str] | PathLike[bytes] | IO[bytes],
             format: str | None = None,
             **params: Any) -> None:
        self._img.save(fp, format, **params)

    def open(self, fp: str | bytes | PathLike[str] | PathLike[bytes] | IO[bytes],
             mode: Literal["r"] = "r",
             formats: list[str] | tuple[str, ...] | None = None) -> None:
        self.img = Image.open(fp, mode, formats)


class Reticle2(FixedSizeList):
    value_type = Optional[Reticle2Frame]

    def __init__(self, *frames):
        if not all(isinstance(f, self.value_type) for f in frames):
            raise TypeError("Value should be a type of Reticle2Frame or None")
        super().__init__(*frames, size=8)

    def __setitem__(self, index, value):
        if not (0 <= index < self._size):
            raise IndexError("Index out of range")
        if not isinstance(value, self.value_type):
            raise TypeError("Value should be a type of Reticle2Frame or None")
        super().__setitem__(index, value)

    def __eq__(self, other):
        if not isinstance(other, Reticle2):
            return False
        return tuple(self) == tuple(other)

    def __hash__(self):
        return hash(tuple(self))  # Convert list to tuple for hashing


class Reticle2ListContainer(list):
    value_type = Optional[Reticle2]

    def __init__(self, *reticles):
        if not all(isinstance(r, self.value_type) for r in reticles):
            raise TypeError("Value should be a type of Reticle2 or None")
        super().__init__(reticles)

    def __setitem__(self, index, value):
        if not isinstance(value, self.value_type):
            raise TypeError("Value should be a type of Reticle2 or None")
        super().__setitem__(index, value)

    def __repr__(self):
        return f"<{self.__class__.__name__}({super().__repr__()})>"


class Reticle2Container(RestrictedDict):
    allowed_keys = {'small', 'hold', 'base', 'lrf'}
    value_type = Optional[Reticle2ListContainer]

    small: Reticle2ListContainer
    hold: Reticle2ListContainer
    base: Reticle2ListContainer
    lrf: Reticle2ListContainer

    def encode(self, __type: Reticle2Type = PXL4ID, *, encode_hold=False) -> bytes:
        return _Compressor().compress(self, __type, compress_hold=encode_hold)

    @staticmethod
    def decode(__b: bytes, *, decode_hold: bool = False) -> 'Reticle2Container':
        return _Compressor.decompress(__b, decompress_hold=decode_hold)


class _Compressor:
    def __init__(self):
        self.indexes = []
        self.base_offset = 0
        self.offset = 0
        self.last_hash = None
        self.buffer = bytearray()

    def _compress_reticle_list(self, __list: Optional[Reticle2ListContainer], reticle_count, zoom_count) -> int:
        start_buf_len = len(self.buffer)

        if not __list:
            self.indexes.extend([self.indexes[-1]] * reticle_count * zoom_count)
            return 0

        for i in range(reticle_count):
            for z in range(zoom_count):

                try:
                    zoom = __list[i][z]
                    if zoom is None or hash(zoom) == self.last_hash:
                        raise IndexError("Empty or non-unique")
                except IndexError:
                    # writing previous index
                    self.indexes.append(self.indexes[-1])
                else:
                    # writing new zoom data
                    self.buffer += zoom.rle
                    self.indexes.append({'offset': self.offset, 'quant': len(zoom) // 4})
                    self.offset = self.base_offset + len(self.buffer)
                    self.last_hash = hash(zoom)

        return len(self.buffer) - start_buf_len

    def compress(self, __o: Reticle2Container, __type: Reticle2Type = PXL4ID, *, compress_hold=False):
        self.__init__()

        if __type == PXL4ID:
            zoom_count = PXL4_ZOOM_COUNT
        elif __type == PXL8ID:
            zoom_count = PXL8_ZOOM_COUNT
        else:
            raise TypeError("Unsupported reticle2 type {!r}".format(__type))

        header_size = TReticle2FileHeaderSize
        small_reticles_count = SMALL_RETICLES_COUNT if __o.small else 0
        hold_reticles_count = HOLD_RETICLES_COUNT if compress_hold else 0
        base_reticles_count = len(__o.base) if __o.base else 0
        lrf_reticles_count = len(__o.lrf) if __o.lrf else 0
        reticles_count = small_reticles_count + hold_reticles_count + base_reticles_count + lrf_reticles_count
        index_size = reticles_count * zoom_count * TReticle2Index.sizeof()

        self.base_offset = header_size + index_size
        self.offset = self.base_offset

        small_offset = self.offset
        small_size = self._compress_reticle_list(__o.small, small_reticles_count, zoom_count)
        hold_offset = self.offset
        if compress_hold:
            hold_size = self._compress_reticle_list(__o.hold, hold_reticles_count, zoom_count)
        else:
            hold_size = 0
        base_offset = self.offset
        base_size = self._compress_reticle_list(__o.base, base_reticles_count, zoom_count)
        lrf_offset = self.offset
        lrf_size = self._compress_reticle_list(__o.lrf, lrf_reticles_count, zoom_count)

        header = {
            'PXLId': __type,
            'ReticleCount': reticles_count,
            'SizeOfAllDataPXL2': header_size + index_size + len(self.buffer),

            'SmallCount': SMALL_RETICLES_COUNT,
            'OffsetSmall': small_offset,
            'SmallSize': small_size,

            'HoldOffCount': hold_reticles_count,
            'OffsetHoldOff': hold_offset,
            'HoldOffSize': hold_size,
            'HoldOffCrc': 0,

            'BaseCount': base_reticles_count,
            'OffsetBase': base_offset,
            'BaseSize': base_size,

            'LrfCount': lrf_reticles_count,
            'OffsetLrf': lrf_offset,
            'LrfSize': lrf_size,
        }

        return TReticle2Build.build({
            'header': header,
            'index': self.indexes,
            'data': self.buffer,
        })

    @staticmethod
    def decompress(__b: bytes, *, decompress_hold: bool = False) -> 'Reticle2Container':
        container = TReticle2Parse.parse(__b)

        index, rle = None, None

        reticle_container = Reticle2Container()

        if decompress_hold:
            keys = ('small', 'hold', 'base', 'lrf')
        else:
            keys = ('small', 'base', 'lrf')

        for key in keys:
            reticles_list = Reticle2ListContainer()
            for i, subcon in enumerate(container.index[key]):
                reticle = Reticle2()
                for z, zoom in enumerate(subcon):
                    _index = zoom
                    if _index != index:
                        _rle = container.reticles[key][i][z]
                        if _rle != rle:
                            reticle[z] = Reticle2Frame(_rle)
                            rle = _rle
                        index = _index
                reticles_list.append(reticle)
            reticle_container[key] = reticles_list
        return reticle_container


if __name__ == "__main__":
    reticle = Reticle2Container(
        small=Reticle2ListContainer(
            Reticle2(
                Reticle2Frame()
            )
        )
    )
    print(reticle)
