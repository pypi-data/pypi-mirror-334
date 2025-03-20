# -*- coding: utf-8 -*-
# @Author: maoyongfan
# @email: maoyongfan@163.com
# @Date: 2025/3/16 18:38
import sys

from pybaselib.interfaces.imgs.img import Img
from PIL import Image, ImageDraw
from pybaselib.utils import IntType


class ImgDefinition(Img):
    def __init__(self, img_path: str) -> None:
        self.img_path = img_path
        self.base_img = Image.open(img_path)
        self.set_image_size()

    def get_img_type(self):
        img_type = self.base_img.mode
        if img_type == "1":
            return "monochrome1bit"
        elif img_type == "L":
            return "monochrome8bit"
        elif img_type == "P":
            return "colorClassic"
        elif img_type == "RGB":
            return "color24bit"
        elif img_type == "RGBA":
            return "color32bit"
        else:
            return img_type

    def get_img_size(self):
        img_type = self.get_img_type()
        if img_type == "monochrome1bit":
            pixels = self.width * self.height
            return IntType.custom_round_division(pixels, 8)
        elif img_type == "color24bit":
            return (self.width * self.height) * 3
        else:
            self.base_img.convert("RGB")
            self.set_image_size()
            return (self.width * self.height) * 3

    def get_graphic_infos(self):
        graphic_type = self.get_img_type()
        graphic_size = self.get_img_size()
        return self.width, self.height, graphic_type, graphic_size

    def get_img_to_hex(self, graphic_type):
        hex_data = None
        if graphic_type == "monochrome1bit":
            # 获取图片的二进制数据
            img_data = self.base_img.tobytes()
            # 以十六进制格式输出  00代表全黑 FF代表全白
            hex_data = img_data.hex()
        return hex_data

    def one_bit_image_to_bits(self):
        """将 1-bit 单色图像转换为比特流，不足8位补0"""
        pixels = self.base_img.load()

        bit_string = ""

        for y in range(self.height):
            for x in range(self.width):
                bit_string += '1' if pixels[x, y] == 255 else '0'  # 白色(255) -> '1'，黑色(0) -> '0'

        # 补齐到8位对齐
        padding_length = (8 - len(bit_string) % 8) % 8
        bit_string += '0' * padding_length  # 末尾补0

        return bit_string

    def split_hex_data(self, hex_data, chunk_size=1024):
        """将十六进制字符串按 1KB (1024字节 = 2048 hex字符) 进行分割"""
        hex_chunk_size = chunk_size * 2  # 1 字节 = 2 hex 字符
        chunks = [hex_data[i:i + hex_chunk_size] for i in range(0, len(hex_data), hex_chunk_size)]

        # 如果最后一块数据不足 1KB，则补 00
        if len(chunks[-1]) < hex_chunk_size:
            chunks[-1] = chunks[-1].ljust(hex_chunk_size, '0')

        return chunks

    def create_monochrome_image(self, hex_data, width, height, save_path):
        """使用十六进制数据生成 1-bit 黑白图像 此方法OK"""
        bit_data = IntType.hex_to_bits(hex_data)
        print(hex_data)
        print(bit_data)
        print(len(bit_data))

        if len(bit_data) < width * height:
            raise ValueError("提供的十六进制数据不足以填充图像")

        img = Image.new('1', (width, height))  # 创建 1-bit 图像
        pixels = img.load()

        for y in range(height):
            for x in range(width):
                index = y * width + x
                pixels[x, y] = 255 if bit_data[index] == '1' else 0  # 1为白，0为黑

        img.save(save_path)

        return img

    def create_monochrome_1bit_image(self, width, height, save_path):
        # 创建 1-bit 黑白图像（默认填充白色）
        img = Image.new("1", (width, height), 1)  # 1 表示白色，0 表示黑色

        # 获取绘图对象
        draw = ImageDraw.Draw(img)

        # 画一些黑色图案（比如矩形、线条）
        draw.rectangle([10, 10, width - 10, height - 10], outline=0, fill=0)  # 画黑色矩形
        draw.line([(0, 0), (width, height)], fill=1)  # 画白色对角线

        # 保存图片
        img.save(save_path)
        print(f"Monochrome 1-bit image saved at: {save_path}")

    # 创建一个 8x8 的 1-bit 黑白图片
    def create_monochrome_1bit_image_2(self, save_path):
        img = Image.new("1", (8, 8), 1)  # 8x8，默认白色（1）
        pixels = img.load()

        # 创建一个简单的黑白图案（前4行黑，后4行白）
        for y in range(4):
            for x in range(8):
                pixels[x, y] = 0  # 设为黑色

        img.save(save_path)  # BMP 格式更容易直接读取二进制数据
        return "monochrome_1bit.bmp"

    def get_pixels(self):
        pixels = list(self.base_img.getdata())
        # print(pixels)
        # print(len(pixels))
        return

    def hex_to_1bit_image(self, hex_data, width, height, save_path):
        """
        有问题,图片数据大于生成图片像素点
        将 1-bit Monochrome 16 进制数据转换为图片
        :param hex_data: 16 进制字符串（每 8-bit 表示 1 字节）
        :param width: 图片宽度
        :param height: 图片高度
        :param save_path: 生成图片的保存路径
        """
        # 去掉空格，转换为字节数据
        binary_data = bytes.fromhex(hex_data.replace(" ", ""))
        print(binary_data)

        # 创建 1-bit 图片
        img = Image.frombytes("1", (width, height), binary_data)

        # 保存图片
        img.save(save_path)
        print(f"Image saved as {save_path}")

        # 显示图片（可选）
        img.show()






if __name__ == '__main__':
    # img_path = '/Users/maoyongfan/Downloads/2.bmp'
    img_path = '/Users/maoyongfan/Downloads/4.png'
    i = ImgDefinition(img_path)
    # 生成 100x100 的黑白 1-bit 图片
    # i.create_monochrome_1bit_image(100, 100, img_path)
    # i.create_monochrome_1bit_image_2(img_path)
    # i.hex_to_1bit_image("000C000007000001E03FFFF80001E0000700000C00", 24, 7, img_path)
    # i.create_monochrome_image("84926308C248A170", 10, 6, img_path)
    print(i.width, i.height, i.get_img_type())
    print(i.get_graphic_infos())
    # i.get_pixels()
    # print(i.get_bitmap_list(i.get_img_type(), 1024))
    bit_data = i.one_bit_image_to_bits()
    print("Bit Data:", bit_data)
    print("Length:", len(bit_data), "bits ({} bytes)".format(len(bit_data) // 8))
    hex_data = IntType.bits_to_hex(bit_data)
    print("Hex Data:", hex_data)
    print(i.split_hex_data(hex_data))