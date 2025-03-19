from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='git2string',
    version='0.1.5',
    author='Ashraff Hathibelagal',
    description='A tool to turn a Git repository into an LLM-friendly prompt',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hathibelagal-dev/git2string',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.6',
    install_requires=[
        'tqdm',
        'tiktoken',
        'rich',
        'pathspec',
        'gitpython'
    ],
    entry_points={
        'console_scripts': [
            'git2string=git2string.main:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='ai language-models devtools gpt-4 openai llama mistral gemini chatbot',
    project_urls={
        'Source': 'https://github.com/hathibelagal-dev/git2string',
        'Tracker': 'https://github.com/hathibelagal-dev/git2string/issues',
    },
)