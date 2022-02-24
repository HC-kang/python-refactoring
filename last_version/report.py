import fileparse

def read_portfolio(filename):
    """
    주식 포트폴리오 파일을 [{'name': s, 'shares': d, 'price': f}]형태의 리스트로 반환한다.
    
    :filename: str
    """
    with open(filename) as lines:
        return fileparse.parse_csv(lines, select=['name','shares','price'], types=[str,int,float])

def read_prices(filename):
    """
    주식 가격 파일을 {'name': price}형태의 딕셔너리로 반환한다.
    
    :filename: str
    """
    with open(filename) as lines:
        return dict(fileparse.parse_csv(lines, types=[str,float], has_headers=False))

def make_report_data(portfolio,prices):
    """
    딕셔너리들의 리스트인 portfolio와 딕셔너리인 prices를 받아 [(name, shares, price, change), ]형태로 반환한다.
    
    :portfolio: list
    :prices: dict
    """
    rows = []
    for stock in portfolio:
        current_price = prices[stock['name']]
        change = current_price - stock['price']
        summary = (stock['name'], stock['shares'], current_price, change)
        rows.append(summary)
    return rows

def print_report(reportdata):
    """
    [(name, shares, price, change),...]형태의 자료를 보기 좋게 출력한다.
    
    :reportdata: list
    """
    headers = ('Name','Shares','Price','Change')
    print('%10s %10s %10s %10s' % headers)
    print(('-'*10 + ' ')*len(headers))
    for row in reportdata:
        print('%10s %10d %10.2f %10.2f' % row)

def portfolio_report(portfoliofile, pricefile):        
    """
    portfolio 파일과 price 파일을 가지고 보고서를 출력한다.
    
    :portfoliofile: str
    :pricefile: str
    """
    portfolio = read_portfolio(portfoliofile)
    prices = read_prices(pricefile)

    report = make_report_data(portfolio, prices)

    print_report(report)

def main(args):
    if len(args) != 3:
        raise SystemExit('Usage: %s portfile pricefile' % args[0])
    portfolio_report(args[1], args[2])

if __name__ == '__main__':
    import sys
    main(sys.argv)
