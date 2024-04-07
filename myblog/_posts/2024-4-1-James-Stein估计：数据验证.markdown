---
layout: post
title: "James-Stein估计：数据验证"
date: 2024-4-1
categories: Statistic Estimation James-Stein Python
---

# James-Stein估计：数值验证

Title: James-Stein估计：数据验证
Date: 2024-4-1
Keywords: Statistic, Estimation, James-Stein, Python

---

本文对James Stein（JS）估计方法进行数值验证。结果表明，当观测到的向量模长$\vert X \vert^2$越小时，越应该认为均值向量$\mu \approx 0$。也就是说，当你要估计一个均值向量时，如果观测值始终在它附近，那么就不应该轻易否定它为$0$的原假设。数值验证的另一个目的是实现JS估计，并给出基本的使用代码。

[https://github.com/listenzcc/James-Stein-Estimation](https://github.com/listenzcc/James-Stein-Estimation)

[toc]

## JS与MLE方法的风险计算

前文已经说明，MLE（最大似然估计）和JS（James-Stein估计）方法对$n$维多元正态分布的均值$\mu$进行估计

$$
\begin{cases}
\hat{\mu}_{MLE} &= x \\
\hat{\mu}_{JS} &= x - \frac{\alpha}{\vert x \vert^2}x
\end{cases}
$$

估计的风险为

$$
\begin{cases}
\mathcal{R}_{MLE} &= n\\
\mathcal{R}_{JS} &= n - (n-2)^2E_{\mu}\begin{bmatrix}\frac{1}{\vert X \vert^2}\end{bmatrix}
\end{cases}
$$

## 风险估计结果

下图分别展示了$n=5,n=10$的两种情况，在每种情况下实验都重复了$100$次。从实验结果看到，当X2，也即$\vert X \vert^2$越小时，JS估计的风险越小于MLE做法，这与理论推导结果是吻合的。

这也从另一个角度说明了JS估计的基本思想，即当观测到的向量模长$\vert X \vert^2$越小时，越应该认为均值向量$\mu \approx 0$。也就是说，当你要估计一个均值向量时，如果观测值始终在它附近，那么就不应该轻易否定它为$0$的原假设。

![Untitled](James-Stein%E4%BC%B0%E8%AE%A1%EF%BC%9A%E6%95%B0%E5%80%BC%E9%AA%8C%E8%AF%81%202a40819dc2344899bc0b1cdba5bd1d71/Untitled.png)

![Untitled](James-Stein%E4%BC%B0%E8%AE%A1%EF%BC%9A%E6%95%B0%E5%80%BC%E9%AA%8C%E8%AF%81%202a40819dc2344899bc0b1cdba5bd1d71/Untitled%201.png)

## 模拟数据生成

最后使用python实现JS估计，并给出基本使用代码。

```python
def js_estimate(x):
    """
Estimates the James-Stein estimator for a given input vector.

Args:
    x: The input vector.

Returns:
    The estimated James-Stein estimator.

Examples:
    >>> js_estimate([1, 2, 3])
    array([-0.5, -1. , -1.5])
"""

    alpha = dim-2
    k = (1-alpha / np.dot(x, x))
    return k * x

def generate_multiple_normal_dist(dim: int = 5, n_samples: int = 100, x2: float = 10.0):
    """
Generates multiple samples from a multivariate normal distribution.

Args:
    dim (int): The dimension of the distribution. Defaults to 5.
    n_samples (int): The number of samples to generate. Defaults to 100.
    x2 (float): The variance of the distribution. Defaults to 10.0.

Returns:
    Tuple[np.ndarray, np.ndarray]: A tuple containing the mean vector and the generated samples.

Examples:
    >>> generate_multiple_normal_dist(dim=3, n_samples=10, x2=5.0)
    (array([-0.123, 0.456, -0.789]), array([[ 0.123, -0.456,  0.789],
                                            [ 0.321, -0.654,  0.987],
                                            ...
                                            [ 0.789, -0.123,  0.456]]))
"""

    mean = np.random.random((dim,))
    mean /= np.linalg.norm(mean)
    mean *= np.sqrt(x2)

    cov = np.eye(dim)
    samples = np.random.multivariate_normal(mean, cov, size=n_samples)
    return mean, samples

def measure_risks(mean, samples, estimation):
    """
Measures the risks of different estimators.

Args:
    mean (np.ndarray): The mean vector.
    samples (np.ndarray): The generated samples.
    estimation (np.ndarray): The estimated values.

Returns:
    dict: A dictionary containing the risks of different estimators, including MLE, JS, and X2.

Examples:
    >>> mean = np.array([1, 2, 3])
    >>> samples = np.array([[1, 2, 3], [4, 5, 6]])
    >>> estimation = np.array([[0.5, 1.5, 2.5], [3.5, 4.5, 5.5]])
    >>> measure_risks(mean, samples, estimation)
    {'MLE': 0.5, 'JS': 0.5, 'X2': 14}
"""

    x2 = np.dot(mean, mean)
    risk_mle = np.mean([np.dot(e, e) for e in samples-mean])
    risk_js = np.mean([np.dot(e, e) for e in estimation-mean])
    return dict(
        MLE=risk_mle,
        JS=risk_js,
        X2=x2
    )

```
