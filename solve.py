import sys

input = sys.stdin.readline
T = int(input())

for _ in range(T):
    N = int(input())
    A = tuple(map(int, input().split())) 

    # Compute total XOR
    X = 0
    for a in A:
        X ^= a

    if X == 0:
        print(0)
        continue

    # Case 1: Change ONE element (optimal when possible)
    min_ops = float('inf')
    for a in A:
        and_val = a & X
        cost = X - 2 * and_val          # = (X ^ a) - a
        if cost >= 0:
            min_ops = min(min_ops, cost)

    if min_ops != float('inf'):
        print(min_ops)
        continue

    # Case 2: No single change works (all elements have the MSB of X set)
    # → Carry one element over the MSB and adjust another
    k = X.bit_length() - 1
    p = 1 << (k + 1)                    # next power of 2
    max_a = max(A)
    carry_cost = p - max_a

    X_prime = X ^ max_a ^ p
    min_adjust = float('inf')
    for a in A:
        and_val = a & X_prime
        cost = X_prime - 2 * and_val
        if cost >= 0:
            min_adjust = min(min_adjust, cost)

    print(carry_cost + min_adjust)