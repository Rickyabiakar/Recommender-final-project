FROM python:3.10-slim

WORKDIR /app

COPY . .

# ✅ Add required build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# ✅ Upgrade pip & install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ✅ Set PYTHONPATH so src/ is importable
ENV PYTHONPATH="/app"

CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
