from setuptools import setup, find_packages

setup(
    name='Genlabs',
    version='0.1.0',
    packages=find_packages(),
    description='GenLabs - Python Client for the GenLabs API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='GenLabsAI',
    author_email='help@genlabs.dev',
    url='https://github.com/genlabsai/genlabspy',  # optional, replace with actual URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Adjust the license as needed
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
