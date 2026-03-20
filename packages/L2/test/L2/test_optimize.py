from L2.constant_folding import constant_folding_term
from L2.constant_prop import constant_propagation_term
from L2.dead_code_elim import dead_code_elimination_term, free_variables
from L2.optimize import optimize_program
from L2.syntax import (
    Abstract,
    Allocate,
    Apply,
    Begin,
    Branch,
    Immediate,
    Let,
    Load,
    Primitive,
    Program,
    Reference,
    Store,
)

# constant prop


def test_constant_propagation_let_and_primitive():
    term = Let(
        bindings=[("x", Immediate(value=5))],
        body=Primitive(
            operator="+",
            left=Reference(name="x"),
            right=Immediate(value=3),
        ),
    )

    expected = Let(
        bindings=[
            (
                "x",
                Immediate(value=5),
            )
        ],
        body=Primitive(
            operator="+",
            left=Immediate(value=5),
            right=Immediate(value=3),
        ),
    )

    actual = constant_propagation_term(term=term, context={})

    assert actual == expected


def test_constant_propagation_let_and_branch():
    term = Let(
        bindings=[("x", Immediate(value=5))],
        body=Branch(
            operator="<",
            left=Reference(name="x"),
            right=Immediate(value=10),
            consequent=Allocate(count=1),
            otherwise=Store(base=Reference(name="y"), index=0, value=Immediate(value=0)),
        ),
    )

    expected = Let(
        bindings=[
            (
                "x",
                Immediate(value=5),
            )
        ],
        body=Branch(
            operator="<",
            left=Immediate(value=5),
            right=Immediate(value=10),
            consequent=Allocate(count=1),
            otherwise=Store(base=Reference(name="y"), index=0, value=Immediate(value=0)),
        ),
    )

    actual = constant_propagation_term(term=term, context={})

    assert actual == expected


def test_constant_propagation_no_context_reference():
    term = Reference(name="y")

    expected = Reference(name="y")

    actual = constant_propagation_term(term=term, context={})

    assert actual == expected


def test_constant_propagation_abstract_and_apply():
    term = Abstract(
        parameters=["x"],
        body=Apply(
            target=Reference(name="x"),
            arguments=[Reference(name="y")],
        ),
    )

    expected = Abstract(
        parameters=["x"],
        body=Apply(
            target=Reference(name="x"),
            arguments=[Immediate(value=25)],
        ),
    )

    actual = constant_propagation_term(term=term, context={"y": Immediate(value=25)})

    assert actual == expected


def test_constant_propagation_load():
    term = Begin(effects=[], value=Load(base=Reference(name="x"), index=0))

    expected = Begin(effects=[], value=Load(base=Immediate(value=1), index=0))

    actual = constant_propagation_term(term=term, context={"x": Immediate(value=1)})

    assert actual == expected


# constant folding


def test_constant_folding_let_and_primitive_add():
    term = Let(
        bindings=[("x", Immediate(value=5))],
        body=Primitive(
            operator="+",
            left=Immediate(value=1),
            right=Immediate(value=1),
        ),
    )

    expected = Let(
        bindings=[
            (
                "x",
                Immediate(value=5),
            )
        ],
        body=Immediate(value=2),
    )

    actual = constant_folding_term(term=term, context={})

    assert actual == expected


def test_constant_folding_let_and_primitive_multiply():
    term = Let(
        bindings=[("x", Immediate(value=5))],
        body=Primitive(
            operator="*",
            left=Immediate(value=2),
            right=Immediate(value=2),
        ),
    )

    expected = Let(
        bindings=[
            (
                "x",
                Immediate(value=5),
            )
        ],
        body=Immediate(value=4),
    )

    actual = constant_folding_term(term=term, context={})

    assert actual == expected


def test_constant_folding_let_and_primitive_subtract():
    term = Let(
        bindings=[("x", Immediate(value=5))],
        body=Primitive(
            operator="-",
            left=Immediate(value=2),
            right=Immediate(value=2),
        ),
    )

    expected = Let(
        bindings=[
            (
                "x",
                Immediate(value=5),
            )
        ],
        body=Immediate(value=0),
    )

    actual = constant_folding_term(term=term, context={})

    assert actual == expected


def test_constant_folding_primitive_not_all_immediate():
    term = Primitive(
        operator="+",
        left=Reference(name="x"),
        right=Immediate(value=3),
    )

    expected = Primitive(
        operator="+",
        left=Reference(name="x"),
        right=Immediate(value=3),
    )

    actual = constant_folding_term(term=term, context={})

    assert actual == expected


def test_constant_folding_let_and_branch_less():
    term = Let(
        bindings=[("x", Immediate(value=5))],
        body=Branch(
            operator="<",
            left=Immediate(value=1),
            right=Immediate(value=10),
            consequent=Allocate(count=1),
            otherwise=Store(base=Reference(name="y"), index=0, value=Immediate(value=0)),
        ),
    )

    expected = Let(
        bindings=[
            (
                "x",
                Immediate(value=5),
            )
        ],
        body=Allocate(count=1),
    )

    actual = constant_folding_term(term=term, context={})

    assert actual == expected


def test_constant_folding_let_and_branch_not_less():
    term = Let(
        bindings=[("x", Immediate(value=5))],
        body=Branch(
            operator="<",
            left=Immediate(value=11),
            right=Immediate(value=10),
            consequent=Allocate(count=1),
            otherwise=Load(base=Reference(name="y"), index=0),
        ),
    )

    expected = Let(
        bindings=[
            (
                "x",
                Immediate(value=5),
            )
        ],
        body=Load(base=Reference(name="y"), index=0),
    )

    actual = constant_folding_term(term=term, context={})

    assert actual == expected


def test_constant_folding_let_and_branch_equal():
    term = Let(
        bindings=[("x", Immediate(value=5))],
        body=Branch(
            operator="==",
            left=Immediate(value=10),
            right=Immediate(value=10),
            consequent=Allocate(count=1),
            otherwise=Store(base=Reference(name="y"), index=0, value=Immediate(value=0)),
        ),
    )

    expected = Let(
        bindings=[
            (
                "x",
                Immediate(value=5),
            )
        ],
        body=Allocate(count=1),
    )

    actual = constant_folding_term(term=term, context={})

    assert actual == expected


def test_constant_folding_let_and_branch_not_all_primitive():
    term = Let(
        bindings=[("x", Immediate(value=5))],
        body=Branch(
            operator="<",
            left=Reference(name="x"),
            right=Immediate(value=10),
            consequent=Allocate(count=1),
            otherwise=Store(base=Reference(name="y"), index=0, value=Immediate(value=0)),
        ),
    )

    expected = Let(
        bindings=[
            (
                "x",
                Immediate(value=5),
            )
        ],
        body=Branch(
            operator="<",
            left=Immediate(value=5),
            right=Immediate(value=10),
            consequent=Allocate(count=1),
            otherwise=Store(base=Reference(name="y"), index=0, value=Immediate(value=0)),
        ),
    )

    actual = constant_folding_term(
        term=term, context={}
    )  # this only completes one pass of constant folding, so it doesn't change the branch to just return the consequent

    assert actual == expected


def test_constant_folding_abstract_and_apply():
    term = Abstract(
        parameters=["x"],
        body=Apply(
            target=Reference(name="x"),
            arguments=[Reference(name="y")],
        ),
    )

    expected = Abstract(
        parameters=["x"],
        body=Apply(
            target=Reference(name="x"),
            arguments=[Reference(name="y")],
        ),
    )

    actual = constant_folding_term(term=term, context={})

    assert actual == expected


def test_constant_folding_begin():
    term = Begin(
        effects=[
            Store(base=Reference(name="x"), index=0, value=Immediate(value=1)),
            Store(base=Reference(name="y"), index=1, value=Immediate(value=2)),
        ],
        value=Primitive(
            operator="+",
            left=Immediate(value=3),
            right=Immediate(value=4),
        ),
    )

    expected = Begin(
        effects=[
            Store(base=Reference(name="x"), index=0, value=Immediate(value=1)),
            Store(base=Reference(name="y"), index=1, value=Immediate(value=2)),
        ],
        value=Immediate(value=7),
    )

    actual = constant_folding_term(term=term, context={})

    assert actual == expected


# test dead code elimination


def test_dead_code_elimination_let():
    term = Let(
        bindings=[
            ("x", Immediate(value=1)),
            ("y", Immediate(value=2)),
        ],
        body=Reference(name="x"),
    )

    expected = Let(
        bindings=[
            ("x", Immediate(value=1)),
        ],
        body=Reference(name="x"),
    )
    actual = dead_code_elimination_term(term=term, context={})

    assert actual == expected


def test_dead_code_elimination_abstract():
    term = Abstract(
        parameters=["x"],
        body=Apply(
            target=Reference(name="x"),
            arguments=[Reference(name="y")],
        ),
    )

    expected = Abstract(
        parameters=["x"],
        body=Apply(
            target=Reference(name="x"),
            arguments=[Reference(name="y")],
        ),
    )

    actual = dead_code_elimination_term(term=term, context={})

    assert actual == expected


def test_dead_code_elimination_branch():
    term = Branch(
        operator="<",
        left=Reference(name="x"),
        right=Reference(name="y"),
        consequent=Allocate(count=1),
        otherwise=Store(base=Reference(name="z"), index=0, value=Immediate(value=0)),
    )

    expected = Branch(
        operator="<",
        left=Reference(name="x"),
        right=Reference(name="y"),
        consequent=Allocate(count=1),
        otherwise=Store(base=Reference(name="z"), index=0, value=Immediate(value=0)),
    )

    actual = dead_code_elimination_term(term=term, context={})

    assert actual == expected


def test_dead_code_elimination_term_begin_and_primitive():  # dead code elimination doesn't actually apply to Begin as it is not required for the assignment
    term = Begin(
        effects=[
            Store(base=Reference(name="x"), index=0, value=Immediate(value=1)),
            Primitive(operator="+", left=Immediate(value=2), right=Immediate(value=3)),
        ],
        value=Reference(name="y"),
    )

    expected = Begin(
        effects=[
            Store(base=Reference(name="x"), index=0, value=Immediate(value=1)),
            Primitive(operator="+", left=Immediate(value=2), right=Immediate(value=3)),
        ],
        value=Reference(name="y"),
    )

    actual = dead_code_elimination_term(term=term, context={})

    assert actual == expected


def test_dead_code_elimination_term_load():
    term = Load(
        base=Reference(name="x"),
        index=0,
    )

    expected = Load(
        base=Reference(name="x"),
        index=0,
    )

    actual = dead_code_elimination_term(term=term, context={})

    assert actual == expected


def test_free_variables_let():
    term = Let(
        bindings=[
            ("x", Immediate(value=1)),
            ("y", Immediate(value=2)),
        ],
        body=Immediate(value=1),
    )

    actual = free_variables(term)

    assert actual == set()


def test_free_variables_abstract():
    term = Abstract(
        parameters=["x"],
        body=Apply(
            target=Reference(name="x"),
            arguments=[Reference(name="y")],
        ),
    )

    expected = {"y"}

    actual = free_variables(term)

    assert actual == expected


def test_free_variables_apply():
    term = Apply(
        target=Reference(name="x"),
        arguments=[Reference(name="y")],
    )

    expected = {"x", "y"}

    actual = free_variables(term)

    assert actual == expected


def test_free_variables_primitive():
    term = Primitive(
        operator="+",
        left=Reference(name="x"),
        right=Reference(name="y"),
    )

    expected = {"x", "y"}

    actual = free_variables(term)

    assert actual == expected


def test_free_variables_primitive_immediates():
    term = Primitive(
        operator="+",
        left=Immediate(value=6),
        right=Immediate(value=7),
    )

    actual = free_variables(term)

    assert actual == set()


def test_free_variables_immediate():
    term = Immediate(value=1)

    actual = free_variables(term)

    assert actual == set()


def test_free_variables_branch():
    term = Branch(
        operator="<",
        left=Reference(name="x"),
        right=Reference(name="y"),
        consequent=Reference(name="a"),
        otherwise=Reference(name="b"),
    )

    expected = {"x", "y", "a", "b"}

    actual = free_variables(term)

    assert actual == expected


def test_free_variables_allocate():
    term = Allocate(count=1)
    actual = free_variables(term)
    assert actual == set()


def test_free_variables_load():
    term = Load(base=Reference(name="x"), index=0)
    expected = {"x"}
    actual = free_variables(term)
    assert actual == expected


def test_free_variables_store():
    term = Store(base=Reference(name="x"), index=0, value=Reference(name="y"))
    expected = {"x", "y"}
    actual = free_variables(term)
    assert actual == expected


def test_free_variables_begin():
    term = Begin(
        effects=[
            Store(base=Reference(name="x"), index=0, value=Reference(name="y")),
            Store(base=Reference(name="z"), index=1, value=Reference(name="w")),
        ],
        value=Reference(name="a"),
    )
    expected = {"x", "y", "z", "w", "a"}
    actual = free_variables(term)
    assert actual == expected


def test_optimize_program():
    program = Program(
        parameters=[],
        body=Primitive(
            operator="+",
            left=Immediate(value=1),
            right=Immediate(value=1),
        ),
    )

    expected = Program(
        parameters=[],
        body=Immediate(value=2),
    )

    actual = optimize_program(program)

    assert actual == expected
