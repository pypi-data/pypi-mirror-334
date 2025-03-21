
import flax.nnx as nnx
from flax.typing import Callable


def get_activation(activation: str | Callable | type(Callable) | None) -> Callable | None:
    match activation:
        case str() as name:
            return getattr(nnx, name)
        case Callable() as module:
            return module
        case type() as constructor:
            return constructor()
        case None:
            return None
        case other:
            raise TypeError(f"Could not find an activation from {other!r}")
