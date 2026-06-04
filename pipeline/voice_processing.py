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
