import os

commands=[
    "cd /workspace",

    "git clone https://github.com/sczhou/CodeFormer.git",

    "cd CodeFormer",

    "pip install -r requirements.txt",

    "python basicsr/setup.py develop",

    "mkdir -p weights/CodeFormer",

    "wget -O weights/CodeFormer/codeformer.pth \
    https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth",

    "apt update",

    "apt install -y ffmpeg",
]

for cmd in commands:
    os.system(cmd)

print("CodeFormer setup complete")
