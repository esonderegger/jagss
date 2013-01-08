from setuptools import setup


requirements = [
    'jinja2>=2.0',
    'markdown2>=2.0',
    'watchdog>=0.6'
]


setup(name='jagss',
    version='0.1',
    description='Just another generator for static sites',
    url='http://github.com/esonderegger/jagss',
    author='Evan Sonderegger',
    author_email='evan.sonderegger@gmail.com',
    license='MIT',
    packages=['jagss'],
    install_requires=requirements,
    zip_safe=False)
