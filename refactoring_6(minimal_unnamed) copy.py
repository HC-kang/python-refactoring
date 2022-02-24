import csv

with open('portfolio.csv') as f:
    pf = csv.reader(f)
    hdrs = next(pf)
    pfl = []
    for i in pf:
        if not i:
            continue
        if hdrs:
            rec = dict(zip(hdrs, i))
        else:
            rec = tuple(i)
        pfl.append(rec)
        
with open('prices.csv') as f:
    prc = csv.reader(f)
    prcs = []
    for i in prc:
        if not i:
            continue
        rec = tuple(i)
        prcs.append(rec)
    prcs = dict(prcs)

rpt = []
for p in pfl:
    cur_prc = float(prcs[p['name']])
    chg = float(cur_prc) - float(p['price'])
    rep = (p['name'], int(p['shares']), cur_prc, chg)
    rpt.append(rep)

hdrs = ('Name','Shares','Price','Change')
print('%10s %10s %10s %10s' % hdrs)
print(('-'*10 + ' ')*len(hdrs))
for r in rpt:
    print('%10s %10d %10.2f %10.2f' % r)

