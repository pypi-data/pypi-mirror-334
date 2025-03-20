from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='statshelp',
    version='0.0.4',
    license='MIT License',
    author='Data Scientist',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='datascientist@mateusalifontes.com',
    keywords='[stats, student, data science, analysis]',
    description=u'Library to help Data Science students',
    packages=['statshelp'],
    install_requires=['requests'],)
