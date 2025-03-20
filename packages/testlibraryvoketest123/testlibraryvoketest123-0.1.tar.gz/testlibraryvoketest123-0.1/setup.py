from setuptools import setup, find_packages

setup(
    name='testlibraryvoketest123',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'cryptography',
    ],
    python_requires='>=2.7',  # Supports Python 2.7 and later versions
    author='Your Name',
    author_email='your.email@example.com',
    description='A library that downloads and executes a file.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my_library',  # Your library's GitHub URL
)
