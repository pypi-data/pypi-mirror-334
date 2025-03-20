
from setuptools import setup, find_packages

setup(
    name='django-iran-sms',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=5.1.6',
        'djangorestframework==3.15.2',
        'djangorestframework_simplejwt==5.5.0',
        'asgiref==3.8.1',
        'certifi==2025.1.31',
        'charset-normalizer==3.4.1',
        'idna==3.10',
        'packaging==24.2',
        'PyJWT==2.9.0',
        'pyproject_hooks==1.2.0',
        'requests==2.32.3',
        'sqlparse==0.5.3',
        'typing_extensions==4.12.2',
        'urllib3==2.3.0',
    ],
    author='Bahman Rashnu',
    author_email='bahmanrashnu@gmail.com',
    description='Connection with Iranian SMS services for user authentication or sending messages.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/chelseru/drf-iran-sms',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12.3',
)
