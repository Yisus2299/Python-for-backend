# 1. Oficial Python image (i chose this one because it's stable)
FROM python:3.11-slim

# 2. Enviroment basic variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Work directory
WORKDIR /app

# 4. Let's copy the requirements from the doc que have
COPY requirements.txt .

# 5. Install all dependencies we need on Python
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 6. copy the rest of the code
COPY . .

# 7. export the port
EXPOSE 8000

# 8. the command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# now, to have an enviroment image with the name we want to we use this line of code:
# docker build -t (the name we want, in my case i used this one: fastapi-store) .

# and, to run it we use this line of code:
# docker run -d -p 8000:8000 --name fastapi-store fastapi-store