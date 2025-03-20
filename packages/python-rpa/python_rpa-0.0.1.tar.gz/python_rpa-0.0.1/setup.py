"""setup.py"""

from setuptools import setup, find_packages

setup(
    name='python-rpa',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        # 필요한 패키지를 여기에 나열합니다
    ],
    description='A description of your package',
    author='Shinyoung Kim',
    author_email='shinyoung.kim@hyundai-autoever.com',
    url='https://gitlab.hmg-corp.io/swdc/python-rpa',
    tests_require=[
        'pytest',  # 또는 원하는 테스트 프레임워크
    ],
)
