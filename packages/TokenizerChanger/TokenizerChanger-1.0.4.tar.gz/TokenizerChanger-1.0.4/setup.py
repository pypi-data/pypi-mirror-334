from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='TokenizerChanger',
    version='1.0.4',
    author='1kkiren',
    author_email='1kkiren@mail.ru',
    description='Library for manipulating the existing tokenizer.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/1kkiRen/Tokenizer-Changer',
    packages=find_packages(),
    install_requires=[
        'tokenizers>=0.20.1',
        'tqdm>=4.66.4',
        'transformers>=4.45.2',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
    ],
    keywords='tokenizer deletion tokens ',
    project_urls={
        'GitHub': 'https://github.com/1kkiRen/Tokenizer-Changer'
    },
    python_requires='>=3.9'
)
