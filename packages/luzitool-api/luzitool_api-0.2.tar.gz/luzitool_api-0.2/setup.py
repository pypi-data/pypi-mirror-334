from setuptools import setup, find_packages

setup(
    name='luzitool-api',  
    version='0.2',  
    client='1.0.1.56324',  
    owner='t.me/legalbaskan',  
    packages=find_packages(), 
    install_requires=[  
       
        'requests>=2.25.0',  
        'numpy>=1.20.0',  
    ],
    description='luzitool-api Python API Modülü',  
    long_description=open('README.md', encoding='utf-8').read(), 
    long_description_content_type='text/markdown',  
    author='Orvix Games', 
    author_email='toolup@luzitool.ct.ws', 
    url='https://luzitool.ct.ws/python-luzitool.php',  
    classifiers=[  
        'Programming Language :: Python :: 3',  
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',  
        'Intended Audience :: Developers',  
        'Topic :: Software Development :: Libraries :: Python Modules',  
    ],
    python_requires='>=3.6',  
    keywords='luzitool-api, python, api, web, tool',  
    include_package_data=True,  
    zip_safe=False,  
    entry_points={  
        'console_scripts': [
            'luzitool-cli=luzitool.cli:main',  
        ],
    },
    test_suite='tests',  
    tests_require=[  
        'pytest',  
    ],
    extras_require={  
        'dev': ['flake8', 'pytest-cov'],  
        'docs': ['sphinx'],  
    },
    project_urls={  
        'Documentation': 'https://luzitool.ct.ws/docs',
        
    },
    license='MIT',  
)
