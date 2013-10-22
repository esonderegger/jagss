from setuptools import setup


def readme():
    with open('readme.md') as f:
        return f.read()

requirements = [
    'jinja2>=2.0',
    'markdown2>=2.0',
    'pyyaml>=3.10',
    'watchdog>=0.6'
]


setup(name='jagss',
      version='0.0.1',
      description='Just another generator for static sites',
      url='http://github.com/esonderegger/jagss',
      author='Evan Sonderegger',
      author_email='evan.sonderegger@gmail.com',
      license='MIT',
      packages=['jagss'],
      install_requires=requirements,
      scripts=['bin/jagss'],
      zip_safe=False)
