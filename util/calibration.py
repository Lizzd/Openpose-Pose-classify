import os
from util.inout import *
import numpy as np

data_dir_path = os.path.join(os.path.abspath('.'), 'data')
calibration_file_path = os.path.join(data_dir_path, 'calibration.cal')

def world2image(globalpos_file_path:str, cam_id:str='cam_0', imageWidth:int=400, imageHeight:int=400)->np.ndarray:
    """
    This function converts global positions to pixel coordinate.
    Input: glo_pos path
    Return: pixel coord np.array with shape (frame_num, targets_len, 2)
    """
    cam_pars = read_calibration_file(calibration_file_path)
    glob_pos = read_global_pos(path=globalpos_file_path)

    foc = cam_pars[cam_id]['fx_fy_cx_cy']
    rotation = cam_pars[cam_id]['rotation']
    translation = cam_pars[cam_id]['translation']
    frame_num, targets_num, _ = glob_pos.shape
    pixel_coord = np.zeros((frame_num, targets_num, 2), dtype=np.int16)

    # a world point in the camera coordinate frame is given by p' = Rp + t) 
    world2cam = np.tensordot(glob_pos, rotation, axes=([-1],[0]))
    world2cam = np.tensordot(glob_pos, rotation, axes=([-1],[0])) + translation
    # a project point for a perfect pinhole camera with no distortion is u = fx* p'.x/p'.zworld point 
    # in the camera coordinate frame is given by p' = Rp + t) 
    # TODO: consider distortion parameters
    # # screen
    # pixel_coord[:, :, 0] = (foc[0]/2 + world2cam[:, :, 0]/world2cam[:, :, 2])/foc[0]
    # pixel_coord[:, :, 1] = (foc[1]/2 + world2cam[:, :, 1]/world2cam[:, :, 2])/foc[1]
    x = foc[0]*(world2cam[:, :, 0]/world2cam[:, :, 2])+foc[2]
    y = foc[1]*(world2cam[:, :, 1]/world2cam[:, :, 2])+foc[3]
    pixel_coord[:, :, 0] = np.floor(x )
    pixel_coord[:, :, 1] = np.floor(y )
    return pixel_coord

# if __name__ == "__main__":
#     globalpos_file_path = os.path.join(data_dir_path, 's1_vicon_pos_ori','S1', 'acting1', 'gt_skel_gbl_pos.txt')
#     cam_id = 'cam_0'