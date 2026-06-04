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
