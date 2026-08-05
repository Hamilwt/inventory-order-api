# 1. Use the official, lightweight Python image
FROM python:3.13-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file first (this makes building faster)
COPY requirements.txt .

# 4. Install the Python dependencies inside the container
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code into the container
COPY . .

# 6. Expose the port that Uvicorn will run on
EXPOSE 8000

# 7. The command to start your server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]