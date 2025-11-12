# 1️⃣ Use lightweight Python image
FROM python:3.11-slim

# 2️⃣ Prevent Python from buffering logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3️⃣ Set working directory inside container
WORKDIR /app

# 4️⃣ Copy dependency list and install it
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc curl && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 5️⃣ Copy all your code into the container
COPY . /app/

# 6️⃣ Migrate and collect static files for Django
RUN python manage.py migrate --noinput || true
RUN python manage.py collectstatic --noinput || true

# 7️⃣ Expose Django and Streamlit ports
EXPOSE 8000
EXPOSE 8501

# 8️⃣ Start both Django and Streamlit
CMD ["bash", "-c", "gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 & streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0"]
