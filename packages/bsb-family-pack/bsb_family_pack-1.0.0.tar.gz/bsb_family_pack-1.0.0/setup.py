from setuptools import setup, find_packages

setup(
    name='bsb_family_pack',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'python-telegram-bot',
        'sqlite3',
    ],
    entry_points={
        'console_scripts': [
            'bsb-connect = bsb_monitor:start_monitoring',
        ],
    },
)
