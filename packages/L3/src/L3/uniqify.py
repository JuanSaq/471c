from collections.abc import Callable, Mapping
from functools import partial

from util.sequential_name_generator import SequentialNameGenerator

from .syntax import (
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
    Term,
)

type Context = Mapping[str, str]


def uniqify_term(
    term: Term,
    context: Context,
    fresh: Callable[[str], str],
) -> Term:
    _term = partial(uniqify_term, context=context, fresh=fresh)

    match term:
        case Let(bindings=bindings, body=body):
            local = {name: fresh(name) for name, _ in bindings}
            return Let(
                bindings=[(local[name], _term(value)) for name, value in bindings],
                body=_term(body, context={**context, **local}),
            )

        case LetRec(bindings=bindings, body=body):
            local = {name: fresh(name) for name, _ in bindings}
            return LetRec(
                bindings=[(local[name], _term(value)) for name, value in bindings],
                body=_term(body, context={**context, **local}),
            )

        case Reference(name=name):
            return Reference(name=context[name])

        case Abstract(parameters=parameters, body=body):
            local = {parameter: fresh(parameter) for parameter in parameters}
            return Abstract(
                parameters=[local[parameter] for parameter in parameters],
                body=_term(body, context={**context, **local}),
            )

        case Apply(target=target, arguments=arguments):
            return Apply(
                target=_term(target),
                arguments=[_term(argument) for argument in arguments],
            )

        case Immediate():
            return term

        case Primitive(operator=operator, left=left, right=right):
            return Primitive(
                operator=operator,
                left=_term(left),
                right=_term(right),
            )

        case Branch(operator=operator, left=left, right=right, consequent=consequent, otherwise=otherwise):
            return Branch(
                operator=operator,
                left=_term(left),
                right=_term(right),
                consequent=_term(consequent),
                otherwise=_term(otherwise),
            )

        case Allocate():
            return term

        case Load(base=base, index=index):
            return Load(
                base=_term(base),
                index=index,
            )

        case Store(base=base, index=index, value=value):
            return Store(
                base=_term(base),
                index=index,
                value=_term(value),
            )

        case Begin(effects=effects, value=value):  # pragma: no branch
            return Begin(
                effects=[_term(effect) for effect in effects],
                value=_term(value),
            )


def uniqify_program(
    program: Program,
) -> tuple[Callable[[str], str], Program]:
    fresh = SequentialNameGenerator()

    _term = partial(uniqify_term, fresh=fresh)

    match program:
        case Program(parameters=parameters, body=body):  # pragma: no branch
            local = {parameter: fresh(parameter) for parameter in parameters}
            return (
                fresh,
                Program(
                    parameters=[local[parameter] for parameter in parameters],
                    body=_term(body, local),
                ),
            )
