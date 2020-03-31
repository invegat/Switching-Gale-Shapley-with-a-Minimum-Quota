# import random
from match import Matcher
from person import Person
from flask import jsonify
from collections import defaultdict
import copy


def setup(v_, j_, flipped):
    # the volunteers and their list of ordered job preferences
    # v_ = dict((m, prefs.split(', ')) for [m, prefs] in (
    #     line.rstrip().split(': ') for line in open('volunteers.short.txt')))
    # j_ = dict((m, prefs.split(', ')) for [m, prefs] in (
    #     line.rstrip().split(': ') for line in open('jobs.txt')))
    volunteers = list(v_.keys())
    jobs = list(j_.keys())

    # print('type v_["abe"]', type(v_['abe']), volunteers)
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
    print(f'initial J keys {J.keys()}')

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
    jKeys = set()
    loop = 0
    while len(J) > 0:
        print("V & J")
        print(V)
        print(J)
        match = Matcher(V, J, forbidden)  # , forbidden_v)

        # match volunteers and jobs; returns a mapping of jobs to volunteers
        matches = match()
        assert match.is_stable(matches)           # should be a stable matching
        print('stable match')

        print(f'loop {loop} list(matches keys) {list(matches.keys())}')
        loop += 1
        # if loop > 2:
        #     break
        # if len(C) == 0:
        #     C = dict((value, [key]) for key, value in enumerate(matches))
        #     print('Initial C.keys()', C.keys())
        # else:
        for _, key in enumerate(matches.items()):
            C[key[1]].append(key[0])
        print('Initial C.keys()', C.keys())
        print('Initial C.values()', C.values())
        jKeys |= set(matches.keys())

        print(
            f"len jKeys {len(jKeys)}  len(J) {len(J)} jKeys {jKeys}  ")
        J_ = copy.copy(J)
        J = {}
        for key, value in enumerate(J_.items()):
            print(
                f'J.items() key {key}  value[0] {value[0]}  type(value[0])  {type(value[0])} value[1] {value[1]}')
            if value[0] in jKeys:
                print(f'value {value[0]} in jKeys)')
            else:
                print(f'value {value[0]} NOT in jKeys)')
                J[value[0]] = value[1]
        print(f'len filtered J {len(J)}  J {J}')
        if len(J) == 0:
            break
        V_ = copy.copy(V)
        for v, prefs in V_.items():
            # print(f'k,v in V k {k}  v {v}')
            prefs = [p for p in prefs if p in list(J.keys())]
            print(f'new prefs {prefs}')
            V[v] = prefs
        # V = {k: v for k, v in mydict.items() if k.startswith('foo')}

        # J = dict((key, value) in enumerate(J.items()))

        # J = dict((key, value) in enumerate(J.items()) if key not in jKeys)
        # J = dict(filter(lamba j, v: j not in jKeys, enumerate(J))
    # if len(J) > 0:
    #     print("len(J) > 0")
    #     V_ = sorted(C.items(), key=lambda kv: len(kv[1]))[:len(J)]
    #     match = Matcher(V_, J, forbidden, forbidden_v)

    #     # match volunteers and jobs; returns a mapping of jobs to volunteers
    #     matches = match()
    #     for key, value in enumerate(matches):
    #         C[value].append(key)

    # print('jobs', jobs)
    print('C.keys()', C.keys())
    print([(key, value) for key, value in enumerate(C)])
    if flipped:
        a = [([j.n for j in value[1]], value[0].n)
             for key, value in enumerate(C.items())]
    else:
        a = [(value[0].n, [j.n for j in value[1]])
             for key, value in enumerate(C.items())]
    # a = [(key.n, [j.n for j in C[key]]) for key in list(C.keys())]

    # a=[(matches[key].n, key.n) for key in list(matches.keys())]
    return jsonify(a)

    # swap the volunteers of two jobs, which should make the matching unstable
    # a, b = random.sample(jobs.keys(), 2)
    # jobs[b], jobs[a] = jobs[a], jobs[b]

    # match.is_stable(jobs, verbose=True)
