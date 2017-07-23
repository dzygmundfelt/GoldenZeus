import PoloniexDataFetcher as pdf
import requests
import json
import tensorflow as tf
import numpy as np

def putDataIntoArray(data):
	ml_array = [[], [], []]
	for item in sorted(data):
		ml_array[0].append(item["date"])
		ml_array[1].append(item["volume"])
		ml_array[2].append(item["weightedAverage"])
	return ml_array

def normalizeArray(arr):
    arr_range = np.amax(arr) - np.amin(arr)
    arr_avg = np.average(arr)
    for i in range(len(arr)):
        arr[i] = (arr[i] - arr_avg) / arr_range
    return arr	

fd, td = pdf.getDateRangeFromUser()
from_date, to_date = pdf.convertRangeToUTC(fd, td)
period = str(raw_input("Choose 300, 900, 1800, 7200, 14400, 86400 second time periods.\n"))
url = pdf.createPoloniexURL(from_date, to_date, period)
data = pdf.getData(url)
ml_array = putDataIntoArray(data)

normal_dates = normalizeArray(ml_array[0])
normal_volumes = normalizeArray(ml_array[1])
weightedAverages = normalizeArray(ml_array[2])

next_utc = normal_dates.pop()
next_volume = normal_volumes.pop()
weightedAverages = weightedAverages[1:]
vector_length = len(normal_dates)

for i in range(vector_length):
	print("date: " + str(normal_dates[i]) + " volume: " + str(normal_volumes[i]) + " next period avg: " + str(weightedAverages[i]))

# set up computational graph
W1 = tf.Variable(0.3, tf.float32)
W2 = tf.Variable(0.3, tf.float32)
b = tf.Variable(0.1, tf.float32)
x1 = tf.placeholder(tf.float32)
x2 = tf.placeholder(tf.float32)
y = tf.placeholder(tf.float32)
linear_model = W1 * x1 + W2 * x2 + b

# define loss function
squared_deltas = tf.square((linear_model - y) / (2*len(normal_volumes)))
loss = tf.reduce_sum(squared_deltas)

# create session and run it
sess = tf.Session()
init = tf.global_variables_initializer()
sess.run(init)
optimizer = tf.train.GradientDescentOptimizer(0.3)
train = optimizer.minimize(loss)
print(sess.run(init))

for i in range(1000):
    _, loss_val, W1_val, W2_val, b_val = sess.run([train, loss, W1, W2, b], feed_dict={x1: normal_dates, x2: normal_volumes, y: weightedAverages})
    if(i % 100 == 99):
        print(i)
        print 'loss = %s' % loss_val
        print 'W1 = %s' % W1_val
        print 'W2 = %s' % W2_val
        print 'b = %s' % b_val

print(sess.run([W1, W2, b]))

print(str(next_utc) + ' ' + str(next_volume) + ' ' + str(weightedAverages[-1]))

print(next_utc*W1_val + next_volume*W2_val + b_val - weightedAverages[-1])