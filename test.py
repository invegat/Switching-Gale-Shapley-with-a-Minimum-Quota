import random
from match import Matcher
from person import Person

# the volunteers and their list of ordered job preferences
m_ = dict((m, prefs.split(', ')) for [m, prefs] in (
    line.rstrip().split(': ') for line in open('volunteers.txt')))
w_ = dict((m, prefs.split(', ')) for [m, prefs] in (
    line.rstrip().split(': ') for line in open('jobs.txt')))


W = {}
with open('volunteers.txt') as F:
    line = F.readline()
    _, prefs_ = line.rstrip().split(': ')
    prefs = prefs_.split(', ')
    # NA = prefs[-1]
    for p in prefs[:-1]:
        w__ = w_[p]
        W[Person(p, int(w__[-1]))] = w__[:-1]

M = {}
with open('jobs.txt') as F:
    line = F.readline()
    _, prefs_ = line.rstrip().split(': ')
    prefs = prefs_.split(', ')
    for p in prefs[:-1]:
        m__ = m_[p]
        person = Person(p, int(m__[-1]))
        M[person] = []
        for n in m__[:-1]:
            #            print('n', n)
            job = list(filter(lambda w: w.n == n, W.keys()))[0]
            M[person].append(job)

for w, prefs in W.items():
    W[w] = []
    for n in prefs:
        volunteer = list(filter(lambda m: m.n == n, M.keys()))[0]
        W[w].append(volunteer)

# for each volunteer construct a random list of forbidden jobs
forbidden = {}      # { 'dan': ['gay', 'eve', 'abi'], 'hal': ['eve'] }
for m, prefs in M.items():
    NA = m.NA
    forbidden[m] = prefs[NA:]
    # n = random.randint(0, len(prefs) - 1)
    # forbidden[m] = random.sample(prefs, n)  # random sample of n wives

match = Matcher(M, W, forbidden)

# match volunteers and jobs; returns a mapping of jobs to volunteers
jobs = match()

assert match.is_stable(jobs)           # should be a stable matching

# swap the husbands of two wives, which should make the matching unstable
a, b = random.sample(jobs.keys(), 2)
jobs[b], jobs[a] = jobs[a], jobs[b]

match.is_stable(jobs, verbose=True)
