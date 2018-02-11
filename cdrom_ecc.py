from cdrom_ecc_tables import EDC_crctable, L2sq


def crc32(data):
    result = 0
    for value in data:
        result = EDC_crctable[(result ^ ord(value)) & 0xFF] ^ (result >> 8)
    return result


L2_RAW = 0x800
L2_P = 43*2*2
L2_Q = 26*2*2


def encode_L2_P(data):
    base_index = 0
    P_index = 4 + L2_RAW + 4 + 8
    target_size = P_index + L2_P
    data = map(ord, data) + ([None] * (target_size-len(data)))
    assert len(data) == target_size
    for j in xrange(43):
        a, b = 0, 0
        index = base_index
        for i in xrange(19, 43):
            assert index < P_index-1
            a ^= L2sq[i][data[index]]
            b ^= L2sq[i][data[index+1]]
            index += (2*43)

        data[P_index] = a >> 8
        data[P_index + (43*2)] = a & 0xFF
        data[P_index + 1] = b >> 8
        data[P_index + (43*2) + 1] = b & 0xFF
        base_index += 2
        P_index += 2
    assert None not in data
    return data


def encode_L2_Q(data):
    base_index = 0
    Q_index = 4 + L2_RAW + 4 + 8 + L2_P
    MOD_INDEX = Q_index
    target_size = Q_index + L2_Q
    data = data + ([None] * (target_size-len(data)))
    assert len(data) == target_size
    counter = 0
    for j in xrange(26):
        a, b = 0, 0
        index = base_index
        for i in xrange(43):
            a ^= L2sq[i][data[index]]
            b ^= L2sq[i][data[index+1]]
            index += (2*44)
            index = index % MOD_INDEX
        data[Q_index] = a >> 8
        data[Q_index + (26*2)] = a & 0xFF
        data[Q_index + 1] = b >> 8
        data[Q_index + (26*2) + 1] = b & 0xFF
        base_index += (2*43)
        Q_index += 2
        counter += 1
    assert None not in data
    return data


def get_edc_ecc(data):
    #  -data- is a string of bytes:
    #  12-byte sync
    #  4-byte address and flag
    #  2048-bytes program data.
    #  The following will be added to -data-:
    #  4 byte EDC, 8 byte zero field, 276 ECC

    assert len(data) == 0x810
    edc = crc32(data[0x00:0x810])  # 4-byte EDC

    for _ in xrange(4):
        data += chr(edc & 0xFF)  # Add least byte of EDC to -data-.
        edc >>= 8                # Remove least byte from the EDC variable.
    assert len(data) == 0x814    # -data- should now include the EDC

    data += chr(0)*8
    temp = encode_L2_P(data[0x0C:])
    temp = encode_L2_Q(temp)

    # Add 276 byte ECC to data.
    data += "".join(map(chr, temp[-0x114:]))
    assert len(data) == 0x930

    # Return EDC, ECC, data
    return data[0x810:0x814], data[0x81C:], data
