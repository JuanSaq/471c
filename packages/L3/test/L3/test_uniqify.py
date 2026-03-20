from L3.syntax import (
    Abstract,
    Allocate,
    Apply,
    Begin,
    Branch,
    Immediate,
    Let,
    LetRec,
    Load,
    Primitive,
    Program,
    Reference,
    Store,
)
from L3.uniqify import Context, uniqify_program, uniqify_term
from util.sequential_name_generator import SequentialNameGenerator


def test_uniqify_term_reference():
    term = Reference(name="x")

    context: Context = {"x": "y"}
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh=fresh)

    expected = Reference(name="y")

    assert actual == expected


def test_uniqify_immediate():
    term = Immediate(value=42)

    context: Context = dict[str, str]()
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = Immediate(value=42)

    assert actual == expected


def test_uniqify_term_let():
    term = Let(
        bindings=[
            ("x", Immediate(value=1)),
            ("y", Reference(name="x")),
        ],
        body=Apply(
            target=Reference(name="x"),
            arguments=[
                Reference(name="y"),
            ],
        ),
    )

    context: Context = {"x": "y"}
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = Let(
        bindings=[
            ("x0", Immediate(value=1)),
            ("y0", Reference(name="y")),
        ],
        body=Apply(
            target=Reference(name="x0"),
            arguments=[
                Reference(name="y0"),
            ],
        ),
    )

    assert actual == expected


def test_uniqify_term_letrec():
    term = LetRec(
        bindings=[
            ("x", Immediate(value=1)),
            ("y", Reference(name="x")),
        ],
        body=Apply(
            target=Reference(name="x"),
            arguments=[
                Reference(name="y"),
            ],
        ),
    )

    context: Context = {"x": "z"}
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = LetRec(
        bindings=[
            ("x0", Immediate(value=1)),
            ("y0", Reference(name="z")),
        ],
        body=Apply(
            target=Reference(name="x0"),
            arguments=[
                Reference(name="y0"),
            ],
        ),
    )

    assert actual == expected


def test_uniqify_term_abstract():
    term = Abstract(
        parameters=["x"],
        body=Reference(name="x"),
    )

    context: Context = {"x": "y"}
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = Abstract(
        parameters=["x0"],
        body=Reference(name="x0"),
    )

    assert actual == expected


def test_uniqify_term_apply():
    term = Apply(
        target=Reference(name="x"),
        arguments=[
            Immediate(value=1),
            Reference(name="y"),
        ],
    )

    context: Context = {"x": "z", "y": "w"}
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = Apply(
        target=Reference(name="z"),
        arguments=[
            Immediate(value=1),
            Reference(name="w"),
        ],
    )

    assert actual == expected


def test_uniqify_term_primitive():
    term = Primitive(
        operator="+",
        left=Immediate(value=1),
        right=Immediate(value=2),
    )

    context: Context = dict[str, str]()
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = Primitive(
        operator="+",
        left=Immediate(value=1),
        right=Immediate(value=2),
    )

    assert actual == expected


def test_uniqify_term_branch():
    term = Branch(
        operator="<",
        left=Immediate(value=1),
        right=Immediate(value=2),
        consequent=Reference(name="x"),
        otherwise=Reference(name="y"),
    )

    context: Context = {"x": "a", "y": "b"}
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = Branch(
        operator="<",
        left=Immediate(value=1),
        right=Immediate(value=2),
        consequent=Reference(name="a"),
        otherwise=Reference(name="b"),
    )

    assert actual == expected


def test_uniqify_term_allocate():
    term = Allocate(count=5)

    context: Context = dict[str, str]()
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = Allocate(count=5)

    assert actual == expected


def test_uniqify_term_load():
    term = Load(
        base=Reference(name="x"),
        index=0,
    )

    context: Context = {"x": "y"}
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = Load(
        base=Reference(name="y"),
        index=0,
    )

    assert actual == expected


def test_uniqify_term_store():
    term = Store(
        base=Reference(name="x"),
        index=0,
        value=Reference(name="y"),
    )

    context: Context = {"x": "a", "y": "b"}
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = Store(
        base=Reference(name="a"),
        index=0,
        value=Reference(name="b"),
    )

    assert actual == expected


def test_uniqify_term_begin():
    term = Begin(
        effects=[
            Store(
                base=Reference(name="x"),
                index=0,
                value=Reference(name="y"),
            ),
            Primitive(
                operator="+",
                left=Immediate(value=1),
                right=Immediate(value=2),
            ),
        ],
        value=Reference(name="z"),
    )

    context: Context = {"x": "a", "y": "b", "z": "c"}
    fresh = SequentialNameGenerator()
    actual = uniqify_term(term, context, fresh)

    expected = Begin(
        effects=[
            Store(
                base=Reference(name="a"),
                index=0,
                value=Reference(name="b"),
            ),
            Primitive(
                operator="+",
                left=Immediate(value=1),
                right=Immediate(value=2),
            ),
        ],
        value=Reference(name="c"),
    )

    assert actual == expected


def test_uniqify_program():
    program = Program(
        parameters=["x", "y"],
        body=Let(
            bindings=[
                ("a", Reference(name="x")),
                ("b", Reference(name="y")),
            ],
            body=Apply(
                target=Reference(name="a"),
                arguments=[Reference(name="b")],
            ),
        ),
    )

    fresh, actual = uniqify_program(program)

    expected = Program(
        parameters=["x0", "y0"],
        body=Let(
            bindings=[
                ("a0", Reference(name="x0")),
                ("b0", Reference(name="y0")),
            ],
            body=Apply(
                target=Reference(name="a0"),
                arguments=[Reference(name="b0")],
            ),
        ),
    )

    assert actual == expected
    assert fresh("x") != "x0"  # so there is no red lines for fresh not being accessed, and check fresh
