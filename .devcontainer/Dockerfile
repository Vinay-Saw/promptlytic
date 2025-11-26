FROM mcr.microsoft.com/devcontainers/python:3.11

WORKDIR /workspace

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install playwright==1.40.0 && \
    playwright install --with-deps chromium
