# 路不都是平的，轮不都是圆的

Title: 路不都是平的，轮不都是圆的
Date: 2024-6-1
Keywords: Game

---

这是一个数学游戏，它展示了轮子并非必须是圆的，只要路修得合适，任意凸图形（convex shapes）都可以是轮子的形状。古人云削足适履，也许不完全是个笑话。本文的计算和交互代码可见我的Observablehq笔记本，欢迎点赞和转发。

[Convex shapes have their roads](https://observablehq.com/@listenzcc/convex-shapes-have-their-roads)

---

[toc]

## 轮子和道路

轮子在路上滚动是常见的物理现象，我给它一个更准确的定义，考虑一个平面图形，其内部的点构成集合$S$；再考虑一条曲线，曲线上的点构成集成$R$。将平面图形视为轮子的剖面，将曲线视为路的剖面，则轮子在路上滚动的现象可以表示成

- 命题1：在任意时刻有且仅有一点$p$，满足$p \in S \cap R$
- 命题2：考虑两个相邻的时刻，$\forall \epsilon>0, \exist \delta \quad s.t. \quad \vert t_1 -t_2 \vert < \delta \rightarrow \vert p_{t_1} - p_{t_2} \vert < \epsilon$

其中，命题1保证了轮子与路面始终有且仅有一个接触点，命题2保证了轮子与路面之间是滚动而不是其他什么奇奇怪怪的运动。

另外，为了保证这个随机图形可以行使轮子的功能，我还要求它在滚动时有稳定的支撑轴，这就是

- 命题3：在平面图形中有一点，其纵坐标始终不变$s \in S, s_y=const.$

我必须承认满足这些要求的图形与路面有点奇怪，它们之间的滚动关系就像下面这样。

![20240601-204849.gif](%E8%B7%AF%E4%B8%8D%E9%83%BD%E6%98%AF%E5%B9%B3%E7%9A%84%EF%BC%8C%E8%BD%AE%E4%B8%8D%E9%83%BD%E6%98%AF%E5%9C%86%E7%9A%84%20dbb39dcd6c554bcebba2799ee9eaa942/20240601-204849.gif)

## 满足条件的异形轮子与道路

下面是一些比较容易理解的图形，比如椭圆对应的道路是三角函数曲线、心形曲线对应的道路有个奇怪的尖尖。当然，对于任意凸图形，我们都能找到它们对应的道路。

虽然如此，**这些道路的性能都不如圆轮子的好，问题出在速度上**。道路上点的颜色代表轮子转动的角速度与轮轴移动的线速度之间的关系。直观来看，由于轮子转动时的等效半径随时可变，因此当轮子绕轮轴以稳定的角速度旋转时，它的线速度时快时慢。在图中颜色越红代表线速度越快，越蓝代表线速度越慢。

想象一下使用“特殊”形状的轮子在匹配的路面上开时的感觉，那简直是晕车制造者。本文的计算和交互代码可见我的Observablehq笔记本，欢迎点赞和转发。

https://observablehq.com/@listenzcc/convex-shapes-have-their-roads

从目前的结果来看，尽管性能堪忧，但只要路修得合适，任意凸图形（convex shapes）都可以是轮子的形状。古人云削足适履，也许不完全是个笑话。

![Untitled](%E8%B7%AF%E4%B8%8D%E9%83%BD%E6%98%AF%E5%B9%B3%E7%9A%84%EF%BC%8C%E8%BD%AE%E4%B8%8D%E9%83%BD%E6%98%AF%E5%9C%86%E7%9A%84%20dbb39dcd6c554bcebba2799ee9eaa942/Untitled.png)

![Untitled](%E8%B7%AF%E4%B8%8D%E9%83%BD%E6%98%AF%E5%B9%B3%E7%9A%84%EF%BC%8C%E8%BD%AE%E4%B8%8D%E9%83%BD%E6%98%AF%E5%9C%86%E7%9A%84%20dbb39dcd6c554bcebba2799ee9eaa942/Untitled%201.png)

![Untitled](%E8%B7%AF%E4%B8%8D%E9%83%BD%E6%98%AF%E5%B9%B3%E7%9A%84%EF%BC%8C%E8%BD%AE%E4%B8%8D%E9%83%BD%E6%98%AF%E5%9C%86%E7%9A%84%20dbb39dcd6c554bcebba2799ee9eaa942/Untitled%202.png)
