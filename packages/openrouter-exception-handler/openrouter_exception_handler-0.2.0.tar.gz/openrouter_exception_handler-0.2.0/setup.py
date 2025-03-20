from setuptools import setup, find_packages

setup(
    name='openrouter_exception_handler',
    version='0.2.0',
    packages=find_packages(),
    install_requires=['requests'],
    author='Dannybombastic',
    description='Handler for exceptions in Python with OpenRouter.ai',
    url='https://github.com/tu_usuario/openrouter_exception_handler',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)