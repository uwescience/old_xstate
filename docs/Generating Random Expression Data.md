# Generating Random Expression Data
Consider  $X = {x_{m,n} }$ where = $m \leq M$ and $n \leq N$. In our case, there are $M$ genes and $N$ times. We want to generate a new matrix is which $f$ of the values are changed in the following way. $x_{m,n}$ is unchanged with probability $1-f$. With probability $f$, $x_{m,n}$ is drawn uniformly from $\{x_{m,1}, \cdots, x_{m,N}\}$.

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
2. Low probability ($q_c$) of correlation between any two rows.

We can calculate $q_s$ and $q_c$. $(1 - p)^K$ is the probability that a row is never selected by $f(K,p)$, and so $q_s = 1 - (1 - p)^K$. Two rows may have correlated values if they are always selected together by $\phi_k$ (if they are selected). The probability of not selecting two rows togther is $2p(1-p)$ and so $q_s = 1 - (2p (1-p))^K$. Thus,

1. $q_s$ is large if $p$ is large and/or $K$ is large.
2. $q_c$ is small if $p$ is close to 0.5 and/or $K$ is large.

From this, we conclude that $p \in [0.5, 1]$. We want to choose $p, K$ to minimize $max(1-q_c, q_s)$ and minimize $K$. This can be done by numerical studies.
