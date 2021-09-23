FROM python:3.6

# Set the working directory to /app
WORKDIR /Users/svankalas/Desktop/python/dash_app

# Copy the current directory contents into the container at /app
COPY . /Users/svankalas/Desktop/python/dash_app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME dev

# Run app.py when the container launches
CMD ["python", "my_dash.py"]
