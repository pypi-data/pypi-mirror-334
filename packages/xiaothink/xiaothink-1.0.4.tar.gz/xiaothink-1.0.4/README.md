# Xiaothink Python 模块使用文档

Xiaothink 是一个以自然语言处理（NLP）为核心的AI研究组织，致力于提供高效、灵活的工具来满足各种应用场景的需求。Xiaothink Python 模块是该组织提供的核心工具包，涵盖了图像生成、文本续写、颜值评分以及对话模型等多种功能。以下是详细的使用指南和代码示例。

## 目录
1. [安装](#安装)
2. [图像生成](#图像生成)
3. [文本续写](#文本续写)
4. [颜值评分](#颜值评分)
5. [在线AI对话](#在线ai对话)
6. [本地对话模型](#本地对话模型)

---

## 安装

首先，您需要通过 pip 安装 Xiaothink 模块：

```bash
pip install xiaothink
```

---

## 图像生成

Xiaothink 提供了强大的图像生成功能，可以通过简单的 API 调用来生成高质量的图像。

### 示例代码

```python
import xiaothink as xt

drawer = xt.openapi.drawer.Drawer(return_type='bytes')
with open('a.jpg', 'wb') as f:
    f.write(drawer.draw('两只猫', style=6))
```

---

## 文本续写

您可以使用 Xiaothink 的文本续写功能来生成连贯且有意义的文本内容。

### 示例代码

```python
import xiaothink as xt

text = '从前，由一位老人，'
out_ = xt.openapi.writer.write(text)
print('续写内容：', out_)
```

---

## 颜值评分

Xiaothink 提供了基于 Web URL 的颜值评分服务。请注意，该服务仅支持传入网络图片 URL，不支持本地路径。

### 示例代码

```python
import xiaothink as xt

image_url = "https://example.com/image.jpg"
num = xt.openapi.yanzhi.get_score(image_url)
print('颜值得分：', num)
```

**重要提示**：`xt.openapi.yanzhi.get_score` 函数只支持传入 Web URL，不支持传入本地路径。

---

## 在线AI对话

Xiaothink 提供了一个简便易用的在线 AI 对话接口。设置用户名后即可进行多轮对话。


### 示例代码

```python
import xiaothink as xt

xt.openapi.set_conf.set_user('YOUR_USERNAME')

while True:
    inp = input('【问】：')
    re = xt.openapi.chatbot_old.chat(inp)
    print('\n【答】：', re, '\n')
```

**重要提示**：在线 AI 对话与本地模型对话是两个完全不同的系统，毫无关系。`xt.openapi.chatbot_old.chat` 函数设置用户名后便支持多轮对话。

---

## 本地对话模型

对于本地加载的对话模型，根据模型类型的不同，应调用相应的函数来进行对话。

### 单轮对话

适用于单轮对话场景。

### 示例代码

```python
import xiaothink.llm.inference.test_formal as tf

model = tf.QianyanModel(
    ckpt_dir=r'E:\小思框架\论文\ganskchat\ckpt_test_40_2_3_1_formal_open',
    MT=40.231,
    vocab=r'E:\小思框架\论文\ganskchat\vocab_lx3.txt'
)

while True:
    inp = input('【问】：')
    if inp == '[CLEAN]':
        print('【清空上下文】\n\n')
        model.clean_his()
        continue
    re = model.chat_SingleTurn(inp)  # 使用 chat_SingleTurn 进行单轮对话
    print('\n【答】：', re, '\n')
```

### 多轮对话

适用于多轮对话场景。

### 示例代码

```python
import xiaothink.llm.inference.test as test

MT = 40.231
m, d = test.load(
    ckpt_dir=r'E:\小思框架\论文\ganskchat\ckpt_test_40_2_3_1_qas',
    model_type=MT,
    vocab=r'E:\小思框架\论文\ganskchat\vocab_lx3.txt',
)

b_chat = {
    1: '给定一个数字列表，找出其中的最大值和最小值。\n数字列表：[3, 9, 2, 7, 5, 1, 8, 4, 6, 0]',
    2: '请生成一段关于“春风”为主题的短故事，提供完整的答案。\n',
    3: '请回答下列问题：“什么是全球变暖？”\n',
    4: '请创建一个简单的Python程序，用于计算两数乘积\n',
    5: '创建一个简单的计算器，并提供任何必需的数学原理。\n',
    6: '根据给定的单词，生成与该单词相关的五个同义词。\n单词：友谊\n',
}[6]

belle_chat = '{"instruction": "{b_chat}", "input": "", "output": "'.replace('{b_chat}', b_chat)
inp_m = belle_chat

ret = test.generate_texts_loop(m, d, inp_m,
                               num_generate=100,
                               every=lambda a: print(a, end='', flush=True),
                               temperature=0.55,
                               pass_char=['▩'])
```

**重要提示**：对于本地模型，单论对话模型应调用 `model.chat_SingleTurn` 函数，多轮对话模型应调用 `model.chat` 函数。

---

以上就是 Xiaothink Python 模块的主要功能及使用方法。

如有任何疑问或建议，请随时联系我们：xiaothink@foxmail.com。