

from setuptools import setup, find_packages

setup(
    # Basic package information:
    name='apimagic',  
    version='0.0.2',
    packages=find_packages(),  # Automatically find packages in the directory

    # Dependencies:
    install_requires=[
        'requests',  
    ],

    # Metadata for PyPI:
    author          ='James A. Rolfsen',
    author_email    ='james@think.dev', 
	description     ='ApiMagic is the fastest way to deploy serverless APIs.',
	url             ='https://github.com/jrolf/apimagic',    
    long_description='ApiMagic is the fastest way to deploy serverless APIs.', 

    #long_description=open('README.md').read(),
    #long_description_content_type='text/markdown',  # If your README is in markdown

    # More classifiers: https://pypi.org/classifiers/
    classifiers=[
        'Programming Language :: Python :: 3.12', 
        'License :: OSI Approved :: MIT License',  # Ensure this matches your LICENSE file
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)





