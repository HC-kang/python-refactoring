import csv

with open('portfolio.csv') as lines:
    rows = csv.reader(lines)
    headers = next(rows)
    select=['name','shares','price']
    
    indices = [ headers.index(colname) for colname in select ]
    headers = select

    portfolio = []
    types=[str,int,float]
    for rowno, row in enumerate(rows, 1):
        if not row:
            continue
        row = [ row[index] for index in indices]
        if types:
            try:
                row = [func(val) for func, val in zip(types, row)]
            except ValueError as e:
                print(f"Row {rowno}: Couldn't convert {row}")
                print(f"Row {rowno}: Reason {e}")

        if headers:
            record = dict(zip(headers, row))
        else:
            record = tuple(row)
        portfolio.append(record)
    
with open('prices.csv') as lines:
    rows = csv.reader(lines)
    
    prices = []
    types=[str,float]
    for rowno, row in enumerate(rows, 1):
        if not row:
            continue

        if types:
            try:
                row = [func(val) for func, val in zip(types, row)]
            except ValueError as e:
                print(f"Row {rowno}: Couldn't convert {row}")
                print(f"Row {rowno}: Reason {e}")

        record = tuple(row)
        prices.append(record)
    prices = dict(prices)

rows = []
for stock in portfolio:
    current_price = prices[stock['name']]
    change = current_price - stock['price']
    summary = (stock['name'], stock['shares'], current_price, change)
    rows.append(summary)
report =  rows

headers = ('Name','Shares','Price','Change')
print('%10s %10s %10s %10s' % headers)
print(('-'*10 + ' ')*len(headers))
for row in report:
    print('%10s %10d %10.2f %10.2f' % row)

