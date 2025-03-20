from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

TypeSolverInput = TypeVar("TypeSolverInput", bound=BaseModel)
TypeSolverOutput = TypeVar("TypeSolverOutput", bound=BaseModel)


class SolverRequest(BaseModel, Generic[TypeSolverInput]):
    """
    Request for a solver, with inputs and quality guarantees.
    """

    model_config = ConfigDict(extra="forbid")

    solverInput: TypeSolverInput | None = None
    falsePositiveRate: float = Field(default=0.01, ge=0, le=1)


class SolverProof(BaseModel):
    """
    Solver proof as bloom filter and number of inserted items.
    """

    model_config = ConfigDict(extra="forbid")

    bloomFilter: bytes = b"BgAAAAAAAADYxCJU"
    countItems: int = Field(default=1, ge=0)


class SolverResponse(BaseModel, Generic[TypeSolverOutput]):
    """
    Solver response with output and proof.
    """

    model_config = ConfigDict(extra="forbid")

    solverOutput: TypeSolverOutput | None = None
    solverProof: SolverProof = SolverProof()


class VerifierRequest(BaseModel, Generic[TypeSolverOutput]):
    """
    Verifier request, with solver request and solver proof as
    input, as well as `verificationRatio` to control the minimum required confidence.
    """

    model_config = ConfigDict(extra="forbid")

    solverRequest: SolverRequest = SolverRequest()
    solverOutput: TypeSolverOutput | None = None
    solverProof: SolverProof = SolverProof()
    verificationRatio: float = Field(default=0.1, ge=0, le=1)


class VerifierResponse(BaseModel):
    """
    Verifier response, with number of verified items and
    the verification outcome.
    """

    model_config = ConfigDict(extra="forbid")

    countItems: int = Field(default=1, ge=0)
    isVerified: bool = False


class Task(Generic[TypeSolverInput, TypeSolverOutput], ABC):
    """
    Abstract class for solver tasks (solver, verifier).
    """

    @staticmethod
    @abstractmethod
    def solve(request: SolverRequest[TypeSolverInput]) -> SolverResponse[TypeSolverOutput]:  # noqa: F841
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def verify(request: VerifierRequest) -> VerifierResponse:  # noqa: F841
        raise NotImplementedError
