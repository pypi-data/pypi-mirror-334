from time import time
import setuptools
# c:\Python38\python.exe setup.py clean --all
# c:\Python38\python.exe setup.py sdist
# c:\Python38\python.exe -m build
# c:\Python38\python.exe -m twine upload dist/* --skip-existing
# 用户名 jerry1979
# pypi-AgEIcHlwaS5vcmcCJGM3OTZmY2E1LWE1NDktNDkyNy1iNTNlLWEwMmM4OTQ1MjhlNAACKlszLCIzNWQzNjY4My0xMTllLTQ1MGItYjcxOC01ODEyNzM5YWRhYTAiXQAABiA40wOXr8lkNhP_8JPFPobklTUCWB7yJEQRIcHre-uMTA

# (myBase) E:\BaiduSyncdisk\pyLib\mxupyPackage>python setup.py sdist bdist_wheel

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mxupy",
    version="1.0.6",
    author="jerry",
    author_email="6018421@qq.com",
    description="An many/more extension/utils for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "mxupy"},
    packages=setuptools.find_packages(where="mxupy"),
    python_requires=">=3.8",
)
