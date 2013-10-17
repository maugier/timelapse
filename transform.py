
class Transform:
	def __init__(self,name,call):
		self.name = name
		self.call = call
	def __call__(self,*k,**kw):
		return self.call(*k, **kw)

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


all_transforms = [Transform("maléfiques", evil_twins),
                  Transform("l33ts", leet),
		  Transform("bruyants", lambda s: s.upper())]
