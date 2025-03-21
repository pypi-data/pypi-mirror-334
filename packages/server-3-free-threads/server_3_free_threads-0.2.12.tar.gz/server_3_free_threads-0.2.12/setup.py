from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='server_3_free_threads',
    version='0.2.12',
    author='Vadim Kazakov',
    author_email='skolkovoinovations@gmail.com',
    description='WSGI server based on threads',
    long_description=readme(),
    long_description_content_type='text/markdown',
    # url='your_url',
    packages=find_packages(),
    # install_requires=['python-dotenv==1.0.1',],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
    keywords=['server', 'WSGI'],
    # project_urls={
    #     'GitHub': 'your_github'
    # },
    python_requires='>=3.10'
)
