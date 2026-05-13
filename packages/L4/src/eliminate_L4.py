from functools import partial

from . import syntax as L4
from L3 import syntax as L3


def eliminate_L4_term(
    term: L4.Term,
) -> L3.Term:
    """
    - (vector e1 e2 ... en) →
      (let ((arr (allocate n)))
        (begin
          (store arr 0 e1)
          (store arr 1 e2)
          ...
          (store arr n-1 en)
          arr))
    
    - (vector-ref arr i) → (load arr i)
    - (vector-set arr i v) → (store arr i v)
    """
    recur = partial(eliminate_L4_term)
    
    match term:
        case L4.Vector(elements=elements):
            # Desugar: (vector e1 e2 ... en)
            n = len(elements)
            arr_name = "_vec"
            
            # Create store operations for each element
            stores = [
                L3.Store(
                    base=L3.Reference(name=arr_name),
                    index=i,
                    value=recur(element),
                )
                for i, element in enumerate(elements)
            ]
            
            # Create: (let ((arr (allocate n))) (begin stores... arr))
            return L3.Let(
                bindings=[
                    (arr_name, L3.Allocate(count=n))
                ],
                body=L3.Begin(
                    effects=stores,
                    value=L3.Reference(name=arr_name),
                ),
            )
        
        case L4.VectorRef(vector=vector, index=index):
            # (vector-ref arr i) → (load arr i)
            return L3.Load(
                base=recur(vector),
                index=index,
            )
        
        case L4.VectorSet(vector=vector, index=index, value=value):
            # (vector-set arr i v) → (store arr i v)
            return L3.Store(
                base=recur(vector),
                index=index,
                value=recur(value),
            )
        
        case L4.Let(bindings=bindings, body=body):
            return L3.Let(
                bindings=[(name, recur(val)) for name, val in bindings],
                body=recur(body),
            )
        
        case L4.LetRec(bindings=bindings, body=body):
            return L3.LetRec(
                bindings=[(name, recur(val)) for name, val in bindings],
                body=recur(body),
            )
        
        case L4.Reference(name=name):
            return L3.Reference(name=name)
        
        case L4.Abstract(parameters=parameters, body=body):
            return L3.Abstract(
                parameters=parameters,
                body=recur(body),
            )
        
        case L4.Apply(target=target, arguments=arguments):
            return L3.Apply(
                target=recur(target),
                arguments=[recur(arg) for arg in arguments],
            )
        
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
        
        case L4.Begin(effects=effects, value=value):
            return L3.Begin(
                effects=[recur(effect) for effect in effects],
                value=recur(value),
            )


def eliminate_L4_program(
    program: L4.Program,
) -> L3.Program:
    match program:
        case L4.Program(parameters=parameters, body=body):  # pragma: no branch
            return L3.Program(
                parameters=parameters,
                body=eliminate_L4_term(body),
            )