import math
from PIL import Image
import colorsys
import requests
from io import BytesIO
import sys
import base64
import os

def convertPixel(mult, rgb):
    r= rgb[0]
    g= rgb[1]
    b= rgb[2]

    if (r == g) & (g == b) : return rgb

    h,s,v = colorsys.rgb_to_hsv(r,g,b)
    
    mult = float(mult)

    s *= (mult/100)
    r,g,b= colorsys.hsv_to_rgb(h,s,v)
    return [r,g,b]

def convertImage(url, mult, isLocal):
    response = None
    img = None
    if not isLocal:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
    else:
        im = Image.open(url)

    out = Image.new('RGB', img.size, 0xffffff)
    width, height = img.size

    for x in range(width):
        for y in range(height):
            r,g,b = img.getpixel((x,y))
            rgbNew = convertPixel(mult, [r,g,b])
            rounded = [round(x) for x in rgbNew]
            out.putpixel((x,y), tuple(rounded))

    print("done converting image")
    if not isLocal:
        return handleImgurPOST(out)
    else:
        out.save(url)
        return

def handleImgurPOST(img):
    client_id = os.environ.get('client_id')
    if client_id is None:
        print("client_id not found in env")
        return None

    postUrl = "https://api.imgur.com/3/image"
    
    headers = {"Authorization": "Client-ID "+client_id}

    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    resp = requests.post(postUrl, headers=headers, data = {'image':img_str})
    

    json = resp.json()

    if 200 == int(json['status']):
        return json['data']['link']
    else:
       print( 'error')

def main(url, mult, isLocal = True):
    if mult is None : mult= 75
    if(math.isnan(int(mult))):
        print("multiplier not a number")
        return "error"
    if isLocal.lower() == "false":
        isLocal = False
    return convertImage(url, mult, isLocal)

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3])
