# todo
# Use an official Python runtime as a parent image
FROM python:latest

# Set the working directory inside the container
WORKDIR /server

# Copy the requirements.txt first (to install dependencies efficiently)
COPY ./demo/server/requirements.txt /server/

# Install dependencies
RUN pip install --no-cache-dir -r /server/requirements.txt

# Copy the rest of the server files to /server
COPY ./demo/server /server/

# Expose port 5000 for Flask
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask app when the container launches
# CMD ["flask", "run"]
CMD ["python", "app.py"]
