
all_transforms = {"Evil Twins": evil_twins,
                  "L33ts": leet}

def replace_many(words):
	maxlen = max(len(x) for x in words)
	def fun(s):
		while len(s):
			for l in range(maxlen,1,-1):
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
	":D","D:",
	":x",":o",
	":P",":6",
	":p",":6"})

leet = replace_many({
	"e":"3",
	"a":"4",
	"s":"5",
	"i","1",
	"o","0",
	"b","8"})
