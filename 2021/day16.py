from bitarray import bitarray
from bitarray.util import hex2ba, ba2int

def debug(*args):
    print(*args)

class LiteralPacket:
    
    def __init__(self, version, ptype, value):
        self.version = version
        self.ptype = ptype
        self.value = value

    def is_literal(self):
        return True

    def is_operator(self):
        return False

    def get_value(self):
        return self.value

    def __str__(self):
        return f'Literal({self.version}, {self.ptype}, {self.value})'

    def __repr__(self):
        return self.__str__()

def sum_operator(operands):
    total = 0
    for operand in operands:
        total += operand
    result =  total
    debug("sum", operands, "=", result)
    return result


def product_operator(operands):
    total = 1
    for operand in operands:
        total *= operand
    result =  total
    debug("product", operands, "=", result)
    return result

def min_operator(operands):
    result =  min(operands)
    debug("min", operands, "=", result)
    return result

def max_operator(operands):
    result =  max(operands)
    debug("max", operands, "=", result)
    return result


def gt_operator(operands):
    assert len(operands) == 2
    if operands[0] > operands[1]:
        result =  1
    else:
        result =  0
    debug("gt", operands, "=", result)
    return result

def lt_operator(operands):
    assert len(operands) == 2
    if operands[0] < operands[1]:
        result =  1
    else:
        result =  0
    debug("lt", operands, "=", result)
    return result

def eq_operator(operands):
    assert len(operands) == 2
    if operands[0] == operands[1]:
        result =  1
    else:
        result =  0
    debug("eq", operands, "=", result)
    return result

class OperatorPacket:

    operators = {
        0: sum_operator,
        1: product_operator,
        2: min_operator,
        3: max_operator,
        5: gt_operator,
        6: lt_operator,
        7: eq_operator,
    }


    def __init__(self, version, ptype, subpackets):
        self.version = version
        self.ptype = ptype
        self.subpackets = subpackets
    
    def is_literal(self):
        return False

    def is_operator(self):
        return True

    def get_value(self):
        op_fcn = self.operators[self.ptype]
        return op_fcn([ p.get_value() for p in self.subpackets ])

    def __str__(self):
        subpacket_str = ','.join([str(sp) for sp in self.subpackets])
        return f'Operator({self.version}, {self.ptype}, [{subpacket_str}])'

    def __repr__(self):
        return self.__str__()


LITERAL_PTYPE=4

def load_data(filename):
    with open(filename) as infile:
        data = infile.read().strip()
    return data

def bits_to_int(bits, offset, length):
    if offset + length > len(bits):
        raise RuntimeError("Overrun in bits_to_int")
    value = ba2int(bits[offset:offset+length])
    return value, offset + length

def process_literal_payload(bits, start_offset):
    more_chunks = True
    literal_val = bitarray()
    offset = start_offset
    while more_chunks:
        #process the chunk at offset
        more_chunks = (bits[offset] == 1)
        literal_val.extend(bits[offset+1:offset+5])
        # print("literal_val", literal_val)
        #incrment the offset
        offset += 5
    return ba2int(literal_val), offset

def process_operator_payload(bits, start_offset):
    offset = start_offset
    is_byte_length_type = (bits[offset] == 0)
    offset += 1
    if is_byte_length_type:
        bit_length, offset = bits_to_int(bits, offset, 15)
        sub_packets, _ = parse_stream(bits[offset:offset+bit_length], 0)
        offset += bit_length
        return sub_packets, offset
    else: #is number of packets length type
        num_packets, offset = bits_to_int(bits, offset, 11)
        sub_packets = []
        for i in range(num_packets):
            packet, offset = parse_single_packet(bits, offset)
            sub_packets.append(packet)
        return sub_packets, offset

def parse_single_packet(bits, start_offset):
    offset=start_offset
    version, offset = bits_to_int(bits, offset, 3)
    ptype, offset = bits_to_int(bits, offset, 3)
    if ptype==LITERAL_PTYPE:
        payload, offset = process_literal_payload(bits, offset)
        return LiteralPacket(version, ptype, payload), offset
    else:
        payload, offset = process_operator_payload(bits, offset)
        return OperatorPacket(version, ptype, payload), offset

def parse_stream(bits, start_offset):
    offset=start_offset
    packets = []
    while 1:
        packet, offset = parse_single_packet(bits, offset)
        packets.append(packet)
        if not bits[offset:].any():
            break
    return packets, offset        

def sum_versions(packets):
    sum = 0
    for packet in packets:
        sum += packet.version
        if packet.is_operator():
            sum += sum_versions(packet.subpackets)
    return sum

def part1(hexstring):
    bits = hex2ba(hexstring)
    packets, _ = parse_stream(bits, 0)
    sum = sum_versions(packets)
    return sum, packets

def part2(hexstring):
    print("hexstring", hexstring)
    bits = hex2ba(hexstring)
    packets, _ = parse_stream(bits, 0)
    print("packets", packets)
    assert len(packets) == 1
    return packets[0].get_value()

if __name__ == "__main__":

    #part 1
    hexdata = load_data('day16.txt')
    sum, packets = part1(hexdata)
    for packet in packets:
        print(packet)
    print("sum", sum)

    print("value", packets[0].get_value())

    # sum 860
    # value 470949537659