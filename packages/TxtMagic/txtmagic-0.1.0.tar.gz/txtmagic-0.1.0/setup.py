from setuptools import setup, find_packages

setup(
    name="TxtMagic",
    version="0.1.0",
    author="Pooja V",
    author_email="poojavelm@gmail.com",
    description="A Python package for adding style, emojis, and colors to your text effortlessly! 🎨✨",
    long_description="TxtMagic is a Python package designed to add magic to your text! With TextMagic, you can easily transform your text into colorful, emoji-filled, and stylized formats. ",
    long_description_content_type="text/markdown",
    url="https://github.com/Pooja-Velmurugen",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',  # Fixed typo here
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.0',
)