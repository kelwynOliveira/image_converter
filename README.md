![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker) ![FastAPI](https://img.shields.io/badge/fastapi-async%20api-green?logo=fastapi)

# 🖼️ Image Converter API

> Fast, lightweight, self-hosted API for image conversion. Built with **FastAPI** and **Pillow**, containerized with Docker.

---

## 🚀 Features

- ✅ Upload an image and convert it to another format.
- ✅ Supports **10+ formats** (JPEG, PNG, WebP, TIFF, BMP, PSD, EPS, ICO, GIF, DDS, etc.).
- ✅ Returns the converted image directly as a download (streamed).
- ✅ Clean API with proper error handling and HTTP status codes.
- ✅ Fully containerized with Docker.
- ✅ CORS enabled (configurable).
- ✅ Healthcheck endpoint for monitoring.

---

## 🔥 Supported Formats

| Extension | MIME Type                 | Pillow Format |
| --------- | ------------------------- | ------------- |
| jpg/jpeg  | image/jpeg                | JPEG          |
| png       | image/png                 | PNG           |
| webp      | image/webp                | WEBP          |
| gif       | image/gif                 | GIF           |
| bmp       | image/bmp                 | BMP           |
| tiff      | image/tiff                | TIFF          |
| ico       | image/vnd.microsoft.icon  | ICO           |
| psd       | image/vnd.adobe.photoshop | PSD           |
| eps       | application/postscript    | EPS           |
| jp2/jpc   | image/jp2                 | JPEG2000      |
| dds       | image/vnd.ms-dds          | DDS           |
| ppm       | image/x-portable-pixmap   | PPM           |
| pgm       | image/x-portable-graymap  | PGM           |
| pbm       | image/x-portable-bitmap   | PBM           |
| pcx       | image/x-pcx               | PCX           |
| tga       | image/x-tga               | TGA           |
| xbm       | image/x-xbitmap           | XBM           |
| xpm       | image/x-xpixmap           | XPM           |

---

## 🐳 Running with Docker

### ✅ Build the image:

```bash
docker build -t image-converter .
```

### ✅ Run the container:

```bash
docker run -d \
  -p 3000:3000 \
  --name image_converter \
  image-converter
```

### 🌐 Access:

```http
http://localhost:3000
```

---

## 🛠️ API Usage

### 🔗 Endpoint

```
POST /convert_image/?output_format={format}
```

### 🧠 Query Parameters

| Name          | Type   | Description                |
| ------------- | ------ | -------------------------- |
| output_format | string | Output format (e.g. `png`) |

### 📤 Form Data

| Name | Type       | Description   |
| ---- | ---------- | ------------- |
| file | UploadFile | Image to send |

### ✅ Example with `curl`

```bash
curl -X POST "http://localhost:3000/convert_image/?output_format=png" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test.jpg" \
  --output converted.png
```

### 🔥 Response

- Returns the image converted to the selected format, directly as a downloadable file.

---

## 🔍 Healthcheck

```http
GET /health
```

**Response:**

```json
{ "status": "ok" }
```

---

## 🧰 Development

### ✅ Install dependencies:

```bash
pip install -r requirements.txt
```

### ✅ Run locally:

```bash
uvicorn main:app --host 0.0.0.0 --port 3000 --reload
```

---

## 🗂️ Project Structure

```
.
├── main.py              # FastAPI app
├── convert_image.py      # Image processing functions
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker image
├── docker-compose.yml    # (optional) Docker compose
└── README.md             # Documentation
```

---

## 🔒 Security Notes

- 🚫 Database or storage is not used. Files are handled **in-memory only**, no persistent storage.
- ✅ No images are saved on the server.
- ✅ Suitable for local, LAN, or private use. For public exposure, add authentication (e.g. API keys, OAuth).
