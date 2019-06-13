# Generating Random Expression Data
Consider  $X = {x_{m,n} }$ where = $m \leq M$ and $n \leq N$. In our case, there are $M$ genes and $N$ times. We want to generate a new matrix is which $f$ of the values are changed in the following way. $x_{m,n}$ is unchanged with probability $1-f$. With probability $f$, $x_{m,n}$ is drawn uniformly from $\{x_{m,1}, \cdots, x_{m,N}\}$.

We proceed as follows using vectorization to calculate $X^{\prime}$ the randomized version of $X$.

1. Create $Y$ with shape $m \times n$ where each column is drawn from the Bernoulli distribution with parameter $f$.
1. Create a column permutation $P$ that randomly permutes the columns. Let $Z = PY$.
1. $W = P^{-1} \times X*Z$, where * is element wise multiplication and $\times$ is normal matrix multiplication.
1. $X^{\prime} = X - Y*X + W$
