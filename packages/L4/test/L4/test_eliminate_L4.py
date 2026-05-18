from L3 import syntax as L3
from L4 import syntax as L4
from L4.eliminate_L4 import eliminate_L4_program, eliminate_L4_term


def test_eliminate_L4_term_boolean():
    term = L4.Boolean(value=True)

    actual = eliminate_L4_term(term)

    expected = L3.Immediate(value=1)

    assert actual == expected


def test_eliminate_L4_term_boolean_false():
    term = L4.Boolean(value=False)

    actual = eliminate_L4_term(term)

    expected = L3.Immediate(value=0)

    assert actual == expected


def test_eliminate_L4_term_immediate():
    term = L4.Immediate(value=42)

    actual = eliminate_L4_term(term)

    expected = L3.Immediate(value=42)

    assert actual == expected


def test_eliminate_L4_term_reference():
    term = L4.Reference(name="x")

    actual = eliminate_L4_term(term)

    expected = L3.Reference(name="x")

    assert actual == expected


def test_eliminate_L4_term_primitive():
    term = L4.Primitive(
        operator="+",
        left=L4.Immediate(value=1),
        right=L4.Immediate(value=2),
    )

    actual = eliminate_L4_term(term)

    expected = L3.Primitive(
        operator="+",
        left=L3.Immediate(value=1),
        right=L3.Immediate(value=2),
    )

    assert actual == expected


def test_eliminate_L4_term_if_true():
    term = L4.If(
        condition=L4.Boolean(value=True),
        consequent=L4.Immediate(value=1),
        otherwise=L4.Immediate(value=0),
    )

    actual = eliminate_L4_term(term)

    expected = L3.Branch(
        operator="==",
        left=L3.Immediate(value=1),
        right=L3.Immediate(value=1),
        consequent=L3.Immediate(value=1),
        otherwise=L3.Immediate(value=0),
    )

    assert actual == expected


def test_eliminate_L4_term_if_false():
    term = L4.If(
        condition=L4.Boolean(value=False),
        consequent=L4.Immediate(value=1),
        otherwise=L4.Immediate(value=0),
    )

    actual = eliminate_L4_term(term)

    expected = L3.Branch(
        operator="==",
        left=L3.Immediate(value=0),
        right=L3.Immediate(value=1),
        consequent=L3.Immediate(value=1),
        otherwise=L3.Immediate(value=0),
    )

    assert actual == expected


def test_eliminate_L4_term_let():
    term = L4.Let(
        bindings=[("x", L4.Immediate(value=0))],
        body=L4.Reference(name="x"),
    )

    actual = eliminate_L4_term(term)

    expected = L3.Let(
        bindings=[("x", L3.Immediate(value=0))],
        body=L3.Reference(name="x"),
    )

    assert actual == expected


def test_eliminate_L4_term_letrec():
    term = L4.LetRec(
        bindings=[("x", L4.Immediate(value=0))],
        body=L4.Reference(name="x"),
    )

    actual = eliminate_L4_term(term)

    expected = L3.LetRec(
        bindings=[("x", L3.Immediate(value=0))],
        body=L3.Reference(name="x"),
    )

    assert actual == expected


def test_eliminate_L4_term_abstract():
    term = L4.Abstract(
        parameters=["x"],
        body=L4.Immediate(value=0),
    )

    actual = eliminate_L4_term(term)

    expected = L3.Abstract(
        parameters=["x"],
        body=L3.Immediate(value=0),
    )

    assert actual == expected


def test_eliminate_L4_term_apply():
    term = L4.Apply(
        target=L4.Reference(name="f"),
        arguments=[L4.Immediate(value=1)],
    )

    actual = eliminate_L4_term(term)

    expected = L3.Apply(
        target=L3.Reference(name="f"),
        arguments=[L3.Immediate(value=1)],
    )

    assert actual == expected


def test_eliminate_L4_term_allocate():
    term = L4.Allocate(count=1)

    actual = eliminate_L4_term(term)

    expected = L3.Allocate(count=1)

    assert actual == expected


def test_eliminate_L4_term_load():
    term = L4.Load(
        base=L4.Reference(name="x"),
        index=0,
    )

    actual = eliminate_L4_term(term)

    expected = L3.Load(
        base=L3.Reference(name="x"),
        index=0,
    )

    assert actual == expected


def test_eliminate_L4_term_store():
    term = L4.Store(base=L4.Reference(name="x"), index=0, value=L4.Immediate(value=1))

    actual = eliminate_L4_term(term)

    expected = L3.Store(
        base=L3.Reference(name="x"),
        index=0,
        value=L3.Immediate(value=1),
    )

    assert actual == expected


def test_eliminate_L4_term_begin():
    term = L4.Begin(
        effects=[L4.Immediate(value=1)],
        value=L4.Immediate(value=2),
    )

    actual = eliminate_L4_term(term)

    expected = L3.Begin(
        effects=[L3.Immediate(value=1)],
        value=L3.Immediate(value=2),
    )

    assert actual == expected


def test_eliminate_L4_program():
    program = L4.Program(
        parameters=["x"],
        body=L4.Reference(name="x"),
    )

    actual = eliminate_L4_program(program)

    expected = L3.Program(
        parameters=["x"],
        body=L3.Reference(name="x"),
    )

    assert actual == expected
