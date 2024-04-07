---
layout: post
title: "James-Stein估计：MLE及其风险"
date: 2024-03-28
categories: Statistic Estimation James-Stein
---

# James-Stein估计：MLE及其风险

Title: James-Stein估计：MLE及其风险
Date: 2024-03-28
Keywords: Statistic, Estimation, James-Stein

---

如果只观测到一组数据，如何估计多元正态分布的均值向量？最大似然估计是经典的方法，但它的风险与数据维度呈线性关系，这让人不是很满意。

[toc]

---

## 问题描述

多元正态分布的符号表示如下

$$
\mathcal{N}(\mu, \Sigma)
$$

其中，均值为向量$\mu \in R^n$，方差为方阵$\Sigma\in R^{n\times n}$。其概率密度函数满足

$$
p(X)\propto \exp\begin{pmatrix}-\frac{1}{2}(\mu-X)^T\Sigma^{-1}(\mu-X)\end{pmatrix}
$$

其中，为了满足概率密度函数的归一化特性，它的归一化系数为

$$
f(\mu, \Sigma)=(2\pi)^{-n/2} \det(\Sigma)^{-1/2}
$$

满足

$$
\int f \cdot p(x) dx = 1
$$

当多元正态分布的变量相互独立时，即$\Sigma = I$时，如何通过单个观测值$u\in R^n$对均值向量进行估计，实现这个过程的方法既可以是让分布与真实情况更接近（max likelyhood），又可以是让估计的风险更小（min risk）

$$
\hat{\mu} = \arg \max_\mu likely\begin{pmatrix}
\mathcal{N}(\mu, I), u
\end{pmatrix}
$$

$$
\hat{\mu} = \arg \min_\mu risk\begin{pmatrix}
\mathcal{N}(\mu, I), u
\end{pmatrix}
$$

## 最大似然估计（MLE）

最大似然估计（maximum likelihood estimation, MLE）的思路是寻找合适的$\hat{\mu}$，使观测值$u$出现的概率最大

$$
\hat{\mu} = \arg \max_{\mu} \log p(u)
$$

其中，$\log p(u)$为对数似然函数。由二次项的性质可知

$$
\hat{\mu}_{MLP} = u
$$

## MLE的风险

但世界充满了不确定性，任何估计都有风险。所谓风险是指估计值与实际值之间的差异大小，这里用估计值与真实值差异的二范数的期望表示

$$
\vert \mu - \hat{\mu} \vert^2
$$

此时，问题转化成了$u$确定时$\mu - \hat{\mu}$的期望。此时，MLE的风险可以表示为
$$
E_\mu(\vert \mu - u \vert^2)
$$

由于多元正态分布的变量相互独立，因此上式恒等于$n$，即

$$
n = (2\pi)^{-n/2} \cdot \int (\mu-x)^T(\mu-x) \cdot \exp\begin{pmatrix}-\frac{1}{2}(\mu-x)^T(\mu-x)\end{pmatrix} dx
$$

这就是说MLE的风险随着数据维度的增加而增加。
