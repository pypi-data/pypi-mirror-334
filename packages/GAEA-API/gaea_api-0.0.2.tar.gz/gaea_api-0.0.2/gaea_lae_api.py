#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GAEA Low-altitude Economy API客户端库
"""

import json
import requests
from typing import Dict, List, Generator

class GAEALAEAPIClient:
    """GAEA API客户端类"""
    
    def __init__(self, mac_address: str, api_key: str, base_url: str = "http://127.0.0.1:8080"):
        """
        初始化客户端
        
        Args:
            mac_address: MAC地址
            api_key: 加密的API密钥
            base_url: API服务器基础URL
        """
        self.mac_address = mac_address
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        
        # 验证参数
        if not mac_address or not api_key:
            raise ValueError("MAC地址和API密钥不能为空")
        
    def _make_request(self, method: str, endpoint: str, data: Dict) -> Dict:
        """
        发送HTTP请求
        
        Args:
            method: HTTP方法
            endpoint: API端点
            data: 请求数据
            
        Returns:
            API响应
        """
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        # 添加认证信息到请求数据
        data['mac_address'] = self.mac_address
        data['api_key'] = self.api_key
        
        try:
            response = requests.request(method, url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"请求失败: {str(e)}"}
    
    def chat(self, messages: List[Dict], reasoning: bool = False) -> Dict:
        """
        发送聊天请求
        
        Args:
            messages: 消息列表
            reasoning: 是否返回思考过程
            
        Returns:
            API响应
        """
        data = {
            "messages": messages,
            "reasoning": reasoning
        }
        return self._make_request("POST", "/api/chat", data)
    
    def stream_chat(self, messages: List[Dict], reasoning: bool = False) -> Generator[Dict, None, None]:
        """
        发送流式聊天请求
        
        Args:
            messages: 消息列表
            reasoning: 是否返回思考过程
            
        Yields:
            响应数据块
        """
        url = f"{self.base_url}/api/stream-chat"
        headers = {'Content-Type': 'application/json'}
        data = {
            "messages": messages,
            "reasoning": reasoning,
            "mac_address": self.mac_address,
            "api_key": self.api_key
        }
        
        try:
            with requests.post(url, headers=headers, json=data, stream=True) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk = json.loads(line.decode('utf-8'))
                            if "error" in chunk:
                                yield chunk
                                break
                            if "done" in chunk:
                                break
                            yield chunk
                        except json.JSONDecodeError:
                            yield {"error": "解析响应数据失败"}
        except requests.exceptions.RequestException as e:
            yield {"error": f"请求失败: {str(e)}"}
    
    def verify_api(self, mac_address: str, encrypted_api: str) -> Dict:
        """
        验证加密API密钥
        
        Args:
            mac_address: MAC地址
            encrypted_api: 加密API密钥
            
        Returns:
            API响应
        """
        data = {
            "mac_address": mac_address,
            "api_key": encrypted_api
        }
        return self._make_request("POST", "/api/verify", data)
    
    def health_check(self) -> Dict:
        """
        检查API服务健康状态
        
        Returns:
            API响应
        """
        return self._make_request("GET", "/api/health", {}) 