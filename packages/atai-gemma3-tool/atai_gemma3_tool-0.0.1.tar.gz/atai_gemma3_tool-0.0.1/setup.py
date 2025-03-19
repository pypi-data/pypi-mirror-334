from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='atai-gemma3-tool',
    version='0.0.1',
    description='CLI tool for generating text from images using the Gemma 3 model.',
    author='AtomGradient',
    author_email="alex@atomgradient.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AtomGradient/atai-gemma3-tool",
    packages=find_packages(),
    install_requires=[
        "transformers@git+https://github.com/huggingface/transformers@v4.49.0-Gemma-3",
        "torch",
        "accelerate",
        "Pillow",
    ],
    entry_points={
        'console_scripts': [
            'atai-gemma3-tool=atai_gemma3_tool:main',
        ],
    },
)