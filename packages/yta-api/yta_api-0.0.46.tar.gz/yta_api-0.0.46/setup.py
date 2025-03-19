from setuptools import setup, find_packages


VERSION = '0.0.46'
DESCRIPTION = 'Youtube Autonomous API Module.'
LONG_DESCRIPTION = 'This is the Youtube Autonomous API module'

setup(
    name = "yta_api", 
    version = VERSION,
    author = "Daniel Alcalá",
    author_email = "<danielalcalavalera@gmail.com>",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = [
        'fastapi',
        'yta_audio',
        'yta_image',
        'yta_general_utils',
        #'pyliblzma' # Only for vercel deployment
    ],
    
    keywords = [
        'youtube autonomous api module software'
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)