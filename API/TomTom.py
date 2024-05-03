import requests, os, math, argparse #web requests and accessing env vars and math for calc        -- reduce os to single function to save space 
from PIL import Image               #PIL is Pillow - image handling library for python
from io import BytesIO              #io.BytesIO used for image bytecode handling
from string import Template         #Template is used for editing the editable URL env var
from dotenv import load_dotenv      #loads env file

#extracts img from given html
def extract_IMG (html):
    #make request
    res = requests.get(html)
    
    #if OK then get img
    if res.status_code == 200:
        image = Image.open(BytesIO(res.content))
        image = image.convert("RGB")
        image.show()

        #make filepath via html link after converting all `/` to `_`
        html = html.replace("/", "_")
        fp = f"./API/Images/{html[html.find('map') + 4 : html.find('?')]}"

        #if filepath DNE then create it
        if not os.path.exists(os.path.dirname(fp)):
            os.makedirs(os.path.dirname(fp))
        
        image.save(fp)
        
    else:
        raise ValueError(f"Improper connection to TomTom. See code: {res.status_code}")

    return

#defines bounds for conversions
def boundChecker (latitude, longitude, zoom, style, verbose):
    if verbose:
        print("Checking bounds...\n")

    if (latitude < -85.051128779807) or (latitude > 85.051128779806):
        raise ValueError("Improper Latitude given. -85.051128779807 < Latitude < 85.051128779806")
    
    if (longitude < -180) or (longitude > 180):
        raise ValueError("Improper Longitude given. -180 < Longitude < 180")
    
    #maximum zoom changes based off of map style:
    #See: (https://developer.tomtom.com/map-display-api/documentation/zoom-levels-and-tile-grid)
    #   Map tiles has 23 zoom levels, numbered 0 through 22.
    #   Satellite tiles has 20 zoom levels, numbered 0 through 19.
    #   Hillshade tiles has 14 zoom levels, numbered 0 through 13.
        
    zoomMax = -1

    if style == "traffic":
        zoomMax = 22
    elif style == "sat":
        zoomMax = 19
    elif style == "hill":
        zoomMax = 13

    if (zoomMax == -1):
        raise ValueError("Improper Style given. Style can be any of the following: \'traffic\', \'sat\', \'hill\'")
    else:
        if (zoom < 0) or (zoom > zoomMax):
            raise ValueError(f"Improper Zoom Level given. 0 < Zoom Level < {zoomMax}")

    if verbose:
        print("Bounds are Valid\n")

    return True

#typecheks latitude, longitude, zoom, and style
def typeChecker (latitude, longitude, zoom, style, verbose):
    if verbose:
        print("Checking Types of Inputs...\n")

    #assert types of inputs: float, float, int, string
    #returns index of input that caused error. 0 o/w
    try:
        float(latitude)
    except:
        return 1
        
    try:
        float(longitude)
    except:
        return 2
    
    try:
        int(zoom)
    except:
        return 3
    
    try: 
        str(style)
    except:
        return 4

    if verbose:
        print("Types are Valid\n")

    return 0        

#function to convert latitude/longitude & zoom to x, y coords
#eg.    dict('x' : VALUE, 'y' : VALUE, 'zoom' : VALUE)
#provided by TomTom and converted to Python
def convertLatLonZ (latitude, longitude, zoom, style, verbose):
    if verbose:
        print("Calculating Map Position...\n")
    
    #basic type checking
    res = typeChecker(latitude, longitude, zoom, style, verbose)
    if (res == 0):
        #typing OK
        latitude = float(latitude)
        longitude = float(longitude)
        zoom = int(zoom)

        #if bounds are correct then utilize formula
        if boundChecker(latitude, longitude, zoom, style, verbose):
            x = math.floor((longitude + 180) / 360 * pow(2, zoom))
            y = math.floor((1 - math.log(math.tan(latitude * math.pi / 180) + 1 / math.cos(latitude * math.pi / 180)) / math.pi) / 2 * pow(2, zoom))

            if verbose:
                print("Map Positions Calculated.\n")

            #dictionary with keys for each calculated value (x, y) and zoom
            return {
                "x" : x,
                "y" : y,                
                "zoom" : zoom
            }
    else:
        #error on type: 
        #   1 == latitude
        #   2 == longitude
        #   3 == zoom
        #   4 == style
        if (res == 1):
            raise TypeError("Given Latitude is not a decimal")
        elif (res == 2):
            raise TypeError("Given Latitude is not a decimal")
        elif (res == 3):
            raise TypeError("Given Zoom Level is not an integer")
        elif (res == 4):
            raise TypeError("Given Style is not a string")
        else:
            raise ValueError("UNEXPECTED ERROR -- CHECK CODE")

#calculates the height of a pixel given RGB
#height will be be in the following units: meters above sea level
def heightCalc (R, G, B):
    #formula from TOMTOM
    #See: https://developer.tomtom.com/map-display-api/documentation/raster/hillshade-tile
    height = -10000 + ((R * 256 * 256 + G * 256 + B) * 0.1)
    
    return height

#runs all tests for various portions of the code
def runTests (verbose):
    ################################################################################################################
    # Test 1:
    #           sample url img retrieval

    if verbose:
        print("Test 1: Obtaining Traffic Data for Sample URL\n")

    #extract image on sample URL
    extract_IMG(os.environ['SAMPLE_URL'])

    ################################################################################################################
    # Test 2:
    #           get template URL and modify it for img retrieval.  this should match the sample URL

    if verbose:
        print("Test 2: Obtaining Traffic Data using Template URL.\nThis image should match the Sample URL\n")

    #get the editable url from env and use template for modification
    TRAFFIC_URL_Template = Template(os.environ['TRAFFIC_URL'])

    #modify template (we are matching the sampleURL manually)
    TRAFFIC_URL = TRAFFIC_URL_Template.substitute(zoom = 12, style = "flow", x = 2044, y = 1360, thickness = 10, tileSize = 512)

    extract_IMG(TRAFFIC_URL)

    ################################################################################################################
    # Test 3:
    #           get template URL and modify it for img retrieval. this location was arbitrarily selected for testing

    if verbose:
        print("Test 3: Obtaining Traffic Data using Template URL.\nThis location was arbitrarily selected for testing\n")

    TRAFFIC_URL = TRAFFIC_URL_Template.substitute(zoom = 12, style = "flow", x = 702, y = 1635, thickness = 10, tileSize = 512)

    extract_IMG(TRAFFIC_URL)

    ################################################################################################################
    # Test 4:
    #            use lat/long conversion then insert to URL for img retrieval for Traffic Data

    if verbose:
        print("Test 4: Utilizing Latitude/Longitude Conversion alongside Template URL.\nThis should be an image of traffic in LA.\n")

    #now we will show an image of LA

    res = convertLatLonZ("34.098907", "-118.327759", "10", "traffic", False)
    #print(res.keys())

    TRAFFIC_URL = TRAFFIC_URL_Template.substitute(zoom = res['zoom'], style = "flow", x = res['x'], y = res['y'], thickness = 10, tileSize = 512)
    #print(TRAFFIC_URL)

    extract_IMG(TRAFFIC_URL)

    #See here for google maps vision of this map:
    #https://www.google.com/maps/d/u/0/viewer?mid=1JrNQOeGSrrvpQrYhLYgJfeCt7so&hl=en&ll=34.060222254822%2C-118.35919115297678&z=11

    ###############################################################################################################
    # Test 5:
    #            get hillshade & satellite images so we can look at 3D data on top of traffic data. we will use the same location & zoom from Test 4

    if verbose:
        print("Test 5: Obtaining HillShade image followed by Satellite image using Template URL.\nThese images are of LA.\n")

    TOPOGRAPHICAL_URL_Template = Template(os.environ['TOPOGRAPHICAL_URL'])

    # hillshade
    #ONLY PNGs for hillshade

    res = convertLatLonZ("34.098907", "-118.327759", "10", "hill", False)
    TOPOGRAPHICAL_URL = TOPOGRAPHICAL_URL_Template.substitute(zoom = res['zoom'], style = "hill", x = res['x'], y = res['y'], format = "png")
    extract_IMG(TOPOGRAPHICAL_URL)

    #calculate height from single pixel for this image we obtained
    #...

    # satellite
    #ONLY JPG for satellite

    res = convertLatLonZ("34.098907", "-118.327759", "10", "sat", False)
    TOPOGRAPHICAL_URL = TOPOGRAPHICAL_URL_Template.substitute(zoom = res['zoom'], style = "sat", x = res['x'], y = res['y'], format = "jpg")
    extract_IMG(TOPOGRAPHICAL_URL)

    if verbose:
        print("\n\n")

    return

#main program
def main():
    parser = argparse.ArgumentParser()

    #arguments:
    #       latitude
    #       longitude
    #       zoom
    #       style
    #       demo            - used for running tests
    #       verbose         - prints during each stage of program

    parser.add_argument('lat', type = float, help = 'Latitude. -85.051128779807 < Latitude < 85.051128779806')
    parser.add_argument('lon', type = float, help = 'Longitude. -180 < Longitude < 180')
    parser.add_argument('zoom', type = int, help = 'Zoom. Zoom level depends on \'style\' selected.\nTraffic: 0 < Zoom < 22\nSat(ellite): 0 < Zoom < 19\nHill(shade): 0 < Zoom < 13')
    parser.add_argument('style', choices = ["traffic", "sat", "hill"], type = str, help = 'Style of Image to obtain. Any of: \'traffic\', \'sat\', \'hill\'')
    parser.add_argument('--demo', action = 'store_true', help = 'If True, runs 5 Tests before using the given values for the program')
    parser.add_argument('--verbose', action = 'store_true', help = 'If True, explicitly states what the program is doing at each step')

    #parse arguments given
    args = parser.parse_args()

    #loads the env file ".env"
    load_dotenv()

    #run Tests
    if args.demo:
        if args.verbose:
            print("Running Tests...\n\n")
        runTests(args.verbose)

    #convert to x,y,z from lat,lon,z
    res = convertLatLonZ(args.lat, args.lon, args.zoom, args.style, args.verbose)

    #start getting image from TOMTOM
    if args.style == "traffic":
        #get TemplateURL
        TRAFFIC_URL_Template = Template(os.environ['TRAFFIC_URL'])

        #substitute
        TRAFFIC_URL = TRAFFIC_URL_Template.substitute(zoom = res['zoom'], style = "flow", x = res['x'], y = res['y'], thickness = 10, tileSize = 512)

        if args.verbose:
            print("Obtaining Image From TomTom...")

        #extract image
        extract_IMG(TRAFFIC_URL)

    else:
        #get TemplateURL
        TOPOGRAPHICAL_URL_Template = Template(os.environ['TOPOGRAPHICAL_URL'])

        #determine img format
        if args.style == "hill":
            imgFormat = 'png'
        else:
            imgFormat = 'jpg'

        #substitute
        TOPOGRAPHICAL_URL = TOPOGRAPHICAL_URL_Template.substitute(zoom = res['zoom'], style = args.style, x = res['x'], y = res['y'], format = imgFormat)

        #extract image
        extract_IMG(TOPOGRAPHICAL_URL)

    if args.verbose:
        print("Image Obtained!")

    return

################################################################################################################
#                       Notes
        
#zoom 1 is basically the whole world

#zoom 6 shows interstates
#zoom 7 shows interstates with names

#zoom 8 shows more freeways besides the interstates
#zoom 9 shows the entirety of LA with major freeways

#zoom 11 shows major streets
#zoom 12 shows the the names of major streets

#zoom 14 is the maximum zoom available for all views

                            #####################################################

#we access the env vars with os.environ['VAR_NAME']

#print(os.environ['TOMTOMKEY'])
#print(os.environ['SAMPLE_URL'])
#print(os.environ['TRAFFIC_URL'])
#print(os.environ['TOPOGRAPHICAL_URL'])

################################################################################################################

#runner of the program
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        raise e