
import jax
import jax.numpy as jnp

from jax.typing import ArrayLike


@jax.jit
def sinkhorn_knopp(key: ArrayLike, x, y, entropic_regularization: float = 1.0, steps: int = 100):
    # TODO: allow axis argument

    residuals = x[:, None] - y[None, :]
    cost = jnp.linalg.norm(residuals, ord=2, axis=-1)

    transition_probabilities = jnp.exp(-0.5 * cost / entropic_regularization)

    def body(loop_var, loop_state):
        loop_state = jax.nn.softmax(loop_state, axis=0)
        loop_state = jax.nn.softmax(loop_state, axis=1)
        return loop_state

    jax.lax.fori_loop(0, steps, body, transition_probabilities)

    y = jax.vmap(lambda _p: jax.random.choice(key, y, p=_p))(transition_probabilities)

    return x, y
