1. 당장 한 번 쓰려고 급하게 만든 코드. 쓸모없는 주석도 붙어있다.

```python
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
```

만약 코드를 당장 한 번 쓰고 말거라면, 이런식으로 간략하게 당장 결과만 볼 수 있을정도라면 충분할 것입니다.

  종종 코드는 무조건 간결한게 좋으니 약어도 쓰고 해서 짧게 만드는게 좋은거 아닌가? 하시는 분도 계실테고, 위 코드도 오히려 짧아서 좋은데.. 싶을수도 있겠지만, 이게 단순히 표 하나 만드는 코드가 아니라, 좀 더 복잡한 비즈니스 로직을 담은 코드였다면 과연 이런 걸 알아볼 수 있을까요?

  분명 며칠, 몇주, 몇달 후 분명 저런 코드를 마주할텐데, 그때도 과연 저 ‘당장 짜기 쉬운 코드'가 우리에게 도움이 될까요?

그럼에도 사실 많은 개발자가 귀찮다, 시간없다 등 수많은 이유와 변명을 가지고 ‘그 때 가서 이해 하면 되니 일단 돌아가게만 만들자’는 생각으로 코드를 작성하고있습니다.

  그래서 간단하게나마 공부 할 겸, 예시를 한번 직접 만들어보고 싶어서 적당한(짧은) 코드를 가지고 하나씩 수정하는 과정으로 예시를 만들어봤습니다. 최종 소스와 데이터는 위키독스의 ‘실용 파이썬 프로그래밍'의 예제에서 발췌하였습니다.

  위 코드는 포트폴리오와 가격표 csv파일을 가지고 현재 포트폴리오가 얼마나 손익을 보고있는지를 사람 눈으로 보기 좋게 프린트 해 주는 단순한 프로그램입니다.

![< portfolio.csv 예시>](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/2586d3a6-87dd-4fe5-adee-ec05da3c8232/Untitled.png)

< portfolio.csv 예시>

![< prices.csv 예시>](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/aa4751c2-d084-4b59-9360-d5fc4230cd75/Untitled.png)

< prices.csv 예시>

![<결과값 예시>](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/6793a4a3-aa5c-4d2b-b497-958a0b4fe5c3/Untitled.png)

<결과값 예시>

뭐 사실 이런 짧은 코드야 그냥 쓰는게 훨씬 간편하고 수정도 편하지만, 일단 이게 꽤나 복잡하고 큰 프로젝트라고 가정하고, 최근 클린코드를 읽으면서 배운 것을 적용 해 봅시다.

먼저 위 코드에서 다른것은 그대로 두고 변수명만 정리를 좀 해보겠습니다.

1. 변수명만 다듬어진 코드

```python
import csv

with open('../Data/portfolio_01.csv') as lines:
    rows = csv.reader(lines)
    headers = next(rows)
    portfolio = []
    for row in rows:
        record = dict(zip(headers, row)) # 헤더와 합치기
        portfolio.append(record)
    
with open('../Data/prices_01.csv') as lines:
    rows = csv.reader(lines)
    prices = []
    for row in rows:
        record = tuple(row)
        prices.append(record)
    prices = dict(prices) # 딕셔너리로 변환

report = []
for stock in portfolio:
    current_price = float(prices[stock['name']])
    change = float(current_price) - float(stock['price'])
    summary = (stock['name'], int(stock['shares']), current_price, change) # 이름, 보유량, 가격, 차익
    report.append(summary)

headers = ('Name','Shares','Price','Change')
print('%10s %10s %10s %10s' % headers)
print(('-'*10 + ' ')*len(headers))
for row in report:
    print('%10s %10d %10.2f %10.2f' % row)
```

일단 비교를 위해 주석을 남겨두긴 했지만, 변수명만 바꿔도 주석이 전혀 필요없어졌습니다. 전부 삭제하겠습니다.

또한 굳이 눈에 힘을 주지 않아도, 대충 무슨 내용이겠구나 하는 흐름이 보입니다.

그런데 지금 상태로는 매번 편집기를 켜서 데이터를 바꿔주어야 하기에 간단하게 함수로 정리 해 봅시다.

1. 함수로 정리된 코드

```python
import csv

def show_report(portfoliofile, pricefile):
    
    with open(portfoliofile) as lines:
        rows = csv.reader(lines)
        headers = next(rows)
        portfolio = []
        for row in rows:
            record = dict(zip(headers, row))
            portfolio.append(record)
        
    with open(pricefile) as lines:
        rows = csv.reader(lines)
        prices = []
        for row in rows:
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
```

이렇게, 터미널에서 쓸 수 있는 간단한 프로그램이 일단 완성은 되었습니다.

여기서 우리는 이 코드를 

1. 뭔가 복잡하고 
2. 나중에 재사용할 필요가 있으며, 
3. 꾸준히 기능 개선이 필요한 프로젝트

라고 가정 해 보겠습니다.

  그런데 이 코드로 서비스를 하다 보니, 종종 이런 오류가 발생합니다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/5c81fa42-0b36-4443-bdce-f08f1f3a1f08/Untitled.png)

  이 코드는 뭔가 복잡하고 어려운 코드이니, 뭐든간에 힘들고 복잡한 과정을 거쳐서 원인을 찾아냅니다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/289eeb7e-a4a6-4f3c-96b2-96738a131890/Untitled.png)

  원인을 찾다보니, 데이터를 작성하던 사용자가 실수로 엔터를 한번 더 쳤나봅니다.(9행) 공백이 들어가면서, length가 0이라 dictionary로 변경을 할 수 없는게 원인이었습니다. 

귀찮으니 그냥 한칸 지우고 쓰세요. 라고 하고싶지만.. 그럴순 없으니 이런 경우에 대응 할 수 있도록 조치를 해야겠습니다.

1. 이슈에 대응한 코드

```python
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
```

자 이제 간단하게 두줄씩 추가해서 우선 이슈를 해결했습니다. 만, 사실은 우리는 매우 복잡한 코드에서 유사하게 반복되는 여러 컴포넌트를 하나씩 일일이 수정해주었습니다. 

물론 이 과정에서 몇 개씩 빼먹어서 QA에서 발견한 부분도 있지만, 다행히 사용자들이 쓰는데에는 문제가 없는 것 같습니다.(모릅니다.. 터지기 전까진.. 알면 안터지지..)

  그렇기에 언젠가 발생할 문제를 막기 위해 조금씩 기술부채를 상환해 봅시다.

1. 반복되는 코드를 함수화 하기

```python
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
```

  보시다시피 csv파일을 파싱하는, (2개밖에 없지만) 수없이 여기저기서 반복되던 코드를 parse_csv라는 하나의 함수로 단순화 하였습니다. bool 인자는 일단 그냥 쓰겠습니다. 또한 나머지 코드들도 최대한 함수화 해서, 추후 변동이나 재사용이 용이하도록 조치하겠습니다.

1. 완전히 함수화 된 코드

```python
import csv

def show_report(portfoliofile, pricefile):
    portfolio = read_portfolio(portfoliofile)
    prices = read_prices(pricefile)
    report = make_report_data(portfolio, prices)
    print_report(report)
        
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

def read_portfolio(filename):
    with open(filename) as lines:
        return parse_csv(lines, has_headers = True)
    
def read_prices(filename):
    with open(filename) as lines:
        return dict(parse_csv(lines))
    
def make_report_data(portfolio, prices):
    report = []
    for stock in portfolio:
        current_price = float(prices[stock['name']])
        change = float(current_price) - float(stock['price'])
        summary = (stock['name'], int(stock['shares']), current_price, change)
        report.append(summary)
    return report

def print_report(reportdata):
    headers = ('Name','Shares','Price','Change')
    print('%10s %10s %10s %10s' % headers)
    print(('-'*10 + ' ')*len(headers))
    for row in reportdata:
        print('%10s %10d %10.2f %10.2f' % row)

# show_report('../Data/portfolio_01.csv', '../Data/prices_01.csv')

def main(args):
    if len(args) != 3:
        raise SystemExit('Usage: %s portfile pricefile' % args[0])
    show_report(args[1], args[2])

if __name__ == '__main__':
    import sys
    main(sys.argv)
```

  매일같은 업무에 치이면서도 어떻게 시간을 내어서 다같이 우리의 프로젝트를 완전히 함수화 했습니다. 물론 아직 맘에 안드는 부분이 있지만, 그래도 꽤나 정돈된 모습을 보입니다. 

  그런데 어느 날, 또다른 이슈가 보고됩니다. 음.. 이번에도 역시 긴 시간을 들여 복잡하고 어려운 코드를 하나씩 뜯어보면서 원인을 찾습니다.

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/430634d3-3195-4661-b329-937e66bcde78/Untitled.png)

  이번에는 타입변경 과정에서 뭔가 문제가 있는 것 같습니다. 이전과 같이 매우 힘들고 어려운 과정을 거쳐서 원인을 찾아보니, 역시나 아까 마음에 안들던 부분에 문제가 좀 있었습니다. 

  기존 코드에서는 make_report_data 함수에서 일부 데이터의 형변환을 진행했는데, 이게 사실 parse_csv에서 똑바로 처리해서 넘겨야지 make_report_data에서 할 일은 아닌것 같습니다. 후자는 그냥 데이터를 합쳐서 하나로 만드는, ‘하나의' 작업만 하면 됩니다. 이제 여태 남의 일까지 짬처리하던 함수를 좀 더 정리 해 줍니다.

1. 함수의 역할이 정리된 코드

```python
import csv

def show_report(portfoliofile, pricefile):
    portfolio = read_portfolio(portfoliofile)
    prices = read_prices(pricefile)
    report = make_report_data(portfolio, prices)
    print_report(report)

def read_portfolio(filename):
    with open(filename) as lines:
        return parse_csv(lines, has_headers = True, types = [str, int, float])
    
def read_prices(filename):
    with open(filename) as lines:
        return dict(parse_csv(lines, types = [str, float]))
        
def parse_csv(lines, has_headers = False, types = None):
    rows = csv.reader(lines)
    headers = next(rows) if has_headers else []
    results = []
    for row in rows:
        if not row:
            continue
        if types:    # <- Here!
            row = [func(val) for func, val in zip(types, row)]
        if headers:
            result = dict(zip(headers, row))
        else:
            result = tuple(row)
        results.append(result)
    
    return results
    
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

def main(args):
    if len(args) != 3:
        raise SystemExit('Usage: %s portfile pricefile' % args[0])
    show_report(args[1], args[2])

if __name__ == '__main__':
    import sys
    main(sys.argv)
```

아, 아직 쪼오금 마음에 안드는 구석이 있지만, 그래도 처음 코드에 비해서는 심적으로나 시각적으로나 모두 좀 더 편안해진 모습을 보이고있습니다.

  자 그러면 이제 다음 단계로, 이런식으로 코드를 정리하는 것이 왜 미래가 편안한지에 대해서 알아보겠습니다.

비교 대상은, 1번 코드는 너무 양심없으니 2번 코드와 7번 코드를 활용하겠습니다.

```python
import csv

def show_report(portfoliofile, pricefile):
    
    with open(portfoliofile) as lines:
        rows = csv.reader(lines)
        headers = next(rows)
        portfolio = []
        for row in rows:
            if not row:
                continue
            record = dict(zip(headers, row))
            portfolio.append(record)
        
    with open(pricefile) as lines:
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

# show_report('../Data/portfolio_01.csv', '../Data/prices_01.csv')
# show_report('../Data/portfolio_02_empty_row.csv', '../Data/prices_02_empty_row.csv')
# show_report('../Data/portfolio_03_delimiter.csv', '../Data/prices_03_delimiter.csv')
# show_report('../Data/portfolio_04_null.csv', '../Data/prices_04_null.csv')

def main(args):
    if len(args) != 3:
        raise SystemExit('Usage: %s portfile pricefile' % args[0])
    show_report(args[1], args[2])

if __name__ == '__main__':
    import sys
    main(sys.argv)
```

```python
import csv

def show_report(portfoliofile, pricefile):
    portfolio = read_portfolio(portfoliofile)
    prices = read_prices(pricefile)
    report = make_report_data(portfolio, prices)
    print_report(report)
        
def parse_csv(lines, has_headers = False, types = None):
    rows = csv.reader(lines)
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
# show_report('../Data/portfolio_02_empty_row.csv', '../Data/prices_02_empty_row.csv')
# show_report('../Data/portfolio_03_delimiter.csv', '../Data/prices_03_delimiter.csv')
# show_report('../Data/portfolio_04_null.csv', '../Data/prices_04_null.csv')

def main(args):
    if len(args) != 3:
        raise SystemExit('Usage: %s portfile pricefile' % args[0])
    show_report(args[1], args[2])

if __name__ == '__main__':
    import sys
    main(sys.argv)
```

(예시를 너무 짧은 코드로 들다 보니 오히려 오른쪽이 길어져 버렸는데, 다들 이해 해 주시리라 믿습니다.)

오른쪽은 바쁜 시간에 짬을내어 리팩토링을 마친 평행우주 2라고 가정하겠습니다.

왼쪽은 리팩토링을 하지 않고, 부채를 그대로 끌어안으며 안일하게 살아가던 평행우주 1이고

  어느 날, 사용자들이 활용하는 편집기가 패치가 되어서 이제는 csv파일이 아닌 ssv형식으로 바뀌었다고 합니다. 따라서 이에 대응을 해야합니다.

이번에는 평행우주 2부터 보겠습니다.

```python
def parse_csv(lines, has_headers = False, types = None):
    rows = csv.reader(lines, delimiter = ' ')   # <- Here!
    
		...

    return results
```

평행우주 2 에서는 명확하게 parse_csv함수 하나만 건드리니 모든 문제가 해결됐습니다. 모두가 바로 퇴근 할 수 있고, 앞으로도 다른 문제가 날 확률은 매우 낮아보입니다.

그렇다면 평행우주 1은어떨까요?

```python
with open(portfoliofile) as lines:
		rows = csv.reader(lines, delimiter = ' ')   # <- Here!
		headers = next(rows)
		...
        
with open(pricefile) as lines:
    rows = csv.reader(lines, delimiter = ' ')   # <- Here!
    prices = []
		...
...

...

...
```

역시 위에서처럼, 일일이 하나씩 손수 바꿔줘야합니다.

다시 말씀드리지만 우리 코드는 간단해 보이지만 뭔가 많이 어렵고 복잡한 로직이므로, 관련된 부분들 모두 찾아서 손수 수정해줘야 합니다. 또한, 만에 하나 뭔가를 빼먹었는데, 자주 사용되는 기능이 아니라면... 그렇게 아무도 모르게 코드에는 점점 더 큰 똥이 만들어지게 됩니다.

간략한 코드로 예시를 설명하려다 보니, 지나치게 간략화를 해버려서 뭔가 많이 아쉬운 설명이 되어버렸지만.. 그래도 개념적으로는 나름 이해를 한 것 같아서 다행입니다. 확실히 코드는 컴퓨터가 아니라 사람이 이해하게 쓰는 것이 맞습니다.

스파게티 없이, 다들 클린한 프로그래밍 즐기시길 바랍니다.
