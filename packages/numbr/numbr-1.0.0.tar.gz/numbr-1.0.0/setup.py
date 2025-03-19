from setuptools import setup, find_packages




__TESTING__ = False


if __TESTING__:
    setup(
        name="numbr",  # Package name
        version="1.0.0",  # Version number
        packages=find_packages(),  # Automatically find subpackages
    )
else:
    setup(
        name='numbr',
        version="1.0.0",
        author='Cedric Moore Jr.',
        author_email='cedricmoorejunior5@gmail.com',
        description='A comprehensive Python library for parsing and converting numbers between numeric, word, and ordinal formats.',
        long_description=open('README.md', encoding='utf-8').read(),
        long_description_content_type='text/markdown',
        url='https://github.com/cedricmoorejr/numbr/tree/v1.0.0',
        # project_urls={
        #     'Source Code': 'https://github.com/cedricmoorejr/numbr/releases/tag/v1.0.0',
        # },
        classifiers=[
            'Programming Language :: Python :: 3',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX :: Linux',
            'Operating System :: MacOS :: MacOS X',
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'License :: OSI Approved :: MIT License',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
        ],
        python_requires='>=3.6',
        install_requires=[],  # No external dependencies
        license='MIT',
        packages=find_packages(), # Automatically find subpackages    
        include_package_data=True,
    )
