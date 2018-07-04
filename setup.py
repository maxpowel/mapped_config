from setuptools import setup

with open('requirements.txt') as fp:
    install_requires = fp.read()

setup(
    name='mapped_config',
    packages=['mapped_config'],
    version='2.34',
    description='Mapped config loader for python for secure, easy and modular configuration management',
    author='Alvaro Garcia Gomez',
    author_email='maxpowel@gmail.com',
    url='https://github.com/maxpowel/mapped_config',
    download_url='https://github.com/maxpowel/mapped_config/archive/master.zip',
    keywords=['config', 'configuration', 'yml', 'json'],
    classifiers=['Topic :: Adaptive Technologies', 'Topic :: Software Development', 'Topic :: System',
                 'Topic :: Utilities'],
    install_requires=install_requires
)
