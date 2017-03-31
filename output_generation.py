import sys

csv = open('Y_train_pose.csv', 'w')

for i in range(400) :
	idx = int(i/100)
	csv.write(str(idx))
	csv.write('\n')

csv.close()