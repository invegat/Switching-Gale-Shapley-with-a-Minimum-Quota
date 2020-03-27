import random
from match import Matcher
from person import Person
from flask import jsonify


def setup(v_, j_):
    # the volunteers and their list of ordered job preferences
    # v_ = dict((m, prefs.split(', ')) for [m, prefs] in (
    #     line.rstrip().split(': ') for line in open('volunteers.short.txt')))
    # j_ = dict((m, prefs.split(', ')) for [m, prefs] in (
    #     line.rstrip().split(': ') for line in open('jobs.txt')))
    volunteers = list(v_.keys())
    jobs = list(j_.keys())

    print('type v_["abe"]', type(v_['abe']), volunteers)
    # remove any missing job names from volunteers

    for v in volunteers:
        NA = v_[v][-1]
        v_[v] = list(filter(lambda j: j in jobs, v_[v][:-1]))
        v_[v].append(NA)

    # remove any missing volunteer names from jobs

    for j in jobs:
        NA = j_[j][-1]
        j_[j] = list(filter(lambda v: v in volunteers, j_[j][:-1]))
        j_[j].append(NA)

    J = {}
    prefs = v_[list(v_.keys())[0]]
    print('type(prefs)', type(prefs))

    # prefs = prefs_.split(', ')
    # NA = prefs[-1]
    for p in jobs:
        w__ = j_[p]
        J[Person(p, int(w__[-1]))] = w__[:-1]

    V = {}
    prefs = j_[list(j_.keys())[0]]
    # prefs = prefs_.split(', ')
    for p in volunteers:
        m__ = v_.get(p, ['0'])
        person = Person(p, int(m__[-1]))
        V[person] = []
        for n in m__[:-1]:
            #            print('n', n)
            job = list(filter(lambda j: j.n == n, J.keys()))[0]
            V[person].append(job)

    for j, prefs in J.items():
        J[j] = []
        for n in prefs:
            volunteer = list(filter(lambda m: m.n == n, V.keys()))[0]
            J[j].append(volunteer)

    # for each volunteer construct a list of forbidden jobs
    forbidden = {}      # { 'dan': ['gay', 'eve', 'abi'], 'hal': ['eve'] }
    for v, prefs in V.items():
        NA = v.NA
        # all jobs at or over the NA index are forbidden
        forbidden[v] = prefs[NA:]
        # n = random.randint(0, len(prefs) - 1)
        # forbidden[m] = random.sample(prefs, n)  # random sample of n wives

    forbidden_v = {}      # { 'dan': ['gay', 'eve', 'abi'], 'hal': ['eve'] }
    for j, prefs in J.items():
        NA = j.NA
        # all volunteers at or over the NA index are forbidden
        forbidden_v[j] = prefs[NA:]

    C = defaultdict(list)
    jKeys = []
    while len(J) >= len(V):
        match = Matcher(V, J, forbidden, forbidden_v)

        # match volunteers and jobs; returns a mapping of jobs to volunteers
        matches = match()
        if C is None:
            C = ((value, [key]) for key, value in enumerate(matches))
        else:
            for key, value in enumerate(matches):
                C[value].append(key)
        jKeys.extend(list(matches.keys()))

        J = dict(filter(lamba j, v: j not in jKeys, enumerate(J))
        assert match.is_stable(matches)           # should be a stable matching
        print('stable match')
    if len(J) > 0:
        V_=sorted(C.items(), key=lambda kv: len(kv[1]))[:len(J)]
        match=Matcher(V_, J, forbidden, forbidden_v)

        # match volunteers and jobs; returns a mapping of jobs to volunteers
        matches=match()
        for key, value in enumerate(matches):
            C[value].append(key)



    # print('jobs', jobs)
    a=[(key.n, [j.n for j in C[key]) for key in list(C.keys())]

    # a=[(matches[key].n, key.n) for key in list(matches.keys())]
    return jsonify(a)

    # swap the volunteers of two jobs, which should make the matching unstable
    a, b=random.sample(jobs.keys(), 2)
    jobs[b], jobs[a]=jobs[a], jobs[b]

    match.is_stable(jobs, verbose=True)
