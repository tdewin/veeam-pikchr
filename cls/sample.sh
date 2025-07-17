NAME=/data/veeamdiagram
FONT="ubuntu mono"
./prepikchr.py --title Test vbr proxy repo -c proxy,repo --filename $NAME.pic
./pikchr --svg-only $NAME.pic | ./postpikchr.py -f "$FONT" -d /icons -o $NAME.svg
rsvg-convert  -o $NAME.png $NAME.svg