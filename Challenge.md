# Increase to Zero

**Problem Statement**

Given an array of **N** non-negative integers **A₁, A₂, ..., Aₙ**.  

In one operation, you can **increase** any one of the elements by **1**.  

Find the **minimum number of operations** needed to make the **XOR** of all elements equal to **0**.  
That is, make **A₁ ⊕ A₂ ⊕ ... ⊕ Aₙ = 0**, where ⊕ denotes the **bitwise XOR** operation.

It can be shown that it is **always possible**.

### Input Format

- The first line contains one integer **T** — the number of test cases.
- For each test case:
  - The first line contains one integer **N** — the size of the array.
  - The second line contains **N** integers **A₁, A₂, ..., Aₙ** — the elements of the array.

### Output Format

For each test case, print **one integer** — the minimum number of operations required to make the XOR of the array equal to **0**.

### Constraints

- **1 ≤ T ≤ 100**
- **2 ≤ N ≤ 10⁵** (for each test case)
- **∑ N ≤ 10⁵** (sum of N over all test cases)
- **0 ≤ Aᵢ < 2⁶⁰** (each element is a non-negative integer less than 2⁶⁰)

### Sample Input / Output

| Description | Content |
|-------------|---------|
| **Input**   | <pre><code>4<br>3<br>3 4 5<br>4<br>5 3 0 7<br>3<br>2 3 1<br>5<br>7 7 7 7 7</code></pre> |
| **Output**  | <pre><code>2<br>1<br>0<br>9</code></pre> |

### Explanation

**Test case 1:**  
Increase A₃ twice using two operations. Thus, the array becomes [3, 4, 7].  
The XOR of all elements of the array is 3 ⊕ 4 ⊕ 7 = 0.  
It can be shown that the XOR of all elements cannot be made equal to 0 using less than 2 operations.

**Test case 2:**  
Use one operation to increase A₃ by 1. Thus, the array becomes [5, 3, 1, 7].  
The XOR of all elements of the array is 5 ⊕ 3 ⊕ 1 ⊕ 7 = 0.  
It can be shown that the XOR of all elements cannot be made equal to 0 using less than 1 operation.

**Test case 3:**  
The XOR of all elements is already 0. Thus, we require 0 operations.

**Test case 4:**  
Array = [7, 7, 7, 7, 7]. Minimum operations required = 9.