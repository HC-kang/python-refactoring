import csv

def parse_csv(lines, select=None, types=None, has_headers=True, delimiter=',', silence_errors=False):
    '''
    CSV 파일의 각 row를 list 형태로 파싱한다.
    
    :lines: row of csv file
    :select: list
    :types: list
    :has_headers: boolean
    :delimiter: str
    :silence_errors: boolean
    '''
    if select and not has_headers:
        raise RuntimeError('select requires column headers')

    rows = csv.reader(lines, delimiter=delimiter)

    headers = next(rows) if has_headers else []

    if select:
        indices = [ headers.index(colname) for colname in select ]
        headers = select

    records = []
    for row_no, row in enumerate(rows, 1):
        if not row:
            continue

        if select:
            row = [ row[index] for index in indices]

        if types:
            try:
                row = [func(val) for func, val in zip(types, row)]
            except ValueError as e:
                if not silence_errors:
                    print(f"Row {row_no}: Couldn't convert {row}")
                    print(f"Row {row_no}: Reason {e}")
                continue

        if headers:
            record = dict(zip(headers, row))
        else:
            record = tuple(row)
        records.append(record)

    return records