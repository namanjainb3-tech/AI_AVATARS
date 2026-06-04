import os

commands = [

    "cd /workspace",

    "git clone https://github.com/KwaiVGI/LivePortrait.git",

    "cd LivePortrait",

    "pip install -r requirements.txt",

    "pip install -U huggingface_hub[cli]",

    "pip uninstall -y torch torchvision torchaudio",

    "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121",

    "mkdir -p pretrained_weights",

    "huggingface-cli download KwaiVGI/LivePortrait \
      --local-dir ./pretrained_weights",

    "hf download KwaiVGI/LivePortrait \
      --local-dir pretrained_weights"
]

for cmd in commands:
    os.system(cmd)

print("LivePortrait setup complete")
