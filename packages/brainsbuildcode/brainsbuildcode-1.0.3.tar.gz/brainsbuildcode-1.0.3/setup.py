from setuptools import setup, find_packages

setup(
    name='brainsbuildcode',
    version='1.0.3',
    author='Mohammad.R.AbuAyyash',
    author_email='brainbuildai@gmail.com',
    description='A machine learning pipeline for preprocessing, model selection, and evaluation.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/achelousace/brainsbuildcode',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'IPython',
        'scikit-learn',
        'xgboost',
        'tqdm',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
    ],
    python_requires='>=3.6',
)
