from jax import numpy as jnp

from flax import nnx

from ..utils.general import solve_full_lstsq
        
        
class ChebyLayer(nnx.Module):
    """
    ChebyLayer class. Corresponds to the Chebyshev version of KANs (ChebyKAN). Ref: https://arxiv.org/pdf/2405.07200

    Attributes:
        n_in (int):
            Number of layer's incoming nodes.
        n_out (int):
            Number of layer's outgoing nodes.
        k (int):
            Degree of Chebyshev polynomial (1st kind).
        rngs (nnx.Rngs):
            Random key selection for initializations wherever necessary.
    """
    
    def __init__(self,
                 n_in: int = 2, n_out: int = 5, k: int = 5, rngs: nnx.Rngs = nnx.Rngs(42)
                ):
        """
        Initializes a ChebyLayer instance.
        
        Args:
            n_in (int):
                Number of layer's incoming nodes.
            n_out (int):
                Number of layer's outgoing nodes.
            k (int):
                Degree of Chebyshev polynomial (1st kind).
            rngs (nnx.Rngs):
                Random key selection for initializations wherever necessary.
            
        Example:
            >>> layer = ChebyLayer(n_in = 2, n_out = 5, k = 5, rngs = nnx.Rngs(42))
        """

        # Setup basic parameters
        self.n_in = n_in
        self.n_out = n_out
        self.k = k

        # Register and initialize the trainable parameters of the layer: c_basis, c_act

        # shape (n_out, n_in, k+1)
        noise_std = 1.0/(self.n_in * (self.k+1))
        self.c_basis = nnx.Param(
            nnx.initializers.normal(stddev=noise_std)(
                rngs.params(), (self.n_out, self.n_in, self.k + 1), jnp.float32)
        )

        # shape (n_out, n_in)
        self.c_act = nnx.Param(jnp.ones((self.n_out, self.n_in)))

    def basis(self, x):
        """
        Based on the degree, the values of the Chebyshev basis functions are calculated on the input.

        Args:
            x (jnp.array):
                Inputs, shape (batch, n_in).

        Returns:
            cheby (jnp.array):
                Chebyshev basis functions applied on inputs, shape (batch, n_in, k+1).
            
        Example:
            >>> layer = ChebyLayer(n_in = 2, n_out = 5, k = 5, rngs = nnx.Rngs(42))
            >>>
            >>> key = jax.random.PRNGKey(42)
            >>> x_batch = jax.random.uniform(key, shape=(100, 2), minval=-4.0, maxval=4.0)
            >>>
            >>> output = layer.basis(x_batch)
        """
        
        # Apply tanh activation
        x = jnp.tanh(x) # (batch, n_in)
        
        x = jnp.expand_dims(x, axis=-1) # (batch, n_in, 1)

        x = jnp.tile(x, (1, 1, self.k + 1)) # (batch, n_in, k+1)

        x = jnp.arccos(x) # (batch, n_in, k+1)

        x *= jnp.arange(self.k+1) # (batch, n_in, k+1)

        x = jnp.cos(x) # (batch, n_in, k+1)

        return x


    def update_grid(self, x, k_new):
        """
        For the case of ChebyKANs there is no concept of grid. However, a fine-graining approach can be followed by progressively increasing the degree of the polynomials.

        Args:
            x (jnp.array):
                Inputs, shape (batch, n_in).
            k_new (int):
                New Chebyshev polynomial degree.
            
        Example:
            >>> layer = ChebyLayer(n_in = 2, n_out = 5, k = 5, rngs = nnx.Rngs(42))
            >>>
            >>> key = jax.random.PRNGKey(42)
            >>> x_batch = jax.random.uniform(key, shape=(100, 2), minval=-4.0, maxval=4.0)
            >>>
            >>> layer.update_grid(x=x_batch, k_new=7)
        """

        # Apply the inputs to the current grid to acquire y = Sum(ciTi(x)), where ci are
        # the current coefficients and Ti(x) are the current Chebyshev basis functions
        Ti = self.basis(x).transpose(1, 0, 2) # (n_in, batch, k+1)
        ci = self.c_basis.value.transpose(1, 2, 0) # (n_in, k+1, n_out)
        ciTi = jnp.einsum('ijk,ikm->ijm', Ti, ci) # (n_in, batch, n_out)

        # Update the degree order
        self.k = k_new

        # Get the Tj(x) for the degree order
        Tj = self.basis(x).transpose(1, 0, 2) # (n_in, batch, k_new+1)

        # Solve for the new coefficients
        cj = solve_full_lstsq(Tj, ciTi) # (n_in, k_new+1, n_out)
        # Cast into shape (n_out, n_in, k_new+1)
        cj = cj.transpose(2, 0, 1)

        self.c_basis = nnx.Param(cj)


    def __call__(self, x):
        """
        The layer's forward pass.

        Args:
            x (jnp.array):
                Inputs, shape (batch, n_in).

        Returns:
            y (jnp.array):
                Output of the forward pass, shape (batch, n_out).
            
        Example:
            >>> layer = ChebyLayer(n_in = 2, n_out = 5, k = 5, rngs = nnx.Rngs(42))
            >>>
            >>> key = jax.random.PRNGKey(42)
            >>> x_batch = jax.random.uniform(key, shape=(100, 2), minval=-4.0, maxval=4.0)
            >>>
            >>> output = layer(x_batch)
        """
        
        batch = x.shape[0]
        
        # Calculate Chebyshev basis activations
        Ti = self.basis(x) # (batch, n_in, k+1)
        cheb = Ti.reshape(batch, -1) # (batch, n_in * (k+1))
        
        # Calculate coefficients
        cheb_w = self.c_basis.value * self.c_act[..., None] # (n_out, n_in, k+1)
        cheb_w = cheb_w.reshape(self.n_out, -1) # (n_out, n_in * (k+1))

        y = jnp.matmul(cheb, cheb_w.T) # (batch, n_out)
        
        return y