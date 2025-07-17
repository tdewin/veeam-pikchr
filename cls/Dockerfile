# Stage 1: Build the C program
FROM alpine:latest AS builder

WORKDIR /build

# Install required tools
RUN apk add --no-cache build-base curl tar make &&\
 curl -L https://pikchr.org/home/tarball/trunk/pikchr.tar.gz | tar xz &&\
 cd pikchr && make pikchr.c && make


# Stage 2: Create a lightweight container with the compiled binary
FROM python:3-alpine


VOLUME /icons
VOLUME /data
VOLUME /fonts

RUN apk add --no-cache librsvg rsvg-convert curl font-ubuntu

# Set working directory
WORKDIR /app

# Copy the compiled binary from the builder stage
COPY --from=builder /build/pikchr/pikchr /app
COPY ./postpikchr.py /app
COPY ./prepikchr.py /app
COPY ./sample.sh /app
COPY ./inline.sh /app

ENV FONT="ubuntu mono"


# Set the entry point
ENTRYPOINT ["/bin/sh"]

#docker build -t veeam-pikchr .


# docker run --rm -it -v .:/data -v ./icons:/icons veeam-pikchr
# ./prepikchr.py --title Test vbr proxy repo -c proxy,repo | ./pikchr --svg-only - | ./postpikchr.py -d /icons -o /data/test.svg

# -or 
# docker run --rm -it -v .:/data -v ./icons:/icons veeam-pikchr
# NAME=/data/test
# ./prepikchr.py --title Test vbr proxy repo -c proxy,repo --filename $NAME.pic
# ./pikchr --svg-only $NAME.pic | ./postpikchr.py -d /icons -o $NAME.svg

# -or inline
# you can modify the stylesheet in the fonts folder
# by default the ubuntu font package is installed
# eg download the ubuntu font from https://fonts.google.com/specimen/Ubuntu+Sans+Mono?query=Ubuntu (you need the latin one)
# notice that /data/test.pic should exist, you can create it with the previous sample, then maintain it outside the container
# docker run --rm -it -v .:/data  -v ./fonts:/fonts -v ./icons:/icons -e FONT="ubuntu mono" -e NAME=veeamfulldemo veeam-pikchr  /app/inline.sh