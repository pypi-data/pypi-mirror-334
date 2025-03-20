from setuptools import setup, find_packages

setup(
    name="dupdetsdk",  # 与你的目录名一致
    version="0.1.0",
    author="Junzhi Cai",
    author_email="junzhi.cai@anker-in.com",
    description="A package for detecting content duplication",
    packages=find_packages(where="src"),  # 指定源代码在src下
    package_dir={"": "src"},  # 指定包根目录
    install_requires=[
        "chromadb>=0.5.5",
        "dataloopsdk",           
        "loguru>=0.7.0",            
        "numpy",
        "Pillow",
        "torch>=2.4.0,<2.5.0",
        "torchvision>=0.19.0,<0.20.0",
        "tokenizers>=0.13.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)