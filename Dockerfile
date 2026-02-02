# 1. Start with a lightweight version of Python 3.12
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

# 2. Set the "Home" directory inside the container
WORKDIR /app

# 3. Copy our requirements first (this helps Docker cache for speed)
COPY requirements.txt .

# 4. Install the libraries
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of our code
COPY . .

# 6. Create the data folder so the container can save history
RUN mkdir -p data

# 7. The command to run when the container starts
CMD ["python", "monitor.py"]