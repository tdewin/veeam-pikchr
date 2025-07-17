# Build the image

Inside the cls directory
```
docker build -t veeam-pikchr .
```
# Run the container

start
```
docker run --rm -it -v .:/data -v ./icons:/icons veeam-pikchr
```

inside
```
./prepikchr.py --title Test vbr proxy repo -c proxy,repo | ./pikchr --svg-only - | ./postpikchr.py -d /icons -o /data/test.svg
```


# 2 stage 

start
```
docker run --rm -it -v .:/data -v ./icons:/icons veeam-pikchr
```

inside
```
NAME=/data/test
./prepikchr.py --title Test vbr proxy repo -c proxy,repo --filename $NAME.pic
./pikchr --svg-only $NAME.pic | ./postpikchr.py -d /icons -o $NAME.svg
```


# Inline
Notice that /data/test.pic should exist, you can create it with the previous sample, then maintain it outside the container

This way you can automate the process, edit & update with vscode for example
```
docker run --rm -it -v .:/data -v ./icons:/icons -e NAME=test veeam-pikchr  /app/inline.sh
```
