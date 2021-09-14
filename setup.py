from setuptools import setup, find_packages

setup(
    name='arcassistant',
    version='0.0.0',
    packages=find_packages(),
    url='',
    license='',
    author='thedjaney',
    author_email='thedjaney@gmail.com',
    description='',
    install_requires=[
        'tasktimer'
        'pyqt5==5.14.*',
    ],
    dependency_links=[
        'https://github.com/djaney/tasktimer/archive/refs/heads/main.zip#egg=tasktimer'
    ],
    entry_points={
        "gui_scripts": [
            "arcassistant = arcassistant.app:main"
        ]
    },

)
