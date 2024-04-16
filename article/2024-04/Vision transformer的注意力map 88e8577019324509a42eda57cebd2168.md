# Vision transformer的注意力map

Title: Vision transformer的注意力map
Date: 2024-4-16
Keywords: Transformer, Attention

---

深度学习大模型的成功在很大程度上是由于transformer结构巧妙地引入了注意力机制，这是个大话题，牵扯到有些繁琐的矩阵计算。这个话题我还把握不住，因此本文还是只有结果而没有分析。

[toc]

---

## Transformer网络的注意力结构

下图是众所周知的经典transformer结构。对于序列式的输入信息，它首先通过位置编码（Positional Encoding）相加的方法对序列中的数据进行“调整”。这时输入数据就包含了关键的元素位置信息。

在信息输入之后，这些数据就开始迭代。经过$N$次迭代，这些信息被不断地分析和重组，形成新的特征，这些特征最终经过线性层（linear）和激活层（softmax），最终输出概率分布。

迭代的核心机制称为“注意力”（Attention）。暂时不论注意力计算的原理，只需要记住注意力模块计算时始终保持输入与输出特征的维度不变。因此，注意力机制的计算可以重复$N$次，不断迭代。

![Untitled](Vision%20transformer%E7%9A%84%E6%B3%A8%E6%84%8F%E5%8A%9Bmap%2088e8577019324509a42eda57cebd2168/Untitled.png)

![Untitled](Vision%20transformer%E7%9A%84%E6%B3%A8%E6%84%8F%E5%8A%9Bmap%2088e8577019324509a42eda57cebd2168/Untitled%201.png)

[Attention Is All You Need](https://arxiv.org/abs/1706.03762)

## Vision transformer的注意力计算

在视觉图像处理领域，transformer将图像分成$16 \times 16$的块（patches），这些块以长度为$256$长度的序列形式输入到transformer的注意力模块中，进行迭代计算，最终形成分析结果。

![Untitled](Vision%20transformer%E7%9A%84%E6%B3%A8%E6%84%8F%E5%8A%9Bmap%2088e8577019324509a42eda57cebd2168/Untitled%202.png)

[An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale](https://arxiv.org/abs/2010.11929)

## 注意力map映射

在以上计算过程中，只要把每次迭代时产生的$Q, K, V$记录下来，尤其需要记录内积

$$
Q\cdot K
$$

它包含着子矩阵，代表输入序列中全部patches的连接关系。

$$
A \in R^{256 \times 256}
$$

数值越大，代表连接关系越强。经过恰当的计算和叠加后，得到以下结果。图中越亮的区域，代表该值越大。这说明大模型在处理这张图片时越“重视”这些区域。

![Untitled](Vision%20transformer%E7%9A%84%E6%B3%A8%E6%84%8F%E5%8A%9Bmap%2088e8577019324509a42eda57cebd2168/Untitled%203.png)

![Untitled](Vision%20transformer%E7%9A%84%E6%B3%A8%E6%84%8F%E5%8A%9Bmap%2088e8577019324509a42eda57cebd2168/Untitled%204.png)

## 附录：核心代码和解释说明

```python
'''
Compute and draw the attention map.
The unit of the attention map is the 16 x 16 grid
'''
att_mat = outputs.vision_model_output.attentions
att_mat = torch.stack(att_mat)
display(f'att_mat.size(): {att_mat.size()}')

att_mat = att_mat[:, 0].squeeze(1).cpu()
display(f'att_mat.size(): {att_mat.size()}')

# Average the attention weights across all heads.
att_mat = torch.mean(att_mat, dim=1)
# att_mat = torch.std(att_mat, dim=1)
# att_mat = att_mat[:, 1].squeeze(1)
display(f'att_mat.size(): {att_mat.size()}')

# To account for residual connections, we add an identity matrix to the
# attention matrix and re-normalize the weights.
residual_att = torch.eye(att_mat.size(1))
aug_att_mat = att_mat + residual_att
aug_att_mat = aug_att_mat / aug_att_mat.sum(dim=-1).unsqueeze(-1)
display(f'aug_att_mat.size(): {aug_att_mat.size()}')

# Recursively multiply the weight matrices
joint_attentions = torch.zeros(aug_att_mat.size())
joint_attentions[0] = aug_att_mat[0]

for n in range(1, aug_att_mat.size(0)):
    joint_attentions[n] = torch.matmul(aug_att_mat[n], joint_attentions[n-1])
display(f'joint_attentions.size(): {joint_attentions.size()}')

joint_attentions = joint_attentions.detach().numpy()
```

> **Attention Mechanisms in Transformers:**
>
> **1. Query, Key, Value (QKV):** Transformers employ QKV vectors to perform attention. Think of it as having a dictionary (key-value pairs) where you want to retrieve specific information (query). Q represents what you’re looking for, K indicates the location of relevant information, and V contains the actual information.
>
> 2. **Scaled Dot-Product Attention:** The heart of attention calculation involves the scaled dot-product attention. It gauges the “closeness” between the query and each key-value pair. The dot product of Q and K is computed, scaled by the square root of K’s dimension, and then passed through a softmax function to derive attention weights. These weights dictate the contribution of each value to the output.
>
> 3. **Weighted Output:** Attention combines the values using the computed weights. Higher weights imply more relevant information is included, allowing the model to focus on the most pertinent parts of the input sequence at each processing step.
>
> [How do attention mechanisms in Transformers, utilizing concepts like QKV vectors and scaled…](https://medium.com/@sujathamudadla1213/how-do-attention-mechanisms-in-transformers-utilizing-concepts-like-qkv-vectors-and-scaled-d2b955c45d4e)
>
