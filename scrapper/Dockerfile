FROM python:3.7

WORKDIR /var/app/scrapper/

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /var/app/scrapper/

# Install any needed packages specified in requirements.txt
RUN pip3.7 install -q -r requirements.txt

# Copy the rest of the application code into the container
COPY . /var/app/scrapper/

RUN chmod +x entrypoint.sh
ENTRYPOINT ["bash", "-c"]
CMD ["/var/app/scrapper/entrypoint.sh"]
