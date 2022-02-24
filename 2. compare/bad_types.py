import csv

def show_report(portfoliofile, pricefile):
    
    with open(portfoliofile) as lines:
        rows = csv.reader(lines)
        headers = next(rows)
        types = [str, int, float]    # <- Here!
        portfolio = []
        for rowno, row in enumerate(rows, 1):
            if not row:
                continue
            if types:    # <- Here!
                try:
                    row = [func(val) for func, val in zip(types, row)]
                except:
                    print(f"Row {rowno}: Couldn't convert {row}")
                    continue
            record = dict(zip(headers, row))
            portfolio.append(record)
        
    with open(pricefile) as lines:
        rows = csv.reader(lines)
        types = [str, float]    # <- Here!
        prices = []
        for rowno, row in enumerate(rows, 1):
            if not row:
                continue
            if types:    # <- Here!
                try:
                    row = [func(val) for func, val in zip(types, row)]
                except:
                    print(f"Row {rowno}: Couldn't convert {row}")
                    continue
            record = tuple(row)
            prices.append(record)
        prices = dict(prices)

    report = []
    for stock in portfolio:
        current_price = prices[stock['name']]
        change = current_price - stock['price']
        summary = (stock['name'], stock['shares'], current_price, change)
        report.append(summary)

    headers = ('Name','Shares','Price','Change')
    print('%10s %10s %10s %10s' % headers)
    print(('-'*10 + ' ')*len(headers))
    for row in report:
        print('%10s %10d %10.2f %10.2f' % row)

# show_report('../Data/portfolio_01.csv', '../Data/prices_01.csv')
# show_report('../Data/portfolio_04_null.csv', '../Data/prices_04_null.csv')

def main(args):
    if len(args) != 3:
        raise SystemExit('Usage: %s portfile pricefile' % args[0])
    show_report(args[1], args[2])

if __name__ == '__main__':
    import sys
    main(sys.argv)