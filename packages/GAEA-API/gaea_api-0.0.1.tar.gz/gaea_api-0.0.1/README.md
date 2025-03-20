# GAEA低空经济AI接口客户端

## 简介

GAEA低空经济AI接口(GAEA Low-altitude Economy API)是一个强大的AI接口服务，为低空经济应用提供智能对话能力。本客户端库提供了简单易用的Python接口，帮助开发者快速集成GAEA AI能力到自己的应用中。

## 安装

```bash
# 使用pip安装
pip install -r requirements.txt
```

## 快速开始

### 基本使用

```python
from gaea_lae_api import GAEALAEAPIClient

# 创建客户端实例
client = GAEALAEAPIClient(
    mac_address="YOUR_MAC_ADDRESS",  # 您的设备MAC地址
    api_key="YOUR_API_KEY",          # 您的API密钥
    base_url="http://api.example.com"  # API服务地址，默认为本地5000端口
)

# 验证API连接
response = client.verify_api()
if "status" in response and response["status"] == "success":
    print("API验证成功")
else:
    print("API验证失败")

# 发送单轮对话
reply = client.simple_chat("你好，请介绍一下自己。")
print(reply)
```

## 功能特性

### 健康检查

检查API服务是否正常运行：

```python
status = client.health_check()
print(status)
```

### 单轮对话

快速进行单次问答：

```python
reply = client.simple_chat("人工智能的发展历程是什么？")
print(reply)
```

### 完整对话API

自定义参数进行对话：

```python
messages = [
    {"role": "user", "content": "写一首关于人工智能的短诗。"}
]
response = client.chat(messages, temperature=0.8, top_p=0.95)
print(response)
```

### 流式输出

实时获取AI生成内容，适用于需要逐字显示的场景：

```python
messages = [
    {"role": "user", "content": "详细解释量子计算的原理。"}
]
for chunk in client.stream_chat(messages):
    print(chunk, end="", flush=True)
print()
```

### 多轮对话

维护对话上下文，实现连贯的多轮交流：

```python
# 初始化对话历史
history = []

# 第一轮对话
response1 = client.multi_turn_chat(history, "什么是Python?")
print(f"回复: {response1['reply']}")
history = response1["history"]

# 第二轮对话
response2 = client.multi_turn_chat(history, "它与Java有什么区别?")
print(f"回复: {response2['reply']}")
```

## API参数说明

### 初始化参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| mac_address | str | 是 | 设备MAC地址，用于API认证 |
| api_key | str | 是 | 加密的API密钥 |
| base_url | str | 否 | API服务的基础URL，默认为"http://laeapi.lavic.cn" |

### 对话参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| messages | List[Dict] | 是 | 消息列表，格式为[{"role": "user", "content": "消息内容"}, ...] |
| temperature | float | 否 | 生成温度，控制随机性，默认0.7 |
| top_p | float | 否 | 生成多样性，控制输出多样性，默认0.9 |

## 错误处理

客户端会自动捕获并处理错误，所有API调用都会返回包含错误信息的字典：

```python
response = client.chat(messages)
if "error" in response:
    print(f"发生错误: {response['error']}")
else:
    print(f"回复: {response['content']}")
```

## 注意事项

1. 请确保您的MAC地址和API密钥正确，否则API将拒绝访问
2. 对于需要长时间处理的复杂查询，建议使用流式输出
3. 多轮对话时请妥善保存对话历史，以维持上下文连贯性

## 许可证

本客户端库使用MIT许可证。

## 支持与反馈

如有问题或建议，请联系GAEA in cloud 团队。 