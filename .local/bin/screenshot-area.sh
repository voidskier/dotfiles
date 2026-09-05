#!/bin/sh

rm -f /tmp/screenshot.png
flameshot gui -p /tmp/screenshot.png || exit
xclip -selection clipboard -t image/png -i /tmp/screenshot.png
