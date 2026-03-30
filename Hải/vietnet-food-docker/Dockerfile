# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for sqlite3 and basic tools
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project code and the XML data
COPY . .

# Expose the port Streamlit runs on
# EXPOSE 8501

# # Run the application
# ENTRYPOINT ["streamlit", "run", "wordnet_browser.py", "--server.port=8501", "--server.address=0.0.0.0"]
RUN pip freeze
EXPOSE 86
ENTRYPOINT ["streamlit", "run", "wordnet_browser.py", "--server.port=86", "--server.address=0.0.0.0"]