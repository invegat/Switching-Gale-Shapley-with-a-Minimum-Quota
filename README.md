This is a variant of the [Gale/Shapley algorithm](https://gist.github.com/joyrexus/9967709) in python designed to address the [Stable Marriage Problem](http://en.wikipedia.org/wiki/Stable_marriage_problem). The variant here is that **certain volunteer/job assignments are forbidden** and **Volunteers can have more than one job.**   Hosted as a AWS Lambda microservice at https://o9ktamo0f2.execute-api.us-east-1.amazonaws.com/dev/app/data

## Problem description

Given a set of volunteers and jobs to be paired, each volunteer ranks all the jobs in order of their preference and each job ranks all the volunteers in order of their preference. There is a NA column meaning that they will not accept matches below that ranking for both volunteers and jobs.

A stable set of engagements for Volunteer/Job is one where no volunteer prefers a job over the one he is assigned to, where that other job also prefers that volunteer over the one they are assigned to. I.e. with consulting Volunteer/Jobs, there would be no reason for the engagements between the people to change.

Gale and Shapley proved that there is a stable set of engagements for any set of preferences and their algorithm finds a set of stable engagements with a worst case running time of _n_^2 iterations through the main loop.

## Task Specifics

We're provided with a list of volunteers (`V`) and jobs (`J`), indicating each volunteer's (and job's) assignment preferences ranked from highest to lowest.

We're also provided with a list of forbidden engagements (a dict that lists for each volunteer the jobs they have forbidden). Forbidden engagements are not permitted, so the algorithm should never match forbidden pairs of volunteers and jobs.

The task is to implement the Gale-Shapley algorithm for finding a stable set of engagements.

We want to use this algorithm to produce a matching, which we can then test for
stability by the criteria indicated above.

We're also asked to perturb the resulting matching (swapping the volunteers of two
jobs) and re-test for stability. The perturbed matching should be found to
be unstable.

**post a body like this:**
```
[
    {
        "abe": [
            "abi",
            "eve",
            "cath",
            "ivy",
            "jan",
            "dee",
            "fay",
            "bea",
            "hope",
            "gay",
            "3"
        ],
        "bob": [
            "cath",
            "hope",
            "abi",
            "dee",
            "eve",
            "fay",
            "bea",
            "jan",
            "ivy",
            "gay",
            "3"
        ],
        "col": [
            "hope",
            "eve",
            "abi",
            "dee",
            "bea",
            "fay",
            "ivy",
            "gay",
            "cath",
            "jan",
            "4"
        ],
        "dan": [
            "ivy",
            "fay",
            "dee",
            "gay",
            "hope",
            "eve",
            "jan",
            "bea",
            "cath",
            "abi",
            "4"
        ],
        "ed": [
            "jan",
            "dee",
            "bea",
            "cath",
            "fay",
            "eve",
            "abi",
            "ivy",
            "hope",
            "gay",
            "5"
        ],
        "fred": [
            "bea",
            "abi",
            "dee",
            "gay",
            "eve",
            "ivy",
            "cath",
            "jan",
            "hope",
            "fay",
            "5"
        ],
        "gav": [
            "gay",
            "eve",
            "ivy",
            "bea",
            "cath",
            "abi",
            "dee",
            "hope",
            "jan",
            "fay",
            "6"
        ],
        "hal": [
            "abi",
            "eve",
            "hope",
            "fay",
            "ivy",
            "cath",
            "jan",
            "bea",
            "gay",
            "dee",
            "6"
        ],
        "ian": [
            "hope",
            "cath",
            "dee",
            "gay",
            "bea",
            "abi",
            "fay",
            "ivy",
            "jan",
            "eve",
            "7"
        ],
        "jon": [
            "abi",
            "fay",
            "jan",
            "gay",
            "eve",
            "bea",
            "dee",
            "cath",
            "ivy",
            "hope",
            "7"
        ]
    },
    {
        "abi": [
            "bob",
            "fred",
            "jon",
            "gav",
            "ian",
            "abe",
            "dan",
            "ed",
            "col",
            "hal",
            "7"
        ],
        "bea": [
            "bob",
            "abe",
            "col",
            "fred",
            "gav",
            "dan",
            "ian",
            "ed",
            "jon",
            "hal",
            "7"
        ],
        "cath": [
            "fred",
            "bob",
            "ed",
            "gav",
            "hal",
            "col",
            "ian",
            "abe",
            "dan",
            "jon",
            "6"
        ],
        "dee": [
            "fred",
            "jon",
            "col",
            "abe",
            "ian",
            "hal",
            "gav",
            "dan",
            "bob",
            "ed",
            "6"
        ],
        "eve": [
            "jon",
            "hal",
            "fred",
            "dan",
            "abe",
            "gav",
            "col",
            "ed",
            "ian",
            "bob",
            "5"
        ],
        "fay": [
            "bob",
            "abe",
            "ed",
            "ian",
            "jon",
            "dan",
            "fred",
            "gav",
            "col",
            "hal",
            "5"
        ],
        "gay": [
            "jon",
            "gav",
            "hal",
            "fred",
            "bob",
            "abe",
            "col",
            "ed",
            "dan",
            "ian",
            "4"
        ],
        "hope": [
            "gav",
            "jon",
            "bob",
            "abe",
            "ian",
            "dan",
            "hal",
            "ed",
            "col",
            "fred",
            "4"
        ],
        "ivy": [
            "ian",
            "col",
            "hal",
            "gav",
            "fred",
            "bob",
            "abe",
            "ed",
            "jon",
            "dan",
            "3"
        ],
        "jan": [
            "ed",
            "hal",
            "gav",
            "abe",
            "bob",
            "jon",
            "col",
            "ian",
            "fred",
            "dan",
            "3"
        ]
    }
]```

**to get this response** 

```[
    [
        "jon",
        [
            "abi"
        ]
    ],
    [
        "bob",
        [
            "cath",
            "fay"
        ]
    ],
    [
        "ian",
        [
            "hope"
        ]
    ],
    [
        "dan",
        [
            "ivy"
        ]
    ],
    [
        "ed",
        [
            "jan"
        ]
    ],
    [
        "fred",
        [
            "bea"
        ]
    ],
    [
        "gav",
        [
            "gay"
        ]
    ],
    [
        "hal",
        [
            "eve"
        ]
    ],
    [
        "col",
        [
            "dee"
        ]
    ]
]```
