
import flax.nnx as nnx
from flax.typing import Callable

from jax import Array

from .utils import get_activation


class FullyConnectedBlock(nnx.Module):
    def __init__(self, in_features: int, hidden_features: int, out_features: int, *, residual: bool = True, activation: str | Callable | type(Callable) | None = nnx.relu, batchnorm: bool | None = True, dropout: float | None = 0.1, rngs: nnx.Rngs):
        self.config = {
            "in_features": in_features,
            "hidden_features": hidden_features,
            "out_features": out_features,
            "residual": residual,
            "activation": activation,
            "batchnorm": batchnorm,
            "dropout": dropout,
        }

        self.linear1 = nnx.Linear(in_features, hidden_features, rngs=rngs)
        self.batchnorm1 = nnx.BatchNorm(hidden_features, rngs=rngs) if batchnorm else None
        self.activation1 = get_activation(activation)
        self.dropout1 = nnx.Dropout(dropout, rngs=rngs) if dropout else None

        self.linear2 = nnx.Linear(hidden_features, out_features, rngs=rngs)
        self.batchnorm2 = nnx.BatchNorm(out_features, rngs=rngs) if batchnorm else None
        self.activation2 = get_activation(activation)
        self.dropout2 = nnx.Dropout(dropout, rngs=rngs) if dropout is not None and dropout > 0 else None

        self.residual_linear = nnx.Linear(in_features, out_features, rngs=rngs) if residual else None

    def __call__(self, x: Array) -> Array:
        y = self.linear1(x)

        if self.batchnorm1 is not None:
            y = self.batchnorm1(y)

        if self.activation1 is not None:
            y = self.activation1(y)

        if self.dropout1 is not None:
            y = self.dropout1(y)

        z = self.linear2(y)

        if self.batchnorm2 is not None:
            z = self.batchnorm2(z)

        if self.activation2 is not None:
            z = self.activation2(z)

        if self.dropout2 is not None:
            z = self.dropout2(z)

        if self.residual_linear is not None:
            z = z + self.residual_linear(x)

        return z


class FullyConnected(nnx.Sequential):
    def __init__(self, widths: list[int], *, residual: bool = True, activation: str | Callable | type(Callable) | None = nnx.relu, batchnorm: bool | None = True, dropout: float | None = 0.1, rngs: nnx.Rngs):
        if len(widths) < 3:
            raise ValueError(f"The network must consist of at least 3 layers, but `len(widths)` is only {len(widths)}.")

        blocks = [
            FullyConnectedBlock(w1, w2, w3, residual=residual, activation=activation, batchnorm=batchnorm, dropout=dropout, rngs=rngs)
            for w1, w2, w3 in zip(widths[:-2:2], widths[1:-1:2], widths[2::2])
        ]

        blocks[-1].dropout2 = None
        blocks[-1].activation2 = None
        blocks[-1].batchnorm2 = None

        super().__init__(*blocks)
