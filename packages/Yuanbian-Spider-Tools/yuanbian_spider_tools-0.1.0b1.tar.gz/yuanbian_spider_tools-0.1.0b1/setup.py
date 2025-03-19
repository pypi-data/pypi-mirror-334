from setuptools import setup, find_packages

setup(
    name='Yuanbian_Spider_Tools',
    version='0.1.0b1',
    packages=find_packages(),
    install_requires=[
        'PyQt5',
        'selenium',
        'webdriver-manager',
        'pyqtwebengine',
    ],
    author='luxp',
    author_email='your_email@example.com',
    description='A spider tools package with custom widgets and browser automation features',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your_username/Yuanbian_Spider_Tools',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires='>=3.12',
)