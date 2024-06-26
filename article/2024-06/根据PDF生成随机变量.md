# 根据PDF生成随机变量

Title: 根据PDF生成随机变量

Date: 2024-6-24

Keywords: Math, Statistics

---

均匀分布的随机数是均匀分布的，这是因为在逆变换抽样法中，我们利用了均匀分布的性质来确保生成的样本正确地反映目标概率分布的特征。

---

[toc]

## 生成服从已知概率密度函数的随机变量

为了生成服从已知概率密度函数的随机变量 $X$，可以使用逆变换抽样法（Inverse Transform Sampling）。其原理步骤如下：

1. 确定概率密度函数 (PDF) 和累积分布函数 (CDF)：
   - 设已知的概率密度函数为 $f(x)$，其中 $x \in (0, 1)$。
   - 通过积分计算累积分布函数 (CDF) $F(x)$，即 $F(x) = \int_0^x f(t) \, dt$。
   - 假设 $f(x)$ 是已知的概率密度函数，首先需要计算它的累积分布函数 $F(x)$。

   $$ F(x) = \int_0^x f(t) \, dt $$

2. 求逆累积分布函数 (Inverse CDF)：
   - 确定 $F(x)$ 的逆函数 $F^{-1}(u)$，其中 $u \in (0, 1)$。

3. 生成服从给定分布的样本：
   - 生成 $n$ 个在区间 (0, 1) 上均匀分布的随机数 $U_i$，即 $U_i \sim \text{Uniform}(0, 1)$，$i = 1, 2, \ldots, n$。
   - 对每个 $U_i$，计算 $X_i = F^{-1}(U_i)$。
   - 生成 $n$ 个在 (0, 1) 上均匀分布的随机数 $U_i$。
   - 通过 $X_i = F^{-1}(U_i)$ 计算每个样本值。

## 小结

通过上述步骤，可以生成服从给定概率密度函数的随机变量采样值。这种方法的核心是利用累积分布函数及其逆函数进行抽样，确保生成的样本符合给定的分布。

## 附录：为什么服从均匀分布的 $U$ 是有效的

假设 $F(x)$ 是累积分布函数，则 $F(X)$ 是一个均匀分布的随机变量 $U$。

证明：设 $U = F(X)$，我们需要证明 $U \sim \text{Uniform}(0, 1)$。

1. CDF的性质：
   $$
   P(U \leq u) = P(F(X) \leq u) = P(X \leq F^{-1}(u)) = F(F^{-1}(u)) = u
   $$
   由于 $F$ 是单调递增且连续的，故 $F(F^{-1}(u)) = u$。

2. 均匀分布：
   $$
   P(U \leq u) = u
   $$
   这正是均匀分布的累积分布函数。

证明毕。$\blacksquare$

因此，利用均匀分布的随机数 $U$ 是有效的，因为它能通过逆变换生成服从目标分布的样本。它保证了如下两件事情：

1. 概率空间的一致性：
   - 使用均匀分布的 $U$ 能够确保每一个区间 \([a, b] \subset (0, 1)\) 内的数值出现的概率是相等的。
   - 这与逆变换抽样法的需求一致，即我们希望每一个 $u$ 对应的 $x = F^{-1}(u)$ 能够正确反映目标分布。

2. 生成样本的有效性：
   - 当 $U$ 均匀分布在 \((0, 1)\) 内时，$X = F^{-1}(U)$ 的分布将由 $F$ 确定，并且 $X$ 的概率密度函数 $f(x)$ 就是我们所希望的目标密度函数。
   - 逆变换 $F^{-1}$ 的作用是将均匀分布的 $U$ 映射到目标分布 $X$ 上，使得生成的样本满足目标概率分布。
