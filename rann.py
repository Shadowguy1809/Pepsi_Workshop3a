import numpy as np
import matplotlib.pyplot as plt
import time
from math import floor


def LennardJonesForce(r_vec, rc):
    r = np.linalg.norm(r_vec)  # calculate norm (= | r_ij |)
    if r > rc:
        return 0. * r_vec
    return 4 * (12 / r ** 14 - 6 / r ** 8) * r_vec


def LennardJonesForceFast(r_vec, rc):
    r = np.linalg.norm(r_vec)  # calculate norm (= | r_ij |)
    if r > rc:
        return 0. * r_vec
    y = 1 / r
    y8 = y * y * y * y * y * y * y * y
    return y8 * (2 * y8 * r * r - 1) * r_vec


def running_time2(func, x, y):
    t_start = time.time()
    func(x, y)
    t_end = time.time()
    return t_end - t_start


if __name__ == '__main__':
    x = np.array(range(10000000))
    print(running_time2(LennardJonesForce, x, 100000000))
    print(running_time2(LennardJonesForceFast, x, 100000000))
