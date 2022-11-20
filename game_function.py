
def get_record() -> int:
    try:
        with open('record') as f:
            return int(f.readline())
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')
        return 0


def set_record(record: int, score: int):
    rec = max(record, score)
    with open('record', 'w') as f:
        f.write(str(rec))
