from setuptools import setup

setup(
    name='py-salus',
    packages=['salus'],
    version='0.1.2',
    url='https://github.com/cipacda/py-salus',
    description='Python library to integrate with it500 Salus devices',
    long_description='Library to connect to it500 Salus devices.',
    author='cipacda',
    author_email='cipaflorescu@gmail.com',
    license='MIT',
    install_requires=[
        'requests',
        'beautifulsoup4',
        'cachetools',
    ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest==4.4.1',
        'requests_mock',
    ],
    test_suite='tests',
)
