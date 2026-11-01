-- Seed data for Coderunner
-- Contains preloaded users and code snippets

-- Preloaded users (Passwords stored as unsalted MD5)
-- admin: !Admin_Super_Sec2026!#$ (b81c35e0cb8bdf19c669e5ecc2adbbe7)
-- martin: starwars (5badcaf789d3d1d09794d8f021f40f0e) -> target credential for lateral movement
-- clara: c1@r4_k3y_unbr34k4bl3_x99 (f96d2ec4a85175c0bec2afbf4dd00f52)

INSERT INTO users (id, username, password_hash, email, role) VALUES
(1, 'admin', 'b81c35e0cb8bdf19c669e5ecc2adbbe7', 'admin@coderunner.local', 'admin'),
(2, 'martin', '5badcaf789d3d1d09794d8f021f40f0e', 'martin@coderunner.local', 'developer'),
(3, 'clara', 'f96d2ec4a85175c0bec2afbf4dd00f52', 'clara@coderunner.local', 'developer');

-- Preloaded snippets
INSERT INTO snippets (id, title, code, author_id) VALUES
(1, 'Healthcheck', 'import sys' || char(10) || 'print(f"System running Python {sys.version.split()[0]}")', 1),
(2, 'Fibonacci Memoized', 'def fib(n, memo={}):' || char(10) || '    if n in memo: return memo[n]' || char(10) || '    if n <= 1: return n' || char(10) || '    memo[n] = fib(n-1, memo) + fib(n-2, memo)' || char(10) || '    return memo[n]' || char(10) || '' || char(10) || 'print([fib(i) for i in range(10)])', 2),
(3, 'Quick Sort', 'def quicksort(arr):' || char(10) || '    if len(arr) <= 1: return arr' || char(10) || '    pivot = arr[len(arr) // 2]' || char(10) || '    left = [x for x in arr if x < pivot]' || char(10) || '    middle = [x for x in arr if x == pivot]' || char(10) || '    right = [x for x in arr if x > pivot]' || char(10) || '    return quicksort(left) + middle + quicksort(right)' || char(10) || '' || char(10) || 'print(quicksort([3, 6, 8, 10, 1, 2, 1]))', 3);
