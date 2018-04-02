import random
import string
import sys
import math
from PIL import \
    Image,ImageDraw,ImageFont,ImageFilter

#用来绘制干扰线
def gene_line(draw):
    py = random.randint(0, 3)
    begin = (-py*50, random.randint(0, 100))
    end = (200-py*50, random.randint(0, 100))
    draw.line([begin, end], fill = 0,width=5)

filename="D:/code/"
typen=2
typet=["arialbd.ttf","corbelb.ttf"]
#字体的位置
font_path = "C:/Windows/Fonts/"
#生成验证码图片的高度和宽度
size = (180,180)
#生成验证码
def gene_code():
    width,height = size #宽和高
    image = Image.new('1',(width,height),1) #创建图片
    font = ImageFont.truetype(font_path+typet[random.randint(0, typen-1)],70) #验证码的字体
    draw = ImageDraw.Draw(image)  #创建画笔
    source = ['0','1','2','3','4','5','6','7','8','9']
    text = random.randint(0, 9) #生成字符串
    font_width, font_height = font.getsize(source[text])
    draw.text(((width - font_width) /2, (height - font_height)/2-5),source[text],font= font,fill=0) #填充字符串
    rx=random.uniform(-0.2, 0.2)
    ry=random.uniform(-0.2, 0.2)
    image = image.transform((width+100,height+100), Image.AFFINE, (1,rx,0,ry,1,0),Image.BILINEAR)  #创建扭曲
    px=random.randint(-20, 20)
    py=random.randint(-6, 6)
    image = image.crop((65-70*rx+py,40-70*ry+px,115-70*rx+py,140-70*ry+px))
    aa = str(".png")
    path = filename + source[text] + aa
    image.save(path)
    draw = ImageDraw.Draw(image)
    gene_line(draw)
    gene_line(draw)
    image.save(path)

gene_code()
