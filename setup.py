from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='delegated',
    version="0.1",
    author="timjolson",
    author_email="timjolson@users.noreply.github.com",
    description="Utility to quickly delegate attributes to subordinate objects via proxy (property).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='proxy delegate attribute',
    url="https://github.com/timjolson/delegated",
    license='GPLv3',
    packages=find_packages(),
    tests_require=['pytest'],
    python_requires='>=3.7',
    classifiers=[  # https://pypi.org/classifiers/
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)


# https://packaging.python.org/guides/distributing-packages-using-setuptools/
#
# setup(
#     name="example-pkg-YOUR-USERNAME-HERE", # Replace with your own username
#     version="0.0.1",
#     author="Example Author",
#     author_email="author@example.com",
#     description="A small example package",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/pypa/sampleproject",
#     packages=find_packages(),
#     python_requires='>=3.6',
#     classifiers=[
#           # How mature is this project? Common values are
#           #   3 - Alpha
#           #   4 - Beta
#           #   5 - Production/Stable
#           'Development Status :: 3 - Alpha',
#
#           # Indicate who your project is intended for
#           'Intended Audience :: Developers',
#           'Topic :: Software Development :: Build Tools',
#
#           # Pick your license as you wish (should match "license" above)
#           'License :: OSI Approved :: MIT License',
#
#           # Specify the Python versions you support here. In particular, ensure
#           # that you indicate whether you support Python 2, Python 3 or both.
#           'Programming Language :: Python :: 2',
#           'Programming Language :: Python :: 2.6',
#           'Programming Language :: Python :: 2.7',
#           'Programming Language :: Python :: 3',
#           'Programming Language :: Python :: 3.2',
#           'Programming Language :: Python :: 3.3',
#           'Programming Language :: Python :: 3.4',
#           ],
#           entry_points={
#               'console_scripts': [
#                   'sample=sample:main',
#               ],
#           },
# )
