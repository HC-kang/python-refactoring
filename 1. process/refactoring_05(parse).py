import csv

def show_report(portfoliofile, pricefile):
    
    with open(portfoliofile) as lines:
        portfolio = parse_csv(lines, has_headers=True)
        
    with open(pricefile) as lines:
        prices = dict(parse_csv(lines))

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
        
def parse_csv(lines, has_headers = False):
    rows = csv.reader(lines)
    headers = next(rows) if has_headers else []
    
    results = []
    for row in rows:
        if not row:
            continue
        if headers:
            result = dict(zip(headers, row))
        else:
            result = tuple(row)
        results.append(result)
    
    return results

# show_report('../Data/portfolio_01.csv', '../Data/prices_01.csv')

def main(args):
    if len(args) != 3:
        raise SystemExit('Usage: %s portfile pricefile' % args[0])
    show_report(args[1], args[2])

if __name__ == '__main__':
    import sys
    main(sys.argv)