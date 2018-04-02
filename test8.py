import urllib.request
from PIL import Image
import tensorflow as tf
import numpy as np


name=["1","2","3","4"]
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
sess=tf.Session()
saver.restore(sess, "D:/tensorflow/model6/crack_capcha.model-36599")
for j in range(50):
    response = urllib.request.urlopen('http://xxxxxx/jw_css/getCheckCode')
    cat_img = response.read()
    with open('D:/tensorflow/test.jpg','wb') as f:
        f.write(cat_img)
    img=Image.open('D:/tensorflow/test.jpg')
    img.save("D:/tensorflow/img/"+str(j)+".jpg")
    for i in range(4):
        img1=img.crop((0+50*i,0,50+50*i,100)).convert('L')
        m=0
        mtr=np.zeros(5000,np.int)
        while m<50:
            n=0
            while n<100:
                if img1.getpixel((m,n))>128:
                    mtr[m+n*50]=1
                else:
                    mtr[m+n*50]=0
                n=n+1
            m=m+1
        batch_x = np.zeros([1,5000])
        batch_x[0,:] = mtr
        result = sess.run(tf.argmax(y_conv,1), feed_dict={x: batch_x,keep_prob: 0.5})
        # print(result,end='')
    print('|'+str(j))