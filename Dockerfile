FROM ubuntu
RUN mkdir /app
WORKDIR /app
RUN apt-get update && apt-get install libvips-dev python3-pip -y
RUN pip3 install matplotlib astropy pyvips
