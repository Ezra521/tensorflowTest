"""
author:ezra
describe:实现tensorboard
实现常量的相加
"""

import tensorflow as tf

node1 = tf.constant(3.0,dtype=tf.float32)
node2 = tf.constant(4.0)
node3 = tf.add(node1, node2)

writer = tf.summary.FileWriter('D:/ten',tf.get_default_graph())
writer.close()