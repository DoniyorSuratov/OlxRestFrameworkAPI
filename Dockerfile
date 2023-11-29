# Use the official Python 3.11 Alpine image
FROM python:3.11-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy the entire content of the local directory to the container
COPY . .

# Ensure Unix line endings and make the entrypoint script executable
RUN sed -i 's/\r$//g' /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh

# Install Python dependencies from requirements.txt
RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip pip install -r requirements.txt
#pip install -r /app/requirements.txtproduct_type__

# Set the entrypoint for the container
ENTRYPOINT ["/app/entrypoint.sh"]
