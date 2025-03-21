from setuptools import setup, find_packages

setup(
    name='obs-tally-luxafor',
    version='0.3.1',
    author='Robin Glauser',
    author_email='robin.glauser@gmail.com',
    description='OBS integration with Luxafor LED devices',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    url='https://github.com/nahakiole/obs-tally-luxafor',
    install_requires=[
        'requests',
        'obsws_python'
    ],
    entry_points={
        'console_scripts': [
            'obs-tally-luxafor=obs_tally_luxafor.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
