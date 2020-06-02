import random
import time

import sys
sys.setrecursionlimit(1000000)


def generate(N, repeat_ratio):
    repeat_time = int(N * repeat_ratio) - 1 if repeat_ratio > 0 else 0
    num_range = N - repeat_time
    print(repeat_time, num_range, repeat_ratio)
    arr = list(range(num_range))
    x = random.choice(arr)
    all_num = arr + [x] * repeat_time
    random.shuffle(all_num)
    random.shuffle(all_num)
    return all_num
    

# def swap(arr, i, j):
#     tmp = arr[j]
#     arr[j] = arr[i]
#     arr[i] = tmp

def random_partition(arr, left, right):
    pid = random.randint(left, right)
    # swap(arr, pid, right)
    arr[pid], arr[right] = arr[right], arr[pid]
    x = arr[right]
    i = left - 1 #小于等于i的index都<= x, i+1 - j-1之间是> x, j是当前考虑的数
    for j in range(left, right):
        if arr[j] <= x: #符合要求，把j与i+1互换; i++, j++, 否则j++
            i += 1
            # swap(arr, j, i)
            arr[j], arr[i] = arr[i], arr[j]
    #最后把x从最后换到中间位置(i+1)
    # swap(arr, right, i + 1)
    arr[right], arr[i + 1] = arr[i + 1], arr[right]
    return i + 1

def random_quicksort(arr, left, right):
    # print(left, right)
    if left < right:
        k = random_partition(arr, left, right)
        random_quicksort(arr, left, k - 1)
        random_quicksort(arr, k + 1, right)

#维护3段，但是多了swap的开销
def improved_partition(arr, left, right):
    # print(left, right)
    pid = random.randint(left, right)
    # swap(arr, pid, right)
    arr[pid], arr[right] = arr[right], arr[pid]
    x = arr[right]
    i = left - 1 #小于等于i的index都< x, i+1-k之间等于x, k+1 - j-1之间是> x, j是当前考虑的数
    k = i
    # print(arr)
    for j in range(left, right):
        if arr[j] < x:
            i += 1
            # swap(arr, j, i)
            arr[j], arr[i] = arr[i], arr[j]
            k += 1
            if (i < k): #如果有相等的元素
                # swap(arr, j, k)
                arr[j], arr[k] = arr[k], arr[j]
        elif arr[j] == x:
            k += 1
            # swap(arr, j, k)
            arr[j], arr[k] = arr[k], arr[j]
    #最后把x从最后换到中间位置(k+1)
    # swap(arr, right, k + 1)
    arr[right], arr[k + 1] = arr[k + 1], arr[right]
    if i + 1 <= k:
        return i + 1, k
    # print(arr)
    return i + 1, i + 1


def improved_quicksort(arr, left, right):
    if (left < right):
        p1, p2 = improved_partition(arr, left, right)
        # print(p1, p2, left, right)
        improved_quicksort(arr, left, p1 - 1)
        improved_quicksort(arr, p2 + 1, right)
    return

def improved_quicksort2(arr, left, right):
    while (left < right):
        # p1, p2 = improved_partition(arr, left, right)
        p1 = random_partition(arr, left, right)
        p2 = p1
        if (p1 - left <= right - p2):
            improved_quicksort2(arr, left, p1 - 1)
            left = p2 + 1
        else:
            improved_quicksort2(arr, p2 + 1, right)
            right = p1 - 1
        
    return

def check_sort(arr):
    for i in range(1, len(arr)):
        if arr[i-1] <= arr[i]:
            continue
        else:
            return False
    return True



def write_files():
    N = 1000000
    for repeat_ratio in range(0, 11):
        repeat_ratio = repeat_ratio / 10
        arr = generate(N, repeat_ratio)
        with open("input-{}.txt".format(int(repeat_ratio * 10)), "w") as txt_file:
            txt_file.write(" ".join([str(i) for i in arr]) + "\n")

def load_run(ratio):
    print("="* 10 + str(ratio) + "="*10)
    # with open("F:\\algorithm-experiments\\Quicksort\\input-{}.txt".format(ratio), mode="r", encoding="utf-8") as fp:
    #     arr = fp.read().split()
    #     x = [int(i) for i in arr]
    # N = len(x)
    N = 2000
    x = generate(N, ratio / 10)
    for algo in [random_quicksort, improved_quicksort]:
        arr_tmp = x.copy()
        if algo == "sort":
            t1 = time.time()
            arr_tmp.sort()
            t2 = time.time()
        else:
            t1 = time.time()
            algo(arr_tmp, 0, N - 1)
            t2 = time.time()
        print(t2 - t1)
        # print(check_sort(arr_tmp))

for j in range(11):
    load_run(j)