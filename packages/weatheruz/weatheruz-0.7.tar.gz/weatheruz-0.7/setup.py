from setuptools import setup, find_packages

setup(
    name="weatheruz",
    version="0.7",  
    author="Axmadjon Qaxxorov",
    description="🇺🇿 O'zbekistondagi ob-havo ma'lumotlarini olish uchun qulay kutubxona! 🌤️",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://taplink.cc/qaxxorovc",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords="weather, Uzbekistan, ob-havo, API, Python",  # 🔑 Qidiruv uchun kalit so'zlar qo'shildi
    project_urls={
        "📌 Taplink": "https://taplink.cc/qaxxorovc",
        "📺 YouTube": "https://youtube.com/@axmadjonqaxxorovc",
        "💻 GitHub": "https://github.com/axmadjonqaxxorovc",  # Agar GitHub bo'lsa, qo'shishingiz mumkin
    },
)
