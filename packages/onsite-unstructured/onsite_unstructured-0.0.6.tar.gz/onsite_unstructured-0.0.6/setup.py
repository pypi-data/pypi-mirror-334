import os
import setuptools
from setuptools import setup, find_packages

# 允许setup.py在任何路径下执行
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setuptools.setup(
    name="onsite_unstructured",  # 库名
    version="0.0.6",  # 版本号
    author="kaiwen",  # 作者
    author_email="xhh666@sjtu.edu.cn",  # 作者邮箱
    description="A small example package",  # 简介
    long_description="long_description",  # 详细描述
    long_description_content_type="text/markdown",  # 描述语法
    url="https://github.com/pypa/sampleproject",  # 项目主页
    packages=find_packages(),
    package_data={
        "onsite_unstructured": [
            "onsite-unstructured/data/*.npy",
            "onsite-unstructured/kinetic_model/linux/*.slxp",  # 递归包含所有 .slxp 文件
            "onsite-unstructured/kinetic_model/linux/*.mat",   # 递归包含所有 .mat 文件
            "onsite-unstructured/kinetic_model/linux/*.m",     # 递归包含所有 .m 文件
            "onsite-unstructured/kinetic_model/linux/*.slx"    # 递归包含所有 .slx 文件
            "onsite-unstructured/kinetic_model/linux/*.slxc"    # 递归包含所有 .slx 文件

            "onsite-unstructured/kinetic_model/win/*.slxp",  # 递归包含所有 .slxp 文件
            "onsite-unstructured/kinetic_model/win/*.mat",   # 递归包含所有 .mat 文件
            "onsite-unstructured/kinetic_model/win/*.m",     # 递归包含所有 .m 文件
            "onsite-unstructured/kinetic_model/win/*.slx"    # 递归包含所有 .slx 文件
            "onsite-unstructured/kinetic_model/win/*.slxc"    # 递归包含所有 .slxc 文件
            "onsite-unstructured/kinetic_model/win/*.mexw64"    # 递归包含所有 .slx 文件

        ]
    },
    include_package_data=True,  # 激活 MANIFEST.in 文件
    classifiers=[  # 指定库的分类器
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[  # 依赖库
        'pyautogui',
        'Django >= 1.11',
    ],
    python_requires='>=3.6',
)