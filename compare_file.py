##################################
#Compare File Function
#By: Angelo Poggi
#
#This is a function that takes two files and compares them
#Generates a new file with the differences
##################################
import os

def compare_file(file1, file2, filename):
    with open('{}.txt'.format(filename), 'w') as filename:
            with open(file1, 'r') as file1:
                with open(file2, 'r') as file2:
                    diff = set(file1).difference(file2)
                for line in diff:
                    filename.write(line)




