from setuptools import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()


setup(
    name='piplock',
    version='0.1.0',
    description='pip requirements For Aliens',
    long_description=readme,
    author='Hiroki Kiyohara',
    author_email='hirokiky@gmail.com',
    url='https://github.com/hirokiky/piplock',
    py_modules=['piplock'],
    entry_points={
        'console_scripts': [
            'piplock=piplock:main',
        ],
    },
)
