# noqa: F841
from collections.abc import Mapping
from functools import partial

from L3 import syntax as L3

from . import syntax as L4

type Context = Mapping[L4.Identifier, None]


def eliminate_letrec_term(
    term: L4.Term,
    context: Context,
) -> L3.Term:
    recur = partial(eliminate_letrec_term, context=context)

    match term:
        case L4.Let(bindings=bindings, body=body):
            return L3.Let(
                bindings=[(name, recur(value)) for name, value in bindings],
                body=recur(body),
            )

        case L4.LetRec(bindings=bindings, body=body):
            return L3.LetRec(
                bindings=[(name, recur(value)) for name, value in bindings],
                body=recur(body),
            )

        case L4.Reference(name=name):
            # if name is a recursive variable -> (Load (Reference name)))
            if name in context:
                return L3.Load(base=L3.Reference(name=name), index=0)
            # else (Reference name)
            else:
                return L3.Reference(name=name)

        case L4.Abstract(parameters=parameters, body=body):
            return L3.Abstract(
                parameters=parameters,
                body=recur(body),
            )

        case L4.Apply(target=target, arguments=arguments):
            return L3.Apply(target=recur(target), arguments=[recur(argument) for argument in arguments])

        case L4.Immediate(value=value):
            return L3.Immediate(value=value)

        case L4.Boolean(value=value):
            if value == True:
                return L3.Immediate(value=1)
            else:
                return L3.Immediate(value=0)

        case L4.Primitive(operator=operator, left=left, right=right):
            return L3.Primitive(
                operator=operator,
                left=recur(left),
                right=recur(right),
            )

        case L4.Branch(operator=operator, left=left, right=right, consequent=consequent, otherwise=otherwise):
            return L3.Branch(
                operator=operator,
                left=recur(left),
                right=recur(right),
                consequent=recur(consequent),
                otherwise=recur(otherwise),
            )

        case L4.Allocate(count=count):
            return L3.Allocate(count=count)

        case L4.Load(base=base, index=index):
            return L3.Load(
                base=recur(base),
                index=index,
            )

        case L4.Store(base=base, index=index, value=value):
            return L3.Store(
                base=recur(base),
                index=index,
                value=recur(value),
            )

        case L4.Begin(effects=effects, value=value):  # pragma: no branch
            return L3.Begin(
                effects=[recur(effect) for effect in effects],
                value=recur(value),
            )
