from utils import *
import numpy as np
import os

def _ikm(self, htm_target, htm = None, q0=None, p_tol=0.005, a_tol=5, no_iter_max=2000, ignore_orientation=False, mode='auto'):
    n = len(self._links)
    if q0 is None:
        q0 = np.matrix(np.reshape((2 * np.pi) * np.random.rand(n) - np.pi, (n, 1)))
        
    if htm is None:
        htm = self.htm

    # Error handling
    if not Utils.is_a_matrix(htm_target, 4, 4):
        raise Exception("The parameter 'htm' should be a 4x4 homogeneous transformation matrix.")

    if not Utils.is_a_natural_number(no_iter_max):
        raise Exception("The parameter 'no_iter_max' should be a nonnegative integer number.")

    if not Utils.is_a_vector(q0, n):
        raise Exception("The parameter 'q0' should be a " + str(n) + " dimensional vector.")

    if (not Utils.is_a_number(p_tol)) or p_tol <= 0:
        raise Exception("The parameter 'p_tol' should be a nonnegative number.")

    if (not Utils.is_a_number(a_tol)) or a_tol <= 0:
        raise Exception("The parameter 'a_tol' should be a nonnegative number.")

    if not str(type(ignore_orientation)) == "<class 'bool'>":
        raise Exception("The parameter 'ignore_orientation' should be a boolean.")

    if mode=='c++' and os.environ['CPP_SO_FOUND']=='0':
        raise Exception("c++ mode is set, but .so file was not loaded!")
        # end error handling

    if mode == 'python' or  (mode=='auto' and os.environ['CPP_SO_FOUND']=='0'):
        return _ikm_python(self, htm_target, htm, q0, p_tol, a_tol, no_iter_max, ignore_orientation)
    else:
        ik_res = self.cpp_robot.ik(htm_target, htm, q0, p_tol, a_tol, no_iter_max, ignore_orientation)

        if not ik_res.success:
            raise Exception("Solution for IK not found. You can try the following: \n" \
                            " Increasing the maximum number of iterations, 'no_iter_max' (currently " + str(
                no_iter_max) + ")\n" \
                            " Increasing the tolerance for the position, 'p_tol' (currently " + str(p_tol) + " meters)\n" \
                                                                                                                " Increasing the tolerance for the orientation, 'a_tol' (currently " + str(
                a_tol) + " degrees).")
        else:
            return np.matrix(ik_res.qf).reshape((n,1))        


# (Private function) Used in IK
def _evolve_config(self, q, htm, p_tol, a_tol, htm_target, iter_remain, ignore_orientation):
    n = len(self.links)
    found = False
    zero_u = False
    iter_end = False

    eta = 0.03
    eps = 0.001
    tol_u = 0.00001 
    i = 0

    while (not found) and (not zero_u) and (not iter_end):

        r, jac_r = self.task_function(htm=htm, htm_des = htm_target, q = np.array(q), mode='python')
        
        # print(r)
        # print(jac_r)

        if ignore_orientation:
            r = r[0:3]
            jac_r = jac_r[0:3, :]
        else:
            r[3:6] = np.sqrt(r[3:6])

        r[0] = np.sign(r[0])*np.sqrt(np.abs(r[0]))
        r[1] = np.sign(r[1])*np.sqrt(np.abs(r[1]))
        r[2] = np.sign(r[2])*np.sqrt(np.abs(r[2]))
            
        u = Utils.dp_inv_solve(jac_r, -eta * r, eps, mode='python')
        q = q + u 
        


        e_pos = max([r[0]**2, r[1]**2, r[2]**2])

        if ignore_orientation:
            e_ori = 0
        else:
            e_ori = max([(180 / np.pi) * acos(min(max(1 - num * num, -1), 1)) for num in r[3:6]])

        i += 1
        
        found = (e_pos < p_tol) and (e_ori < a_tol)
        zero_u = max(abs(u)) < tol_u
        iter_end = i > iter_remain

    return found, i, q


# Inverse kinematics for the end-effector
def _ikm_python(self, htm_target, htm, q0=None, p_tol=0.005, a_tol=5, no_iter_max=2000, ignore_orientation=False):
    n = len(self._links)

    j = 0
    found = False
    q = np.matrix(q0).reshape((n, 1))
    no_iter_remain = no_iter_max

    while not found and no_iter_remain >= 0:
        found, i, q = _evolve_config(self, q, htm, p_tol, a_tol, htm_target, no_iter_remain, ignore_orientation)
        no_iter_remain -= i
        if not found:
            q = np.matrix(np.reshape((2 * np.pi) * np.random.rand(n), (n, 1)))

    if not found:
        raise Exception("Solution for IK not found. You can try the following: \n" \
                        " Increasing the maximum number of iterations, 'no_iter_max' (currently " + str(
            no_iter_max) + ")\n" \
                           " Increasing the tolerance for the position, 'p_tol' (currently " + str(p_tol) + " meters)\n" \
                                                                                                            " Increasing the tolerance for the orientation, 'a_tol' (currently " + str(
            a_tol) + " degrees).")
    else:
        return q
