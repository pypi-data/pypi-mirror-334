from setuptools import setup, find_packages

setup(
    name="rotate_pcd",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'open3d'  # 确认open3d的正确版本
    ],
    author="tcbtcb9999",
    author_email="3035719537@qq.com",
    description="Point cloud rotation package",
    long_description_content_type="text/markdown",
    url="https://github.com/tcbtcb9999/rotate_pcd",
)