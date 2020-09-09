from setuptools import setup, find_packages


setup(
    name='delegated',
    version="1.0",
    author="timjolson",
    author_email="timjolson@users.noreply.github.com",
    description="Utility to quickly delegate methods and attributes to subordinate objects.",
    url="https://github.com/timjolson/delegated",
    packages=find_packages(),
    tests_require=['pytest'],
)


# with open("README.md", "r") as fh:
#     long_description = fh.read()
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
#     classifiers=[
#         "Programming Language :: Python :: 3",
#         "License :: OSI Approved :: MIT License",
#         "Operating System :: OS Independent",
#     ],
#     python_requires='>=3.6',
# )
