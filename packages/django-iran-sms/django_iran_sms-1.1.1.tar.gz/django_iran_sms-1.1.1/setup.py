
from setuptools import setup, find_packages

setup(
    name='django-iran-sms',
    version='1.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=5.1.6',
        'djangorestframework==3.15.2',
        'djangorestframework_simplejwt==5.5.0',
        'PyJWT==2.9.0',
        'requests==2.32.3',
    ],
    author='Sobhan Bahman Rashnu',
    author_email='bahmanrashnu@gmail.com',
    description='A Django package for seamless integration with Iranian SMS services like ParsianWebCo and Melipayamak.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://djangoiransms.chelseru.com',
    project_urls={
        "Documentation": "https://github.com/Chelseru/django-iran-sms/",
        "Telegram Group": "https://t.me/bahmanpy",
        "Telegram Channel": "https://t.me/djangoiransms",
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    keywords="djangoiransms djangosms drfsms drfiransms chelseru lor lur bahman rashnu sobhan bahman bahman rashnu melipayamak parsianwebco sms",
)
