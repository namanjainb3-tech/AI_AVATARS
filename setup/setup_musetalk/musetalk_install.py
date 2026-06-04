import subprocess

commands = [

    "cd /workspace && git clone https://github.com/TMElyralab/MuseTalk.git",

    "pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121",

    """
    pip install
    transformers==4.36.2
    huggingface_hub==0.20.3
    diffusers==0.25.0
    gradio==3.50.2
    accelerate==0.28.0
    omegaconf
    ffmpeg-python
    """,

    "pip install mmengine==0.10.3",

    "pip install mmdet==3.3.0",

    "pip install mmpose==1.3.1",

    "pip install mmcv==2.1.0 -f https://download.openmmlab.com/mmcv/dist/cu121/torch2.1/index.html"
]

for cmd in commands:
    print(f"🚀 {cmd}")
    subprocess.run(cmd, shell=True, check=True)

print("\n✅ MuseTalk installation complete")
