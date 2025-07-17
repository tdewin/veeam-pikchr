NAME=/data/veeamdiagram
FONT="ubuntu mono"
./veeamdiagram.py vbr proxy repo -c proxy,repo --filename $NAME.prepic
./prepikchr.py --title Test -o $NAME.pic -i $NAME.prepic
./pikchr --svg-only $NAME.pic | ./postpikchr.py -f "$FONT" -d /icons -o $NAME.svg
rsvg-convert  -o $NAME.png $NAME.svg