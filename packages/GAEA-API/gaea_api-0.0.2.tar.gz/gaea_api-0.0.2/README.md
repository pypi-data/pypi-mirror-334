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
from client import GAEALAEAPIClient

# 创建客户端实例
client = GAEALAEAPIClient(
    mac_address="YOUR_MAC_ADDRESS",  # 您的设备MAC地址
    api_key="YOUR_API_KEY",          # 您的API密钥
    base_url="http://api.example.com"  # API服务地址，默认为本地5000端口
)

# 验证API连接
response = client.verify_api("YOUR_MAC_ADDRESS", "YOUR_API_KEY")
if "error" not in response:
    print("API验证成功")
else:
    print(f"API验证失败: {response['error']}")

# 发送单轮对话
messages = [
    {"role": "user", "content": "你好，请介绍一下自己。"}
]
response = client.chat(messages)
if "error" in response:
    print(f"错误: {response['error']}")
else:
    print(f"回答: {response['content']}")
```

## 功能特性

### 健康检查

检查API服务是否正常运行：

```python
response = client.health_check()
print(f"健康检查响应: {response}")
```

### 普通对话

发送对话请求并获取完整响应：

```python
messages = [
    {"role": "user", "content": "请简单介绍一下量子计算的原理。"}
]

# 不带思考过程的对话
response = client.chat(messages, reasoning=False)
if "error" in response:
    print(f"错误: {response['error']}")
else:
    print(f"回答: {response['content']}")

# 带思考过程的对话
response = client.chat(messages, reasoning=True)
if "error" in response:
    print(f"错误: {response['error']}")
else:
    if "reasoning" in response:
        print(f"思考过程: {response['reasoning']}")
    print(f"回答: {response['content']}")
```

### 流式输出

实时获取AI生成内容，适用于需要逐字显示的场景：

```python
messages = [
    {"role": "user", "content": "请简单介绍一下量子计算的原理。"}
]

# 不带思考过程的流式输出
print("回答: ", end="", flush=True)
for chunk in client.stream_chat(messages, reasoning=False):
    if "error" in chunk:
        print(f"\n错误: {chunk['error']}")
        break
    if "content" in chunk:
        print(chunk["content"], end="", flush=True)
print()

# 带思考过程的流式输出
has_shown_reasoning = False
has_shown_answer = False
reasoning_content = ""

for chunk in client.stream_chat(messages, reasoning=True):
    if "error" in chunk:
        print(f"\n错误: {chunk['error']}")
        break
    if "reasoning" in chunk:
        # 只打印新增的思考过程内容
        new_content = chunk["reasoning"][len(reasoning_content):]
        if new_content:
            if not has_shown_reasoning:
                print("思考过程: ", end="", flush=True)
                has_shown_reasoning = True
            print(new_content, end="", flush=True)
            reasoning_content = chunk["reasoning"]
    if "content" in chunk:
        if not has_shown_answer:
            if has_shown_reasoning:
                print("\n回答: ", end="", flush=True)
            else:
                print("回答: ", end="", flush=True)
            has_shown_answer = True
        print(chunk["content"], end="", flush=True)
print()
```

## API参数说明

### 初始化参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| mac_address | str | 是 | 设备MAC地址，用于API认证 |
| api_key | str | 是 | 加密的API密钥 |
| base_url | str | 否 | API服务的基础URL，默认为"http://127.0.0.1:8080" |

### 对话参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| messages | List[Dict] | 是 | 消息列表，格式为[{"role": "user", "content": "消息内容"}, ...] |
| reasoning | bool | 否 | 是否返回思考过程，默认为False |

## 错误处理

客户端会自动捕获并处理错误，所有API调用都会返回包含错误信息的字典：

```python
response = client.chat(messages)
if "error" in response:
    print(f"错误: {response['error']}")
else:
    print(f"回答: {response['content']}")
```

## 注意事项

1. 请确保您的MAC地址和API密钥正确，否则API将拒绝访问
2. 对于需要长时间处理的复杂查询，建议使用流式输出
3. 流式输出时，思考过程会先完整显示，然后显示回答内容
4. 使用流式输出时，建议使用flush=True确保实时显示

## 许可证

本客户端库使用MIT许可证。

## 支持与反馈

如有问题或建议，请联系开发团队。 