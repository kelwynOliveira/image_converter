
import time
import logging
from pathlib import Path
from enum import Enum

from fastapi import FastAPI, UploadFile, File, Query, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from convert_image import SUPPORTED_FORMATS, convert_image, sanitize_filename, open_file

# Logger
# logger = logging.getLogger("uvicorn")
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("image_converter")

# App FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],
    allow_origins=["http://morfeu.like","http://192.168.1.100:2005"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

OutputFormat = Enum('OutputFormat', {fmt.upper(): fmt for fmt in SUPPORTED_FORMATS.keys()})

@app.post("/convert_image/")
async def convert_image_endpoint(
    file: UploadFile = File(...),
    output_format: OutputFormat = Query(...)
):
    filename = sanitize_filename(file.filename)
    image = open_file(file)

    try:
        converted = convert_image(image, output_format.value)
        data = SUPPORTED_FORMATS.get(output_format.value)
        mime = data["mime"] if data else "application/octet-stream"

        logger.info(f"File recieved: {filename}")
        logger.info(f"Output format: {output_format}")
        logger.info(f"MIME: {mime}")

        base_filename = Path(filename).stem

        return StreamingResponse(
            converted,
            media_type=mime,
            headers={
                "Content-Disposition": f"attachment; filename={base_filename}.{output_format}"
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error with {filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = f"{request.method} {request.url}"
    logger.info(f"🔵 Receiving request: {idem}")

    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000

    logger.info(f"🟢 {idem} finished in {process_time:.2f}ms with status {response.status_code}")
    return response

@app.get("/health")
def health_check():
    return {"status": "ok"}