import requests, os                 #web requests and accessing env vars        -- reduce os to single function to save space
from PIL import Image               #PIL is Pillow - image handling library for python
from io import BytesIO              #io.BytesIO used for image bytecode handling
from string import Template         #Template is used for editing the editable URL env var
from dotenv import load_dotenv      #loads env file

#extracts img from given html
def extract_IMG (html):
    res = requests.get(html)
    
    #if ok then get img
    if res.status_code == 200:
        image = Image.open(BytesIO(res.content))
        #show img
        image.show()
    else:
        print(res.status_code)

#loads the env file ".env"
load_dotenv()

'''
we access the env vars with os.environ['VAR_NAME']

print(os.environ['TOMTOMKEY'])
print(os.environ['SAMPLE_URL'])
print(os.environ['EDITABLE_URL'])
'''

#extract image on sample URL
extract_IMG(os.environ['SAMPLE_URL'])

#get the editable url from env and use template for modification
mod_URL_Template = Template(os.environ['EDITABLE_URL'])

#modify template (we are matching the sampleURL manually)
mod_URL = mod_URL_Template.substitute(zoom=12, x = 2044, y = 1360, thickness = 10, tileSize = 512)
print(mod_URL)

extract_IMG(mod_URL)