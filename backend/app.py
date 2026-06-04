from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

import os
import shutil
import uuid

READY_FOLDER = r"J:\My Drive\avatar_pipeline"

# ==========================
# LOAD ENV
# ==========================
load_dotenv()

# ==========================
# APP
# ==========================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# FOLDERS
# ==========================
os.makedirs("uploads", exist_ok=True)
os.makedirs("temp", exist_ok=True)
os.makedirs(READY_FOLDER, exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

app.mount(
    "/avatar_pipeline",
    StaticFiles(directory=READY_FOLDER),
    name="avatar_pipeline"
)

# ==========================
# HOME
# ==========================
@app.get("/")
def home():

    return {
        "message": "Conversely AI Running"
    }

# ==========================
# GENERATE AVATAR
# ==========================
@app.post("/generate-avatar")
async def generate_avatar(
    image: UploadFile = File(...),
    voice: UploadFile = File(...),
    text: str = Form(...)
):

    try:

        # ==========================
        # UNIQUE ID
        # ==========================
        uid = str(uuid.uuid4())

        # ==========================
        # LOCAL TEMP PATHS
        # ==========================
        raw_image_path = f"uploads/raw_{uid}.jpg"

        voice_sample_path = f"uploads/voice_{uid}.wav"

        script_path = f"temp/script_{uid}.txt"

        # ==========================
        # SAVE IMAGE
        # ==========================
        with open(raw_image_path, "wb") as buffer:

            shutil.copyfileobj(
                image.file,
                buffer
            )

        # ==========================
        # SAVE VOICE SAMPLE
        # ==========================
        with open(voice_sample_path, "wb") as buffer:

            shutil.copyfileobj(
                voice.file,
                buffer
            )

        # ==========================
        # SAVE SCRIPT
        # ==========================
        with open(
            script_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(text)

        # ==========================
        # CREATE JOB FOLDER
        # ==========================
        job_folder = os.path.join(
            READY_FOLDER,
            f"job_{uid}"
        )

        os.makedirs(
            job_folder,
            exist_ok=True
        )

        # ==========================
        # COPY FILES TO JOB
        # ==========================
        shutil.copy(
            raw_image_path,
            f"{job_folder}/image.jpg"
        )

        shutil.copy(
            voice_sample_path,
            f"{job_folder}/voice_sample.wav"
        )

        shutil.copy(
            script_path,
            f"{job_folder}/script.txt"
        )

        # ==========================
        # CREATE STATUS FILE
        # ==========================
        with open(
            f"{job_folder}/status.txt",
            "w"
        ) as f:

            f.write("pending")

        # ==========================
        # RESPONSE
        # ==========================
        return {

            "message":
                "Avatar Job Submitted Successfully",

            "job_id":
                uid,

            "status":
                "pending",

            "image_url":
                f"http://localhost:8000/uploads/{os.path.basename(raw_image_path)}"
        }

    except Exception as e:

        print("ERROR:", e)

        return {
            "error": str(e)
        }
    

@app.get("/job-status/{job_id}")
def job_status(job_id: str):

    try:

        job_folder = os.path.join(
            READY_FOLDER,
            f"job_{job_id}"
        )

        status_file = os.path.join(
            job_folder,
            "status.txt"
        )

        if not os.path.exists(status_file):

            return {
                "error": "Job not found"
            }

        status = open(status_file).read().strip()

        response = {
            "job_id": job_id,
            "status": status
        }

        final_video = os.path.join(
            job_folder,
            "final.mp4"
        )

        if os.path.exists(final_video):

            response["video_url"] = (
            f"http://localhost:8000/avatar_pipeline/job_{job_id}/final.mp4"
            )

        return response

    except Exception as e:

        return {
            "error": str(e)
        }
