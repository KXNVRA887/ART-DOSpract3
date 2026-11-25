"""Три прогона: исходная версия, версия с дефектом, повторный.
Дефект вносится только во временную копию, service.py не изменяется."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GOOD = "if len(values) > capacity:"
BAD = "if len(values) >= capacity:"


def run(folder, output):
    result = subprocess.run([sys.executable, "-B", "check.py"], cwd=folder,
                            capture_output=True, text=True, encoding="utf-8")
    text = result.stdout + result.stderr
    (ROOT / output).write_text(text, encoding="utf-8")
    print(f"\n=== {output} (код завершения {result.returncode}) ===")
    print(text, end="")
    return result.returncode


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    source = (ROOT / "service.py").read_text(encoding="utf-8")
    if source.count(GOOD) != 1:
        sys.exit("В service.py нет исходного условия: восстановите его.")
    first = run(ROOT, "protocol.txt")
    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(ROOT / "check.py", tmp)
        Path(tmp, "service.py").write_text(source.replace(GOOD, BAD), encoding="utf-8")
        defect = run(tmp, "protocol_defect.txt")
    retest = run(ROOT, "protocol_retest.txt")
    ok = first == 0 and defect == 1 and retest == 0
    print("\nСценарий выполнен как ожидалось." if ok else "\nЕсть расхождения, проверьте протоколы.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
