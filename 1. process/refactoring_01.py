import csv

with open('../Data/portfolio_02_empty_row.csv') as f:
    pf = csv.reader(f)
    hdrs = next(pf)
    pfl = []
    for i in pf:
        rec = dict(zip(hdrs, i)) # 헤더와 합치기
        pfl.append(rec)
        
with open('../Data/prices_02_empty_row.csv') as f:
    prc = csv.reader(f)
    prcs = []
    for i in prc:
        rec = tuple(i)
        prcs.append(rec)
    prcs = dict(prcs) # 딕셔너리로 변환

rpt = []
for p in pfl:
    cur_prc = float(prcs[p['name']])
    chg = float(cur_prc) - float(p['price'])
    rep = (p['name'], int(p['shares']), cur_prc, chg) # 이름, 보유량, 가격, 차익
    rpt.append(rep)

hdrs = ('Name','Shares','Price','Change')
print('%10s %10s %10s %10s' % hdrs)
print(('-'*10 + ' ')*len(hdrs))
for r in rpt:
    print('%10s %10d %10.2f %10.2f' % r)