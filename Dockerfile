# Use a small Python image
FROM python:3.11-slim

# Set working dir
WORKDIR /app

# Copy everything
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Streamlit port (Render uses $PORT)
EXPOSE 8501

# Start Django (backend) in background, then start Streamlit using Render's $PORT
CMD ["bash", "-c", "\
python manage.py migrate --noinput && \
python manage.py collectstatic --noinput || true && \
python manage.py runserver 0.0.0.0:8000 & \
streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0"]
