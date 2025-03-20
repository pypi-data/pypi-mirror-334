import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='xcs-rc',
    version='1.3.1',
    license='Free for non-commercial use',
    author='Nugroho Fredivianus',
    author_email='nuggfr@gmail.com',
    description='Accuracy-based Learning Classifier Systems with Rule Combining',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(include=['xcs_rc']),
    keywords='machine learning, reinforcement learning, classifier systems, rule-based',
    package_data={'': ['LICENSE.txt']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Operating System :: OS Independent",
        "License :: Free for non-commercial use",
    ],
)
