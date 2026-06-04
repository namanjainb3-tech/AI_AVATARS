import os

commands=[  
    "cd /workspace",
    "git clone https://github.com/Plachtaa/seed-vc.git",
    "cd seed-vc",

    "pip install -U pip",
    "pip install torch torchaudio torchvision",
    "pip install gradio librosa soundfile transformers diffusers accelerate sentencepiece",
    "pip install praat-parselmouth pyworld resemblyzer ffmpeg-python",
    "pip install numpy scipy einops munch",

    "apt update",
    "apt install ffmpeg -y",

    "mkdir -p checkpoints",
    "cd checkpoints",
    "wget https://huggingface.co/Plachta/Seed-VC/resolve/main/DiT_seed_v2_uvit_whisper_small_wavenet_bigvgan_pruned.pth",

    "cd /workspace/seed-vc",

    "GRADIO_SERVER_NAME=0.0.0.0 GRADIO_SERVER_PORT=7862 python app.py --enable-v1",
]

for cmd in commands:
    os.system(cmd)

print("SeedVC setup complete")
