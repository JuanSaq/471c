from collections.abc import Sequence
from typing import Annotated, Literal

from pydantic import BaseModel, Field

type Identifier = Annotated[str, Field(min_length=1)]

type Nat = Annotated[int, Field(ge=0)]


class Program(BaseModel, frozen=True):
    tag: Literal["l4"] = "l4"
    parameters: Sequence[Identifier]
    body: Term


type Term = Annotated[
    Let
    | Reference
    | Abstract
    | Apply
    | Immediate
    | Boolean
    | Primitive
    | If
    | Allocate
    | Load
    | Store
    | Begin
    | LetRec
    | Vector
    | VectorRef
    | VectorSet,
    Field(discriminator="tag"),
]


class Let(BaseModel, frozen=True):
    tag: Literal["let"] = "let"
    bindings: Sequence[tuple[Identifier, Term]]
    body: Term


class LetRec(BaseModel, frozen=True):
    tag: Literal["letrec"] = "letrec"
    bindings: Sequence[tuple[Identifier, Term]]
    body: Term


class Reference(BaseModel, frozen=True):
    tag: Literal["reference"] = "reference"
    name: Identifier


class Abstract(BaseModel, frozen=True):
    tag: Literal["abstract"] = "abstract"
    parameters: Sequence[Identifier]
    body: Term


class Apply(BaseModel, frozen=True):
    tag: Literal["apply"] = "apply"
    target: Term
    arguments: Sequence[Term]


class Immediate(BaseModel, frozen=True):
    tag: Literal["immediate"] = "immediate"
    value: int


class Boolean(BaseModel, frozen=True):
    tag: Literal["boolean"] = "boolean"
    value: bool


class Primitive(BaseModel, frozen=True):
    tag: Literal["primitive"] = "primitive"
    operator: Literal["+", "-", "*"]
    left: Term
    right: Term


class If(BaseModel, frozen=True):
    tag: Literal["if"] = "if"
    condition: Term
    consequent: Term
    otherwise: Term


class Allocate(BaseModel, frozen=True):
    tag: Literal["allocate"] = "allocate"
    count: Nat


class Load(BaseModel, frozen=True):
    tag: Literal["load"] = "load"
    base: Term
    index: Nat


class Store(BaseModel, frozen=True):
    tag: Literal["store"] = "store"
    base: Term
    index: Nat
    value: Term


class Begin(BaseModel, frozen=True):
    tag: Literal["begin"] = "begin"
    effects: Sequence[Term]
    value: Term


# Hold the initial values
class Vector(BaseModel, frozen=True):
    tag: Literal["vector"] = "vector"
    elements: Sequence[Term]


# Array for reads
class VectorRef(BaseModel, frozen=True):
    tag: Literal["vector-ref"] = "vector-ref"
    vector: Term
    index: Nat


# Array for writes
class VectorSet(BaseModel, frozen=True):
    tag: Literal["vector-set"] = "vector-set"
    vector: Term
    index: Nat
    value: Term
