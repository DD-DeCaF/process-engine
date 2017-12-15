FROM python:3.5
RUN apt-get update && apt-get install -y postgresql

# add this first to be able to cache requirements.
ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

ADD . /modeling/
WORKDIR /modeling
