from functools import partial

from .syntax import (
    Abstract,
    Allocate,
    Apply,
    Begin,
    Branch,
    Identifier,
    Immediate,
    Let,
    Load,
    Primitive,
    Reference,
    Store,
    Term,
)

type Context = dict[Identifier, Term]


def constant_propagation_term(
    term: Term,
    context: Context,
) -> Term:
    recur = partial(constant_propagation_term, context=context)

    match term:
        case Let(bindings=bindings, body=body):
            updated_bindings: list[tuple[Identifier, Term]] = []
            updated_context = context.copy()
            for name, value in bindings:
                updated_value = constant_propagation_term(value, updated_context)
                updated_bindings.append((name, updated_value))
                updated_context[name] = updated_value
            return Let(bindings=updated_bindings, body=constant_propagation_term(body, updated_context))

        case Reference(name=name):
            if name in context:
                return context[name]
            else:
                return term

        case Abstract(parameters=parameters, body=body):
            return Abstract(parameters=parameters, body=recur(body))

        case Apply(target=target, arguments=arguments):
            return Apply(
                target=recur(target),
                arguments=[recur(argument) for argument in arguments],
            )

        case Immediate(value=_value):
            return term

        case Primitive(operator=operator, left=left, right=right):
            return Primitive(
                operator=operator,
                left=recur(left),
                right=recur(right),
            )

        case Branch(operator=operator, left=left, right=right, consequent=consequent, otherwise=otherwise):
            return Branch(
                operator=operator,
                left=recur(left),
                right=recur(right),
                consequent=recur(consequent),
                otherwise=recur(otherwise),
            )

        case Allocate(count=_count):
            return term

        case Load(base=base, index=index):
            return Load(base=recur(base), index=index)

        case Store(base=base, index=index, value=value):
            return Store(
                base=recur(base),
                index=index,
                value=recur(value),
            )

        case Begin(effects=effects, value=value):  # pragma: no branch
            return Begin(
                effects=[recur(effect) for effect in effects],
                value=recur(value),
            )
