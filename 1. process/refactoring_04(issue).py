import csv

def show_report(portfoliofile, pricefile):
    
    with open(portfoliofile) as lines:
        rows = csv.reader(lines)
        headers = next(rows)
        portfolio = []
        for row in rows:
            if not row:     # <- Here!
                continue
            record = dict(zip(headers, row))
            portfolio.append(record)
        
    with open(pricefile) as lines:
        rows = csv.reader(lines)
        prices = []
        for row in rows:
            if not row:     # <- Here!
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

# show_report('../Data/portfolio_01.csv', '../Data/prices_01.csv')

def main(args):
    if len(args) != 3:
        raise SystemExit('Usage: %s portfile pricefile' % args[0])
    show_report(args[1], args[2])

if __name__ == '__main__':
    import sys
    main(sys.argv)