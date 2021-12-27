# Python imports
import io

import clr
from PIL import Image

# .NET runtime imports
clr.AddReference('System.Drawing')
clr.AddReference('System.IO')

from System.Drawing import Icon as net_Icon
from System.Drawing import Imaging
from System.Drawing import Size
from System.IO import MemoryStream


class Icon:
    def __init__(self, exe_path):
        self.exe_path = exe_path
        self.img_pil = self.get_pil_img()
        self.dominant_color = self.get_dominant_color()

    def get_pil_img(self) -> Image:
        img_bmp = net_Icon(net_Icon.ExtractAssociatedIcon(self.exe_path), Size(64, 64)).ToBitmap()
        mem_stream = MemoryStream()

        img_bmp.Save(mem_stream, Imaging.ImageFormat.Png)
        img_bytes = bytearray(mem_stream.ToArray())
        mem_stream.Flush()
        mem_stream.Dispose()

        img_file_object = io.BytesIO(img_bytes)
        img_pil = Image.open(img_file_object)

        return img_pil

    def get_dominant_color(self) -> str:
        img_copy = self.img_pil.copy()
        img_compressed = img_copy.quantize(colors=8, kmeans=3).convert('RGBA')
        pixels = img_compressed.getcolors(8)
        # remove transparent (a = 0) and almost black (sum(r, g, b) < 45) and white (sum(r, g, b) < 720) pixels
        pixels = [i for i in pixels if i[1][3] != 0 and 45 < sum(i[1][0:3]) < 720]
        dominant_rgb = max(pixels, key=lambda i: i[0])[1][0:3]
        dominant_hex = '#' + '%02x%02x%02x' % dominant_rgb

        return dominant_hex
