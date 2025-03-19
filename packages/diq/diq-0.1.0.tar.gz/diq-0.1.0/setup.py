from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='diq',
    version='0.1.0',
    keywords=['dict', 'class'],
    description='Pythonic Object Serializer',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT Licence',
    url='https://github.com/Jyonn/dik',
    author='Qijiong Liu',
    author_email='liu@qijiong.work',
    platforms='any',
    packages=find_packages(),
    install_requires=[],
)
