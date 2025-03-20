from setuptools import setup, find_packages

setup(
    name="voicecover",
    version="1.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "tensorboardX",
        "fairseq==0.12.2",
        "faiss-cpu==1.7.3",
        "numpy==1.23.5",
        "ffmpeg-python>=0.2.0",
        "praat-parselmouth>=0.4.2",
        "pyworld==0.3.4",
        "torchcrepe==0.0.23",
        "edge-tts",
        "einops",
        "local-attention",
        "mega.py",        
        "wget",
        "gdown",
        "torch<2.6",
        "torchaudio<2.6",
        "torchvision<0.21"
    ],
    include_package_data=True,
)
