# Use an official Python runtime as a parent image
FROM python:latest

# Set the working directory in the container
WORKDIR /usr/src/app


# Install necessary dependencies for Chrome and ChromeDriver
RUN apt-get update && apt-get install -y \ 
    wget \
    unzip \
    libglib2.0-0 \
    gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/ap>
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*
    && wget -O /var/lib/chrome/chrome-linux64.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-f>
    && unzip /var/lib/chrome/chrome-linux64.zip -d /usr/local/bin/
    && chmod +x /usr/local/bin/chrome-linux64/chrome
# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install chromedriver-autoinstaller

# Make port 8090 available to the world outside this container
EXPOSE 8090

# Define environment variable
ENV FLASK_APP=./server/app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=8090"]
