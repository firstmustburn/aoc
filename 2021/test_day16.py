import pytest

from day16 import *

def test_bits_to_int():
    bits = bitarray('111001111000')
    offset = 0
    value, offset = bits_to_int(bits, offset, 3)
    assert value == 7
    assert offset == 3
    value, offset = bits_to_int(bits, offset, 4)
    assert value == 3
    assert offset == 7
    value, offset = bits_to_int(bits, offset, 5)
    assert value == 24
    assert offset == 12
    with pytest.raises(RuntimeError):
        bits_to_int(bits, offset, 1)
    
def test_process_literal_payload():
    bits = bitarray('11111111110000010')
    offset = 0
    value, offset = process_literal_payload(bits, offset)
    assert value == 4080 #111111110000 --> 4080
    assert offset == 15

    bits = bitarray('01111111110000010')
    offset = 0
    value, offset = process_literal_payload(bits, offset)
    assert value == 15 #1111 --> 15
    assert offset == 5
    value, offset = process_literal_payload(bits, offset)
    assert value == 240 #11110000 --> 240
    assert offset == 15


def test_parse_single_packet():

    bits = hex2ba('D2FE28')
    offset = 0
    packet, offset = parse_single_packet(bits, offset)
    assert offset == 21
    assert isinstance(packet, LiteralPacket)
    assert packet.version == 6
    assert packet.ptype == 4
    assert packet.value == 2021

    #                       VVVTTTPPPPPVVVTTTPPPPPPPPPP
    # 00111000000000000110111101000101001010010001001000000000
    # VVVTTTILLLLLLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBBBBBB
    bits = hex2ba('38006F45291200')
    offset = 0
    packet, offset = parse_single_packet(bits, offset)
    assert offset == 49
    assert isinstance(packet, OperatorPacket)
    assert packet.version == 1
    assert packet.ptype == 6
    assert len(packet.subpackets) == 2
    sp = packet.subpackets[0]
    assert sp.version == 6
    assert sp.ptype == 4
    assert sp.value == 10
    sp = packet.subpackets[1]
    assert sp.version == 2
    assert sp.ptype == 4
    assert sp.value == 20 #00010100

    #                   VVVTTTPPPPPVVVTTTPPPPPVVVTTTPPPPP
    # 11101110000000001101010000001100100000100011000001100000
    # VVVTTTILLLLLLLLLLLAAAAAAAAAAABBBBBBBBBBBCCCCCCCCCCC
    bits = hex2ba('EE00D40C823060')
    offset = 0
    packet, offset = parse_single_packet(bits, offset)
    assert offset == 51
    assert isinstance(packet, OperatorPacket)
    assert packet.version == 7
    assert packet.ptype == 3
    assert len(packet.subpackets) == 3
    sp = packet.subpackets[0]
    assert sp.version == 2
    assert sp.ptype == 4
    assert sp.value == 1
    sp = packet.subpackets[1]
    assert sp.version == 4
    assert sp.ptype == 4
    assert sp.value == 2
    sp = packet.subpackets[2]
    assert sp.version == 1
    assert sp.ptype == 4
    assert sp.value == 3

# 8A004A801A8002F478 represents an operator packet (version 4) which contains an operator packet 
# (version 1) which contains an operator packet (version 5) which contains a literal value (version 6); this packet has a version sum of 16.

# 620080001611562C8802118E34 represents an operator packet (version 3) which contains two sub-packets; 
# each sub-packet is an operator packet that contains two literal values. This packet has a version sum of 12.

# C0015000016115A2E0802F182340 has the same structure as the previous example, but the outermost packet 
# uses a different length type ID. This packet has a version sum of 23.

# A0016C880162017C3686B18A3D4780 is an operator packet that contains an operator packet that contains
# an operator packet that contains five literal values; it has a version sum of 31.

def test_part1():
    sum, _ = part1('8A004A801A8002F478')
    assert sum == 16
    sum, _ = part1('620080001611562C8802118E34')
    assert sum == 12
    sum, _ = part1('C0015000016115A2E0802F182340')
    assert sum == 23
    sum, _ = part1('A0016C880162017C3686B18A3D4780')
    assert sum == 31

# C200B40A82 finds the sum of 1 and 2, resulting in the value 3.
# 04005AC33890 finds the product of 6 and 9, resulting in the value 54.
# 880086C3E88112 finds the minimum of 7, 8, and 9, resulting in the value 7.
# CE00C43D881120 finds the maximum of 7, 8, and 9, resulting in the value 9.
# D8005AC2A8F0 produces 1, because 5 is less than 15.
# F600BC2D8F produces 0, because 5 is not greater than 15.
# 9C005AC2F8F0 produces 0, because 5 is not equal to 15.
# 9C0141080250320F1802104A08 produces 1, because 1 + 3 = 2 * 2.

def test_part2():
    value = part2('C200B40A82')
    assert value == 3
    value = part2('04005AC33890')
    assert value == 54
    value = part2('880086C3E88112')
    assert value == 7
    value = part2('CE00C43D881120')
    assert value == 9
    value = part2('D8005AC2A8F0')
    assert value == 1
    value = part2('F600BC2D8F')
    assert value == 0
    value = part2('9C005AC2F8F0')
    assert value == 0
    value = part2('9C0141080250320F1802104A08')
    assert value == 1

if __name__ == "__main__":
    test_part2()