FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py utm_to_lat_lon_converter.py .
EXPOSE 7860
CMD ["python", "app.py"]
