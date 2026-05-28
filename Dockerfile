# 1. THE BASE: We start with a microscopic version of Linux that already has Python installed. (Alpine Linux is only ~5 megabytes!)
FROM python:3.9-alpine

# 2. THE WORKSPACE: We tell Docker to create a folder called /app inside the container and stand inside it.
WORKDIR /app

# 3. THE CODE: We copy your three files from your Ubuntu server into the container's /app folder.
COPY engine.py baseline.json live-state.json ./

# 4. THE INSTRUCTION: We tell the container what to do the moment it turns on.
CMD ["python", "engine.py"]
