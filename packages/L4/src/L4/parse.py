from collections.abc import Sequence
from pathlib import Path

from lark import Lark, Token, Transformer
from lark.visitors import v_args  # pyright: ignore[reportUnknownVariableType]

from .syntax import (
    Abstract,
    Allocate,
    Apply,
    Begin,
    Boolean,
    DefData,
    Identifier,
    If,
    Immediate,
    Let,
    LetRec,
    Load,
    Match,
    Nat,
    Pattern,
    PatternImmediate,
    PatternVariable,
    PatternVector,
    PatternWildcard,
    Primitive,
    Program,
    Reference,
    Store,
    Term,
    Vector,
    VectorRef,
    VectorSet,
)


class AstTransformer(Transformer[Token, Program | Term]):
    @v_args(inline=True)
    def program(
        self,
        _program: Token,
        parameters: Sequence[Identifier],
        body: Term,
    ) -> Program:
        return Program(
            parameters=parameters,
            body=body,
        )

    def parameters(
        self,
        parameters: Sequence[Identifier],
    ) -> Sequence[Identifier]:
        return parameters

    @v_args(inline=True)
    def term(
        self,
        term: Term,
    ) -> Term:
        return term

    @v_args(inline=True)
    def let(
        self,
        _let: Token,
        bindings: Sequence[tuple[Identifier, Term]],
        body: Term,
    ) -> Term:
        return Let(
            bindings=bindings,
            body=body,
        )

    @v_args(inline=True)
    def letrec(
        self,
        _letrec: Token,
        bindings: Sequence[tuple[Identifier, Term]],
        body: Term,
    ) -> Term:
        return LetRec(
            bindings=bindings,
            body=body,
        )

    def bindings(
        self,
        bindings: Sequence[tuple[Identifier, Term]],
    ) -> Sequence[tuple[Identifier, Term]]:
        return bindings

    @v_args(inline=True)
    def binding(
        self,
        name: Identifier,
        value: Term,
    ) -> tuple[Identifier, Term]:
        return name, value

    @v_args(inline=True)
    def reference(
        self,
        name: Identifier,
    ) -> Term:
        return Reference(
            name=name,
        )

    @v_args(inline=True)
    def abstract(
        self,
        _lambda: Token,
        parameters: Sequence[Identifier],
        body: Term,
    ) -> Term:
        return Abstract(
            parameters=parameters,
            body=body,
        )

    @v_args(inline=True)
    def apply(
        self,
        target: Term,
        *arguments: Term,
    ) -> Term:
        return Apply(
            target=target,
            arguments=list(arguments),
        )

    @v_args(inline=True)
    def immediate(
        self,
        value: int,
    ) -> Term:
        return Immediate(value=value)

    @v_args(inline=True)
    def boolean(
        self,
        value: bool,
    ) -> Term:
        return Boolean(value=value)

    @v_args(inline=True)
    def primitive(
        self,
        operator: Token,
        left: Term,
        right: Term,
    ) -> Term:
        return Primitive(
            operator=operator.value,
            left=left,
            right=right,
        )

    @v_args(inline=True)
    def If(  # capitalized because `if` is a reserved keyword
        self, _if: Token, condition: Term, consequent: Term, otherwise: Term
    ) -> Term:
        return If(
            condition=condition,
            consequent=consequent,
            otherwise=otherwise,
        )

    @v_args(inline=True)
    def allocate(
        self,
        _allocate: Token,
        count: Immediate,
    ) -> Term:
        return Allocate(count=count.value)

    @v_args(inline=True)
    def load(
        self,
        _load: Token,
        base: Term,
        index: Immediate,
    ) -> Term:
        return Load(
            base=base,
            index=index.value,
        )

    @v_args(inline=True)
    def store(
        self,
        _store: Token,
        base: Term,
        index: Immediate,
        value: Term,
    ) -> Term:
        return Store(
            base=base,
            index=index.value,
            value=value,
        )

    @v_args(inline=True)
    def begin(self, _begin: Token, *terms: Term) -> Term:
        return Begin(
            effects=list(terms[:-1]),
            value=terms[-1],
        )

    @v_args(inline=True)
    def vector(
        self,
        *elements: Term,
    ) -> Vector:
        return Vector(elements=elements)

    @v_args(inline=True)
    def vector_ref(
        self,
        vector: Term,
        index: Nat,
    ) -> VectorRef:
        return VectorRef(vector=vector, index=index)

    @v_args(inline=True)
    def vector_set(
        self,
        vector: Term,
        index: Nat,
        value: Term,
    ) -> VectorSet:
        return VectorSet(vector=vector, index=index, value=value)

    @v_args(inline=True)
    def match(self, _match: Token, expr: Term, cases: Sequence[tuple[Pattern, Term]]) -> Term:
        return Match(expr=expr, cases=cases)

    @v_args(inline=True)
    def case(self, pattern: Pattern, term: Term) -> tuple[Pattern, Term]:
        return (pattern, term)

    @v_args(inline=True)
    def pattern_variable(self, name: Identifier) -> Pattern:
        return PatternVariable(name=name)

    @v_args(inline=True)
    def pattern_wildcard(self, _wildcard: Token) -> Pattern:
        return PatternWildcard()

    @v_args(inline=True)
    def pattern_immediate(self, value: Nat) -> Pattern:
        return PatternImmediate(value=value)

    @v_args(inline=True)
    def pattern_vector(self, _vector: Token, patterns: Sequence[Pattern]) -> Pattern:
        return PatternVector(patterns=patterns)

    @v_args(inline=True)
    def def_data(
        self,
        _defdata: Token,
        name: Identifier,
        constructors: Sequence[tuple[Identifier, Sequence[tuple[Identifier, Term]]]],
    ) -> Term:
        return DefData(name=name, constructors=constructors)


def parse_term(source: str) -> Term:
    grammar = Path(__file__).with_name("L3.lark").read_text()
    parser = Lark(grammar, start="term")
    tree = parser.parse(source)  # pyright: ignore[reportUnknownMemberType]
    return AstTransformer().transform(tree)  # pyright: ignore[reportReturnType]


def parse_program(source: str) -> Program:
    grammar = Path(__file__).with_name("L3.lark").read_text()
    parser = Lark(grammar, start="program")
    tree = parser.parse(source)  # pyright: ignore[reportUnknownMemberType]
    return AstTransformer().transform(tree)  # pyright: ignore[reportReturnType]
