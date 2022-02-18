# Schelbert-Image-MC-Converter

This script can generate a google map thumbnail<br>
given coordinates, and then can convert that image<br>
into an array suitable for Minecraft Education Edition...

```java
usage: map_generator.py [-h] [-lo LONGITUDE] [-la LATITUDE] [--width WIDTH] [--height HEIGHT] [-z ZOOM]

Generate Real-World Map

optional arguments:
  -h, --help            show this help message and exit
  -lo LONGITUDE, --long LONGITUDE
                        Longitude of Center of Map
  -la LATITUDE, --lat LATITUDE
                        Latitude of Center of Map
  --width WIDTH         Pixel Width of the Map
  --height HEIGHT       Pixel Height of the Map
  -z ZOOM, --zoom ZOOM  Amount to Zoom for Map
```

```java
usage: generate_blackmap.py [-h] [-u URL | -f INFILE] [-v] [-n]

Generate MC Conversion

optional arguments:
  -h, --help       show this help message and exit
  -u URL           Supply the URL for the Image
  -f INFILE        Supply the Input File for the Image
  -v, --verbose    add verbose cli
  -n, --showNames  show names in the render
```
