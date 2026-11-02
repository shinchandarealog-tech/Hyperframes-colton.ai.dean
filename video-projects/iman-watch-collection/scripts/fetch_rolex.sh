#!/bin/bash
# Retry Wikimedia thumbnail downloads with backoff (shared IP gets 429s).
cd "$(dirname "$0")/.."
for n in Rolex_Submariner.JPG Rolex-Submariner.jpg Rolex_Submariner_diving_watch.jpg Rolex_Submariner_Professional.JPG Mysub16613x_cropped.jpg; do
  h=$(printf "%s" "$n" | md5sum | cut -c1-32)
  for try in 1 2 3 4; do
    code=$(curl -s -m 30 -A "HyperframesWorkspace/1.0 (video editing)" -o /tmp/rolex.part -w "%{http_code}" "https://upload.wikimedia.org/wikipedia/commons/thumb/${h:0:1}/${h:0:2}/$n/960px-$n")
    if [ "$code" = 200 ] && file /tmp/rolex.part | grep -q JPEG; then mv /tmp/rolex.part assets/photos/rolex.jpg; echo "OK $n"; exit 0; fi
    sleep $((60*try))
  done
done
echo FAIL; exit 1
