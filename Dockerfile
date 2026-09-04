FROM python:3.12-slim

# Pillow's placeholder-avatar rendering falls back to a bundled font if none
# of these are present, but installing one keeps entry cards looking right.
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render (and most PaaS hosts) inject PORT; main.py reads it via config.py
# and binds the health server there. 8080 is just the local/default value.
ENV PORT=8080
EXPOSE 8080

CMD ["python", "main.py"]
