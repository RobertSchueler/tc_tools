from setuptools import setup

setup(
    name='tc_tools',
    version='0.3.0',
    description='Simple trading card generation',
    url='https://github.com/RobertSchueler/tc_tools',
    author='Robert Schüler',
    author_email='robert.schueler1989@gmail.com',
    license='Apache-2.0',
    packages=['tc_tools'],
    install_requires=['pandas'],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.10',
    ],
)