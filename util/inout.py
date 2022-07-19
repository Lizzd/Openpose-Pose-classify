
import numpy as np

def read_calibration_file(path:str)->dict:
    """
    This function reads the calibration file which has the following format: 
    num_cameras distortion_order (0)
    (Camera 1) 
    min_row max_row min_col max_col (1)
    fx fy cx cy (2)
    distortion params (3)
    3x3 Rotation matrix R (4, 5, 6)
    3x1 translation t (7)
    (Such that a world point in the camera coordinate frame is given by p' = Rp + t) 
    (Such that a project point for a perfect pinhole camera with no distortion is u = fx* p'.x/p'.zworld point in the camera coordinate frame is given by p' = Rp + t) 
    (Camera 2)...
    ...
    (Camera num_cameras)

    return: {"cam_0": {"fx_fy_cx_cy": np.array(1,3),
            "rotation": np.array(3,3),
            "translation": np.array(1,3)},
            "cam_1": {"fx_fy_cx_cy": np.array(1,3),
            "rotation": np.array(3,3),
            "translation": np.array(1,3)},
            ...
            }
    """
    calibration_dict = {}

    with open(path,'r') as file:
        for index, line in enumerate(file):
            if index == 0:
                num_cameras = line.split()
                print("This file contains calibration info for {} cameras.".format(num_cameras[0]))
                for c_i in range(int(num_cameras[0])):
                    cam_id = "cam_"+str(c_i)
                    calibration_dict[cam_id] = {}

            elif index % 7 == 2: #fx fy cx cy (2)
                cam_id = "cam_"+str(index//7)
                f_mat = np.zeros((1, 4))
                f_mat = np.float32(line.split())
                calibration_dict[cam_id]["fx_fy_cx_cy"] = f_mat
           
            elif index % 7 == 4: #3x3 Rotation matrix R (4, 5, 6)
                rot_mat = np.zeros((3, 3))
                rot_mat[0, :] = np.float32(line.split())
            elif index % 7 == 5: #3x3 Rotation matrix R (4, 5, 6)
                rot_mat[1, :] = np.float32(line.split())
            elif index % 7 == 6: #3x3 Rotation matrix R (4, 5, 6)
                cam_id = "cam_"+str(index//7)
                rot_mat[2, :] = np.float32(line.split())
                calibration_dict[cam_id]["rotation"] = rot_mat
            
            elif index % 7 == 0: #3x1 translation t (7)
                cam_id = "cam_"+str(index//7-1)
                t_mat = np.zeros((1, 3))
                t_mat[0, :] = np.float32(line.split())
                calibration_dict[cam_id]["translation"] = t_mat
            else:
                pass
    
    return calibration_dict

def read_global_pos(path:str)->np.ndarray:
    
    """
    This func read global_pos file and save for each frame global coord of the following IMU
    
    Head	Head
    Sternum	Spine3
    Pelvis	Hips
    L_UpArm	LeftArm
    R_UpArm	RightArm
    L_LowArm	LeftForeArm
    R_LowArm	RightForeArm
    L_UpLeg	LeftUpLeg
    R_UpLeg	RightUpLeg
    L_LowLeg	LeftLeg
    R_LowLeg	RightLeg
    L_Foot	LeftFoot
    R_Foot	RightFoot

    input: file path
    return: np.array with shape(frame_num, 12, 3)
    """

    target_list = ['Head','Spine3', 'Hips', 'LeftArm', 'RightArm', 'LeftForeArm','RightForeArm', 'LeftUpLeg',\
        'RightUpLeg', 'LeftLeg', 'RightLeg', 'LeftFoot', 'RightFoot']
    
    with open(path,'r') as file:
        frame_num = len(file.readlines())-1
        glob_pos = np.zeros((frame_num, len(target_list), 3))
        file.close()
    
    with open(path,'r') as file:    
        for index, line in enumerate(file):
            if index == 0:
                header = line.split()
                target_id = [header.index(i) for i in target_list]
            else:
                j = 0
                for i in target_id:
                    glob_pos[index-1, j, :] = np.float32(line.split())[[int(3*i+0), int(3*i+1), int(3*i+2)]]
                    j += 1
        file.close()
    return glob_pos

