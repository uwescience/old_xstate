# Generating Random Expression Data
Consider  $X = {x_{m,n} }$ where = $m \leq M$ and $n \leq N$. In our case, there are $M$ genes and $N$ times. We want to generate a new matrix is which $f$ of the values are changed in the following way. $x_{m,n}$ is unchanged with probability $1-f$. With probability $f$, $x_{m,n}$ is drawn uniformly from $\{x_{m,1}, \cdots, x_{m,N}\}$.

We proceed as follows using vectorization to calculate $X^{\prime}$ the randomized version of $X$.

1. Create $Y$ with shape $m \times n$ where each column is drawn from the Bernoulli distribution with parameter $f$.
1. Create  $f = \{\phi^R_i, \pi^C_i\}$ a sequence of selector of rows and permutation of columns.
  1. $Z_{i+1} = Z_i$ for rows not selected by $\phi^R_{i+1}$
  1. $\pi^C_{i+1}(Z_{i+1}) = \pi^C_{i+1}(\phi^R_{i+1}(Z_i))$ 
  1. $Z_0 = Y$.
1. $W = f^{-1}(Z*X)$, where * is element wise multiplication and $\times$ is normal matrix multiplication.
1. $X^{\prime} = X - Y*X + W$

In step (2), consider that the fraction of rows selected and the number of elements in the series should achieve the following:

1. Low probability of correlation between any two rows
2. Achieve uniform distribution for values replaced.
