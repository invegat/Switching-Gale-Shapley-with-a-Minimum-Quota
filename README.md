This is a variant of the [Gale/Shapley algorithm](https://gist.github.com/joyrexus/9967709) in python designed to address the [Stable Marriage Problem](http://en.wikipedia.org/wiki/Stable_marriage_problem). The variant here is that **certain marriages are forbidden**.

## Problem description

Given a set of volunteers and jobs to be paired, each volunteer ranks all the jobs in order of their preference and each job ranks all the volunteers in order of their preference. There is a NA column meaning that they will not accept matches below that ranking for both volunteers and jobs.

A stable set of engagements for Volunteer/Job is one where no volunteer prefers a job over the one he is engaged to, where that other job also prefers that volunteer over the one they are engaged to. I.e. with consulting Volunteer/Jobs, there would be no reason for the engagements between the people to change.

Gale and Shapley proved that there is a stable set of engagements for any set of preferences and their algorithm finds a set of stable engagements with a worst case running time of _n_^2 iterations through the main loop.

## Task Specifics

We're provided with a list of volunteers (`V`) and jobs (`J`), indicating each volunteer's (and job's) engagement preferences ranked from highest to lowest.

We're also provided with a list of forbidden engagements (a dict that lists for each volunteer the jobs they have forbidden). Forbidden engagements are not permitted, so the algorithm should never marry forbidden pairs of volunteers and jobs.

The task is to implement the Gale-Shapley algorithm for finding a stable set of engagements.

We want to use this algorithm to produce a matching, which we can then test for
stability by the criteria indicated above.

We're also asked to perturb the resulting matching (swapping the volunteers of two
jobs) and re-test for stability. The perturbed matching should be found to
be unstable.
