import subprocess

commands = [

    "apt -y install -qq aria2",

    "mkdir -p /workspace/MuseTalk/models/dwpose",
    "mkdir -p /workspace/MuseTalk/models/face-parse-bisent",
    "mkdir -p /workspace/MuseTalk/models/musetalk",
    "mkdir -p /workspace/MuseTalk/models/sd-vae-ft-mse",
    "mkdir -p /workspace/MuseTalk/models/whisper",
    "mkdir -p /workspace/MuseTalk/models/syncnet",

    # DWPose
    "aria2c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/MuseTalk/resolve/main/dwpose/dw-ll_ucoco.pth -d /workspace/MuseTalk/models/dwpose -o dw-ll_ucoco.pth",

    "aria2c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/MuseTalk/resolve/main/dwpose/dw-ll_ucoco_384.onnx -d /workspace/MuseTalk/models/dwpose -o dw-ll_ucoco_384.onnx",

    "aria2c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/MuseTalk/resolve/main/dwpose/yolox_l.onnx -d /workspace/MuseTalk/models/dwpose -o yolox_l.onnx",

    # Face Parse
    "aria2c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/MuseTalk/resolve/main/face-parse-bisent/79999_iter.pth -d /workspace/MuseTalk/models/face-parse-bisent -o 79999_iter.pth",

    "aria2c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/MuseTalk/resolve/main/face-parse-bisent/resnet18-5c106cde.pth -d /workspace/MuseTalk/models/face-parse-bisent -o resnet18-5c106cde.pth",

    # MuseTalk
    "aria2c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/MuseTalk/raw/main/musetalk/musetalk.json -d /workspace/MuseTalk/models/musetalk -o musetalk.json",

    "aria2c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/MuseTalk/resolve/main/musetalk/pytorch_model.bin -d /workspace/MuseTalk/models/musetalk -o pytorch_model.bin",

    # SD VAE
    "aria2c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/MuseTalk/raw/main/sd-vae-ft-mse/config.json -d /workspace/MuseTalk/models/sd-vae-ft-mse -o config.json",

    "aria2c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/MuseTalk/resolve/main/sd-vae-ft-mse/diffusion_pytorch_model.bin -d /workspace/MuseTalk/models/sd-vae-ft-mse -o diffusion_pytorch_model.bin",

    # Whisper
    "aria2c -x 16 -s 16 -k 1M https://huggingface.co/camenduru/MuseTalk/resolve/main/whisper/tiny.pt -d /workspace/MuseTalk/models/whisper -o tiny.pt",

    # SyncNet
    "wget -O /workspace/MuseTalk/models/syncnet/syncnet.pth https://github.com/camenduru/MuseTalk-colab/releases/download/models/syncnet.pth"
]

for cmd in commands:
    print(f'🚀 {cmd}')
    subprocess.run(cmd, shell=True, check=True)

print('\n✅ MuseTalk weights downloaded')
