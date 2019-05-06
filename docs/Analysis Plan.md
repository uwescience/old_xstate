# Analysis Plan

## Background

The analysis will focus on developing and validating algorithms for state characterization and assignment.

At present, we only have one example of ground truth for state assignments, with six states. We will extend this by proposing error models for read counts that create synthetic data to evaluate the robustness of state characterization and assignment.

## Technical Description of Tasks

The **state characterization task** specifies for each state a set of genes along the expected value of the gene for up- and down-regulation. The characterization is uniquely identify state vectors for each state.


The **state assignment task** assigns a measure in [0, 1] to each state to indicate whether an expression vector to indicate the relative likelihood of an expression vector belonging to a state. 



## Factors in Studies

1. Algorithm

1. Error model. 
   1. Random reordering of read counts.
   2. Gaussian error model with fixed variance.

1. Units used in analysis
   1. Normalized read counts
   2. z-score
   3. significance level

1. Distance for state characterization and assignment
   1. Eucleadian
   2. for significance level, infinite if below threshold and 0 if above threshold

1. Including both up and down regulation

## Initial Analysis

Develop a framework for analysis by assessing the quality of state characterization.