FROM python:3.5
RUN apt-get update && apt-get install -y postgresql

# add this first to be able to cache requirements.
ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common sudo
RUN curl -fsSL https://download.docker.com/linux/$(. /etc/os-release; echo "$ID")/gpg | sudo apt-key add -
RUN lsb_release -csa
RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") \
   $(lsb_release -cs) \
   stable"
RUN apt-get update && apt-get install -y docker-ce
VOLUME /var/run/docker.sock

ADD . /modeling/
WORKDIR /modeling
