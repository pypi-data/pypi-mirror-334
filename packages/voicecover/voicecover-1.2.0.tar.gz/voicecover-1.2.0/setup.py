from setuptools import setup, find_packages

setup(
    name="voicecover",
    version="1.2.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "tensorboardX",
        "fairseq",
        "faiss-cpu",
        "numpy",
        "ffmpeg-python",
        "praat-parselmouth",
        "pyworld",
        "torchcrepe",
        "edge-tts",
        "einops",
        "local-attention",
        "mega.py",
        "wget",
        "gdown",
        "torch",
        "torchaudio",
        "torchvision",
    ],
    include_package_data=True,
)
