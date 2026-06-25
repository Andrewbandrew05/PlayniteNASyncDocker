#this lets the installer know that we want the 3.11-slim image. A small image containing whats needed to run python 3.11 and that's about it
FROM python:3.11-slim

#this defines the work directory, leaving as app as its nice and concise and I believe it may be the industry standard for projects just getting started (also easy to change)
WORKDIR /app

#Copy application source code into the image (kind of important)
COPY src/ /app/src/

#lets Docker/Unraid know what port the server will be listening on I think
EXPOSE 8080

# Run the script
CMD ["python", "/app/src/server.py"]