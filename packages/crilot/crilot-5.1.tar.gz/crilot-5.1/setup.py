from setuptools import setup, find_packages

setup(
    name="crilot",
    version="5.1",
    author="Axmadjon Qaxxorov",
    description="Krill ⬌ Lotin matnlarini oson konvertatsiya qilish uchun Python kutubxonasi!",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/axmadjonqaxxorovc/",
    project_urls={
        "🌐 Taplink": "https://taplink.cc/qaxxorovc",
        "📺 YouTube": "https://youtube.com/@axmadjonqaxxorovc",
        "✈️ Telegram": "https://t.me/axmadjonqaxxorovc",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)