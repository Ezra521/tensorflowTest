import random
import string
import sys
import math
import numpy as np
import tensorflow as tf
from PIL import Image,ImageDraw,ImageFont,ImageFilter

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
    draw = ImageDraw.Draw(image)
    gene_line(draw)
    gene_line(draw)
    m=0
    mtr=np.zeros(5000,np.int)
    while m<50:
        n=0
        while n<100:
            mtr[m+n*50]=image.getpixel((m,n))
            n=n+1
        m=m+1
    return text,mtr

def get_next_batch(batch_size=128):
    batch_x = np.zeros([batch_size,5000])
    batch_y = np.zeros([batch_size,10])
    for i in range(batch_size):
        text, image = gene_code()
        batch_x[i,:] = image
        batch_y[i,text] = 1
    return batch_x, batch_y

x = tf.placeholder(tf.float32, [None, 5000])
y_ = tf.placeholder(tf.float32, [None, 10])
#=======================================
def weight_variable(shape):
    initial = tf.truncated_normal(shape,stddev=0.1)
    return tf.Variable(initial)
def bias_variable(shape):
    initial =tf.constant(0.01,shape=shape)
    return tf.Variable(initial)
def conv2d(x,W):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')
def max_pool_2x2(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

#===============网络=====================

x_image = tf.reshape(x, [-1,100,50,1])
W_conv1=weight_variable([5,5,1,32])
b_conv1=bias_variable([32])
h_conv1=tf.nn.relu(conv2d(x_image,W_conv1)+b_conv1)
h_pool1=max_pool_2x2(h_conv1)

W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

W_fc1 = weight_variable([20800, 1024])
b_fc1 = bias_variable([1024])
h_pool2_flat = tf.reshape(h_pool2, [-1, 20800])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])

y_conv=tf.matmul(h_fc1_drop,W_fc2)+b_fc2
#===============================================
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_,logits=y_conv))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
saver = tf.train.Saver()
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    i=0
    ggg=0.5
    while True:
        batch = get_next_batch(250)
        train_accuracy=accuracy.eval(feed_dict={
            x:batch[0], y_: batch[1], keep_prob: 1.0})
        print ("step %d, training accuracy %g"%(i, train_accuracy))
        if i%600==599:
            saver.save(sess, filename+"model", global_step=i)
        if train_accuracy>ggg:
            ggg=(ggg+1.02)/2
            saver.save(sess, filename+"model", global_step=i)

        train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
        i=i+1



gene_code()
