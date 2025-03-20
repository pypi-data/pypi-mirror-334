from setuptools import setup
from pathlib import Path

setup(
  name='uvicorn_daemonite',
  version='0.1.1',
  description='Run you apps as server. A start/stop/status commandline for your ASGI/WSGI compatible frameworks.',
  long_description=Path("README.rst").read_text(encoding="utf-8"),
  url='https://github.com/etm/uvicorn_daemonite',
  author="Juergen 'eTM' Mangler",
  author_email='juergen.mangler@gmail.com',
  license='LGPL',
  packages=['uvicorn_daemonite'],
  install_requires=['uvicorn>=0.34.0',
                    'psutil>=5.9.8',
                    ],
  classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python :: 3.11'
  ],
)
