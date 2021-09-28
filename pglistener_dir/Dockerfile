FROM python:3.6

# Set the working directory to /app
WORKDIR /listener

# Copy the requirements file into the container at /app
# (a text files with all the libraries you want to install)
COPY requirements.txt /listener
COPY listener.py /listener

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run app.py when the container launches
CMD ["python", "listener.py"]