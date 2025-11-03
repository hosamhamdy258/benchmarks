import time
import statistics
import sys


get_size = sys.getsizeof
size_note = " (shallow)"

def benchmark(max_power=7, test_times=3):
    results = []

    for power in range(1, max_power + 1):
        n = 10 ** power
        data = list(range(n))
        target = n // 2  # middle element
        non_target = n + 1  # not in list

        # Direct list membership check
        list_times = []
        for _ in range(test_times):
            t0 = time.perf_counter()
            _ = target in data
            _ = non_target in data
            list_times.append(time.perf_counter() - t0)
        list_time = statistics.mean(list_times)

        # List creation + membership check
        list_create_times = []
        for _ in range(test_times):
            t0 = time.perf_counter()
            lst = list(range(n))
            _ = target in lst
            _ = non_target in lst
            list_create_times.append(time.perf_counter() - t0)
        list_create_time = statistics.mean(list_create_times)

        # Set membership check (set pre-created)
        s = set(data)
        set_check_times = []
        for _ in range(test_times):
            t0 = time.perf_counter()
            _ = target in s
            _ = non_target in s
            set_check_times.append(time.perf_counter() - t0)
        set_check_time = statistics.mean(set_check_times)

        # Set creation + membership check
        set_create_times = []
        for _ in range(test_times):
            t0 = time.perf_counter()
            s2 = set(data)
            _ = target in s2
            _ = non_target in s2
            set_create_times.append(time.perf_counter() - t0)
        total_set_time = statistics.mean(set_create_times)
        
        # Frozenset membership check
        fs = frozenset(data)
        fset_check_times = []
        for _ in range(test_times):
            t0 = time.perf_counter()
            _ = target in fs
            _ = non_target in fs
            fset_check_times.append(time.perf_counter() - t0)
        fset_check_time = statistics.mean(fset_check_times)

        # Frozenset creation + membership check
        fset_create_times = []
        for _ in range(test_times):
            t0 = time.perf_counter()
            s2 = frozenset(data)
            _ = target in s2
            _ = non_target in s2
            fset_create_times.append(time.perf_counter() - t0)
        total_fset_time = statistics.mean(fset_create_times)

        # Memory sizes
        mem_list = get_size(data)
        mem_set = get_size(s)
        mem_fset = get_size(fs)

        # store stats
        results.append((n, list_time, list_create_time, set_check_time, total_set_time,
                        fset_check_time, total_fset_time, mem_list, mem_set, mem_fset))

    # Pretty print
    print(f"{'N':>10} | {'List (s)':>10} | {'List+Create (s)':>15} | {'Set only (s)':>12} | {'Set+Create (s)':>15} | {'Frozenset only (s)':>15} | {'Frozenset+Create (s)':>18} | {'List (MB)':>10} | {'Set (MB)':>10} | {'Fset (MB)':>10}")
    print("-" * 150)
    for n, list_time, list_create_time, set_check_time, total_set_time, fset_check_time, total_fset_time, mem_list, mem_set, mem_fset in results:
        print(f"{n:10d} | {list_time:10.9f} | {list_create_time:15.9f} | {set_check_time:12.9f} | {total_set_time:15.9f} | {fset_check_time:15.9f} | {total_fset_time:18.9f} | {mem_list/1e6:10.3f} | {mem_set/1e6:10.3f} | {mem_fset/1e6:10.3f}")

    print(f"\nNote: memory sizes measured using getsizeof{size_note}")

if __name__ == "__main__":
    benchmark(8)


# Example of results if you can't run it locally if script is killed change benchmark parameter to smaller number
"""
             N |   List (s) | List+Create (s) | Set only (s) |  Set+Create (s) | Frozenset only (s) | Frozenset+Create (s) |  List (MB) |   Set (MB) |  Fset (MB)
------------------------------------------------------------------------------------------------------------------------------------------------------
        10 | 0.000000383 |     0.000000737 |  0.000000210 |     0.000000583 |     0.000000147 |        0.000000440 |      0.000 |      0.001 |      0.001
       100 | 0.000001050 |     0.000001657 |  0.000000107 |     0.000003160 |     0.000000093 |        0.000002593 |      0.001 |      0.008 |      0.008
      1000 | 0.000009270 |     0.000028114 |  0.000000143 |     0.000019544 |     0.000000107 |        0.000014840 |      0.008 |      0.033 |      0.033
     10000 | 0.000092535 |     0.000309374 |  0.000000137 |     0.000341654 |     0.000000130 |        0.000174692 |      0.080 |      0.525 |      0.525
    100000 | 0.000959446 |     0.003376484 |  0.000000340 |     0.003459281 |     0.000000183 |        0.001957022 |      0.800 |      4.195 |      4.195
   1000000 | 0.009256057 |     0.038151841 |  0.000000580 |     0.034823984 |     0.000000577 |        0.033766844 |      8.000 |     33.555 |     33.555
  10000000 | 0.095921202 |     0.405553808 |  0.000000723 |     0.368235128 |     0.000000663 |        0.389376908 |     80.000 |    268.436 |    268.436
 100000000 | 0.926654788 |     3.877026882 |  0.000000793 |     5.393334521 |     0.000000773 |        5.586292617 |    800.000 |   4294.968 |   4294.968
"""
