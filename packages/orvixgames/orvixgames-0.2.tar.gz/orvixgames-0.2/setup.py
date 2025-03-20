from setuptools import setup, find_packages

setup(
    name='orvixgames',  # Paket adınız
    version='0.2',  # Versiyon numaranız
    packages=find_packages(),  # Bulunan tüm paketleri dahil et
    install_requires=[  # Eğer başka bağımlılıklarınız varsa, buraya yazabilirsiniz
        # 'numpy', 'requests' gibi
    ],
    description='Orvix Games Python API Modülü',  # Modülünüzün kısa açıklaması
    long_description=open(r'C:\Users\luzih\OneDrive\Desktop\dist\README.md', encoding='utf-8').read(),  # Uzun açıklama
    long_description_content_type='text/markdown',  # README dosyanız markdown formatında ise
    author='Orvix Games',  # Yazar adı
    author_email='help@orvixgames.com.tr',  # E-posta adresi
    url='https://orvixgames.com/python-orvixgames.php',  # Projenizin web sitesi veya GitHub adresi
    classifiers=[  # PyPI’de görünmesini sağlayan sınıflandırmalar
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Hangi Python sürümünü desteklediğinizi belirtin
    keywords='orvix, games, python, api',  # Projenizle ilgili anahtar kelimeler
    include_package_data=True,  # Paketle birlikte ekstra dosyaları dahil et
)
