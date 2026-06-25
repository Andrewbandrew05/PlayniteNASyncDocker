#this lets the installer know that we want the 3.11-slim image. A small image containing whats needed to run python 3.11 and that's about it
FROM python:3.11-slim

#this defines the work directory, leaving as app as its nice and concise and I believe it may be the industry standard for projects just getting started (also easy to change)
WORKDIR /app

# Install NiceGUI and its essential encryption dependencies for session management
RUN pip install --no-cache-dir nicegui cryptography
#install rsync
RUN apt-get update && apt-get install -y rsync && rm -rf /var/lib/apt/lists/*
#install samba for the internal network share
RUN apt-get update && apt-get install -y samba rsync supervisor

# Copy supervisor to right location
COPY /src/Supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

#copy samba setup script to right place
COPY /src/SambaSetup/setup_samba.sh /app/src/SambaSetup/setup_samba.sh

#Copy Python code into app
COPY src/Python /app/src/Python

#copy actual samba conf file
COPY /src/SambaSetup/smb.conf /etc/samba/smb.conf

#make setup_samba.sh executable
RUN chmod +x /app/src/SambaSetup/setup_samba.sh

#lets Docker/Unraid know what port the server will be listening on I think
#(web port)
EXPOSE 8080
#(socket server port)
EXPOSE 8081

#samba ports
EXPOSE 445 139 137/udp 138/udp

# Run the script
CMD ["/usr/bin/supervisord"]