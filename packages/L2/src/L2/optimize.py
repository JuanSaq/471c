from .constant_folding import constant_folding_term
from .constant_prop import constant_propagation_term
from .dead_code_elim import dead_code_elimination_term
from .syntax import Program


def optimize_program_part(
    program: Program,
) -> Program:
    optimized = program

    optimized = Program(parameters=optimized.parameters, body=constant_propagation_term(optimized.body, {}))

    optimized = Program(parameters=optimized.parameters, body=constant_folding_term(optimized.body, {}))

    optimized = Program(parameters=optimized.parameters, body=dead_code_elimination_term(optimized.body, {}))

    return optimized


def optimize_program(
    program: Program,
) -> Program:
    while True:
        optimized = optimize_program_part(program)
        if optimized == program:
            return program
        program = optimized
