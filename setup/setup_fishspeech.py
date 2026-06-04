import os

commands=[
    "cd /workspace",

    "git clone -b v1.5.0 https://github.com/fishaudio/fish-speech.git",

    "cd /workspace/fish-speech",

    "pip install -U pip setuptools wheel",

    "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121",

    "pip install -e .",

    "pip install \
    transformers==4.46.3 \
    huggingface_hub==0.26.2 \
    lightning \
    pytorch-lightning \
    pyrootutils \
    ormsgpack",

    "apt update && apt install git-lfs -y",

    "git lfs install",

    "mkdir -p /workspace/fish-speech/checkpoints",
  
    "cd /workspace/fish-speech/checkpoints",

    "git clone https://huggingface.co/fishaudio/fish-speech-1.5",

    "cd /workspace/fish-speech",

    "pip install hydra-core pytorch-lightning lightning \
    transformers==4.41.2 huggingface_hub==0.23.2 \
    pyrootutils loguru rich librosa soundfile \
    einops einx vector-quantize-pytorch \
    loralib ormsgpack funasr kui natsort uvicorn cachetools tiktoken",

    "pip install git+https://github.com/descriptinc/audiotools",

    "pip install descript-audio-codec",

    "python -m tools.api_server \
      --listen 0.0.0.0:7860 \
      --llama-checkpoint-path /workspace/fish-speech/checkpoints/fish-speech-1.5 \
      --decoder-checkpoint-path /workspace/fish-speech/checkpoints/fish-speech-1.5/firefly-gan-vq-fsq-8x1024-21hz-generator.pth"
]

for cmd in commands:
    os.system(cmd)

print("FishSpeech setup complete")
