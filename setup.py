import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iago",
    version="0.1",
    author="Lorenzo Coacci",
    author_email="lorenzo@coacci.com",
    description="The package contains your python assistant for Speech Recognition and Text to Speech ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lollococce/iago",
    packages=setuptools.find_packages(),
    keywords='',
    license='MIT',
    include_package_data=True,
    install_requires=[
       'pandas',
       'playsound',
       'pyttsx3',
       'speech_recognition',
       'termcolor',
       'traceback'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
    ]
)