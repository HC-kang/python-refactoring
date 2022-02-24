import report

def portfolio_cost(filename):
    '''
    portfolio 파일을 가지고 전체 cost(shares * price)를 계산하는 함수.
    '''
    portfolio = report.read_portfolio(filename)
    return sum([s['shares'] * s['price'] for s in portfolio])

def main(args):
    if len(args) != 2:
        raise SystemExit('Usage: %s portfoliofile' % args[0])
    filename = args[1]
    print('Total cost:', portfolio_cost(filename))

if __name__ == '__main__':
    import sys
    main(sys.argv)

