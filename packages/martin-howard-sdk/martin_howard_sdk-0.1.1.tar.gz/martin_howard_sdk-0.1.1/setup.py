from setuptools import setup, find_packages

setup(
    name='martin_howard_sdk',
    version='0.1.1',
    packages=find_packages(),
    description='A brief description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Martin J. Howard',
    author_email='hey@eucon.edu',
    url='https://github.com/yourusername/your_package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11.11',
)
