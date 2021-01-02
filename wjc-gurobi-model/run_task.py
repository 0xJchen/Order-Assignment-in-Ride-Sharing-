from rtv import *
import greedy as gd
import time
import pickle

if __name__ == '__main__':
    total_st = time.time()
    task_list = [i for i in range(4, 121)]

    gd1_time = []
    gd1_cost = []

    gd2_time = []
    gd2_cost = []

    pure_mip_time = []
    pure_mip_value = []

    mip_gd1_time = []
    mip_gd1_value = []

    mip_gd2_time = []
    mip_gd2_value = []

    for i in task_list:
        task_info(i)

        for j in range(2,3):
            msg("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            infor="task num: "+str(i)+ "iter:"+str(j)
            msg(infor)
            if j == 0:
                mip_time, mip_cost, gd_cost, gd_time = run_one_task(
                    i, from_metadata=False, greedy=j)
            else:
                mip_time, mip_cost, gd_cost, gd_time = run_one_task(
                    i, from_metadata=True, greedy=j)

            if j == 0:  # pure mip
                pure_mip_time.append(mip_time)
                pure_mip_value.append(mip_cost)
            elif j == 1:  # mip+greedy1
                gd1_time.append(gd_time)
                gd1_cost.append(gd_cost)
                mip_gd1_time.append(mip_time)
                mip_gd1_value.append(mip_cost)
            else:
                assert(j == 2)
                gd2_time.append(gd_time)
                gd2_cost.append(gd_cost)
                mip_gd2_time.append(mip_time)
                mip_gd2_value.append(mip_cost)

    result = {}
    result["gd1_time"] = gd1_time
    result["gd1_cost"] = gd1_cost
    result["gd2_time"] = gd2_time
    result["gd2_cost"] = gd2_cost
    result["pure_mip_time"] = pure_mip_time
    result["pure_mip_value"] = pure_mip_value
    result["mip_gd1_time"] = mip_gd1_time
    result["mip_gd1_value"] = mip_gd1_value
    result["mip_gd2_time"] = mip_gd2_time
    result["mip_gd2_time"] = mip_gd2_value

    # pickle.dump(result,open("result","wb"))
    stamp="result_gd2"+str(len(task_list))
    with open(stamp, "wb") as fp:
        pickle.dump(result, fp)
    print("finish in {}".format(time.time()-total_st))
