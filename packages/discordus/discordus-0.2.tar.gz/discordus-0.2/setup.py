from setuptools import setup, find_packages

setup(
    name='discordus',
    version='0.2',
    description='A simpler version of discord.py. View github page: https://github.com/RobloxFactoryRyaturmite/discordus/tree/main',
    packages=find_packages(),
    install_requires=[
        'discord.py',  # Adds the Discord library as a dependency
    ],
    entry_points={
        'console_scripts': [
            'initialize-discordus = discordus.init_app:main',  # Example script entry point
        ],
    }
)
