from setuptools import setup

setup(
    name="GAEA_API",    # 包名（pip install 时用的名字）
    version="0.0.2",               # 版本号
    py_modules=["gaea_lae_api"], # 直接指定你的Python文件名（不带.py）
    author="Yongtan Wang",
    description="A client modules for using gaea low-altitude economy gaea_lae_api",
    python_requires=">=3.10",
    install_requires=["requests"],         # 依赖库列表，例如 ["requests"]
    url="http://codebase.gaeaincloud.com:solution/gaea_lae_api_client.git",
)