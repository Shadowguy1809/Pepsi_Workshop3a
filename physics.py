import numpy as np
import matplotlib.pyplot as plt
import time
from math import floor
from numba import jit


def running_time(func, x):
    t_start = time.time()
    func(x)
    t_end = time.time()
    return t_end - t_start


# r_vec is a np . array of D elements ( D is the number of dimensions ).
# it is the vector which points from particle 1 to particle 2 (= r_ij = ri - rj )
# this function returns the Lennard - Jones potential between the two particles
@jit
def LennardJonesPotential(r_vec, rc):
    r = np.linalg.norm(r_vec)  # calculate norm (= | r_ij |)
    if r > rc:
        return 0.
    rc2 = rc * rc
    rc6 = rc2 * rc2 * rc2
    rc12 = rc6 * rc6
    r2 = r * r
    r6 = r2 * r2 * r2
    r12 = r6 * r6
    return 4 / r12 - 4 / r6 - 4 / rc12 + 4 / rc6


print(LennardJonesPotential(np.linspace(0, 10, 10000), 3))


# same as previous method but returns the force between the two particles
# this is the gradient of the previous method
@jit
def LennardJonesForce(r_vec, rc):
    r = np.linalg.norm(r_vec)  # calculate norm (= | r_ij |)
    if r > rc:
        return 0. * r_vec
    y = 1 / r
    y2 = y * y
    y4 = y2 * y2
    y6 = y4 * y2
    y8 = y4 * y4
    y14 = y6 * y8
    return (48 * y14 - 24 * y8) * r_vec


def pressure_virial(virial, Ek, L):
    return 2 * Ek / L ** 3


print(LennardJonesForce(np.linspace(0, 10, 100000), 3))


# this method calculates the total force on each particle
# r is a 2 D array where r [i ,:] is a vector with length D ( dimensions )
# which represents the position of the i - th particle
# ( in 2 D case r [i ,0] is the x coordinate and r [i ,1] is the y coordinate of the i - th particle )
# this function returns a numpy array F of the same dimensions as r
# where F [i ,:] is a vector which represents the force that acts on the i - th particle
# this function also returns the virial
@jit
def LJ_Forces(r, L, rc):
    F = np.zeros_like(r)
    virial = 0
    N = r.shape[0]  # number of particles
    # loop on all pairs of particles i , j
    for i in range(1, N):
        for j in range(i):
            r_ij = r[i, :] - r[j, :]
            r_ij = r_ij - L * np.rint(r_ij / L)  # see class on boundary conditions
            f_ij = LennardJonesForce(r_ij, rc)
            F[i, :] += f_ij
            F[j, :] -= f_ij  # third law of newton
            virial += np.dot(f_ij, r_ij)  # see class on virial theorem
    return F, virial


print(LJ_Forces(np.random.rand(100, 2), 1, 3))


def system_energy(r_old, r, r_new, dt, L, rc):
    """

    :param r_old:
    :param r:
    :param r_new:
    :param dt:
    :param L:
    :param rc:
    :return:
    """
    T = 0
    for i in range(len(r)):
        r_tmp = (r_new[i] - r_old[i]) / dt
        T = T + 0.125 * np.dot(r_tmp, r_tmp)
    V = 0
    for i in range(len(r)):
        for j in range(i + 1, len(r)):
            V = V + LennardJonesPotential(r[i] - r[j], rc)
    return T, V, T + V


if __name__ == '__main__':
    x = np.array([1, 2])
    system_energy(np.array([x, x]), np.array([x, x]), np.array([x, x]), 1, 1, 1)


def verlet_step(r_old, r, dt, L, rc):
    F, virial = LJ_Forces(r, L, rc)
    r_new = 2 * r + F * dt ** 2 - r_old
    return r_new, virial
