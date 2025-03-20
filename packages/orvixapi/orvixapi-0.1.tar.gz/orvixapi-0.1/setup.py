from setuptools import setup, find_packages

setup(
    name='orvixapi', 
    version='0.1', 
    packages=find_packages(), 
    install_requires=[  
        # 'numpy', 'requests' gibi
    ],
    description='Orvix Games Python API Modülü',  
    long_description=open(r'C:\Users\luzih\OneDrive\Desktop\dist\README.md', encoding='utf-8').read(),  
    long_description_content_type='text/markdown',  
    author='Orvix Games',  
    author_email='help@orvixgames.com.tr',  
    url='https://orvixgames.com/python-orvixgames.php',  
    classifiers=[ 
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  
    keywords='orvix, games, python, api', 
    include_package_data=True,  
)











