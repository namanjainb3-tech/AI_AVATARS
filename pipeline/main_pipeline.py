import os
import time
import shutil
import glob
import requests
import base64
import cv2

BASE_FOLDER = "/content/drive/MyDrive/avatar_pipeline"

FISHSPEECH_URL = YOUR_FISHSPEECH_URL
SEEDVC_URL = YOUR_SEEDVC_URL
CODEFORMER_URL = YOUR_CODEFORMER_URL

print("FishSpeech:", FISHSPEECH_URL)
print("SeedVC:", SEEDVC_URL)
print("CodeFormer:", CODEFORMER_URL)

print("======= Conversely AI =======")
print("MASTER AVATAR WORKER STARTED")


# =========================================================
# ALIGN_FACE + ENHANCE_FACE
# =========================================================
from insightface.app import FaceAnalysis

app = FaceAnalysis(
    name='buffalo_l',
    providers=['CUDAExecutionProvider', 'CPUExecutionProvider']
)

app.prepare(
    ctx_id=0,
    det_size=(640, 640)
)

print("✅ InsightFace Loaded")

def align_face(input_path, output_path):

    img = cv2.imread(input_path)
    if img is None:
      raise Exception(f"Could not load image: {input_path}")

    faces = app.get(img)

    if len(faces) == 0:
        raise Exception("No face detected")

    # largest face
    face = sorted(
        faces,
        key=lambda x: x.bbox[2] * x.bbox[3],
        reverse=True
    )[0]

    bbox = face.bbox.astype(int)

    x1, y1, x2, y2 = bbox

    # padding
    pad = 220

    h, w, _ = img.shape

    x1 = max(0, x1 - pad)
    y1 = max(0, y1 - pad)
    x2 = min(w, x2 + pad)
    y2 = min(h, y2 + pad)

    cropped = img[y1:y2, x1:x2]

    cropped = cv2.resize(cropped, (768, 768))

    cv2.imwrite(output_path, cropped)

    print("✅ Face aligned:", output_path)



def enhance_face(input_path, output_path):

    os.chdir("/content/GFPGAN")

    # clear old results
    shutil.rmtree(
        "/content/GFPGAN/results",
        ignore_errors=True
    )

    os.makedirs(
        "/content/GFPGAN/results",
        exist_ok=True
    )

    # run GFPGAN
    os.system(
        f'''
        python inference_gfpgan.py \
        -i "{input_path}" \
        -o results \
        -v 1.4 \
        -s 2 \
        --bg_upsampler realesrgan
        '''
    )

    restored = glob.glob(
        "/content/GFPGAN/results/restored_imgs/*"
    )

    print("\n===== GFPGAN OUTPUTS =====")
    print(restored)

    if len(restored) == 0:
        raise Exception("GFPGAN failed")

    latest = max(
        restored,
        key=os.path.getctime
    )

    shutil.copy(
        latest,
        output_path
    )

    print("✅ Face enhanced:", output_path)

# =========================================================
# FISHSPEECH GENERATION
# =========================================================
def generate_voice_fishspeech(
    script_text,
    reference_audio,
    reference_text,
    output_path
):

    with open(reference_audio, "rb") as f:

        audio_base64 = base64.b64encode(
            f.read()
        ).decode("utf-8")

    payload = {
        "text": script_text,
        "references": [
            {
                "audio": audio_base64,
                "text": reference_text
            }
        ],
        "format": "wav"
    }

    response = requests.post(
      f"{FISHSPEECH_URL}/v1/tts",
      json=payload,
      timeout=600
    )

    if response.status_code != 200:

        raise Exception(
            f"FishSpeech failed: {response.text}"
        )

    with open(output_path, "wb") as f:

        f.write(response.content)

    print("✅ FishSpeech voice generated")


# =========================================================
# SEEDVC PLACEHOLDER
# =========================================================
def enhance_voice_seedvc(
    generated_audio,
    reference_audio,
    output_path
):

    print("🚀 Sending audio to SeedVC...")

    files = {
        "source_audio": open(
            generated_audio,
            "rb"
        ),
        "reference_audio": open(
            reference_audio,
            "rb"
        )
    }

    response = requests.post(
        f"{SEEDVC_URL}/convert",
        files=files,
        timeout=1800
    )

    if response.status_code != 200:

        raise Exception(
            f"SeedVC failed: {response.text}"
        )

    with open(output_path, "wb") as f:

        f.write(response.content)

    print("✅ SeedVC enhancement complete")

# =========================================================
# CODEFORMER_ENHANCEMENT
# =========================================================

def enhance_video_codeformer(
    input_video,
    output_video
):

    print("🚀 Sending video to CodeFormer...")

    files = {
        "video": open(
            input_video,
            "rb"
        )
    }

    response = requests.post(
        f"{CODEFORMER_URL}/enhance",
        files=files,
        timeout=3600
    )

    if response.status_code != 200:

        raise Exception(
            f"CodeFormer failed: {response.text}"
        )

    with open(output_video, "wb") as f:

        f.write(response.content)

    print("✅ CodeFormer enhancement complete")


# =========================================================
# MASTER LOOP
# =========================================================
while True:

    jobs = os.listdir(BASE_FOLDER)

    for job_id in jobs:

        job_path = os.path.join(
            BASE_FOLDER,
            job_id
        )

        if not os.path.isdir(job_path):
            continue

        status_file = os.path.join(
            job_path,
            "status.txt"
        )

        if not os.path.exists(status_file):
            continue

        status = open(
            status_file
        ).read().strip()

        # =====================================================
        # WAITING JOBS
        # =====================================================
        if status == "pending":

            try:

                print(f"\n🎬 Processing: {job_id}")

                # =====================================================
                # FILES
                # =====================================================
                image_path = os.path.join(
                    job_path,
                    "image.jpg"
                )

                script_path = os.path.join(
                    job_path,
                    "script.txt"
                )

                voice_sample_path = os.path.join(
                    job_path,
                    "voice_sample.wav"
                )

                # =====================================================
                # VALIDATION
                # =====================================================
                if not os.path.exists(image_path):

                    raise Exception(
                        "image.jpg missing"
                    )

                if not os.path.exists(script_path):

                    raise Exception(
                        "script.txt missing"
                    )

                if not os.path.exists(
                    voice_sample_path
                ):

                    raise Exception(
                        "voice_sample.wav missing"
                    )

                # =====================================================
                # READ SCRIPT
                # =====================================================
                with open(script_path, "r") as f:

                    script_text = f.read().strip()

                # =====================================================
                # VOICE CLONING
                # =====================================================
                with open(status_file, "w") as f:

                    f.write("voice_cloning")

                generated_audio = os.path.join(
                    job_path,
                    "generated_voice.wav"
                )

                generate_voice_fishspeech(
                    script_text=script_text,
                    reference_audio=voice_sample_path,
                    reference_text="sample voice",
                    output_path=generated_audio
                )

                # =====================================================
                # SEEDVC ENHANCEMENT
                # =====================================================
                with open(status_file, "w") as f:

                    f.write("voice_enhancing")

                enhanced_audio = os.path.join(
                    job_path,
                    "enhanced_voice.wav"
                )

                enhance_voice_seedvc(
                    generated_audio,
                    voice_sample_path,
                    enhanced_audio
                )

                # =====================================================
                # FACE ENHANCEMENT
                # =====================================================
                with open(status_file, "w") as f:

                    f.write("enhancing_face")

                print("🚀 Enhancing face...")

                aligned_image = os.path.join(
                    job_path,
                    "aligned_face.jpg"
                )

                align_face(
                    image_path,
                    aligned_image
                )

                enhanced_image = os.path.join(
                    job_path,
                    "enhanced_face.jpg"
                )

                enhance_face(
                    aligned_image,
                    enhanced_image
                )

                print("✅ Face enhancement done")

                # =====================================================
                # LIVEPORTRAIT
                # =====================================================
                with open(status_file, "w") as f:

                    f.write(
                        "liveportrait_processing"
                    )

                print("🚀 Running LivePortrait...")

                os.chdir("/content/LivePortrait")

                shutil.rmtree(
                    "/content/LivePortrait/animations",
                    ignore_errors=True
                )

                os.makedirs(
                    "/content/LivePortrait/animations",
                    exist_ok=True
                )

                exit_code = os.system(
                    f'''
                    python inference.py \
                    --source "{enhanced_image}" \
                    --driving assets/examples/driving/driving_1.mp4
                    '''
                )

                if exit_code != 0:

                    raise Exception(
                        "LivePortrait command failed"
                    )

                generated_videos = glob.glob(
                    "/content/LivePortrait/animations/*--driving_1.mp4"
                )

                if len(generated_videos) == 0:

                    raise Exception(
                        "LivePortrait failed"
                    )

                latest_video = max(
                    generated_videos,
                    key=os.path.getctime
                )

                liveportrait_output = os.path.join(
                    job_path,
                    "liveportrait.mp4"
                )

                shutil.copy(
                    latest_video,
                    liveportrait_output
                )

                print("✅ LivePortrait Done")

                # =====================================================
                # MUSETALK
                # =====================================================
                with open(status_file, "w") as f:

                    f.write(
                        "musetalk_processing"
                    )

                print("🚀 Running MuseTalk...")

                os.chdir("/content/MuseTalk")

                shutil.rmtree(
                    "/content/MuseTalk/results/test",
                    ignore_errors=True
                )

                os.makedirs(
                    "/content/MuseTalk/results/test",
                    exist_ok=True
                )

                os.makedirs(
                    "/content/MuseTalk/data/audio",
                    exist_ok=True
                )

                converted_audio = (
                    "/content/MuseTalk/data/audio/processed.wav"
                )

                os.system(
                    f'''
                    ffmpeg -y -i "{enhanced_audio}" \
                    -ar 16000 -ac 1 "{converted_audio}"
                    '''
                )

                yaml_content = f"""
                task_0:
                  video_path: "{liveportrait_output}"
                  audio_path: "{converted_audio}"
                """

                with open(
                    "/content/MuseTalk/configs/inference/test.yaml",
                    "w"
                ) as f:

                    f.write(yaml_content)

                print(yaml_content)

                exit_code = os.system(
                    '''
                    python -m scripts.inference \
                    --inference_config configs/inference/test.yaml \
                    --result_dir results/test \
                    --unet_model_path ./models/musetalkV15/unet.pth \
                    --unet_config ./models/musetalkV15/musetalk.json \
                    --version v15
                    '''
                )

                if exit_code != 0:

                    raise Exception(
                        "MuseTalk command failed"
                    )

                musetalk_outputs = glob.glob(
                    "/content/MuseTalk/results/**/*.mp4",
                    recursive=True
                )

                if len(musetalk_outputs) == 0:

                    raise Exception(
                        "MuseTalk failed"
                    )

                mp4_outputs = [
                    x for x in musetalk_outputs
                    if x.endswith(".mp4")
                ]

                final_video = max(
                    mp4_outputs,
                    key=os.path.getctime
                )

                raw_video_path = os.path.join(
                    job_path,
                    "raw_musetalk.mp4"
                )

                shutil.copy(
                    final_video,
                    raw_video_path
                )

                with open(status_file, "w") as f:

                    f.write(
                        "codeformer_processing"
                    )

                enhanced_final_video = os.path.join(
                    job_path,
                    "final.mp4"
                )

                enhance_video_codeformer(
                    raw_video_path,
                    enhanced_final_video
                )

                with open(status_file, "w") as f:

                    f.write(
                        "rendering"
                    )

                print("✅ Final video saved")

                # =====================================================
                # COMPLETE
                # =====================================================
                with open(status_file, "w") as f:

                    f.write("completed")

                print(
                    f"\n🔥 FULL PIPELINE DONE: {job_id}"
                )

            except Exception as e:

                print("\n❌ ERROR:", str(e))

                with open(status_file, "w") as f:

                    f.write("failed")

    time.sleep(10)
