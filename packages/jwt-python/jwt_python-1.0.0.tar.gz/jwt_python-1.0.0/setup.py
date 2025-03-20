from setuptools import setup, find_packages

setup(
    name='jwt-python',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        # 依赖列表
    ],
    author='ZhongYang',
    author_email='19865697458@163.com',
    description='用于生成和验证JWT令牌的Python模块',
    long_description=open('README.md',encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://gitee.com/yangyingyun/jwt-python',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)