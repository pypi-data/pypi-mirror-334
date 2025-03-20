from setuptools import setup, find_packages

setup(
    name='ByteLightProject',
    version='2.6',
    packages=find_packages(),
    install_requires=[
        'pyautogui',
        'requests',
        'pyperclip'
    ],
    extras_require={
        "email_support": ["smtplib"],
    },
    author='ByteLightDev',
    author_email='bytelightdevofficial@gmail.com',
    description='ByteLightProject Python Module',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ByteLightDev1/ByteLight',
    classifiers=[  
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
    ],
)
