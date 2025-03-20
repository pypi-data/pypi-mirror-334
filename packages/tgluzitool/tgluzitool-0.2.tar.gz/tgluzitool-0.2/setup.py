from setuptools import setup, find_packages

setup(
    name='tgluzitool',  
    version='0.2',  
    packages=find_packages(),  # Paketlerin bulunduğu klasörü bul
    install_requires=[
        'requests>=2.25.0',  # İhtiyaç duyulan kütüphaneler
        'numpy>=1.20.0',
    ],
    description='luzitool-api Python API Modülü',  
    long_description=open('README.md', encoding='utf-8').read(), 
    long_description_content_type='text/markdown',  
    author='Luzi inc', 
    author_email='toolup@luzitool.ct.ws', 
    url='https://luzitool.ct.ws/python-luzitool.php',  
    classifiers=[
        'Programming Language :: Python :: 3',  # Python 3 için
        'License :: OSI Approved :: MIT License',  # MIT lisansı
        'Operating System :: OS Independent',  # Platform bağımsız
    ],
    python_requires='>=3.6',  # Python 3.6 ve üzeri
    entry_points={  
        'console_scripts': [
            'luzitool-cli=tgluzitool.cli:main',  # Komut satırı arayüzü
        ],
    },
    include_package_data=True,  # Package verisi dahil et
    zip_safe=False,  # Güvenli zipleme
)
