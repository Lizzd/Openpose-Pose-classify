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
    # len_per_pixel_x = foc[2]/(imageWidth/2)
    # len_per_pixel_y = foc[3]/(imageHeight/2)
    # pixel_coord[:, :, 0] = np.floor(x / len_per_pixel_x)
    # pixel_coord[:, :, 1] = np.floor(y / len_per_pixel_y)
    # x = x/imageWidth
    # y = y/imageHeight
    # ndc_x = np.subtract(x, x.min())/(x.max() - x.min())
    # ndc_y = np.subtract(y, y.min())/(y.max() - y.min())
    # # # raster
    # pixel_coord[:, :, 0] = np.floor(ndc_x * imageWidth)
    # pixel_coord[:, :, 1] = np.floor((1 - ndc_y) * imageHeight)
    # pixel_coord[:, :, 0] = np.floor((1-ndc_x) * imageWidth)
    # pixel_coord[:, :, 1] = np.floor(ndc_y * imageHeight)

    return pixel_coord

# if __name__ == "__main__":
#     globalpos_file_path = os.path.join(data_dir_path, 's1_vicon_pos_ori','S1', 'acting1', 'gt_skel_gbl_pos.txt')
#     cam_id = 'cam_0'
# [1.989109992980957, 60.6077995300293, 5.868690013885498]
# NameError("name 'array' is not defined")SyntaxError('invalid syntax', ('<string>', 1, 25, '[array([ 1.98910999, ...86869001]), array([ 0.78448302, ...04090023]), array([ 1.06169999, ...89519978]), array([-3.87739992, ...09268999]), array([ 6.72721004, ...77048016]), array([-15.13770008,...60737991]), array([17.64559937, ...14669991]), array([-2.23257995, ...06339979]), array([ 4.46345997, ...3291502 ]), array([-2.94156003, ...13940001]), array([ 4.63754988, ...29121017]), array([-3.62496996, ...25333023]), array([3.88003993, 3...81606007])]'))