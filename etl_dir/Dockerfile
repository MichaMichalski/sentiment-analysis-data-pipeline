FROM python:3.6

# Set the working directory to /my_etl
WORKDIR /my_etl

# Copy the requirements file into the container at /my_etl
# (a text files with all the libraries you want to install)
COPY requirements.txt /my_etl
COPY myetl.py /my_etl

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Run myetl.py when the container launches
CMD ["python", "myetl.py"]
