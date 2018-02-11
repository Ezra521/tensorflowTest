import tensorflow as tf

sess = tf.Session()
W = tf.Variable([.3],dtype=tf.float32)
b = tf.Variable([-.3],dtype=tf.float32)
x = tf.placeholder(tf.float32)
linear_model = W*x+b
init=tf.global_variables_initializer()
sess.run(init)

y = tf.placeholder(tf.float32) #占位符，用于输入想要得到的数据集
squared_deltas = tf.square(linear_model-y) #正确结果与模型结果差的平方
loss = tf.reduce_sum(squared_deltas) #所有差平方的和
print(sess.run(loss,{x:[1,2,3,4],y:[0,-1,-2,-3]})) #打印损失函数的值



#我们可以通过给W、b再分配值来改进模型。一个变量的初始值由tf.Variable提供，但可以用tf.assign来改变：
#这里是我手动找到w，b
# fixW = tf.assign(W,[-1.])
# fixb = tf.assign(b,[1.])
# sess.run([fixW,fixb])
# print(sess.run(loss,{x:[1,2,3,4],y:[0,-1,-2,-3]}))

#这里使用tensorflow提供的api梯度下降来实现
optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(loss)
sess.run(init)
for i in range(1000):
    sess.run(train,{x:[1,2,3,4],y:[0,-1,-2,-3]})
print(sess.run([W,b]))

#保存tensorboard图
writer = tf.summary.FileWriter('D:/ten', tf.get_default_graph())
writer.close()