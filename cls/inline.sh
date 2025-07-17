echo "Building from /data/$NAME.pic"
./pikchr --svg-only "/data/$NAME.pic" | ./postpikchr.py -f "$FONT" -d /icons -o "/data/$NAME.svg"

echo "Converting to png /data/$NAME.png /data/$NAME.svg"
rsvg-convert  --stylesheet "/fonts/font.css"  -o "/data/$NAME.png" "/data/$NAME.svg"