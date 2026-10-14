# Sort out my CP toolbox -- DO NOT INVENT WHEEL TWICE!!
####################### Industry-Standard Python CP Boilerplate #######################
import sys
import os
import math
import bisect
from sys import stdin, stdout
from math import gcd, floor, ceil, sqrt, log
from collections import defaultdict as dd
from bisect import bisect_left as bl, bisect_right as br
from io import BytesIO, IOBase

# 1. SYSTEM CONFIGURATION - Beyond 10^6, you risk C-stack overflow (SegFault).
sys.setrecursionlimit(1000000)

MOD = 1000000007

# 2. FAST I/O SETUP - Bypasses slow native input functions. Essential for >10^5 I/O operations.
BUFSIZE = 8192
class FastIO(IOBase):
    newlines = 0
    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while self.buffer.getbuffer().nbytes:
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2)
            self.buffer.write(os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE)))
            self.buffer.seek(ptr)
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2)
            self.buffer.write(b)
            self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

# Replace standard streams
sys.stdin, sys.stdout = FastIO(sys.stdin), FastIO(sys.stdout)

# Decode to string immediately to prevent bytes/str type mismatches in CP logic
input = lambda: sys.stdin.readline().decode("utf-8").rstrip("\r\n")

####### 3. OPTIMIZED SHORTHANDS #######
def inp(): return int(input())
def inp_str(): return input().strip()
def inp_list(): return list(map(int, input().split()))
def inp_map(): return map(int, input().split())
def inp_float_list(): return list(map(float, input().split()))
def str_list(): return list(input().strip())
def join_str(x, l): return x.join(map(str, l))

# Math shorthands (Algebraically optimal ceiling division)
ceildiv = lambda x, d: (x + d - 1) // d

# I/O shorthands
flush = stdout.flush
stdpr = lambda x: stdout.write(str(x) + "\n")

####### 4. CORE LOGIC WRAPPER #######
def solve():   # Write your solution here.

    pass

if __name__ == "__main__":  # Handles multiple test cases smoothly
    t = 1   # t = inp() # Uncomment if the problem provides multiple test cases
    for _ in range(t):
        solve()
        
    flush()


####################### LA func in CP #######################
# Dot product
def dot(a, b):
    return sum(x * y for x, y in zip(a, b))
# -------------------------------------------------
# Matrix × Vector
def matvec(A, x):
    return [sum(a * b for a, b in zip(row, x)) for row in A]
# -------------------------------------------------
# Matrix × Matrix
def matmul(A, B):
    n, m = len(A), len(B)
    p = len(B[0])
    C = [[0] * p for _ in range(n)]
    for i in range(n):
        for k in range(m):
            aik = A[i][k]
            if aik == 0:
                continue
            for j in range(p):
                C[i][j] += aik * B[k][j]
    return C
# -------------------------------------------------
# Matrix × Matrix (mod MOD)
def matmul_mod(A, B, MOD):
    n, m = len(A), len(B)
    p = len(B[0])
    C = [[0] * p for _ in range(n)]
    for i in range(n):
        for k in range(m):
            aik = A[i][k]
            if aik == 0:
                continue
            for j in range(p):
                C[i][j] = (C[i][j] + aik * B[k][j]) % MOD
    return C
# -------------------------------------------------
# Identity Matrix
def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]
# -------------------------------------------------
# Matrix Exponentiation
def matpow(A, e):
    R = identity(len(A))
    while e:
        if e & 1:
            R = matmul(R, A)
        A = matmul(A, A)
        e >>= 1
    return R
# -------------------------------------------------
# Matrix Exponentiation (mod MOD)
def matpow_mod(A, e, MOD):
    R = identity(len(A))
    while e:
        if e & 1:
            R = matmul_mod(R, A, MOD)
        A = matmul_mod(A, A, MOD)
        e >>= 1
    return R
# -------------------------------------------------
# Matrix Transpose
def transpose(A):
    return [list(row) for row in zip(*A)]
# -------------------------------------------------
# Gaussian Elimination (floating point) - 1) Returns rank; 2) Matrix is modified in-place.
def gauss(A, eps=1e-12):
    A = [row[:] for row in A]
    n = len(A)
    m = len(A[0])
    r = 0

    for c in range(m):
        pivot = max(range(r, n), key=lambda i: abs(A[i][c]))
        if abs(A[pivot][c]) < eps:
            continue

        A[r], A[pivot] = A[pivot], A[r]

        piv = A[r][c]
        for j in range(c, m):
            A[r][j] /= piv

        for i in range(n):
            if i != r:
                factor = A[i][c]
                if abs(factor) > eps:
                    for j in range(c, m):
                        A[i][j] -= factor * A[r][j]
        r += 1

    return r
# -------------------------------------------------
# Gaussian Elimination (mod prime) - Returns rank
def gauss_mod(A, MOD):
    A = [row[:] for row in A]
    n = len(A)
    m = len(A[0])
    r = 0

    for c in range(m):
        pivot = None
        for i in range(r, n):
            if A[i][c] % MOD:
                pivot = i
                break
        if pivot is None:
            continue

        A[r], A[pivot] = A[pivot], A[r]

        inv = pow(A[r][c], MOD - 2, MOD)
        for j in range(c, m):
            A[r][j] = A[r][j] * inv % MOD

        for i in range(n):
            if i != r and A[i][c]:
                factor = A[i][c]
                for j in range(c, m):
                    A[i][j] = (A[i][j] - factor * A[r][j]) % MOD

        r += 1

    return r
# -------------------------------------------------
# Determinant (mod prime) - O(n^3)
def det_mod(A, MOD):
    A = [row[:] for row in A]
    n = len(A)
    det = 1

    for i in range(n):
        pivot = None
        for j in range(i, n):
            if A[j][i]:
                pivot = j
                break
        if pivot is None:
            return 0

        if pivot != i:
            A[i], A[pivot] = A[pivot], A[i]
            det = -det

        det = det * A[i][i] % MOD
        inv = pow(A[i][i], MOD - 2, MOD)

        for j in range(i + 1, n):
            factor = A[j][i] * inv % MOD
            for k in range(i, n):
                A[j][k] = (A[j][k] - factor * A[i][k]) % MOD

    return det % MOD
# -------------------------------------------------
# Solve Ax=b (floating point) - Returns solution vector or None
# -------------------------------------------------
def solve(A, b):
    n = len(A)
    M = [A[i][:] + [b[i]] for i in range(n)]

    if gauss(M) < n:
        return None

    return [M[i][-1] for i in range(n)]
# -------------------------------------------------
# Bitset Gaussian Elimination over GF(2) - 1) rows are integers; 2) Returns rank
def gauss_xor(rows):
    rows = rows[:]
    rank = 0

    while rows:
        pivot = max(rows)
        if pivot == 0:
            break
        rows.remove(pivot)
        bit = pivot.bit_length() - 1
        for i in range(len(rows)):
            if (rows[i] >> bit) & 1:
                rows[i] ^= pivot
        rank += 1

    return rank