import sqlite3 as db
import re
from os.path import dirname, join

INIT = False

INVALID = (-1, '', '')

lumis = {}
pools = {}
whitelists = {}
blacklists = {}

# workaround for old global variable
global anapool
anapool = set()


class listdict(dict):
    def __missing__(self, key):
        self[key] = []
        return self[key]


subpools = listdict()
norms = listdict()
smc = listdict()

name_pat = re.compile(r'([A-Z0-9]+_\d{4}_[IS]\d{6,8}[^/]*)/(d\d+-x\d+-y\d+)')
subpool_pat = re.compile(r'([A-Z0-9]+_\d{4}_[IS]\d{6,8}[^/]*)_(R\d+)')


def init_dbs():
    dbfile = join(dirname(__file__), 'analyses.db')
    conn = db.connect(dbfile)
    c = conn.cursor()

    for row in c.execute('SELECT id,lumi,pool FROM analysis;'):
        ana, lumi, pool = row
        lumis[ana] = lumi
        if pool:
            pools[ana] = pool
            anapool.add(pool)
        else:
            pools[ana] = ''

    for row in c.execute('SELECT id,group_concat(pattern) FROM whitelist GROUP BY id;'):
        ana, patterns = row
        patterns = patterns.split(',')
        whitelists[ana] = patterns

    for row in c.execute('SELECT id,group_concat(pattern) FROM blacklist GROUP BY id;'):
        ana, patterns = row
        patterns = patterns.split(',')
        blacklists[ana] = patterns

    for row in c.execute('SELECT id,pattern,subid FROM subpool;'):
        ana, pattern, subid = row
        subid = 'R%s' % (subid + 1)
        subpools[ana].append((pattern, subid))

    for row in c.execute('SELECT id,pattern,norm,scalemc FROM normalization;'):
        ana, pattern, norm, scalemc = row
        norms[ana].append((pattern, norm))
        smc[ana].append((pattern, scalemc))

    conn.close()

    global INIT
    INIT = True


class InvalidPath(Exception):
    pass


def splitPath(path):
    m = name_pat.search(path)
    if not m:
        m1 = subpool_pat.match(path)
        if not m1:
            return INVALID
            # print 'Path not found or understood for "%s"' % path
            # raise InvalidPath('Parse error in "%s"' % path)
        else:
            analysis = m1.group(1)
            tag = ''
            subpool = m1.group(2)
    else:
        analysis = m.group(1)
        tag = m.group(2)
        subpool = ''
    return analysis, tag, subpool


def validHisto(h):
    """Tests a histo path to see if it is a valid contur histogram"""
    if not INIT:
        init_dbs()
    try:
        ana, tag, sub = splitPath(h)
    except InvalidPath:
        return INVALID

    if ana in lumis:
        if ana not in whitelists:
            if ana not in blacklists:
                return True
            elif ana in blacklists:
                for pattern in blacklists[ana]:
                    if pattern in tag:
                        return False
                    # else:
                    #    return True
                return True
        elif ana in whitelists:
            for pattern in whitelists[ana]:
                if pattern in tag:
                    return True
                # else:
                #    return False
            return False
    else:
        return False


def LumiFinder(h):
    if not INIT:
        init_dbs()

    try:
        ana, tag, sub = splitPath(h)
    except InvalidPath:
        return INVALID

    try:
        lumi, pool = lumis[ana], pools[ana]
    except KeyError:
        return INVALID

    # tag is '' if we're looking at an R.. group
    # but R goups should not be excluded here
    if ana in whitelists and tag:
        for pattern in whitelists[ana]:
            if pattern in tag:
                break
        else:
            return INVALID

    if ana in blacklists:
        for pattern in blacklists[ana]:
            if pattern in tag:
                return INVALID

    subpool = sub

    if ana in subpools:
        for p, subid in subpools[ana]:
            if re.search(p, tag):
                subpool = subid
                break
        # else:
        # not in any subpools
        # strict mode should exit here
        # return INVALID

    return lumi, pool, subpool


#############################################################################################
### Special function to help with plots normalised to total xs
def isNorm(h):
    if not INIT:
        init_dbs()

    ana, tag, _ = splitPath(h)

    isNorm = False
    normFac = 1.0
    scale_MC = 0

    if ana in norms:
        for p, norm in norms[ana]:
            if re.search(p, tag):
                isNorm = True
                normFac = norm
                break

        for p, scalemc in smc[ana]:
            if re.search(p, tag):
                scale_MC = scalemc
                break

    return isNorm, normFac, scale_MC
