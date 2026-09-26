import re, os

base = r"C:\Users\biyyl234\Desktop\dabbit ai\spss_textbook\chapters"
expect = {"ch09.tex": (6, 16), "ch10.tex": (6, 18), "ch11.tex": (6, 7)}

for fn, (eb, ea) in expect.items():
    p = os.path.join(base, fn)
    txt = open(p, encoding="utf-8").read()
    basic = len(re.findall(r"\\basicalgo\{", txt))
    adv = len(re.findall(r"\\advancedalgo\{", txt))
    stars = len(re.findall(r"\\starmark", txt))
    # env balance
    envs = re.findall(r"\\(begin|end)\{([a-zA-Z]+)\}", txt)
    from collections import Counter
    c = Counter()
    for b, name in envs:
        c[(b, name)] += 1
    unbalanced = []
    names = set(n for _, n in envs)
    for n in names:
        if c[("begin", n)] != c[("end", n)]:
            unbalanced.append((n, c[("begin", n)], c[("end", n)]))
    # stray html tags
    stray = re.findall(r"</[a-zA-Z]+>", txt)
    # raw & not escaped
    raw_amp = len(re.findall(r"&(?!amp;|lt;|gt;)", txt))
    print(f"=== {fn} ===")
    print(f"  basic={basic} (expect {eb})  advanced={adv} (expect {ea})  total={basic+adv}  stars={stars}")
    print(f"  unbalanced envs: {unbalanced}")
    print(f"  stray html tags: {stray}")
    print(f"  raw & occurrences: {raw_amp}")
