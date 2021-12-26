import base64
import io
import subprocess

from PIL import Image


class Icon:
    def __init__(self, exe_path):
        self.exe_path = exe_path
        self.img_pil = self.get_pil_img()
        self.dominant_color = self.dominant_color()

    def get_pil_img(self) -> Image:
        img_base64 = subprocess.run(['powershell', '-executionpolicy', 'bypass', './icons.ps1', '-ExePath', rf'"{self.exe_path}"'], capture_output=True).stdout
        img_bytes = base64.decodebytes(img_base64)
        img_file_object = io.BytesIO(img_bytes)
        img_pil = Image.open(img_file_object)

        return img_pil

    def get_dominant_color(self) -> str:
        img_copy = self.img_pil.copy()
        pixels = img_copy.getcolors(2 ** 16)
        # remove transparent (a = 0) and black (sum(r, g, b) < 45) and white (sum(r, g, b) < 720) pixels
        pixels = [i for i in pixels if i[1][3] != 0 and 45 < sum(i[1][0:3]) < 720]
        dominant_rgb = max(pixels, key=lambda i: i[0])[1][0:3]
        dominant_hex = '%02x%02x%02x' % dominant_rgb
        
        return dominant_hex
