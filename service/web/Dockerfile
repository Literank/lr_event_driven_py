# Use Alpine Linux with Python 3 as base image
FROM python:3.12.3-alpine3.19

RUN apk add --no-cache gcc libc-dev librdkafka-dev

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY service/ /app/service

CMD ["uvicorn", "service.web.main:app", "--host", "0.0.0.0", "--port", "8000"]

