# Generating Random Expression Data
Consider  $X = {x_{m,n} }$ where = $m \leq M$ and $n \leq N$. In our case, there are $M$ genes and $N$ times. We want to generate a new matrix is which $f$ of the values are changed in the following way. $x_{m,n}$ is unchanged with probability $1-f$. With probability $f$, $x_{m,n}$ is drawn uniformly from $\{x_{m,1}, \cdots, x_{m,N}\}$.

## Algorithm

We proceed as follows using vectorization to calculate $X^{\prime}$ the randomized version of $X$.

1. Create $Y$ with shape $m \times n$ where each column is drawn from the Bernoulli distribution with parameter $f$.
1. Define the fuction $f(K,p)$ to be the result of a series of operations $\{\phi^R_k, \pi^C_k\}$, a sequence of selector of rows and permutation of columns. $k \leq K$ and $p$ is the probability of a row being selected by $\phi^R_k$.
  1. $Z_{i+1} = Z_k$ for rows not selected by $\phi^R_{i+1}$
  1. $\phi^R_{i+1}(Z_{i+1}) = \pi^C_{i+1}(\phi^R_{i+1}(Z_k))$ 
  1. $Z_0 = Y$.
1. $W = f^{-1}(Z*X)$, where * is element wise multiplication and $\times$ is normal matrix multiplication.
1. $X^{\prime} = X - Y*X + W$

In step (2), consider that the fraction of rows selected and the number of elements in the series should achieve the following:

1. The values replaced in $X$ should come from the empirical distribution for the row (e.g., gene) of the replaced value. That is, there must be a high probability ($q_s$) of a row being selected by $\phi^R_k$ for some $k$.
2. High probability of no correlation between any two rows. For this, we consider the probability $q_c$ that for a pair of rows there exists at least one iteration when one row is selected and the other is not.

We can calculate $q_s$ and $q_c$. $(1 - p)^K$ is the probability that a row is never selected by $f(K,p)$, and so $q_s = 1 - (1 - p)^K$. 

Two rows may have correlated values if they are always selected together by $\phi_k$. The probability of *not* selecting two rows togther at least once is $p^2 + (1-p)^2$ and so $q_c = 1 - (2p^2 -2p + 1)^K$. Thus,

1. $q_s$ is large if $p$ is large and/or $K$ is large.
2. $q_c$ is large if $p$ is close to 0.25 and/or $K$ is large.

From this, we conclude that $p \in [0.25, 1]$. We want to choose $p, K$ to maximize $min(q_c, q_s)$ and minimize $K$. This can be done by numerical studies.

## Alternative Algorithm

A more computationally efficient approach works as follows is to ensure that each row has at most one value of $Y$ equal to one. So, $Y$ is constructed as follows:

  1. Construct $Y_n$ (the $n$-th column of $Y$) by:
     1. v is a vector of $M$ Bernoulli values with probability ${f}\over{N}$
     1. $Y_n = v * (1-\sum_i^{n-1} Y_i) $. 
  
This procedure ensures that there's a single 1 in a row. However, we still have to be ca)reful about correlated rows.
  
  1. $Z$ is constructed by:
     1. Randomly permuting the columns of $Y$ in the manner described in the previous section (by using successive subsets) to do sampling from the original data. In the alternative algorithm procedure, we do not need inverse permutations.
     1. Extracting the replacement value by summing across columns (since there is at most one value per row) to produce a vector $z$ of $M$ values.
     1. $Z = expand(z, N) * Y$, where $expand$ creates a $M \times N$ matrix by repeating values across the column.

  1. As before, $X^{\prime} = X - X * Y + Z$.

Note that for $p = 0.25$ and $K=10$, $q_c > 0.99$. And for $K=20$, $q_c > 0.9999$.

## Implementation Notes

1. Having a larger $K$ is unlikely to be costly since it's we're just changing pointers to columns, not moving data.
