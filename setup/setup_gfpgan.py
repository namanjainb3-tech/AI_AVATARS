import os

commands = [
    "cd /workspace && git clone https://github.com/TencentARC/GFPGAN.git",
    "cd /workspace/GFPGAN && pip install basicsr facexlib realesrgan",
    "cd /workspace/GFPGAN && python setup.py develop",
    "cd /workspace/GFPGAN && mkdir -p weights",

    """cd /workspace/GFPGAN && wget -O weights/GFPGANv1.4.pth \
https://github.com/TencentARC/GFPGAN/releases/download/v1.4/GFPGANv1.4.pth""",

    """cd /workspace/GFPGAN && wget -O weights/RealESRGAN_x2plus.pth \
https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth""",

    "pip uninstall -y huggingface_hub",
    "pip install huggingface_hub==0.23.0"
]

for cmd in commands:
    os.system(cmd)

print("✅ GFPGAN Setup Complete")
