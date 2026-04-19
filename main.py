import sys
import time
import os
from concurrent.futures import ProcessPoolExecutor, as_completed


def collatz_steps(n: int) -> int:
    steps = 0
    while n != 1:
        if n & 1:
            n = 3 * n + 1
        else:
            n >>= 1
        steps += 1
    return steps



def process_chunk(lo: int, hi: int):
    result = []
    local_max = 0
    local_max_idx = lo
    for idx in range(lo, hi):
        s = collatz_steps(idx + 1)
        result.append(s)
        if s > local_max:
            local_max = s
            local_max_idx = idx
    return lo, result, local_max, local_max_idx


def main():
    N = 10_000_000

    hw_cpus = os.cpu_count() or 4
    num_workers = hw_cpus

    if len(sys.argv) >= 2:
        try:
            arg = int(sys.argv[1])
            if arg > 0:
                num_workers = arg
            else:
                print(f"Неприпустима к-сть процесів. Використовується: {num_workers}",
                      file=sys.stderr)
        except ValueError:
            print(f"Неприпустимий аргумент. Використовується: {num_workers}",
                  file=sys.stderr)

    if len(sys.argv) >= 3:
        try:
            arg_n = int(sys.argv[2])
            if arg_n > 0:
                N = arg_n
            else:
                print(f"Неприпустиме N. Використовується: {N}", file=sys.stderr)
        except ValueError:
            print(f"Неприпустиме N. Використовується: {N}", file=sys.stderr)


    print("  Гіпотеза Колатца — паралельні обчислення (Python)")
    print(f"  Числа         : 1 .. {N:,}")
    print(f"  Воркерів      : {num_workers}  (ProcessPoolExecutor)")
    print(f"  Апаратних ядер: {hw_cpus}")

    steps = [0] * N

    chunk = max(1_000, N // 1_000)
    chunks = [(lo, min(lo + chunk, N)) for lo in range(0, N, chunk)]
    num_chunks = len(chunks)

    t_start = time.perf_counter()

    with ProcessPoolExecutor(max_workers=num_workers) as pool:
        futures = {
            pool.submit(process_chunk, lo, hi): lo
            for lo, hi in chunks
        }

        completed = 0
        for future in as_completed(futures):
            lo, result, _, _ = future.result()
            steps[lo:lo + len(result)] = result
            completed += 1
            if completed % max(1, num_chunks // 10) == 0:
                pct = completed / num_chunks * 100
                print(f"  Прогрес: {pct:5.1f}%  ({completed}/{num_chunks} блоків)", flush=True)

    t_end = time.perf_counter()

    total_steps = sum(steps)
    avg_steps   = total_steps / N
    max_steps   = max(steps)
    max_num     = steps.index(max_steps) + 1
    elapsed_ms  = (t_end - t_start) * 1000

    print("  Результати")
    print(f"  Оброблено чисел      : {N:,}")
    print(f"  Задач у пулі         : {num_chunks}  (блок ~{chunk:,} чисел)")
    print(f"  Середня к-сть кроків : {avg_steps:.3f}")
    print(f"  Максимум кроків      : {max_steps}  (число {max_num:,})")
    print(f"  Час обчислень : {elapsed_ms:.2f} мс")


if __name__ == "__main__":
    main()