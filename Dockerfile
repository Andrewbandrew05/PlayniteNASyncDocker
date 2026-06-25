FROM python:3.11-slim

WORKDIR /app

# Copy application source code into the image
COPY src/ /app/src/

# Expose the default internal port
EXPOSE 8080

# Run the script
CMD ["python", "/app/src/server.py"]