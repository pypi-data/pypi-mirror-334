from setuptools import setup, find_packages

setup(
    name='Yuanbian_Spider_Tools',
    version='0.1.1b1',
    packages=["spider88_test"],
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'PyQt5',
        'selenium',
        'webdriver-manager',
        'pyqtwebengine',
    ],
    author='luxp',
    author_email='luxp4588@gmail.com',
    description='A spider tools package with custom widgets and browser automation features',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/luxp4588/Yuanbian_Spider_Tools',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.8',
)