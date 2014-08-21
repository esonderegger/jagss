from setuptools import setup, find_packages


def readme():
    with open('readme.md') as f:
        return f.read()

requirements = [
    'jinja2>=2.0',
    'markdown2>=2.0',
    'pyyaml>=3.10',
    'watchdog>=0.6',
    'paramiko>=1.12.0',
    'boto_rsync>=0.8.1'
]


setup(name='jagss',
      version='0.0.1',
      description='Just another generator for static sites',
      url='http://jagss.rpy.xyz',
      author='Evan Sonderegger',
      author_email='evan.sonderegger@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['examples*']),
      install_requires=requirements,
      scripts=['bin/jagss'],
      zip_safe=False)
