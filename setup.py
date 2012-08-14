from setuptools import setup

README = open('README').read()

setup(
        name='gists',
        packages=['gists'],
        version='1.0-beta',
        author='Jaume Devesa',
        author_email='jaumedevesa@gmail.com',
        url='http://github.com/jdevesa/gists',
        description='CLI interface for manage Github gists',
        install_requires=['requests', 'clint'],
        scripts=['gists/gists'],
        classifiers=[
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Development Status :: 4 - Beta ",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Operating System :: POSIX :: Linux"
            ]
)
