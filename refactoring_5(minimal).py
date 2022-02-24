import csv

with open('portfolio.csv') as lines:
    rows = csv.reader(lines)
    headers = next(rows)
    portfolio = []
    for row in rows:
        if not row:
            continue
        if headers:
            record = dict(zip(headers, row))
        else:
            record = tuple(row)
        portfolio.append(record)
    
with open('prices.csv') as lines:
    rows = csv.reader(lines)
    prices = []
    for row in rows:
        if not row:
            continue
        record = tuple(row)
        prices.append(record)
    prices = dict(prices)

report = []
for stock in portfolio:
    current_price = float(prices[stock['name']])
    change = float(current_price) - float(stock['price'])
    summary = (stock['name'], int(stock['shares']), current_price, change)
    report.append(summary)

headers = ('Name','Shares','Price','Change')
print('%10s %10s %10s %10s' % headers)
print(('-'*10 + ' ')*len(headers))
for row in report:
    print('%10s %10d %10.2f %10.2f' % row)

