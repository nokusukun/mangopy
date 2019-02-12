ffmpeg -i nichiop.mkv -filter_complex "[0:v] fps=15,scale=w=480:h=-1" -f gif nichiop2.gif
