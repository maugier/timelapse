import re

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

nick_pattern = re.compile(r'^(<.*?>\s+)(.*)') 

def on_text(f):
    def fun(s):
        match = nick_pattern.match(s)
        if match:
            (nick,msg) = match.groups()
            return "".join([nick, f(msg)])
        else:
            return f(s)
    return fun


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

double_vowels = replace_many({'a':'aa','e':'ee','i':'ii','o':'oo','u':'uu','y':'yy',
                              'A':'AA','E':'EE','I':'II','O':'OO','U':'UU','Y':'YY'})

@on_text
def suisses(s):
    return "De dieu de dieu, {0} ou bien ?".format(double_vowels(s))

@on_text
def marseillais(s):
    return "Putain, {0} con.".format(s)

@on_text
def yoda(s):
    l = s.split()
    l.reverse()
    return " ".join(l)

zozote = replace_many({'j':'z', 'J':'Z', 'ch':'s', 's':'f', 'S':'F'})

grossier = on_text(replace_many({" du ":" du putain de ", " de la ": " de la saloperie de ", " la ":" la salope de ", 
                                 " le ": " l'enculé de ", " les ": " les enculés de ", " un ":" un connard de ",
                                 " ce ": " ce putain de ", " cette ": " cette chiure de ", " une ":" une grognasse de ",
                                 " des " : " des merdes de ", " ma ": " ma pute de ", " mon ":" mon pédé de ",
                                 " ton ": " ton trouduc de ", " ta ": " ta conasse de ", " son ":" son salaud de ",
                                 " sa ": " sa truie de "}))

basic_transforms = [
                  Transform("marseillais", marseillais),
                  Transform("suisses", suisses),
                  Transform("grossiers", grossier),
                  Transform("maléfiques", evil_twins),
                  Transform("zozotants", zozote),
                  Transform("yodas", yoda),
                  Transform("l33ts", leet),
                  Transform("bruyants", lambda s: s.upper())]

all_transforms = [CombinedTransform(*ts) for ts in powerset(basic_transforms) if len(ts) < 3]
