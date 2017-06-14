import os
import numpy as np
#from sklearn.metrics import accuracy_score
import tensorflow as tf
import random
import math
import time
import csv

exec(open('processData.py').read())

st_time = time.time()
# number of neurons in each layer
input_num_units = len(data_set[0])-2
hidden_num_units_1 = input_num_units*4
#hidden_num_units_2 = int(hidden_num_units_1*1.5)
hidden_num_units_2 = 1 + int(hidden_num_units_1/5)
output_num_units = 1

# To stop potential randomness
seed = 128
rng = np.random.RandomState(seed)

def batch_creator(batch_size, dataset_length, dataset_name):
    """Create batch with random samples and return appropriate format"""
    batch_mask = rng.choice(dataset_length, batch_size)
    batch = eval(dataset_name + '_set')[batch_mask]
    #batch_y = eval(dataset_name + '_x')[batch_mask,:]
    return batch

def x_y_separation(dataset):
    x = dataset[:,1:-1]
    y = dataset[:,-1:]
    return x, y

#split intro training and test set
split_ratio = 1.0
train_size = int(len(data_set) * split_ratio)

temp_set = np.stack(data_set)
np.random.shuffle(temp_set)
train_set, test_set = temp_set[:train_size],temp_set[train_size:]
del temp_set

targets = np.stack(target_set)
targets_x = targets[:,1:]

print('Sets created in ' + str(time.time()-st_time) + ' seconds')
st_time =time.time()

### set all variables

# define placeholders
x = tf.placeholder(tf.float32, [None, input_num_units])
y = tf.placeholder(tf.float32, [None, output_num_units])

# set remaining variables
epochs = 200
batch_size = 500
learning_rate = 0.01

### define weights and biases of the neural network (refer this article if you don't understand the terminologies)

weights = {
    'hidden1': tf.Variable(tf.random_normal([input_num_units, hidden_num_units_1], seed=seed)),
    'hidden2': tf.Variable(tf.random_normal([hidden_num_units_1, hidden_num_units_2], seed=seed)),
    #'hidden3': tf.Variable(tf.random_normal([hidden_num_units_2, hidden_num_units_3], seed=seed)),
    'output': tf.Variable(tf.random_normal([hidden_num_units_2, output_num_units], seed=seed))
}

biases = {
    'hidden1': tf.Variable(tf.random_normal([hidden_num_units_1], seed=seed)),
    'hidden2': tf.Variable(tf.random_normal([hidden_num_units_2], seed=seed)),
    #'hidden3': tf.Variable(tf.random_normal([hidden_num_units_3], seed=seed)),
    'output': tf.Variable(tf.random_normal([output_num_units], seed=seed))
}

#net structure
hidden_layer_1 = tf.add(tf.matmul(x, weights['hidden1']), biases['hidden1'])
hidden_layer_1 = tf.nn.sigmoid(hidden_layer_1)

hidden_layer_2 = tf.add(tf.matmul(hidden_layer_1, weights['hidden2']), biases['hidden2'])
hidden_layer_2 = tf.nn.sigmoid(hidden_layer_2)

#hidden_layer_3 = tf.add(tf.matmul(hidden_layer_2, weights['hidden3']), biases['hidden3'])
#hidden_layer_3 = tf.nn.sigmoid(hidden_layer_3)

output_layer = tf.sigmoid(tf.matmul(hidden_layer_2, weights['output']) + biases['output'])

#cost
cost = tf.reduce_mean(tf.square(output_layer - y))

#optimizer
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

init = tf.global_variables_initializer()

with tf.Session() as sess:
    # create initialized variables
    sess.run(init)

    ### for each epoch, do:
    ###   for each batch, do:
    ###     create pre-processed batch
    ###     run optimizer by feeding batch
    ###     find cost and reiterate to minimize

    for epoch in range(epochs):
        avg_cost = 0
        total_batch = int(len(train_set)/batch_size)
        for i in range(total_batch):
            batch = batch_creator(batch_size, len(train_set), 'train')
            batch_x, batch_y = x_y_separation(batch)
            _, c = sess.run([optimizer, cost], feed_dict = {x: batch_x, y: batch_y})

            avg_cost += c / total_batch

        print("Epoch: " + str((epoch+1)) +  " cost = " +  str("{:.5f}".format(avg_cost)))

    print("\nTraining complete!")

    if len(test_set)>1:
    # find predictions on val set
        val_x, val_y = x_y_separation(test_set)
        pred_temp = tf.equal(tf.round(output_layer), y)
        pred = pred_temp.eval({x: val_x, y: val_y })
        accuracy = tf.reduce_mean(tf.cast(pred_temp, "float"))
        print("Validation Accuracy: " + str(accuracy.eval({x: val_x.reshape(-1, input_num_units), y: val_y})))

    #find targets
    pred_output = tf.round(output_layer)
    target_output = pred_output.eval({x: targets_x.reshape(-1, input_num_units)})

deliv = [[x,y] for x,y in zip(targets[:,0],target_output[:,0])]
for i in range(len(deliv)):
    if deliv[i][1] > 0.5:
        deliv[i][1] = 'F'
    else:
        deliv[i][1] = 'M'

with open('deliverable5noV.csv','w') as resfile:
    wr = csv.writer(resfile,dialect='excel')
    wr.writerows(deliv)




print('Training completed in ' + str(time.time()-st_time) + ' seconds')

    #predict = tf.argmax(output_layer, 1)
    #pred = predict.eval({x: test_x.reshape(-1, input_num_units)})
