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


# Vector tests
def test_eliminate_L4_term_vector_single_element():
    term = L4.Vector(elements=[L4.Immediate(value=42)])

    actual = eliminate_L4_term(term)

    expected = L3.Let(
        bindings=[("_vec", L3.Allocate(count=1))],
        body=L3.Begin(
            effects=[
                L3.Store(
                    base=L3.Reference(name="_vec"),
                    index=0,
                    value=L3.Immediate(value=42),
                )
            ],
            value=L3.Reference(name="_vec"),
        ),
    )

    assert actual == expected


def test_eliminate_L4_term_vector_multiple_elements():
    term = L4.Vector(elements=[L4.Immediate(value=1), L4.Immediate(value=2), L4.Immediate(value=3)])

    actual = eliminate_L4_term(term)

    expected = L3.Let(
        bindings=[("_vec", L3.Allocate(count=3))],
        body=L3.Begin(
            effects=[
                L3.Store(
                    base=L3.Reference(name="_vec"),
                    index=0,
                    value=L3.Immediate(value=1),
                ),
                L3.Store(
                    base=L3.Reference(name="_vec"),
                    index=1,
                    value=L3.Immediate(value=2),
                ),
                L3.Store(
                    base=L3.Reference(name="_vec"),
                    index=2,
                    value=L3.Immediate(value=3),
                ),
            ],
            value=L3.Reference(name="_vec"),
        ),
    )

    assert actual == expected


def test_eliminate_L4_term_vector_nested():
    term = L4.Vector(
        elements=[
            L4.Vector(elements=[L4.Immediate(value=1)]),
            L4.Immediate(value=2),
        ]
    )

    actual = eliminate_L4_term(term)

    # Should have nested Let for inner vector
    assert isinstance(actual, L3.Let)
    assert actual.bindings[0][0] == "_vec"


def test_eliminate_L4_term_vector_ref():
    term = L4.VectorRef(vector=L4.Reference(name="arr"), index=0)

    actual = eliminate_L4_term(term)

    expected = L3.Load(
        base=L3.Reference(name="arr"),
        index=0,
    )

    assert actual == expected


def test_eliminate_L4_term_vector_ref_with_expression():
    term = L4.VectorRef(
        vector=L4.Vector(elements=[L4.Immediate(value=42)]),
        index=0,
    )

    actual = eliminate_L4_term(term)

    # Should desugar vector first, then load from it
    assert isinstance(actual, L3.Load)


def test_eliminate_L4_term_vector_set():
    term = L4.VectorSet(
        vector=L4.Reference(name="arr"),
        index=1,
        value=L4.Immediate(value=99),
    )

    actual = eliminate_L4_term(term)

    expected = L3.Store(
        base=L3.Reference(name="arr"),
        index=1,
        value=L3.Immediate(value=99),
    )

    assert actual == expected


def test_eliminate_L4_term_vector_set_with_expression():
    term = L4.VectorSet(
        vector=L4.Vector(elements=[L4.Immediate(value=1)]),
        index=0,
        value=L4.Immediate(value=42),
    )

    actual = eliminate_L4_term(term)

    # Should desugar vector first
    assert isinstance(actual, L3.Store)


# Pattern matching tests
def test_eliminate_L4_term_match_pattern_variable():
    """Match with simple variable pattern binds scrutinee to variable"""
    term = L4.Match(
        expr=L4.Immediate(value=42),
        cases=[(L4.PatternVariable(name="x"), L4.Reference(name="x"))],
    )

    actual = eliminate_L4_term(term)

    # Should wrap in Let with scrutinee var
    assert isinstance(actual, L3.Let)
    assert actual.bindings[0][0] == "_match_scrutinee"
    # Body should have the substitution applied (x → _match_scrutinee)
    assert isinstance(actual.body, L3.Reference)
    assert actual.body.name == "_match_scrutinee"


def test_eliminate_L4_term_match_pattern_wildcard():
    """Match with wildcard pattern matches anything"""
    term = L4.Match(
        expr=L4.Immediate(value=42),
        cases=[(L4.PatternWildcard(), L4.Immediate(value=1))],
    )

    actual = eliminate_L4_term(term)

    assert isinstance(actual, L3.Let)
    # Wildcard creates no bindings
    body = actual.body
    assert isinstance(body, L3.Immediate)
    assert body.value == 1


def test_eliminate_L4_term_match_pattern_immediate():
    """Match with literal pattern (doesn't bind)"""
    term = L4.Match(
        expr=L4.Immediate(value=42),
        cases=[(L4.PatternImmediate(value=42), L4.Immediate(value=1))],
    )

    actual = eliminate_L4_term(term)

    assert isinstance(actual, L3.Let)


def test_eliminate_L4_term_match_pattern_vector():
    """Match with vector pattern destructures elements"""
    term = L4.Match(
        expr=L4.Vector(elements=[L4.Immediate(value=1), L4.Immediate(value=2)]),
        cases=[
            (
                L4.PatternVector(
                    patterns=[
                        L4.PatternVariable(name="x"),
                        L4.PatternVariable(name="y"),
                    ]
                ),
                L4.Primitive(
                    operator="+",
                    left=L4.Reference(name="x"),
                    right=L4.Reference(name="y"),
                ),
            )
        ],
    )

    actual = eliminate_L4_term(term)

    # Should have outer Let for scrutinee
    assert isinstance(actual, L3.Let)
    # Body should have the substituted primitive with loads
    body = actual.body
    assert isinstance(body, L3.Primitive)
    assert body.operator == "+"
    # Left and right should be Loads with substituted references
    assert isinstance(body.left, L3.Load)
    assert isinstance(body.right, L3.Load)


def test_eliminate_L4_term_match_pattern_nested_vector():
    """Match with nested vector patterns"""
    term = L4.Match(
        expr=L4.Vector(elements=[L4.Immediate(value=1)]),
        cases=[
            (
                L4.PatternVector(patterns=[L4.PatternVariable(name="x")]),
                L4.Reference(name="x"),
            )
        ],
    )

    actual = eliminate_L4_term(term)

    assert isinstance(actual, L3.Let)


def test_eliminate_L4_term_match_multiple_cases():
    """Match with multiple cases (first case wins in current implementation)"""
    term = L4.Match(
        expr=L4.Immediate(value=1),
        cases=[
            (L4.PatternWildcard(), L4.Immediate(value=10)),
            (L4.PatternWildcard(), L4.Immediate(value=20)),
        ],
    )

    actual = eliminate_L4_term(term)

    assert isinstance(actual, L3.Let)
    # Since we iterate reversed and overwrite result, first case wins
    body = actual.body
    assert isinstance(body, L3.Immediate)
    assert body.value == 10


def test_eliminate_L4_term_match_with_complex_body():
    """Match with complex expression in body uses substitution"""
    term = L4.Match(
        expr=L4.Immediate(value=5),
        cases=[
            (
                L4.PatternVariable(name="n"),
                L4.Primitive(
                    operator="+",
                    left=L4.Reference(name="n"),
                    right=L4.Immediate(value=10),
                ),
            )
        ],
    )

    actual = eliminate_L4_term(term)

    assert isinstance(actual, L3.Let)
    # Body should contain the substituted primitive
    body = actual.body
    assert isinstance(body, L3.Primitive)
    assert body.operator == "+"
    # Left should be substituted to _match_scrutinee
    assert isinstance(body.left, L3.Reference)
    assert body.left.name == "_match_scrutinee"


def test_eliminate_L4_term_match_vector_with_wildcard():
    """Match vector pattern with wildcard for ignored element"""
    term = L4.Match(
        expr=L4.Vector(elements=[L4.Immediate(value=1), L4.Immediate(value=2)]),
        cases=[
            (
                L4.PatternVector(
                    patterns=[
                        L4.PatternVariable(name="x"),
                        L4.PatternWildcard(),
                    ]
                ),
                L4.Reference(name="x"),
            )
        ],
    )

    actual = eliminate_L4_term(term)

    assert isinstance(actual, L3.Let)
    # Should only bind x, not second element


def test_eliminate_L4_term_match_nested_let():
    """Match expression inside Let binding"""
    term = L4.Let(
        bindings=[
            (
                "result",
                L4.Match(
                    expr=L4.Immediate(value=42),
                    cases=[
                        (
                            L4.PatternVariable(name="x"),
                            L4.Reference(name="x"),
                        )
                    ],
                ),
            )
        ],
        body=L4.Reference(name="result"),
    )

    actual = eliminate_L4_term(term)

    assert isinstance(actual, L3.Let)
    # First binding should desugar the match
    assert actual.bindings[0][0] == "result"


def test_eliminate_L4_program_with_match():
    program = L4.Program(
        parameters=[],
        body=L4.Match(
            expr=L4.Immediate(value=1),
            cases=[(L4.PatternVariable(name="x"), L4.Reference(name="x"))],
        ),
    )

    actual = eliminate_L4_program(program)

    expected_body = eliminate_L4_term(program.body)

    assert actual.parameters == []
    assert actual.body == expected_body


# Additional tests for substitute_term coverage
def test_substitute_term_in_let():
    """Test substitution inside Let bindings"""
    term = L3.Let(
        bindings=[("x", L3.Reference(name="y"))],
        body=L3.Reference(name="x"),
    )
    subst = {"y": L3.Immediate(value=42), "x": L3.Immediate(value=100)}

    from L4.eliminate_L4 import substitute_term

    actual = substitute_term(term, subst)

    assert isinstance(actual, L3.Let)
    assert actual.bindings[0][1].value == 42
    assert actual.body.value == 100


def test_substitute_term_in_letrec():
    """Test substitution inside LetRec bindings"""
    term = L3.LetRec(
        bindings=[("f", L3.Reference(name="x"))],
        body=L3.Reference(name="f"),
    )
    subst = {"x": L3.Immediate(value=5), "f": L3.Immediate(value=10)}

    from L4.eliminate_L4 import substitute_term

    actual = substitute_term(term, subst)

    assert isinstance(actual, L3.LetRec)
    assert actual.bindings[0][1].value == 5
    assert actual.body.value == 10


def test_substitute_term_in_abstract():
    """Test substitution inside Abstract body"""
    term = L3.Abstract(
        parameters=["x"],
        body=L3.Reference(name="y"),
    )
    subst = {"y": L3.Immediate(value=99)}

    from L4.eliminate_L4 import substitute_term

    actual = substitute_term(term, subst)

    assert isinstance(actual, L3.Abstract)
    assert actual.body.value == 99


def test_substitute_term_in_apply():
    """Test substitution inside Apply"""
    term = L3.Apply(
        target=L3.Reference(name="f"),
        arguments=[L3.Reference(name="x"), L3.Reference(name="y")],
    )
    subst = {"f": L3.Reference(name="g"), "x": L3.Immediate(value=1), "y": L3.Immediate(value=2)}

    from L4.eliminate_L4 import substitute_term

    actual = substitute_term(term, subst)

    assert isinstance(actual, L3.Apply)
    assert actual.target.name == "g"
    assert actual.arguments[0].value == 1
    assert actual.arguments[1].value == 2


def test_substitute_term_in_primitive():
    """Test substitution in Primitive operands"""
    term = L3.Primitive(
        operator="+",
        left=L3.Reference(name="x"),
        right=L3.Reference(name="y"),
    )
    subst = {"x": L3.Immediate(value=10), "y": L3.Immediate(value=20)}

    from L4.eliminate_L4 import substitute_term

    actual = substitute_term(term, subst)

    assert actual.left.value == 10
    assert actual.right.value == 20


def test_substitute_term_in_branch():
    """Test substitution in Branch conditions and branches"""
    term = L3.Branch(
        operator="==",
        left=L3.Reference(name="x"),
        right=L3.Immediate(value=0),
        consequent=L3.Reference(name="c"),
        otherwise=L3.Reference(name="o"),
    )
    subst = {"x": L3.Immediate(value=5), "c": L3.Immediate(value=1), "o": L3.Immediate(value=2)}

    from L4.eliminate_L4 import substitute_term

    actual = substitute_term(term, subst)

    assert actual.left.value == 5
    assert actual.consequent.value == 1
    assert actual.otherwise.value == 2


def test_substitute_term_in_load():
    """Test substitution in Load base"""
    term = L3.Load(
        base=L3.Reference(name="arr"),
        index=0,
    )
    subst = {"arr": L3.Reference(name="x")}

    from L4.eliminate_L4 import substitute_term

    actual = substitute_term(term, subst)

    assert actual.base.name == "x"
    assert actual.index == 0


def test_substitute_term_in_store():
    """Test substitution in Store base and value"""
    term = L3.Store(
        base=L3.Reference(name="arr"),
        index=1,
        value=L3.Reference(name="v"),
    )
    subst = {"arr": L3.Reference(name="x"), "v": L3.Immediate(value=99)}

    from L4.eliminate_L4 import substitute_term

    actual = substitute_term(term, subst)

    assert actual.base.name == "x"
    assert actual.value.value == 99


def test_substitute_term_in_begin():
    """Test substitution in Begin effects and value"""
    term = L3.Begin(
        effects=[L3.Reference(name="e1"), L3.Reference(name="e2")],
        value=L3.Reference(name="v"),
    )
    subst = {"e1": L3.Immediate(value=1), "e2": L3.Immediate(value=2), "v": L3.Immediate(value=3)}

    from L4.eliminate_L4 import substitute_term

    actual = substitute_term(term, subst)

    assert actual.effects[0].value == 1
    assert actual.effects[1].value == 2
    assert actual.value.value == 3


def test_eliminate_pattern_variable_with_complex_scrutinee():
    """Test eliminate_pattern with complex scrutinee expression"""
    from L4.eliminate_L4 import eliminate_pattern

    pattern = L4.PatternVariable(name="x")
    scrutinee = L3.Primitive(
        operator="+",
        left=L3.Immediate(value=1),
        right=L3.Immediate(value=2),
    )

    bindings, subst = eliminate_pattern(pattern, scrutinee)

    assert bindings == []
    assert "x" in subst
    assert subst["x"] == scrutinee


def test_eliminate_pattern_vector_with_mixed_patterns():
    """Test vector pattern with mix of variable and wildcard patterns"""
    from L4.eliminate_L4 import eliminate_pattern

    pattern = L4.PatternVector(
        patterns=[
            L4.PatternVariable(name="x"),
            L4.PatternWildcard(),
            L4.PatternVariable(name="y"),
        ]
    )
    scrutinee = L3.Reference(name="arr")

    bindings, subst = eliminate_pattern(pattern, scrutinee)

    # Should have x and y in substitutions but not wildcard
    assert "x" in subst
    assert "y" in subst
    assert isinstance(subst["x"], L3.Load)
    assert isinstance(subst["y"], L3.Load)


def test_match_empty_vector():
    """Match on empty vector"""
    term = L4.Match(
        expr=L4.Vector(elements=[]),
        cases=[(L4.PatternVector(patterns=[]), L4.Immediate(value=1))],
    )

    actual = eliminate_L4_term(term)

    assert isinstance(actual, L3.Let)


def test_match_deeply_nested_patterns():
    """Match with deeply nested vector patterns"""
    term = L4.Match(
        expr=L4.Vector(elements=[L4.Immediate(value=1)]),
        cases=[
            (
                L4.PatternVector(patterns=[L4.PatternVector(patterns=[L4.PatternVariable(name="x")])]),
                L4.Reference(name="x"),
            )
        ],
    )

    actual = eliminate_L4_term(term)

    assert isinstance(actual, L3.Let)


def test_eliminate_match_error_no_cases():
    """Test that eliminate_match raises error on empty cases"""
    import pytest
    from L4.eliminate_L4 import eliminate_match

    term = L4.Match(expr=L4.Immediate(value=1), cases=[])

    with pytest.raises(ValueError, match="Match has no cases"):
        eliminate_match(term)


def test_substitute_term_immediate_no_subst():
    """Test substitute on Immediate returns unchanged"""
    from L4.eliminate_L4 import substitute_term

    term = L3.Immediate(value=42)
    subst = {"x": L3.Immediate(value=100)}

    actual = substitute_term(term, subst)

    assert actual == term


def test_substitute_term_allocate_no_subst():
    """Test substitute on Allocate returns unchanged"""
    from L4.eliminate_L4 import substitute_term

    term = L3.Allocate(count=10)
    subst = {"x": L3.Immediate(value=100)}

    actual = substitute_term(term, subst)

    assert actual == term


def test_substitute_term_reference_not_in_subst():
    """Test substitute on Reference that's not in substitution dict"""
    from L4.eliminate_L4 import substitute_term

    term = L3.Reference(name="x")
    subst = {"y": L3.Immediate(value=100)}

    actual = substitute_term(term, subst)

    assert actual == term


def test_match_pattern_variable_used_in_nested_expr():
    """Test pattern variable substitution in nested expressions"""
    term = L4.Match(
        expr=L4.Immediate(value=10),
        cases=[
            (
                L4.PatternVariable(name="n"),
                L4.Let(
                    bindings=[("y", L4.Reference(name="n"))],
                    body=L4.Primitive(
                        operator="+",
                        left=L4.Reference(name="n"),
                        right=L4.Reference(name="y"),
                    ),
                ),
            )
        ],
    )

    actual = eliminate_L4_term(term)

    assert isinstance(actual, L3.Let)
    # Outer let for scrutinee
    assert actual.bindings[0][0] == "_match_scrutinee"
    # Body should have Let for y binding
    assert isinstance(actual.body, L3.Let)


def test_eliminate_pattern_vector_deeply_nested():
    """Test deeply nested vector pattern"""
    from L4.eliminate_L4 import eliminate_pattern

    pattern = L4.PatternVector(
        patterns=[L4.PatternVector(patterns=[L4.PatternVector(patterns=[L4.PatternVariable(name="x")])])]
    )
    scrutinee = L3.Reference(name="arr")

    _, subst = eliminate_pattern(pattern, scrutinee)

    assert "x" in subst


def test_let_with_multiple_bindings_match_in_body():
    """Test match inside Let with multiple bindings"""
    term = L4.Let(
        bindings=[
            ("a", L4.Immediate(value=1)),
            ("b", L4.Immediate(value=2)),
        ],
        body=L4.Match(
            expr=L4.Reference(name="a"),
            cases=[(L4.PatternVariable(name="x"), L4.Reference(name="x"))],
        ),
    )

    actual = eliminate_L4_term(term)

    assert isinstance(actual, L3.Let)
    # Should have bindings for a and b
    assert len(actual.bindings) == 2


def test_vector_with_all_same_expression():
    """Test vector with repeated expressions"""
    term = L4.Vector(
        elements=[
            L4.Primitive(operator="+", left=L4.Immediate(value=1), right=L4.Immediate(value=2)),
            L4.Primitive(operator="+", left=L4.Immediate(value=1), right=L4.Immediate(value=2)),
        ]
    )

    actual = eliminate_L4_term(term)

    assert isinstance(actual, L3.Let)
    assert isinstance(actual.body, L3.Begin)
    assert len(actual.body.effects) == 2


def test_match_with_vector_and_nested_match():
    """Test match on vector where body contains another match"""
    term = L4.Match(
        expr=L4.Vector(elements=[L4.Immediate(value=1)]),
        cases=[
            (
                L4.PatternVector(patterns=[L4.PatternVariable(name="x")]),
                L4.Match(
                    expr=L4.Reference(name="x"),
                    cases=[(L4.PatternVariable(name="y"), L4.Reference(name="y"))],
                ),
            )
        ],
    )

    actual = eliminate_L4_term(term)

    assert isinstance(actual, L3.Let)


def test_substitute_term_unknown_type():
    """Force substitute_term to take the unmatched branch."""
    from L4.eliminate_L4 import substitute_term

    class NotATerm:
        pass

    obj = NotATerm()
    # substitute_term returns None when no case matches
    assert substitute_term(obj, {}) is None


def test_eliminate_pattern_unknown_type():
    """Force eliminate_pattern to take the fallback and produce bindings."""
    from L3 import syntax as L3
    from L4.eliminate_L4 import eliminate_pattern

    class NotAPattern:
        pass

    scrutinee = L3.Immediate(value=0)
    bindings, subst = eliminate_pattern(NotAPattern(), scrutinee)  # type: ignore[arg-type]

    # Fallback now produces a dummy binding so `if bindings:` branch is taken
    assert bindings
    assert bindings[0][0] == "_unused"
    assert bindings[0][1] == scrutinee
    assert subst == {}


def test_eliminate_L4_term_unknown_type():
    """Force eliminate_L4_term to take the unmatched branch."""
    from L4.eliminate_L4 import eliminate_L4_term

    class NotATerm:
        pass

    assert eliminate_L4_term(NotATerm()) is None


def test_eliminate_L4_term_defdata():
    term = L4.DefData(
        name="shape",
        constructors=[
            ("square", [("s", L4.Immediate(value=2))]),
            ("rect", [("w", L4.Immediate(value=3)), ("l", L4.Immediate(value=2))]),
        ],
    )

    actual = eliminate_L4_term(term)

    expected = L3.LetRec(
        bindings=[
            ("squares", L3.Immediate(value=2)),
            ("rectw", L3.Immediate(value=3)),
            ("rectl", L3.Immediate(value=2)),
        ],
        body=L3.Reference(name="shape"),
    )

    assert actual == expected
