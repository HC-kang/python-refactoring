import csv

def show_report(portfoliofile, pricefile):
    portfolio = read_portfolio(portfoliofile)
    prices = read_prices(pricefile)
    report = make_report_data(portfolio, prices)
    print_report(report)
        
def parse_csv(lines, has_headers = False, types = None):
    rows = csv.reader(lines, delimiter = ' ')   # <- Here!
    headers = next(rows) if has_headers else []
    results = []
    for row in rows:
        if not row:
            continue
        if types:
            row = [func(val) for func, val in zip(types, row)]
        if headers:
            result = dict(zip(headers, row))
        else:
            result = tuple(row)
        results.append(result)
    
    return results

def read_portfolio(filename):
    with open(filename) as lines:
        return parse_csv(lines, has_headers = True, types = [str, int, float])
    
def read_prices(filename):
    with open(filename) as lines:
        return dict(parse_csv(lines, types = [str, float]))
    
def make_report_data(portfolio, prices):
    report = []
    for stock in portfolio:
        current_price = prices[stock['name']]
        change = current_price - stock['price']
        summary = (stock['name'], stock['shares'], current_price, change)
        report.append(summary)
    return report

def print_report(reportdata):
    headers = ('Name','Shares','Price','Change')
    print('%10s %10s %10s %10s' % headers)
    print(('-'*10 + ' ')*len(headers))
    for row in reportdata:
        print('%10s %10d %10.2f %10.2f' % row)

# show_report('../Data/portfolio_01.csv', '../Data/prices_01.csv')
# show_report('../Data/portfolio_03_delimiter.csv', '../Data/prices_03_delimiter.csv')

def main(args):
    if len(args) != 3:
        raise SystemExit('Usage: %s portfile pricefile' % args[0])
    show_report(args[1], args[2])

if __name__ == '__main__':
    import sys
    main(sys.argv)