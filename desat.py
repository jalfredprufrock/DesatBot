import math
from PIL import Image
import colorsys

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

def convertImage(image, mult):
    im = Image.open(image)
    out = Image.new('RGB', im.size, 0xffffff)
    width, height = im.size
    for x in range(width):
        for y in range(height):
            r,g,b = im.getpixel((x,y))
            rgbNew =convertPixel(mult, [r,g,b])
            rounded = [round(x) for x in rgbNew]
            out.putpixel((x,y), tuple(rounded))
    print("done converting image")
    out.save(image)
    return

def main(image, mult):
    mult = None
    if mult is None : mult= 50
    if(math.isnan(mult)):
        print("multiplier not a number")
        return "error"
    convertImage(image, mult)

if __name__ == "__main__":
    main()