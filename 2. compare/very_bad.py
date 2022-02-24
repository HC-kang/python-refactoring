import csv

with open('../Data/portfolio_01.csv') as f:
    pf = csv.reader(f)
    hdr = next(pf)
    pfl = []
    for i in pf:
        rec = dict(zip(hdr, i))
        pfl.append(rec)
        
with open('../Data/prices_01.csv') as f:
    prc = csv.reader(f)
    prcs = []
    for i in prc:
        rec = tuple(i)
        prcs.append(rec)
    prcs = dict(prcs)

rpt = []
for p in pfl:
    prc2 = float(prcs[p['name']])
    chg = float(prc2) - float(p['price'])
    rep = (p['name'], int(p['shares']), prc2, chg)
    rpt.append(rep)

hdr = ('Name','Shares','Price','Change')
print('%10s %10s %10s %10s' % hdr)
print(('-'*10 + ' ')*len(hdr))
for r in rpt:
    print('%10s %10d %10.2f %10.2f' % r)