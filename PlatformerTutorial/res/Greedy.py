import sys
from typing import List
import random

INF = int(1e9 + 7)
MAX_N = 1000 + 1
MAX_K = 100

class Truck:
    def __init__(self):
        self.route = [0]
        self.distance = 0

# Khởi tạo ma trận thời gian và các biến
distance_matrix = [[0] * MAX_N for _ in range(MAX_N)]
N = 0
K = 0
visited = [False] * MAX_N
trucks = [Truck() for _ in range(MAX_K)]

# Hàm nhập dữ liệu
def import_data():
    global N, K
    N, K = map(int, input().split())
    visited[0] = True
    for i in range(1, N + 1):
        visited[i] = False

    for i in range(N + 1):
        distance_matrix[i] = list(map(int, input().split()))

# Tính thời gian chạy cho một lộ trình
def calc_distance(route: List[int]) -> int:
    _distance = 0
    for i in range(1, len(route)):
        _distance += distance_matrix[route[i - 1]][route[i]]
    return _distance

# Giải bài toán
def solve():
    nodes = [i for i in range (N + 1)]
    random.shuffle(nodes)
    for i in range(1, N + 1):
        best_pos = -1
        best_distance = INF
        best_node = -1

        for node in nodes:
            if visited[node]:
                continue

            for pos in range(K):
                _distance = trucks[pos].distance + distance_matrix[trucks[pos].route[-1]][node]
                if _distance < best_distance:
                    best_pos = pos
                    best_distance = _distance
                    best_node = node

        trucks[best_pos].route.append(best_node)
        trucks[best_pos].distance = best_distance
        visited[best_node] = True


# In kết quả
def print_sol():
    print(K)
    for pos in range(K):
        print(len(trucks[pos].route))
        print(" ".join(map(str, trucks[pos].route)))
    lst = []
    for i in range(K):
        lst.append(1-K)
        lst.extend(trucks[i].route)
        print(trucks[i].route)
    print(lst)

if __name__ == "__main__":
    import_data()
    solve()
    print_sol()