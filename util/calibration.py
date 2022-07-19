import os
from inout import *

data_dir_path = os.path.join(os.path.abspath('.'), 'data')

def world2image(path:str, cam_id:str='cam_0')->np.ndarray:
    """
    This function converts global positions to pixel coordinate.
    Input: glo_pos path
    Return: pixel coord np.array with shape (frame_num, targets_len, 2)
    """
    # a world point in the camera coordinate frame is given by p' = Rp + t) 
    # a project point for a perfect pinhole camera with no distortion is u = fx* p'.x/p'.zworld point in the camera coordinate frame is given by p' = Rp + t) 
    calibration_file_path = os.path.join(data_dir_path, 'calibration.cal')
    cam_pars = read_calibration_file(calibration_file_path)
    glob_pos = read_global_pos(path=globalpos_file_path)

    foc = cam_pars[cam_id]['fx_fy_cx_cy']
    rotation = cam_pars[cam_id]['rotation']
    translation = cam_pars[cam_id]['translation']
    frame_num, targets_num, _ = glob_pos.shape
    pixel_coord = np.zeros((frame_num, targets_num, 2), dtype=np.int16)
    world2cam = glob_pos*rotation + translation
    pixel_coord[:, :, 0] = foc[0] * world2cam[:, :, 0]/world2cam[:, :, 2]
    pixel_coord[:, :, 1] = foc[2] * world2cam[:, :, 1]/world2cam[:, :, 2]
    return pixel_coord

if __name__ == "__main__":
    globalpos_file_path = os.path.join(data_dir_path, 's1_vicon_pos_ori','S1', 'acting1', 'gt_skel_gbl_pos.txt')
    cam_id = 'cam_0'
    world2image(globalpos_file_path, cam_id)
