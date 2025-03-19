# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='kksn',
    version='1.0.0',
    packages=find_packages(),
    package_data={
        'kksn': ['*.exe']  # 指定要包含的文件模式
    },
    description='kksn序列号生成器',
    # long_description=open('README.md').read(),
    # python3，readme文件中文报错
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Kuizi',
    author_email='123751307@qq.com',
    license='MIT',
    license_files="LICEN[CS]E*",
    install_requires=[
        'wmi',
        'ntplib'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Intended Audience :: Developers',
        'Topic :: Utilities'
    ]
)
