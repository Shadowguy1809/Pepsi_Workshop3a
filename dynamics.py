import numpy as np
import matplotlib as plt
from random import random


def T0_config(dt, N, L, rc):
    x_initial_locations = []
    y_initial_locations = []
    z_initial_locations = []
    x_locations = []
    y_locations = []
    z_locations = []
    r_old = []
    r = []
    r_new = []

    for i in range(N):
        x_initial_locations.append(np.random.random(L))
        y_initial_locations.append(np.random.random(L))
        z_initial_locations.append(np.random.random(L))
        x_locations.append(np.random.random(L))
        y_locations.append(np.random.random(L))
        z_locations.append(np.random.random(L))
        r_old.append([x_initial_locations[i], y_initial_locations[i], z_initial_locations[i]])
        r.append([x_locations[i], y_locations[i], z_locations[i]])

    while True:
        for i in range(N):
            r_new.append(verlet_step(r_old, r, dt, L, rc))




def verlet_step(r_old, r, dt, L, rc):
    pass
