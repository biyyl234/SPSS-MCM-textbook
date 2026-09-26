import json, sys, os

base = r"C:\Users\biyyl234\Desktop\dabbit ai\spss_textbook\data"
out = r"C:\Users\biyyl234\Desktop\dabbit ai\spss_textbook\work"
os.makedirs(out, exist_ok=True)

files = {
    "ch09": "cat_09_问卷研究.json",
    "ch10": "cat_10_医学统计.json",
    "ch11": "cat_11_机器学习.json",
}

for key, fn in files.items():
    d = json.load(open(os.path.join(base, fn), encoding="utf-8"))
    lines = []
    lines.append(f"### {key} {d['category']} total={d['total']} basic={d['basic_count']} adv={d['advanced_count']}")
    lines.append(f"STARS: {d['star_algos']}")
    for c in d["cases"]:
        lines.append("\n" + "="*80)
        lines.append(f"SEQ={c['seq']} | NAME={c['algorithmName']} | TIER={c['tier']} | STAR={c['is_star']}")
        lines.append(f"PARAMS: {json.dumps(c.get('params',{}), ensure_ascii=False)}")
        bg = c.get('background','') or ''
        lines.append(f"BACKGROUND: {bg[:800]}")
        rep = c.get('report','') or ''
        lines.append(f"REPORT(len={len(rep)}): {rep[:2500]}")
    outp = os.path.join(out, f"{key}_dump.txt")
    open(outp, "w", encoding="utf-8").write("\n".join(lines))
    print("wrote", outp, os.path.getsize(outp))
