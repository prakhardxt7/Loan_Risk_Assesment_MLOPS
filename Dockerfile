# Use an official Python image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the main application files to the container
COPY main.py /app/
COPY prediction_model /app/prediction_model
COPY tests /app/tests

# Copy the requirements file to the container
COPY requirements.txt /app/

# Install necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that FastAPI will run on
EXPOSE 8000

# Start the FastAPI app using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
