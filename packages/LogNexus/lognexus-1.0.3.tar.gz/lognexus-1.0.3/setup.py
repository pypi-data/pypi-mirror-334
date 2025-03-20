import setuptools

setuptools.setup(
    name="LogNexus",
    version="1.0.3",
    author="csq",
 # 如果项目由多个文件组成，我们可以使用find_packages()自动发现所有包和子包，而不是手动列出每个包，在这种情况下，包列表将是example_pkg
    packages=setuptools.find_packages(),
    # 关于包的其他元数据(metadata)
    classifiers=[
         # 该软件包仅与Python3兼容
        "Programming Language :: Python :: 3",
        # 根据MIT许可证开源
        "License :: OSI Approved :: MIT License",
        # 与操作系统无关
        "Operating System :: OS Independent",
    ]
)