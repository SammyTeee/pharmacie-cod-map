"""Small LZ4 block reader for validating BO3's export2bin envelope.

An existing file/zero exit is insufficient: generic compression can wrap plain
text in the same envelope. Models must contain the MODEL binary token.
"""
import struct


def unpack_lz4(data):
    if data[:5] != b'*LZ4*':
        raise ValueError('Not a BO3 LZ4 envelope')
    size = struct.unpack_from('<I',data,5)[0]
    source, out, i = data[9:], bytearray(), 0
    while i < len(source):
        token = source[i]
        i += 1
        literal = token >> 4
        if literal == 15:
            while True:
                n = source[i]
                i += 1
                literal += n
                if n != 255:
                    break
        out.extend(source[i:i+literal])
        i += literal
        if i == len(source):
            break
        offset = struct.unpack_from('<H',source,i)[0]
        i += 2
        if not offset or offset > len(out):
            raise ValueError('Invalid LZ4 back reference')
        length = (token & 15)+4
        if token & 15 == 15:
            while True:
                n = source[i]
                i += 1
                length += n
                if n != 255:
                    break
        for _ in range(length):
            out.append(out[-offset])
    if len(out) != size:
        raise ValueError('Wrong LZ4 expanded size')
    return bytes(out)


def validate_model_binary(path):
    tokens = unpack_lz4(path.read_bytes())
    # MODEL token, padded to four bytes; VERSION token followed by uint16.
    if tokens[:6] != bytes.fromhex('c8460000d124'):
        raise ValueError('Envelope does not contain binary MODEL/VERSION tokens')
    version = struct.unpack_from('<H',tokens,6)[0]
    if version != 7:
        raise ValueError('Expected BO3 model version 7, got '+str(version))
    return version
