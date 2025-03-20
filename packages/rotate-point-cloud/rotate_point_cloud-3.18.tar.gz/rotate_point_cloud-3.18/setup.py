from setuptools import setup, find_packages

setup(
    name="rotate_point_cloud",  # 包名
    version="3.18",           # 版本号
    author="tcb",        # 作者
    author_email="3035719537@qq.com",  # 作者邮箱
    description="A utility for rotating point clouds",  # 包描述
    packages=find_packages(),  # 自动查找包
    install_requires=[         # 依赖项
        "numpy",
        "open3d"
    ],
    python_requires=">=3.8",  # Python版本要求
)