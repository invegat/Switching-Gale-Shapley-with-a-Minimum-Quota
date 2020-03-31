from collections import defaultdict


class Matcher:

    def __init__(self, volunteers, jobs, forbidden_jobs, forbidden_volunteers):
        '''
        Constructs a Matcher instance.

        Takes a dict of volunteers's job preferences, `volunteers`,
        a dict of jobs's volunteer preferences, `jobs`,
        and a dict specifying which jobs are forbidden_jobs
        for each volunteer:

        >>> forbidden_jobs = { 'dan': ['ann', 'eve', ... ] }

        '''
        self.V = volunteers
        self.J = jobs
        self.forbidden_jobs = forbidden_jobs
        self.forbidden_volunteers = forbidden_volunteers
        self.jobs = {}
        self.pairs = []

        # we index volunteer/jobs preferences at initialization
        # to avoid expensive lookups when matching
        # `vrank[v][j]` is volunteer's ranking of jobs
        self.vrank = defaultdict(dict)
        # `jrank[j][v]` is job's ranking of volunteers
        self.jrank = defaultdict(dict)

        for v, prefs in volunteers.items():
            for i, j in enumerate(prefs):
                self.vrank[v][j] = i

        for j, prefs in jobs.items():
            for i, v in enumerate(prefs):
                self.jrank[j][v] = i

    def __call__(self):
        return self.match()

    def prefers(self, j, v, h):
        '''
        Test whether j prefers v over h.

        '''
        return self.jrank[j][v] < self.jrank[j][h]

    def is_forbidden(self, v, j):
        '''
        Test whether (v, j) is a forbidden pairing.

        '''
        return (j in self.forbidden_jobs.get(v, [])) or (v in self.forbidden_volunteers.get(j, []))

    def after(self, v, j):
        '''
        Return the job favored by v after j.

        '''
        prefs = self.V[v]               # v's ordered list of preferences
        # index of jobs following job in list of prefs
        i = self.vrank[v][j] + 1
        if i >= len(prefs):
            return ''                   # no more jobs left!
        j = prefs[i]                    # job following j in list of prefs
        if self.is_forbidden(v, j):     # if (v, j) is forbidden
            return self.after(v, j)     # try next j
        return j

    def match(self, volunteers=None, next=None, jobs=None):
        '''
        Try to match all volunteers with their next preferred job.

        '''
        if volunteers is None:
            volunteers = self.V.keys()         # get the complete list of volunteers
        if next is None:
            # if not defined, map each volunteer to their first preference
            next = dict((v, rank[0]) for v, rank in self.V.items())
        if jobs is None:
            jobs = {}                  # mapping from jobs to current volunteer
        if not len(volunteers):
            self.pairs = [(h, j) for j, h in jobs.items()]
            self.jobs = jobs
            return jobs
        lvol = list(volunteers)
        v, volunteers = lvol[0], lvol[1:]
        j = next[v]                     # next job for v to take
        if not j:                       # continue if no job to take
            return self.match(volunteers, next, jobs)
        next[v] = self.after(v, j)      # job after j in v's list of prefs
        if j in jobs:
            h = jobs[j]                # current volunteer
            if self.prefers(j, v, h):
                # volunteer becomes available again
                volunteers.append(h)
                jobs[j] = v            # j becomes v's job
            else:
                volunteers.append(v)           # v remains without a job
        else:
            jobs[j] = v                # j becomes job of v
        return self.match(volunteers, next, jobs)

    def is_stable(self, jobs=None, verbose=False):
        if jobs is None:
            jobs = self.jobs
        for j, v in jobs.items():
            i = self.V[v].index(j)
            preferred = self.V[v][:i]
            for p in preferred:
                # if p in self.forbidden_jobs.get(v, []):  # no need to worry about
                if self.is_forbidden(v, p):
                    continue                        # forbidden Volunteer/Jobs@
                if p not in jobs:
                    continue
                h = jobs[p]
                if self.J[p].index(v) < self.J[p].index(h):
                    msg = "{}'s volunteer to {} is unstable: " + \
                          "{} prefers {} over {} and {} prefers " + \
                          "{} over their current volunteer {}"
                    if verbose:
                        print(msg.format(v.n, j.n, v.n, p.n, j.n, p.n, v.n, h.n))
                    return False
        return True
