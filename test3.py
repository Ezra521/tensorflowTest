import tensorflow as tf

sess = tf.Session()

W = tf.Variable([.3],dtype=tf.float32)
b = tf.Variable([-.3],dtype=tf.float32)
x = tf.placeholder(tf.float32)
linear_model = W*x+b

#tf.global_variables_initializer()的解释是当用tf.Variable()时没有初始化变量，所以需要它来初始化变量
init=tf.global_variables_initializer()
sess.run(init)

#保存tensorboard图
writer = tf.summary.FileWriter('D:/ten', tf.get_default_graph())
writer.close()

print(sess.run(linear_model,{x:[1,2,3,4]}))