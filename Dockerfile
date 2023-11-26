# Use the official Python 3.11 Alpine image
FROM python:3.11-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the entire content of the local directory to the container
COPY . .

# Ensure Unix line endings and make the entrypoint script executable
RUN sed -i 's/\r$//g' /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh
RUN apk add --no-cache docker-compose
# Install Python dependencies from requirements.txt
RUN pip install -r /app/requirements.txt

# Set the entrypoint for the container
ENTRYPOINT ["/app/entrypoint.sh"]
