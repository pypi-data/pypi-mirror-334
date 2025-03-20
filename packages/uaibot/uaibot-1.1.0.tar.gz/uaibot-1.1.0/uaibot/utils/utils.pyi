from typing import Union, List, TypeAlias, Tuple
import numpy as np
import numpy.typing as npt

#Union[List[float], npt.NDArray[np.float64], np.matrix]
#means that we can send either a list, a numpy float, of a numpy matrix

Vector: TypeAlias = Union[List[float], npt.NDArray[np.float64], np.matrix]
Matrix: TypeAlias = Union[npt.NDArray[np.float64], np.matrix]

class Utils:
    @staticmethod
    def S(v: Vector) -> np.matrix: ...
    
    @staticmethod
    def rot(axis: Vector, angle: float) -> np.matrix: ...
    
    @staticmethod
    def trn(vector: Vector) -> np.matrix: ...
    
    @staticmethod
    def rotx(angle: float) -> np.matrix: ...
    
    @staticmethod
    def roty(angle: float) -> np.matrix: ...

    @staticmethod
    def rotz(angle: float) -> np.matrix: ...

    @staticmethod
    def htm_rand(trn_min: float, trn_max: float, rot: float) -> np.matrix: ...
    
    @staticmethod
    def inv_htm(htm: float, trn_max: float, rot: float) -> np.matrix: ...
    
    @staticmethod
    def axis_angle(htm: Matrix) -> Tuple[Vector, float]: ...
    
    @staticmethod
    def euler_angles(htm: Matrix) -> Tuple[float, float, float]: ...
    
    @staticmethod
    def dp_inv(A: Matrix, eps: float) -> Matrix: ...
    
    @staticmethod
    def dp_inv_solve(A: Matrix, b: Vector, eps: float, mode: str) -> Vector: ...
    
    #Continue declaring the methods...