import numpy as np
import open3d as o3d
#旋转算法，输入是旋转半径R（旋转中心z值），手镯半径R_shouzhuo，还有xyz最大最小值
def rotate_point_cloud(pcd, best_z,R,R_shouzhuo,x_max,x_min,y_max,y_min,z_max,z_min):

    r = R
    # 确定旋转轴线
    axis = np.array([1, 0, 0])
    axis = axis / np.linalg.norm(axis)

    # 获取点云数据并平移 z 坐标
    points = np.asarray(pcd.points)
    # points[:, 2] = points[:, 2] - best_z
    num_points = points.shape[0]
    # print("点云点数:", num_points)
    print(f"x最大{x_max},x最小{x_min},y最大{y_max},y最小{y_min},z最大{z_max},z最小{z_min}")
    # 计算每个点的旋转角度
    # distances = calculate_path_length_vectorized(points, center_line)  # 向量化计算路径长度
    # angles=(points[:,1]-y_min)/(points[:,2]+R)
    angles = (points[:, 1] - y_min) / R_shouzhuo
    angles_rad=angles
    print("第一个角度",angles_rad[0:2],"和最后一个角度",angles_rad[-2:])
    K = np.array([
        [0, -axis[2], axis[1]],
        [axis[2], 0, -axis[0]],
        [-axis[1], axis[0], 0]
    ])
    I = np.eye(3)  # 单位矩阵

    # 向量化旋转
    sin_a = np.sin(angles_rad)
    cos_a = np.cos(angles_rad)
    rot_matrices = I + sin_a[:, None, None] * K + (1 - cos_a[:, None, None]) * np.dot(K, K)

    # 点到旋转中心的向量,旋转中心是（point_i_x,y_min,-R）
    points_to_axis = points - np.array([points[:, 0], np.full(num_points, y_min), np.full(num_points, r)]).T
    points_to_axis[:,1]=y_min

    # 旋转点
    rotated_points_to_axis = np.einsum('ijk,ik->ij', rot_matrices, points_to_axis)
    rotated_points = rotated_points_to_axis + np.array([points[:, 0], np.full(num_points, y_min), np.full(num_points, r)]).T
    rotated_pcd = o3d.geometry.PointCloud()
    rotated_pcd.points = o3d.utility.Vector3dVector(rotated_points)
    # 计算旋转后点云的边界
    zmax = np.max(rotated_points[:, 2])
    zmin = np.min(rotated_points[:, 2])
    ymax = np.max(rotated_points[:, 1])
    ymin = np.min(rotated_points[:, 1])
    xmax = np.max(rotated_points[:, 0])
    xmin = np.min(rotated_points[:, 0])
    print(f"z方向最大差值{zmax - zmin},y方向最大差值{ymax - ymin},x方向最大差值{xmax - xmin}")
    return rotated_pcd