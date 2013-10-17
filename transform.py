
class Transform:
    def __init__(self,name,call):
        self.name = name
        self.call = call
    def __call__(self,arg):
        return self.call(arg)

class CombinedTransform(Transform):
    def __init__(self,*subs):
        self.name = " et ".join(s.name for s in subs)
        self.subs = subs

    def __call__(self,arg):
        for f in self.subs:
            arg = f(arg)
        return arg

def replace_many(words):
    maxlen = max(len(x) for x in words)
    def fun(s):
        while len(s):
            for l in range(maxlen,0,-1):
                if s[:l] in words:
                    yield words[s[:l]]
                    s = s[l:]
                    break
            else:
                yield s[:1]
                s = s[1:]
    def fun2(s):
        return "".join(fun(s))
    return fun2

def powerset(l):
    if not l:
        return [[]]
    else:
        head = l[:1]
        tail = l[1:]
        return [ x for tail2 in powerset(tail) for x in [ tail2, head+tail2 ] ]

evil_twins = replace_many({
    ":)":":(",
    ":(":":)",
    ":))":":((",
    ":((":":))",
    ":>":":<",
    ":<":":>",
    ":')":":'(",
    ":]":":[",
    ":D":"D:",
    ":x":":o",
    ":P":":6",
    ":p":":6"})

leet = replace_many({
    "e":"3",
    "a":"4",
    "s":"5",
    "i":"1",
    "o":"0",
    "b":"8"})


basic_transforms = [Transform("maléfiques", evil_twins),
                  Transform("l33ts", leet),
                  Transform("bruyants", lambda s: s.upper())]

all_transforms = [CombinedTransform(*ts) for ts in powerset(basic_transforms)]
