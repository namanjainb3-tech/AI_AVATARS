import os
import shutil
import subprocess

MUSE_PATH = "/workspace/MuseTalk"

# =====================================
# Rename folders
# =====================================

if os.path.exists(
    f"{MUSE_PATH}/models/sd-vae-ft-mse"
):
    os.rename(
        f"{MUSE_PATH}/models/sd-vae-ft-mse",
        f"{MUSE_PATH}/models/sd-vae"
    )

if os.path.exists(
    f"{MUSE_PATH}/models/musetalk"
):
    os.rename(
        f"{MUSE_PATH}/models/musetalk",
        f"{MUSE_PATH}/models/musetalkV15"
    )

# =====================================
# Create unet.pth
# =====================================

src = (
    f"{MUSE_PATH}/models/musetalkV15/"
    "pytorch_model.bin"
)

dst = (
    f"{MUSE_PATH}/models/musetalkV15/"
    "unet.pth"
)

if os.path.exists(src):
    shutil.copy(src, dst)

# =====================================
# Whisper configs
# =====================================

downloads = [

    (
        "https://huggingface.co/openai/whisper-tiny/resolve/main/config.json",
        "config.json"
    ),

    (
        "https://huggingface.co/openai/whisper-tiny/resolve/main/preprocessor_config.json",
        "preprocessor_config.json"
    ),

    (
        "https://huggingface.co/openai/whisper-tiny/resolve/main/tokenizer_config.json",
        "tokenizer_config.json"
    ),

    (
        "https://huggingface.co/openai/whisper-tiny/resolve/main/vocab.json",
        "vocab.json"
    ),

    (
        "https://huggingface.co/openai/whisper-tiny/resolve/main/merges.txt",
        "merges.txt"
    ),

    (
        "https://huggingface.co/openai/whisper-tiny/resolve/main/pytorch_model.bin",
        "pytorch_model.bin"
    )
]

for url, file_name in downloads:

    subprocess.run(
        f"wget -O {MUSE_PATH}/models/whisper/{file_name} {url}",
        shell=True,
        check=True
    )

# =====================================
# Fix huggingface version
# =====================================

subprocess.run(
    "pip uninstall -y huggingface-hub",
    shell=True
)

subprocess.run(
    "pip install huggingface-hub==0.23.0",
    shell=True
)

print("\n✅ MuseTalk patches complete")
