from math import sqrt

def calc_error_from_list_of_points_in_pixel(pointlist_1, pointlist_2):
    error_list = []
    for p1, p2 in zip(pointlist_1, pointlist_2):
        if p1[0] != p2[0]:
            raise Exception("Numbers of compared Reference Points do not fit! Please check Input! Error List can't be calculated.")
        error_x = p1[1] - p2[1]
        error_y = p1[2] - p2[2]
        error_list.append([error_x, error_y])
    return error_list
    
def calc_rmse_in_pixel_from_error_list(error_list_in_pixel):
    rmse_in_pixel = 0
    for point in error_list_in_pixel:
        error_per_point = sqrt(point[0] * point[0] + point[1] * point[1])
        rmse_in_pixel += error_per_point
    rmse_in_pixel = rmse_in_pixel / len(error_list_in_pixel)
    return rmse_in_pixel

def calc_rmse_in_meter(rmse_in_pixel, scale_factor):
    rmse_in_meter = rmse_in_pixel / scale_factor
    return rmse_in_meter

if __name__ == "__main__":
    pointlist_refimg = [[1, 1494.91, 2993.0], [2, 1493.3, 2669.95], [3, 1492.5, 2343.97], [4, 1492.9, 2018.5], [5, 1492.6, 1694.5], [6, 1492.4, 1362.9], [7, 1492.5, 1031.0]]
    pointlist_ground_floor = [[1, 1492.5, 2988.4], [2, 1491.5, 2669.5], [3, 1490.5, 2346.7], [4, 1490.5, 2027.4], [5, 1490.5, 1708.5], [6, 1489.8, 1373.8], [7, 1489.0, 1029.6]]

    pointlist_refimg_second_floor = [[2, 1493.3, 2669.95], [3, 1492.5, 2343.97], [4, 1492.9, 2018.5], [5, 1492.6, 1694.5], [6, 1492.4, 1362.9], [7, 1492.5, 1031.0]]
    pointlist_second_floor = [[2, 1495.5, 2668.5], [3, 1493.8, 2339.3], [4, 1494.3, 2014.36], [5, 1493.2, 1691.75], [6, 1494.3, 1359.4], [7, 1495.3, 1031.1]]

    scale_factor = 65.4 # pix per meter

    ground_floor_error_list = calc_error_from_list_of_points_in_pixel(pointlist_refimg, pointlist_ground_floor)
    second_floor_error_list = calc_error_from_list_of_points_in_pixel(pointlist_refimg_second_floor, pointlist_second_floor)

    ground_floor_rmse_pix = calc_rmse_in_pixel_from_error_list(ground_floor_error_list)
    second_floor_rmse_pix = calc_rmse_in_pixel_from_error_list(second_floor_error_list)

    ground_floor_rmse_meter = calc_rmse_in_meter(ground_floor_rmse_pix, scale_factor)
    second_floor_rmse_meter = calc_rmse_in_meter(second_floor_rmse_pix, scale_factor)

    print("Ground Floor:")
    print(ground_floor_error_list)
    print(ground_floor_rmse_pix)
    print("RMSE in Meter: {:f}".format(ground_floor_rmse_meter))
    print("Second Floor:")
    print(second_floor_error_list)
    print(second_floor_rmse_pix)
    print("RMSE in Meter: {:f}".format(second_floor_rmse_meter))