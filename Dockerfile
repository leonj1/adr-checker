# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required packages
RUN pip install --no-cache-dir requests

# Run the script when the container launches
ENTRYPOINT ["python", "list_gitlab_mrs.py"]

# Set the project as a command argument (this will be overridden by docker run command)
CMD ["gitlab-org/gitlab"]

# Set the GITLAB_ACCESS_TOKEN as an environment variable
# This will be overwritten when running the container if provided
ENV GITLAB_ACCESS_TOKEN=""
