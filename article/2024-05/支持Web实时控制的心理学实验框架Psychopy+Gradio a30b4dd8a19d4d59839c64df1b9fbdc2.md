# 支持Web实时控制的心理学实验框架Psychopy+Gradio

Title: 支持Web实时控制的心理学实验框架Psychopy+Gradio
Date: 2024-5-22
Keywords: Experiment, Web

---

本文介绍了一个结合`Psychopy`和`Gradio`的实时控制框架，能够通过Web实现心理学实验的远程控制。该框架允许控制端实时调整视觉刺激参数，并从受控端获取实验快照，确保实验过程的高精度和低干扰。

---

[toc]

## 实时控制演示

我总有一个想法，那就是只要程序开源且通信方式设计合理，那么科研工作的方方面面都可以实现实时控制。这就是一个集成`Psychopy`和`Gradio`的实时控制框架。

下图是一个程序样例，在左侧的窗口是心理学实验常用的`Psychopy`软件生成的界面，它生成球形`GratingStim`，即不断移动的球形光栅作为视觉刺激，在本例中属于受控端。而我通过右侧的`Gradio`控制器对它的参数进行实时控制，参数包括光栅的位置、方向、颜色密度等。

另外，为了保证控制者能够实时了解实验的运行状态，我还将受控端的快照传输实时到控制端进行展示。控制端可以通过点击快照上的位置，将光栅移动过去。

![Untitled](%E6%94%AF%E6%8C%81Web%E5%AE%9E%E6%97%B6%E6%8E%A7%E5%88%B6%E7%9A%84%E5%BF%83%E7%90%86%E5%AD%A6%E5%AE%9E%E9%AA%8C%E6%A1%86%E6%9E%B6Psychopy+Gradio%20a30b4dd8a19d4d59839c64df1b9fbdc2/Untitled.gif)

## 本框架的优势

由于心理学实验，或者说视觉实验往往需要对刺激的呈现过程进行精确控制，（光栅闪烁的时间精度甚至要达到毫秒级），这就需要刺激端具有较强的计算能力，并且在实验过程中主试不易中途打扰。本框架尝试从两个角度解决以上问题

- 呈现端（即受控端）只需要按当前的参数进行显示，不需要额外考虑过于复杂的实验设计。实时反馈（如果有的话）也可以完全通过其他计算机去做，不需要占用本机的任何计算资源。
- 将控制端与呈现端完全隔离，完全避免主试参与对实验的负面影响。熟悉Web原理和应用的朋友不难发现，尽管这个样本中两个窗口是在一起的，但只要通过合适的`TCP/IP` 网络进行连接，那么控制端和受控端就可以实现十万八千里之外的远程连接。

## 一个小坑

为了将受控端的快照传输实时到控制端进行展示，我需要对刺激界面进行快照。这时就遇到一个坑，即窗口的**快照**只能在生成它的实例中调用，否则会抛出奇怪的异常`glException: Invalid operation`。我猜测该异常的原因是在其他栈中无法调用显示`buffer`，我也正是顺着这个思路想到了避免它的解决方式，思路如下代码所示。这种方式同样避免了快照生成过早，导致最新修改没有被照到的情况。

```python
class MainWindow(object):
    # Options
    size = [800, 600]

    # create a window
    win = visual.Window(
        size, monitor="testMonitor", units="deg")
        
    def screenshot(self):
        # ! It only works in THIS class.
        img = self.win.screenshot
        self.screenshot_img = img
        return img
        
    def update_frame(self):
        self.msg.text = f'Phase: {self.d_phase:.2f}'
        self.advance_phase()

        self.win.flip()

        if self.screenshot_countdown > 0:
            self.screenshot_countdown -= 1
            if self.screenshot_countdown == 1:
                self.screenshot()
```

## 附录：Psychopy是什么？

`Psychopy`是一款用于创建心理学实验的软件，它可以生成各种视觉和听觉刺激，并且能够精确控制这些刺激的呈现时间和方式。在心理学实验中，Psychopy常用于研究视觉感知、注意力和记忆等方面的问题。

[Home — PsychoPy®](https://www.psychopy.org/)

## 附录：Gradio是什么？

`Gradio`是一款用于构建和分享机器学习模型和应用的工具。它可以通过简单的界面让用户实时输入和调整参数，快速查看模型输出，常用于快速构建和测试人工智能应用的输入输出界面。

[Gradio](https://www.gradio.app/)
