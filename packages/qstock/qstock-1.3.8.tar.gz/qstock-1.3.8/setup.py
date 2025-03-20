
from setuptools import setup, find_packages

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='qstock',
    version='1.3.8',
    keywords=['pip','qstock'],
    description='Quantitative finance and stock analysis using Python',
    long_description=long_description,
    author='Jinyi Zhang',
    author_email='723195276@qq.com',
    url='https://github.com/tkfy920/qstock',
    
    license = "MIT Licence",
    
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy", "pandas","matplotlib","pyecharts",
                        "tqdm","jieba","seaborn","plotly_express",
                        "beautifulsoup4","jsonpath","multitasking",
                        "plotly","py_mini_racer","requests","PyExecJS",
                        "func_timeout","pywencai"]
)
