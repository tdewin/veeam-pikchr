NAME=/data/veeamdiagram
./prepikchr.py --title Test vbr proxy repo -c proxy,repo --filename $NAME.pic
./pikchr --svg-only $NAME.pic | ./postpikchr.py -d /icons -o $NAME.svg