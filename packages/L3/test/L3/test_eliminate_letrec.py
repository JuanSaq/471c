from L2 import syntax as L2
from L3 import syntax as L3
from L3.eliminate_letrec import Context, eliminate_letrec_program, eliminate_letrec_term


def test_check_term_let():
    term = L3.Let(
        bindings=[
            ("x", L3.Immediate(value=0)),
        ],
        body=L3.Reference(name="x"),
    )

    context: Context = {}

    expected = L2.Let(
        bindings=[
            ("x", L2.Immediate(value=0)),
        ],
        body=L2.Reference(name="x"),
    )

    actual = eliminate_letrec_term(term, context)

    assert actual == expected


def test_eliminate_letrec_term_letrec():
    term = L3.LetRec(
        bindings=[
            ("x", L3.Immediate(value=0)),
        ],
        body=L3.Reference(name="x"),
    )

    context: Context = {}

    expected = L2.Let(
        bindings=[("x", L2.Immediate(value=0))],
        body=L2.Load(base=L2.Reference(name="x"), index=0),
    )

    actual = eliminate_letrec_term(term, context)

    assert actual == expected


def test_eliminate_letrec_term_reference_name_no_context():
    term = L3.Reference(name="x")

    context: Context = {}

    expected = L2.Reference(name="x")

    actual = eliminate_letrec_term(term, context)

    assert actual == expected


def test_eliminate_letrec_term_abstract():
    term = L3.Abstract(
        parameters=["x"],
        body=L3.Immediate(value=0),
    )

    context: Context = {}

    excepted = L2.Abstract(
        parameters=["x"],
        body=L2.Immediate(value=0),
    )

    actual = eliminate_letrec_term(term, context)

    assert actual == excepted


def test_eliminate_letrec_term_apply():
    term = L3.Apply(
        target=L3.Reference(name="x"),
        arguments=[L3.Immediate(value=0)],
    )

    context: Context = {}

    expected = L2.Apply(
        target=L2.Reference(name="x"),
        arguments=[L2.Immediate(value=0)],
    )

    actual = eliminate_letrec_term(term, context)

    assert actual == expected


def test_eliminate_letrec_term_immediate():
    term = L3.Immediate(value=0)

    context: Context = {}

    expected = L2.Immediate(value=0)

    actual = eliminate_letrec_term(term, context)

    assert actual == expected


def test_eliminate_letrec_term_primitive():
    term = L3.Primitive(
        operator="+",
        left=L3.Immediate(value=1),
        right=L3.Immediate(value=2),
    )

    context: Context = {}

    expected = L2.Primitive(
        operator="+",
        left=L2.Immediate(value=1),
        right=L2.Immediate(value=2),
    )

    actual = eliminate_letrec_term(term, context)

    assert actual == expected


def test_eliminate_letrec_term_branch():
    term = L3.Branch(
        operator="<",
        left=L3.Immediate(value=1),
        right=L3.Immediate(value=2),
        consequent=L3.Immediate(value=0),
        otherwise=L3.Immediate(value=1),
    )

    context: Context = {}

    expected = L2.Branch(
        operator="<",
        left=L2.Immediate(value=1),
        right=L2.Immediate(value=2),
        consequent=L2.Immediate(value=0),
        otherwise=L2.Immediate(value=1),
    )

    actual = eliminate_letrec_term(term, context)

    assert actual == expected


def test_eliminate_letrec_term_allocate():
    term = L3.Allocate(count=0)

    context: Context = {}

    expected = L2.Allocate(count=0)

    actual = eliminate_letrec_term(term, context)

    assert actual == expected


def test_eliminate_letrec_term_load():
    term = L3.Load(
        base=L3.Reference(name="x"),
        index=0,
    )

    context: Context = {}

    expected = L2.Load(
        base=L2.Reference(name="x"),
        index=0,
    )

    actual = eliminate_letrec_term(term, context)

    assert actual == expected


def test_eliminate_letrec_term_store():
    term = L3.Store(
        base=L3.Reference(name="x"),
        index=0,
        value=L3.Immediate(value=0),
    )

    context: Context = {}

    expected = L2.Store(base=L2.Reference(name="x"), index=0, value=L2.Immediate(value=0))

    actual = eliminate_letrec_term(term, context)

    assert actual == expected


def test_eliminate_letrec_term_begin():
    term = L3.Begin(
        effects=[L3.Immediate(value=0)],
        value=L3.Immediate(value=0),
    )

    context: Context = {}

    expected = L2.Begin(
        effects=[L2.Immediate(value=0)],
        value=L2.Immediate(value=0),
    )

    actual = eliminate_letrec_term(term, context)

    assert actual == expected


def test_eliminate_letrec_program():
    program = L3.Program(
        parameters=[],
        body=L3.Immediate(value=0),
    )

    expected = L2.Program(
        parameters=[],
        body=L2.Immediate(value=0),
    )

    actual = eliminate_letrec_program(program)

    assert actual == expected
