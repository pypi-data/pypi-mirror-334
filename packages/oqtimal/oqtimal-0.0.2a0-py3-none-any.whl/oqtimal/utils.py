
import jax.numpy as jnp

from jax import Array


def is_doubly_stochastic(matrix: Array, atol: float = 1e-8, rtol: float = 1e-5, axis1: int = -2, axis2: int = -1) -> Array:
    is_real = jnp.all(jnp.isreal(matrix))
    is_positive = jnp.all(matrix >= 0.0)
    is_normalized =  jnp.logical_and(
        jnp.allclose(jnp.sum(matrix, axis=axis1), 1.0, atol=atol, rtol=rtol),
        jnp.allclose(jnp.sum(matrix, axis=axis2), 1.0, atol=atol, rtol=rtol),
    )

    return jnp.logical_and(is_real, jnp.logical_and(is_positive, is_normalized))
