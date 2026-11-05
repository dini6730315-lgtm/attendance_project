
FROM python:3.11-slim

WORKDIR /app

# התקנת Tesseract ו-Poppler עבור OCR וקבצי PDF
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-heb \
    tesseract-ocr-eng \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# התקנת ספריות Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת הפרויקט
COPY . .

CMD ["python", "main.py"]
.venv/
__pycache__/
.git/
.idea/
*.pyc