from collections.abc import Callable
from functools import partial

from L0 import syntax as L0

from . import syntax as L1


def close_term(
    statement: L1.Statement,
    fresh: Callable[[str], str],
) -> L0.Statement:
    recur = partial(close_term, fresh=fresh)

    match statement:
        case L1.Copy(destination=destination, source=source, then=then):
            return L0.Copy(destination=destination, source=source, then=recur(then))

        case L1.Abstract(destination=destination, parameters=_parameters, body=_body, then=then):
            env = fresh("env")
            return L0.Allocate(
                destination=destination,
                count=0,
                then=L0.Store(
                    base=destination,
                    index=0,
                    value=destination,
                    then=L0.Store(
                        base=destination,
                        index=1,
                        value=destination,
                        then=recur(then),
                    ),
                ),
            )

        case L1.Apply(target=target, arguments=arguments):
            # 1. separate code and environment from the closure
            # 2. call the code with the environment and then arguments

            code = fresh("code")
            env = fresh("env")
            return L0.Load(
                destination=code,
                base=target,
                index=0,
                then=L0.Load(
                    destination=env, base=target, index=1, then=L0.Call(target=code, arguments=[*arguments, env])
                ),
            )

        case L1.Immediate(destination=destination, value=value, then=then):
            return L0.Immediate(destination=destination, value=value, then=recur(then))

        case L1.Primitive(destination=destination, operator=operator, left=left, right=right, then=then):
            return L0.Primitive(
                destination=destination,
                operator=operator,
                left=left,
                right=right,
                then=recur(then),
            )

        case L1.Branch(operator=operator, left=left, right=right, then=then, otherwise=otherwise):
            return L0.Branch(
                operator=operator,
                left=left,
                right=right,
                then=recur(then),
                otherwise=recur(otherwise),
            )
        case L1.Allocate(destination=destination, count=count, then=then):
            return L0.Allocate(destination=destination, count=count, then=recur(then))

        case L1.Load(destination=destination, base=base, index=index, then=then):
            return L0.Load(
                destination=destination,
                base=base,
                index=index,
                then=recur(then),
            )

        case L1.Store(base=base, index=index, value=value, then=then):
            return L0.Store(
                base=base,
                index=index,
                value=value,
                then=recur(then),
            )

        case L1.Halt(value=value):  # pragma: no branch
            return L0.Halt(value=value)
