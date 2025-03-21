from setuptools import setup, find_packages
setup(
    name = 'bigOAINet',
    version = '1.0.0',
    description = 'bigO AI Network',
    author = 'jerry',
    author_email = '6018421@qq.com',
    url = 'http://www.xtbeiyi.com/',
    packages = find_packages()
)
# .\py310\python.exe -m pip install twine
# .\py310\python.exe setup.py sdist bdist_wheel
# .\py310\python.exe twine upload dist/*