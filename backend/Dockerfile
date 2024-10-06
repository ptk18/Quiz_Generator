# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set working directory
WORKDIR /backend

# Copy requirements file
COPY ./requirements.txt /backend/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . /backend

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
