try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='robohash',
    packages=['robohash'],
    version='2.0a1',
    description='One of the leading robot-based hashing tools on the web',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='e1ven',
    author_email='robo@robohash.org',
    url='https://github.com/e1ven/Robohash',
    download_url='https://github.com/e1ven/Robohash/tarball/2.0a1',
    keywords=['robots', 'avatar', 'identicon'],
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Development Status :: 4 - Beta",
        "Topic :: Security",
    ],
    package_data={
        'robohash': [
            'sets/set1/*/*/*',
            'sets/set2/*/*',
            'sets/set3/*/*',
            'sets/set4/*/*',
            'sets/set5/*/*',
            'backgrounds/*/*',
        ]
    },
    install_requires=['pillow>=9.1.1', 'natsort>=8.1.0'],
    extras_require={
        'web': ['tornado>=6.1'],
    },
    python_requires='>=3.6',
)
