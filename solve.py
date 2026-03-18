import sys
import heapq

input = sys.stdin.readline

def take_last(x, m):
    return x & ((1 << (m + 1)) - 1)

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    sx = 0
    for v in a:
        sx ^= v

    if sx == 0:
        print(0)
        continue

    ans = float('inf')
    used = [False] * n
    can = []

    # First phase
    for mx in range(60, -1, -1):
        pq = []
        for i in range(n):
            if used[i]:
                continue
            if not ((a[i] >> mx) & 1):
                heapq.heappush(pq, (take_last(a[i], mx), i))
                if len(pq) > 2:
                    heapq.heappop(pq)
        while pq:
            _, ind = heapq.heappop(pq)
            used[ind] = True
            can.append(a[ind])

    a = can
    n = len(a)

    # Second phase
    for mx in range(60, -1, -1):
        cur_ans = 0
        suf = take_last(sx, mx)
        pre = suf ^ sx

        if pre > 0:
            break

        b = a[:]
        ok = False

        for bit in range(mx, -1, -1):
            if bit != mx and not ((suf >> bit) & 1):
                continue

            b.sort(key=lambda u: take_last(u, bit), reverse=True)

            for i in range(n):
                if not ((b[i] >> bit) & 1) and (not ok or ((suf >> bit) & 1)):
                    ok = True
                    to = (1 << bit)
                    cur_ans += to - take_last(b[i], bit)
                    suf ^= take_last(b[i], bit) ^ to
                    b[i] ^= take_last(b[i], bit) ^ to

        if ok and suf == 0:
            ans = min(ans, cur_ans)

    print(ans)