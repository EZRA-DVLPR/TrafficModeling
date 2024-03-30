import requests, os, math                 #web requests and accessing env vars and math for calc        -- reduce os to single function to save space 
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
        image.show()
    else:
        print(res.status_code)

    return

#defines bounds for conversions
def boundChecker (latitude, longitude, zoom):
    if (latitude < -85.051128779807) or (latitude > 85.051128779806):
        raise ValueError("Improper Latitude given. 0 < Latitude < 22")
    
    if (longitude < -180) or (longitude > 180):
        raise ValueError("Improper Longitude given. 0 < Longitude < 22")
    
    if (zoom < 0) or (zoom > 22):
        raise ValueError("Improper Zoom Level given. 0 < Zoom Level < 22")

    return True

#typecheks latitude, longitude, and zoom
def typeChecker (latitude, longitude, zoom):
    #assert types of inputs: float, float, int
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

    return 0        

#function to convert latitude/longitude & zoom to x, y coords
#eg.    dict('x' : VALUE, 'y' : VALUE, 'zoom' : VALUE)
#provided by TomTom and converted to Python
def convertLatLonZ (latitude, longitude, zoom):
    #basic type checking
    res = typeChecker(latitude, longitude, zoom)
    if (res == 0):
        #typing OK
        latitude = float(latitude)
        longitude = float(longitude)
        zoom = int(zoom)

        #if bounds are correct then utilize formula
        if boundChecker(latitude, longitude, zoom):
            x = math.floor((longitude + 180) / 360 * pow(2, zoom))
            y = math.floor((1 - math.log(math.tan(latitude * math.pi / 180) + 1 / math.cos(latitude * math.pi / 180)) / math.pi) / 2 * pow(2, zoom))

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
        if (res == 1):
            raise TypeError("Given Latitude is not a decimal")
        elif (res == 2):
            raise TypeError("Given Latitude is not a decimal")
        elif (res == 3):
            raise TypeError("Given Zoom Level is not an integer")
        else:
            raise ValueError("UNEXPECTED ERROR -- CHECK CODE")

################################################################################################################
#                       Notes
        
#zoom 1 is basically the whole world

#zoom 6 shows interstates
#zoom 7 shows interstates with names

#zoom 8 shows more freeways besides the interstates
#zoom 9 shows the entirety of LA with major freeways

#zoom 11 shows major streets
#zoom 12 shows the the names of major streets

################################################################################################################

#loads the env file ".env"
load_dotenv()

'''
we access the env vars with os.environ['VAR_NAME']

print(os.environ['TOMTOMKEY'])
print(os.environ['SAMPLE_URL'])
print(os.environ['EDITABLE_URL'])
'''

################################################################################################################
# Test 1:
#           sample url img retrieval

#extract image on sample URL
extract_IMG(os.environ['SAMPLE_URL'])

################################################################################################################
# Test 2:
#           get template URL and modify it for img retrieval.  this should match the sample URL

#get the editable url from env and use template for modification
mod_URL_Template = Template(os.environ['EDITABLE_URL'])

#modify template (we are matching the sampleURL manually)
mod_URL = mod_URL_Template.substitute(zoom = 12, x = 2044, y = 1360, thickness = 10, tileSize = 512)
print(mod_URL)

extract_IMG(mod_URL)

################################################################################################################
# Test 3:
#           get template URL and modify it for img retrieval. this location was arbitrarily selected for testing

mod_URL = mod_URL_Template.substitute(zoom = 12, x = 702, y = 1635, thickness = 10, tileSize = 512)
print(mod_URL)

extract_IMG(mod_URL)

################################################################################################################
# Test 4:
#            use lat/long conversion then insert to URL for img retrieval

#now we will show an image of LA

res = convertLatLonZ("34.098907", "-118.327759", "10")
print(res.keys())

mod_URL = mod_URL_Template.substitute(zoom = res['zoom'], x = res['x'], y = res['y'], thickness = 10, tileSize = 512)
print(mod_URL)

extract_IMG(mod_URL)

#See here for google maps vision of this map:
#https://www.google.com/maps/d/u/0/viewer?mid=1JrNQOeGSrrvpQrYhLYgJfeCt7so&hl=en&ll=34.060222254822%2C-118.35919115297678&z=11

################################################################################################################
# Test 5:
#            get hillshade & satellite images so we can look at 3D data on top of traffic data. we will use the same location from Test 4

# hillshade
# see: https://developer.tomtom.com/map-display-api/documentation/raster/hillshade-tile

# satellite
# see: https://developer.tomtom.com/map-display-api/documentation/raster/satellite-tile