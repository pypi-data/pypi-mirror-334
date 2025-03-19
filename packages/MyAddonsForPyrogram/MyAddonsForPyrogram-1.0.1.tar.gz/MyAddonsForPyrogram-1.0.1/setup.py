from setuptools import find_packages, setup


setup(
    name="MyAddonsForPyrogram",
    version="1.0.1",
    description="A simple addon for pyrogram to manage database, broadcast users, send THANKS FOR JOINING msg to new users who has joined through the bot nd to send reaction through bot.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Pʀɪᴍᴇ Hʀɪᴛᴜ",
    packages=find_packages(),
    install_requires=[
        "pymongo==4.11.2",
        "Pyrogram==2.0.106",
        "Requests==2.32.3",
        "TgCrypto==1.2.3",
    ],
    project_urls={"GitHub": "https://github.com/Prime-Hritu/MyAddonsForPyrogram"},
)
