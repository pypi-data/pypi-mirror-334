# -*- coding: utf-8 -*-
# @Author: maoyongfan
# @email: maoyongfan@163.com
# @Date: 2025/3/17 13:28
from pybaselib.interfaces.imgs.img import Img
from pybaselib.utils.imgs.img import ImgFactory
from pybaselib.utils import IntType


class RGBImg(ImgFactory, Img):
    def __init__(self, img_path: str):
        super().__init__(img_path)
        self.img_size_byte = self.get_img_size()

    def get_img_size(self):
        return (self.width * self.height) * 3

    def rgb_to_hex(self):
        if self.img_type != "color24bit":
            self.base_img = self.base_img.convert("RGB")
            self.update_img_type()
        # print(self.base_img.mode)
        # print(self.img_type)
        rgb_pixels = list(self.base_img.getdata())
        hex_pixels = []
        for r, g, b in rgb_pixels:
            hex_pixel = f"{r:02x}{g:02x}{b:02x}"  # 将每个颜色值转换为两位十六进制
            hex_pixels.append(hex_pixel)

        # 将所有像素的十六进制表示合并为一个字符串
        hex_data = ''.join(hex_pixels)

        return hex_data

    def get_bitmap_list(self, block_size=1024):
        hex_data = self.rgb_to_hex()
        return self.split_hex_data(hex_data, block_size)
