"""Read ISO BMFF timing/sample metadata without changing media."""
import json
import struct
import sys
from pathlib import Path


def boxes(data, start, end):
    offset = start
    while offset + 8 <= end:
        size, kind = struct.unpack_from('>I4s', data, offset)
        header = 8
        if size == 1:
            size = struct.unpack_from('>Q', data, offset + 8)[0]
            header = 16
        elif size == 0:
            size = end - offset
        if size < header or offset + size > end:
            raise ValueError(f'Invalid box at {offset}')
        yield kind.decode('ascii'), offset + header, offset + size
        offset += size


def timing(data, pos):
    version = data[pos]
    cursor = pos + (20 if version else 12)
    scale = struct.unpack_from('>I', data, cursor)[0]
    duration = struct.unpack_from('>Q' if version else '>I', data, cursor + 4)[0]
    return dict(timescale=scale, duration=duration, seconds=duration / scale)


def inspect(path):
    data = Path(path).read_bytes()
    result = dict(path=str(Path(path).resolve()), bytes=len(data), tracks=[])
    for kind, begin, end in boxes(data, 0, len(data)):
        if kind != 'moov':
            continue
        for kind2, begin2, end2 in boxes(data, begin, end):
            if kind2 == 'mvhd':
                result['movie'] = timing(data, begin2)
            if kind2 != 'trak':
                continue
            track = {}
            for kind3, begin3, end3 in boxes(data, begin2, end2):
                if kind3 != 'mdia':
                    continue
                for kind4, begin4, end4 in boxes(data, begin3, end3):
                    if kind4 == 'mdhd':
                        track.update(timing(data, begin4))
                    elif kind4 == 'hdlr':
                        track['handler'] = data[begin4 + 8:begin4 + 12].decode('ascii')
                    elif kind4 == 'minf':
                        for k5, b5, e5 in boxes(data, begin4, end4):
                            if k5 != 'stbl':
                                continue
                            for k6, b6, e6 in boxes(data, b5, e5):
                                if k6 == 'stsz':
                                    track['samples'] = struct.unpack_from('>I', data, b6 + 8)[0]
            result['tracks'].append(track)
    return result


for argument in sys.argv[1:]:
    print(json.dumps(inspect(argument), indent=2))
