#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GAEA Low-altitude Economy API客户端库
"""

import json
import requests
from typing import Dict, List, Any, Optional, Union, Generator

class GAEALAEAPIClient:

    def __init__(self, mac_address: str, api_key: str, base_url: str = "http://laeapi.lavic.cn"):
        """
        初始化客户端
        
        Args:
            mac_address: MAC地址
            api_key: 加密的API密钥
            base_url: API服务的基础URL
        """
        self.mac_address = mac_address
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        
        # 验证参数
        if not mac_address or not api_key:
            raise ValueError("MAC地址和API密钥不能为空")
    
    def health_check(self) -> Dict[str, Any]:
        """
        健康检查
        
        Returns:
            Dict: 健康状态信息
        """
        try:
            response = requests.get(f"{self.base_url}/api/health")
            return response.json()
        except Exception as e:
            return {"error": f"健康检查失败: {str(e)}"}

    def verify_api(self) -> Dict[str, Any]:
        """
        验证API密钥
        
        Returns:
            Dict: 验证结果
        """
        try:
            data = {
                "mac_address": self.mac_address,
                "api_key": self.api_key
            }
            
            response = requests.post(
                f"{self.base_url}/api/verify", 
                json=data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                error_data = response.json() if response.content else {"error": f"请求失败，状态码: {response.status_code}"}
                return error_data
                
        except Exception as e:
            return {"error": f"验证API调用失败: {str(e)}"} 
        
    def simple_chat(self, message: str) -> str:
        """
        简单聊天函数，适用于单轮对话
        
        Args:
            message: 用户消息
            
        Returns:
            str: 聊天回复内容
        """
        messages = [{"role": "user", "content": message}]
        response = self.chat(messages)
        
        if "error" in response:
            return f"错误: {response['error']}"
        
        if "content" in response:
            return response["content"]
        
        return str(response)
        
    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7, top_p: float = 0.9) -> Dict[str, Any]:
        """
        聊天API调用
        
        Args:
            messages: 消息列表，格式为[{"role": "user", "content": "消息内容"}, ...]
            temperature: 生成温度，越高越随机
            top_p: 生成多样性，越高越多样
            
        Returns:
            Dict: API响应
        """
        try:
            data = {
                "mac_address": self.mac_address,
                "api_key": self.api_key,
                "messages": messages,
                "temperature": temperature,
                "top_p": top_p
            }
            
            response = requests.post(
                f"{self.base_url}/api/chat", 
                json=data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return response.json().get("content")
            else:
                error_data = response.json() if response.content else {"error": f"请求失败，状态码: {response.status_code}"}
                return error_data
                
        except Exception as e:
            return {"error": f"聊天API调用失败: {str(e)}"}
    
    def stream_chat(self, messages: List[Dict[str, str]], temperature: float = 0.7, top_p: float = 0.9) -> Generator[str, None, None]:
        """
        流式聊天API调用
        
        Args:
            messages: 消息列表，格式为[{"role": "user", "content": "消息内容"}, ...]
            temperature: 生成温度，越高越随机
            top_p: 生成多样性，越高越多样
            
        Yields:
            str: 生成的文本片段
        """
        try:
            data = {
                "mac_address": self.mac_address,
                "api_key": self.api_key,
                "messages": messages,
                "temperature": temperature,
                "top_p": top_p
            }
            
            with requests.post(
                f"{self.base_url}/api/stream-chat", 
                json=data,
                headers={"Content-Type": "application/json"},
                stream=True
            ) as response:
                
                if response.status_code != 200:
                    error_msg = response.json() if response.content else {"error": f"请求失败，状态码: {response.status_code}"}
                    yield json.dumps(error_msg)
                    return
                
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk = json.loads(line.decode('utf-8'))
                            if "error" in chunk:
                                yield chunk["error"]
                                return
                            if "done" in chunk:
                                return
                            if "content" in chunk:
                                yield chunk["content"]
                        except json.JSONDecodeError:
                            yield f"解析响应失败: {line.decode('utf-8')}"
                
        except Exception as e:
            yield f"流式聊天API调用失败: {str(e)}"
      
    def multi_turn_chat(self, history: List[Dict[str, str]], new_message: str) -> Dict[str, Any]:
        """
        多轮对话函数
        
        Args:
            history: 历史消息列表
            new_message: 新的用户消息
            
        Returns:
            Dict: 包含完整对话历史的响应
        """
        # 添加新消息到历史
        messages = history.copy()
        messages.append({"role": "user", "content": new_message})
        
        # 调用聊天API
        response = self.chat(messages)
        
        if "error" in response:
            return {"error": response["error"], "history": messages}
        
        # 将回复添加到历史
        if "content" in response:
            messages.append({"role": "assistant", "content": response["content"]})
        
        return {
            "reply": response,
            "history": messages,
            "finish_reason": response
        } 