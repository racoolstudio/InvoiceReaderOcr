FROM python:3.10-slim
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /api-ocr
COPY requirements.txt requirements.txt
COPY ./services ./services
COPY ocr_flask.py .
RUN pip install -r requirements.txt
CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "ocr:app"]
EXPOSE 5000