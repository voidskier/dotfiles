# Session
export XDG_SESSION_TYPE=x11
export GDK_BACKEND=x11
export QT_QPA_PLATFORM=xcb
export ELECTRON_OZONE_PLATFORM_HINT=x11

systemctl --user import-environment DISPLAY ${XAUTHORITY+XAUTHORITY}
dbus-update-activation-environment DISPLAY XAUTHORITY

# Variables
export XCURSOR_THEME=voidskier-cursor
export XCURSOR_SIZE=32
export GTK_THEME=BlackAndWhite
export GTK_APPLICATION_PREFER_DARK_THEME=1
export QT_QPA_PLATFORMTHEME=gtk3

# Software
picom &                     # Launch compositor
plank &                     # Launch launcher
polybar &                   # Launch panel
pcmanfm --desktop &         # Launch desktop
~/.local/bin/clock.py &     # Launch clock

# Set background
feh --bg-scale ~/Pictures/background.png

# Launch window manager
exec openbox-session
