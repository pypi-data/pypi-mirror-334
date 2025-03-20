'''
Author: Tong hetongapp@gmail.com
Date: 2025-02-15 19:34:24
LastEditors: Tong tong.he@generac.com
LastEditTime: 2025-03-15 20:16:21
FilePath: /server/setup.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
# setup.py
from setuptools import setup, find_packages

setup(
    name='utm_cli',
    version='0.1.11',
    description='A CLI tool for UTM server',
    author='Tong He',
    author_email='hetongapp@gmail.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},  # 指定包的根目录为 src
    install_requires=[
        'typer>=0.15.1',
    ],
    entry_points={
        'console_scripts': [
            'utm-cli=server.cli:main',  # 注册命令行工具
        ],
    },
    include_package_data=True,  # 包含非 Python 文件（如 JSON）
)