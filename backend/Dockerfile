# Stage 1: Build the application
FROM python:3.12 AS builder

RUN python -m venv /venv

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY backend_requirements.txt .

# Install the dependencies
RUN /venv/bin/pip install -r backend_requirements.txt


# Stage 2: Run the application
FROM python:3.12-slim

# Set the working directory
WORKDIR /app
# Copy the application code
COPY . .

# Copy the dependencies from the builder stage
COPY --from=builder /venv/ /venv/
COPY --from=builder /app /app

# Add the virtual environment to the path
ENV PATH="/venv/bin:$PATH"

ENV PYTHONPATH=/app

RUN apt update && apt install libpq5 -y

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["fastapi", "run", "main.py"]