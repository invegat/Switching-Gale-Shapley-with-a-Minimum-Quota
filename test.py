import random
from match import Matcher
from person import Person

# the men and their list of ordered spousal preferences
m_ = dict((m, prefs.split(', ')) for [m, prefs] in (
    line.rstrip().split(': ') for line in open('men.txt')))
w_ = dict((m, prefs.split(', ')) for [m, prefs] in (
    line.rstrip().split(': ') for line in open('women.txt')))


W = {}
with open('men.txt') as F:
    line = F.readline()
    m, prefs_ = line.rstrip().split(': ')
    prefs = prefs_.split(', ')
    # NA = prefs[-1]
    for p in prefs[:-1]:
        w__ = w_[p]
        W[Person(p, int(w__[-1]))] = w__[:-1]

M = {}
with open('women.txt') as F:
    line = F.readline()
    m, prefs_ = line.rstrip().split(': ')
    prefs = prefs_.split(', ')
    for p in prefs[:-1]:
        m__ = m_[p]
        person = Person(p, int(m__[-1]))
        M[person] = []
        for n in m__[:-1]:
            #            print('n', n)
            woman = list(filter(lambda w: w.n == n, W.keys()))[0]
            M[person].append(woman)

for w, prefs in W.items():
    W[w] = []
    for n in prefs:
        man = list(filter(lambda m: m.n == n, M.keys()))[0]
        W[w].append(man)


# M = {}
# for man, prefs in m_.items():
#     p = Person(man, int(prefs[-1]))
#     M[p] = []
#     for p in prefs[:-1]:
#         M[p] = Person(p, int(w_[p][-1]))


# the women and their list of ordered spousal preferences
# W = {}
# for woman, prefs in w_.items():
#     p = Person(woman, int(prefs[-1]))
#     W[p] = prefs[:-1]


# for each man construct a random list of forbidden wives
forbidden = {}      # { 'dan': ['gay', 'eve', 'abi'], 'hal': ['eve'] }
for m, prefs in M.items():
    NA = m.NA
    forbidden[m] = prefs[NA:]
    # n = random.randint(0, len(prefs) - 1)
    # forbidden[m] = random.sample(prefs, n)  # random sample of n wives

match = Matcher(M, W, forbidden)

# match men and women; returns a mapping of wives to husbands
wives = match()

assert match.is_stable(wives)           # should be a stable matching

# swap the husbands of two wives, which should make the matching unstable
a, b = random.sample(wives.keys(), 2)
wives[b], wives[a] = wives[a], wives[b]

match.is_stable(wives, verbose=True)
