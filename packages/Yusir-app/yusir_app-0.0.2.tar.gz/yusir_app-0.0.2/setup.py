from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'some function for rpa_application '
LONG_DESCRIPTION = '一些通用函数'

setup(
    name="Yusir_app",
    version="0.0.2",
    author="Yu.sir",
    author_email="linxing_1@163.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[]
    , dependencies=[
        'pyautogui',
        'opencv-python',
        'pywin32',
        'xlrd'
    ]
)
