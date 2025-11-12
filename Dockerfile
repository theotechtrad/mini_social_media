# Use a small Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Render-assigned port
EXPOSE 10000

# Start Streamlit as the main app and run Django in the background
CMD ["bash", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000 & streamlit run streamlit_app.py --server.port=10000 --server.address=0.0.0.0"]
