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
        'tasktimer',
        'pyqt5==5.14.*',
    ],
    dependency_links=[
        'git+https://github.com/djaney/tasktimer.git@main#egg=tasktimer-0.0.1'
    ],
    entry_points={
        "gui_scripts": [
            "arcassistant = arcassistant.app:main"
        ]
    },

)
