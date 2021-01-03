import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import pickle


def sepa():
    print('*'*80)


def sepan(t):
    for i in range(t):
        print('*'*80)


def p_df(data):
    sepa()
    print(data)
    # print(type(data))
    # print(data.index)
    # print(data.columns)


def p_shape(data):
    print(data.shape)


def p_l(data):
    print("length: ", len(data))
    print(data)


def get_task(task_count):
    filename = './split_data/task'+str(task_count)+'.txt'
    with open(filename, 'r') as f:
        info = f.readline()
    requests = int(info.split('Orders=')[1].split(' ')[0])
    vehicles = int(info.split('Vehicles=')[1].split(' ')[0])
    scores = int(info.split('Scores=')[1].split(r'\n')[0])
    data = pd.read_table(filename, delim_whitespace=True)
    # data = data.drop(task_name, 1)
    trips = data.shape[0]
    # costs=int(info.split('Scores=')[1].split(r'\n')[0])
    print("No:{},requests: {}, trips: {},vehicles: {}".format(
        task_count, requests, trips, vehicles))
    print(data.shape)
    return requests, trips, vehicles, scores, data


def if_request_in_trip(request, new_trip_number, reverse_trip_hash):
    """

    """
    # find corresponding trip pair from the {newly assigned number}
    trip_pair = reverse_trip_hash[str(new_trip_number)]
    # print(trip_pair)
    trip_member = trip_pair.split(',')
    flag = 0
    if str(request) in trip_member:
        flag = 1
    return flag


def msg(msg):
    print("*"*20+msg+"*"*20)


def compare_time(mip, gd):
    # plt.clf()
    # plt.cla()
    plt.plot(mip, label='pure mip')
    plt.plot(gd, label='greedy initialize')
    plt.legend(loc='upper center', shadow=True, fontsize='x-large')
    plt.title("time consumed")
    plt.show()
    plt.savefig('total_time.png')


def compare_value(mip, gd):
    # plt.clf()
    # plt.cla()
    diff = [a_i - b_i for a_i, b_i in zip(mip, gd)]
    # plt.plot(mip,label='pure mip')
    # plt.plot(gd,label='greedy initialize')
    plt.plot(diff)
    plt.legend(loc='upper center', shadow=True, fontsize='x-large')
    plt.title("value computed: mip-greedy")
    plt.show()
    plt.savefig('total_value.png')


def save_list(a, b, c, d):
    new = [a, b, c, d]
    pickle.dump(new, open("serialized_list.p", "wb"))


def load_list():
    with open("serialized_list.p", 'rb') as f:
        new = pickle.load(f)
    return new
