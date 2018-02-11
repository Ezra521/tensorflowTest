"""
author:ezra
describe:实现tensorboard
"""
import tensorflow as tf

sess=tf.Session()
a=tf.placeholder(tf.float32)
b=tf.placeholder(tf.float32)
adder_node=a+b
print(sess.run(adder_node,{a:30,b:4.5}))
print(sess.run(adder_node,{a:[1,2],b:[2,4.5]}))
add_and_triple=adder_node*6.5
print(sess.run(add_and_triple,{a:30,b:4.5}))


writer = tf.summary.FileWriter('D:/ten', tf.get_default_graph())
writer.close()