import math

def exp_complement_curve(z: float): 
    exponential_constant = 0.005
    return 1 - math.exp(-exponential_constant * z)

depth_attenuation = exp_complement_curve
# TODO: Add interesting functions for wacky viewports
