FROM python:3.6

# Set the working directory to /app
WORKDIR /notifier

# Copy the requirements file into the container at /app
# (a text files with all the libraries you want to install)
COPY requirements.txt /notifier
COPY notifier.py /notifier

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run app.py when the container launches
CMD ["python", "notifier.py"]