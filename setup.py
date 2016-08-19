from distutils.core import setup
setup(
  name = 'mapped_config',
  packages = ['mapped_config'],
  version = '1.1',
  description = 'Mapped config loader for python for secure, easy and modular configuration management',
  author = 'Alvaro Garcia Gomez',
  author_email = 'maxpowel@gmail.com',
  url = 'https://github.com/maxpowel/mapped_config',
  download_url = 'https://github.com/maxpowel/mapped_config/archive/master.zip',
  keywords = ['config', 'configuration', 'yml', 'json'],
  classifiers = ['Topic :: Adaptive Technologies', 'Topic :: Software Development', 'Topic :: System', 'Topic :: Utilities'],
  install_requires = ['pyyaml']
)