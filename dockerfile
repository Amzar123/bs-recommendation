# Base image python 3.8
FROM python:3.8-alpine

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install PostgreSQL development files (including pg_config)
RUN apk add --no-cache postgresql-dev gcc musl-dev

# Install psycopg2
RUN pip install --no-cache-dir psycopg2-binary

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]