from setuptools import setup

setup(
    name='RD-transform',    # This is the name of your PyPI-package.
    version='0.1.0',                          # Update the version number for new releases
    url='https://github.com/CasvandenBogaard/RD_transform',

    author='Cas van den Bogaard',
    author_email='casvandenbogaard@gmail.com',

    license='MIT',
    
    keywords='coordinate transform latitude longitude RD rijksdriehoek rijksdriehoeksstelsel',
    
    scripts=['RD_transform']                  # The name of your scipt, and also the command you'll be using for calling it
)
