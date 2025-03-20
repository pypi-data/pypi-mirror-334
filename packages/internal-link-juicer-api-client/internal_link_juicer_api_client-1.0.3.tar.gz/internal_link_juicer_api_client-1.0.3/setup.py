from setuptools import setup, find_packages
import os

setup(
    name='internal_link_juicer_api_client',  # Lowercase, underscores
    version='1.0.3',
    author='Onur Gürpınar',
    author_email='onurgurpinar@gmail.com',
    description='An Unofficial Python client for the Internal Link Juicer WordPress plugin API.',
    long_description=open('README.md').read() if os.path.exists('README.md') else "",
    long_description_content_type='text/markdown',
    url='https://github.com/onur222/internal-link-juicer-api-client',  # Replace!
    packages=find_packages(),
    install_requires=[
        'requests',
        'phpserialize',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.7',
     project_urls={
        'Bug Reports': 'https://github.com/onur222/internal-link-juicer-api-client/issues',
        'Source': 'https://github.com/onur222/internal-link-juicer-api-client',
    },
)