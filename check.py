import sys

from service import check

sys.stdout.reconfigure(encoding="utf-8")

N = 10 + 2
K = 8 + N % 5
results = []


def report(case, expected, action):
    """action - функция без аргументов, чтобы исключение не прервало прогон."""
    try:
        actual = action()
    except Exception as error:
        actual = f"EXCEPTION:{type(error).__name__}"
    status = "PASS" if actual == expected else "FAIL"
    results.append(status)
    print(case, expected, actual, status, sep=" | ")


print(f"# Python {sys.version.split()[0]}; N={N}; K={K}")

cases = [([0, 60], "OK"), ([30] * K, "OK"), (None, "TYPE"),
         ([], "EMPTY"), ([30, True], "BAD_ITEM"), ([61], "BAD_ITEM"),
         ([-1], "BAD_ITEM"), ([None] * (K + 1), "OVERLOAD")]
for i, (values, expected) in enumerate(cases, 1):
    report(f"Б-{i:02}", expected, lambda: check(values, K))

report("Б-09", ("OVERLOAD", "OK"),
       lambda: (check([30] * (1000 * K), K), check([30], K)))

report("Б-10", ("OVERLOAD", "OK"),
       lambda: (check([30] * (1000 * K), K), check([30] * K, K)))

passed = results.count("PASS")
failed = results.count("FAIL")
planned = 10
print(f"# ИТОГО: запланировано={planned}; PASS={passed}; FAIL={failed}; "
      f"не выполнено={planned - len(results)}")
sys.exit(1 if failed or len(results) != planned else 0)
