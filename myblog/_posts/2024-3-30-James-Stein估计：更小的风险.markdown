---
layout: post
title: "James-Stein估计：更小的风险"
date: 2024-3-30
categories: Statistic Estimation James-Stein
---

# James-Stein估计：更小的风险

Title: James-Stein估计：更小的风险
Date: 2024-3-30
Keywords: Statistic, Estimation, James-Stein

---

本文对James Stein估计方法进行简要证明，推导过程的核心是选择合适的替身函数。替身函数的选择条件也值得记录下来，以备后用。

[toc]

---

## JS估计方法

有协方差矩阵为单位矩阵的$n$维多元正态分布，在观测到单一采样值$u$时，为了估计它的均值向量$\mu$，MLE方法给出的估计值是

$$
\hat{\mu} = u
$$

它的风险为

$$
n = E_\mu(\vert \mu - u \vert^2)
$$

而JS（James Stein）估计的策略是

$$
\hat{\mu}_{JS} = u - \frac{\alpha}{\vert u \vert^2}u
$$

其中，$\alpha \in N^+$，接下来要证明它有机会使风险更小，在理想情况下可以选择$\alpha=n-2$。

## JS估计对风险降低的证明

由JS估计得到的值构造随机变量

$$
V: v = u - \frac{\alpha}{\vert u\vert^2}u
$$

其风险为

$$
\mathcal{R} = E_{\mu}(\vert \mu - V \vert^2)
$$

展开得

$$
\mathcal{R} = E\begin{pmatrix}
\vert \mu - U \vert^2
\end{pmatrix}+
2\alpha E\begin{pmatrix}
\frac{(\mu - U)^TU}{\vert U \vert^2}
\end{pmatrix}+
\alpha^2E\begin{pmatrix}
\frac{1}{\vert U \vert^2}
\end{pmatrix}
$$

由引理1和引理2可知，选择$h$函数为

$$
\begin{cases}
h(x) = \frac{x_i}{\vert x\vert^2}\\
\frac{\partial h}{\partial x_i} = \frac{1}{\vert x \vert^2} - \frac{2 x_i^2}{\vert x \vert^4}
\end{cases}
$$

推知中间项为

$$
E_{\theta}\begin{bmatrix}
\frac{(\theta - X)^TX}{\vert X \vert^2}
\end{bmatrix} = \sum_{i=1}^{n}-E_{\theta}\begin{bmatrix}
\frac{\partial h(x)}{\partial x_i}
\end{bmatrix}
$$

解得

$$
E_{\theta}\begin{bmatrix}
\frac{(\theta - X)^TX}{\vert X \vert^2}
\end{bmatrix} = -\sum_{i=1}^{n}E_{\theta}\begin{bmatrix}
\frac{1}{\vert x \vert^2} - \frac{2 x_i^2}{\vert x \vert^4}
\end{bmatrix} = -(n-2) E_{\theta}\begin{bmatrix}\frac{1}{\vert x \vert^2}\end{bmatrix}
$$

代回风险式得

$$
\mathcal{R} = n - (2\alpha(n-2) - \alpha^2)E_{\mu}\begin{bmatrix}\frac{1}{\vert U \vert^2}\end{bmatrix}
$$

易见，$\alpha = n-2$时$\mathcal{R}$达到最小

$$
\mathcal{R} = n - (n-2)^2E_{\mu}\begin{bmatrix}\frac{1}{\vert U \vert^2}\end{bmatrix}
$$

### 引理1

下式随机变量的期望为

$$
E_{\theta}\begin{bmatrix}
\frac{(\theta - X)^TX}{\vert X \vert^2}
\end{bmatrix} =
\sum_{i=1}^{n}E_{\theta}\begin{bmatrix}(\theta_i - X_i)
\frac{X_i}{\vert X \vert^2}
\end{bmatrix}
$$

$\blacksquare$

### 引理2

考虑可积的多元函数作为替身函数

$$
h(X), X \in R^n
$$

即期望存在

$$
E_{\theta}\begin{bmatrix}
(\theta_i - X_i) \cdot h(X) \vert X_j = x_j (j \neq i)
\end{bmatrix}
$$

当概率密度函数为多元正态分布时，它的解析式为

$$
c\cdot\int(\theta_i-x_i)\cdot h(x)\cdot \exp\begin{pmatrix}-\frac{1}{2}(\theta-x)^T(\theta-x)\end{pmatrix}dx
$$

其中，多元正态分布的归一化系数为$c=(2 \pi)^{-n/2}$。经整理得

$$
c\cdot\int h(x)\cdot \exp\begin{pmatrix}-\frac{1}{2}(\theta-x)^T(\theta-x)\end{pmatrix} \frac{\partial}{\partial x_i}\begin{pmatrix}-\frac{1}{2}(\theta-x)^T(\theta-x)\end{pmatrix} dx_i
$$

继续整理得

$$
c\cdot\int h(x)\frac{\partial}{\partial x_i} \exp \begin{pmatrix}-\frac{1}{2}(\theta-x)^T(\theta-x)\end{pmatrix} dx_i
$$

继续分成两项之和

$$
c\cdot \begin{bmatrix} h(x) \cdot \exp \begin{pmatrix}-\frac{1}{2}(\theta-x)^T(\theta-x)\end{pmatrix} \end{bmatrix}_{x_i=-\infty}^{\infty}\\ - c \int \frac{\partial h(x)}{\partial x_i} \cdot \exp \begin{pmatrix}-\frac{1}{2}(\theta-x)^T(\theta-x)\end{pmatrix} dx_i
$$

通过合适的选择，可以使首项为$0$，即

$$
0 = \begin{bmatrix}
h(x) \cdot \exp \begin{pmatrix}-\frac{1}{2}(\theta-x)^T(\theta-x)\end{pmatrix}
\end{bmatrix}_{x_i=-\infty}^{\infty}
$$

此时有

$$
E_{\theta}\begin{bmatrix}
(\theta_i - X_i) \cdot h(X) \vert X_j = x_j (j \neq i)
\end{bmatrix} =
-E_{\theta}\begin{bmatrix}
\frac{\partial h(x)}{\partial x_i}
\end{bmatrix}
$$

$\blacksquare$

## 参考材料

[James–Stein estimator](https://en.wikipedia.org/wiki/James–Stein_estimator)

[Stein's example](https://en.wikipedia.org/wiki/Stein's_example)
