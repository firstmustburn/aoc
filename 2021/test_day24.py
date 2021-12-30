from day24 import *



def test_day24_binary_prog():
    data = """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2
"""
    lines = data.strip().split("\n")

    alu = ALU()
    program = alu.parse_instructions(lines)

    for input_val in range(16):

        state = ALUstate()
        alu.run_instruction_sequence(state, program, input_val)
        print(f"Input {input_val} -> state {state}")
        assert state.registers['w'] == (input_val & 8) >> 3
        assert state.registers['x'] == (input_val & 4) >> 2
        assert state.registers['y'] == (input_val & 2) >> 1
        assert state.registers['z'] == (input_val & 1)


    
    