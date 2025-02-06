## Use this to mount a drive
##  arguments
##    [1]: drive symbol (letter)

sudo mount -t drvfs ${1^}: /mnt/${1,}
