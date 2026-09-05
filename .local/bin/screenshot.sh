#!/bin/sh

rm -f /tmp/screenshot.png
flameshot full -p /tmp/screenshot.png || exit
xclip -selection clipboard -t image/png -i /tmp/screenshot.png
