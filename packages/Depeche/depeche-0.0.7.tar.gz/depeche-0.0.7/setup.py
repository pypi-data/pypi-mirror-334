if __name__ == "__main__":
    from setuptools import setup, find_packages

    setup(
        name='Depeche',
        version='0.0.7',
        packages=find_packages(),
        install_requires=[],
        author='Jan Lerking',
        author_email='',
        description='A simple message pipeline.',
        long_description=open('README.md').read(),
        long_description_content_type='text/markdown',
        url='https://gitea.com/Lerking/depeche',
        classifiers=[
                    'Programming Language :: Python :: 3',
                    'License :: OSI Approved :: MIT License',
                    'Operating System :: OS Independent',
                    ],
        python_requires='>=3.12',
    )