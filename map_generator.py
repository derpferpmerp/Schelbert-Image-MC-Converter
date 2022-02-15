from staticmap import StaticMap, CircleMarker
import argparse

parser = argparse.ArgumentParser(
	description='Generate Real-World Map'
)

parser.add_argument(
	'-lo',
	'--long',
	dest="longitude",
	type=float,
	help='Longitude of Center of Map',
	default=-87.687697
)

parser.add_argument(
	'-la',
	'--lat',
	dest="latitude",
	type=float,
	help='Latitude of Center of Map',
	default=42.045072
)

parser.add_argument(
	'--width',
	dest="width",
	default=1000,
	help='Pixel Width of the Map',
)

parser.add_argument(
	'--height',
	dest="height",
	default=1000,
	help='Pixel Height of the Map',
)

parser.add_argument(
	'-z',
	'--zoom',
	dest="zoom",
	default=10,
	help='Amount to Zoom for Map',
)

args = parser.parse_args()

def generateMap(width=None, height=None, COORD=None, ZOOM=None, outfile=None):
	if width is None: width = args.width
	if height is None: height = args.height
	if COORD is None: COORD = ( args.longitude, args.latitude )
	if ZOOM is None: ZOOM = args.zoom
	if outfile is None: outfile = "map.png"

	map_instance = StaticMap(width, height)
	marker = CircleMarker(COORD, 'blue', 0.1)
	map_instance.add_marker(marker)
	
	image = map_instance.render(zoom=ZOOM)
	image.save(outfile)

if __name__ == "__main__":
	generateMap()