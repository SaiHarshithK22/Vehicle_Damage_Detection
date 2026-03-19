from fastapi import FastAPI, File, UploadFile
from model_helper import predict
import tempfile
import os

app = FastAPI()


@app.post("/finding")
async def get_prediction(file: UploadFile = File(...)):
    tmp_path = None
    try:
        image_bytes = await file.read()

        # Preserve the original file extension to avoid format mismatches
        suffix = os.path.splitext(file.filename)[-1] if file.filename else ".jpg"

        # Write to a unique temp file to avoid race conditions with concurrent requests
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(image_bytes)
            tmp_path = tmp.name

        prediction = predict(tmp_path)
        return {"prediction": prediction}

    except Exception as e:
        return {"error": str(e)}

    finally:
        # Always clean up the temp file
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)