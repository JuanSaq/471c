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


def free_variables(term: Term) -> set[Identifier]:
    match term:
        case Let(bindings=bindings, body=body):
            bound = {name for name, _ in bindings}
            return free_variables(body) - bound

        case Reference(name=name):
            return {name}

        case Abstract(parameters=parameters, body=body):
            bound = set(parameters)
            return free_variables(body) - bound

        case Apply(target=target, arguments=arguments):
            result = free_variables(target)
            for argument in arguments:
                result |= free_variables(argument)
            return result

        case Immediate(value=_value):
            return set()

        case Primitive(operator=_operator, left=left, right=right):
            return free_variables(left) | free_variables(right)

        case Branch(operator=_operator, left=left, right=right, consequent=consequent, otherwise=otherwise):
            return free_variables(left) | free_variables(right) | free_variables(consequent) | free_variables(otherwise)

        case Allocate(count=_count):
            return set()

        case Load(base=base, index=_index):
            return free_variables(base)

        case Store(base=base, index=_index, value=value):
            return free_variables(base) | free_variables(value)

        case Begin(effects=effects, value=value):  # pragma: no branch
            result = free_variables(value)
            for effect in effects:
                result |= free_variables(effect)
            return result


def dead_code_elimination_term(term: Term, context: Context) -> Term:
    recur = partial(dead_code_elimination_term, context=context)

    match term:
        case Let(bindings=bindings, body=body):
            return Let(
                bindings=[(name, recur(value)) for name, value in bindings if name in free_variables(body)],
                body=recur(body),
            )

        case Reference(name=_name):
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
