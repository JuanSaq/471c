from L0 import syntax as L0
from L1 import syntax as L1
from L1.close import close_term
from util.sequential_name_generator import SequentialNameGenerator


def test_close_term_copy():
    fresh = SequentialNameGenerator()

    statement = L1.Copy(
        destination="x",
        source="y",
        then=L1.Halt(value="x"),
    )

    actual = close_term(statement, fresh)

    expected = L0.Copy(
        destination="x",
        source="y",
        then=L0.Halt(value="x"),
    )

    assert actual == expected


def test_close_term_abstract():
    fresh = SequentialNameGenerator()

    statement = L1.Abstract(
        destination="f",
        parameters=["x", "y"],
        body=L1.Halt(value="x"),
        then=L1.Halt(value="f"),
    )

    actual = close_term(statement, fresh)

    expected = L0.Allocate(
        destination="f",
        count=0,
        then=L0.Store(
            base="f",
            index=0,
            value="f",
            then=L0.Store(
                base="f",
                index=1,
                value="f",
                then=L0.Halt(value="f"),
            ),
        ),
    )

    assert actual == expected


def test_close_term_apply():
    fresh = SequentialNameGenerator()

    statement = L1.Apply(
        target="f",
        arguments=["x", "y"],
    )

    actual = close_term(statement, fresh)

    expected = L0.Load(
        destination="code0",
        base="f",
        index=0,
        then=L0.Load(
            destination="env0",
            base="f",
            index=1,
            then=L0.Call(
                target="code0",
                arguments=["x", "y", "env0"],
            ),
        ),
    )

    assert actual == expected


def test_close_term_immediate():
    fresh = SequentialNameGenerator()

    statement = L1.Immediate(
        destination="x",
        value=42,
        then=L1.Halt(value="x"),
    )

    actual = close_term(statement, fresh)

    expected = L0.Immediate(
        destination="x",
        value=42,
        then=L0.Halt(value="x"),
    )

    assert actual == expected


def test_close_term_primitive():
    fresh = SequentialNameGenerator()

    statement = L1.Primitive(
        destination="x",
        operator="+",
        left="y",
        right="z",
        then=L1.Halt(value="x"),
    )

    actual = close_term(statement, fresh)

    expected = L0.Primitive(
        destination="x",
        operator="+",
        left="y",
        right="z",
        then=L0.Halt(value="x"),
    )

    assert actual == expected


def test_close_term_branch():
    fresh = SequentialNameGenerator()

    statement = L1.Branch(
        operator="==",
        left="x",
        right="y",
        then=L1.Halt(value="x"),
        otherwise=L1.Halt(value="y"),
    )

    actual = close_term(statement, fresh)

    expected = L0.Branch(
        operator="==",
        left="x",
        right="y",
        then=L0.Halt(value="x"),
        otherwise=L0.Halt(value="y"),
    )

    assert actual == expected


def test_close_term_allocate():
    fresh = SequentialNameGenerator()

    statement = L1.Allocate(
        destination="x",
        count=10,
        then=L1.Halt(value="x"),
    )

    actual = close_term(statement, fresh)

    expected = L0.Allocate(
        destination="x",
        count=10,
        then=L0.Halt(value="x"),
    )

    assert actual == expected


def test_close_term_load():
    fresh = SequentialNameGenerator()

    statement = L1.Load(
        destination="x",
        base="y",
        index=0,
        then=L1.Halt(value="x"),
    )

    actual = close_term(statement, fresh)

    expected = L0.Load(
        destination="x",
        base="y",
        index=0,
        then=L0.Halt(value="x"),
    )

    assert actual == expected


def test_close_term_store():
    fresh = SequentialNameGenerator()

    statement = L1.Store(
        base="x",
        index=0,
        value="y",
        then=L1.Halt(value="x"),
    )

    actual = close_term(statement, fresh)

    expected = L0.Store(
        base="x",
        index=0,
        value="y",
        then=L0.Halt(value="x"),
    )

    assert actual == expected


def test_close_term_halt():
    fresh = SequentialNameGenerator()

    statement = L1.Halt(value="x")

    actual = close_term(statement, fresh)

    expected = L0.Halt(value="x")

    assert actual == expected
