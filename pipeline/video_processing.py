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
           ''
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
