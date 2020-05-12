#!/usr/bin/env python

import time
import math

import numpy as np
import pcl
import pcl.pcl_visualization

from pcl_helper import get_color_list
from filtering_helper import do_ransac_plane_segmentation
from clustering import get_clusters

def main():
    cloud_filtered = pcl.load('/python-pcl/apollo_scape_pcd/333.pcd')
    print("cloud points : " + str(cloud_filtered.size))

    # Voxel grid filter
    vg = cloud_filtered.make_voxel_grid_filter()
    LEAF_SIZE = 0.09
    vg.set_leaf_size(LEAF_SIZE, LEAF_SIZE, LEAF_SIZE)
    cloud_filtered = vg.filter()
    print('point size after voxel_grid_filter: ' + str(cloud_filtered.size))

    # Statistical_outlier_filter
    stat_filter = cloud_filtered.make_statistical_outlier_filter()
    stat_filter.set_mean_k(100)
    stat_filter.set_std_dev_mul_thresh(2.0)
    cloud_filtered = stat_filter.filter()
    print('point size after statistical_outlier_filter: ' + str(cloud_filtered.size))

    # Ransac for ground plane segmentation
    plane_cloud, cloud_filtered = do_ransac_plane_segmentation(cloud_filtered, max_distance = 0.2)

    print('object_cloud size: %s' % cloud_filtered.size)
    print('plane_cloud size: %s' % plane_cloud.size)
    pcl.save(plane_cloud, 'ground_points_'+str(time.time())+'.pcd')

    #gray_visualizer(cloud_filtered)
    #gray_visualizer(plane_cloud)
    #exit(0)
    points = []
    for i in range(cloud_filtered.size):
        # Ground plane filter
        # Please think here, why use parameter -1.55?
        # if cloud_filtered[i][2] > -1.55 and cloud_filtered[i][2] < 2.5:
        #    points.append([cloud_filtered[i][0], cloud_filtered[i][1], cloud_filtered[i][2]])

        # Radius and ROI Filter
        r = math.sqrt(cloud_filtered[i][0]*cloud_filtered[i][0] + cloud_filtered[i][1]*cloud_filtered[i][1])
        if r < 10.0:
            points.append([cloud_filtered[i][0], cloud_filtered[i][1], cloud_filtered[i][2]])

    cloud_input = pcl.PointCloud()
    cloud_input.from_list(points)

    print("cloud_input points : " + str(cloud_input.size))
    # pcl.save(cloud_input, 'cloud_input'+str(time.time())+'.pcd')
    # exit(0)

    cluster_indices = get_clusters(cloud_input, tolerance = 0.65, min_size = 30, max_size = 3500)

    print('cluster_indices : ' + str(len(cluster_indices)) + ' count.')
    cluster_color = get_color_list(len(cluster_indices))

    viewer = pcl.pcl_visualization.PCLVisualizering('3D Viewer')
    # color_cluster_point_list = []
    for j, indices in enumerate(cluster_indices):
        cluster_points = []
        min_x = 0
        max_x = 0
        min_y = 0
        max_y = 0
        min_z = 0
        max_z = 0
        for i, indice in enumerate(indices):
            cluster_points.append([
                cloud_input[indice][0],
                cloud_input[indice][1],
                cloud_input[indice][2]])
            if cloud_input[indice][0] < min_x: min_x = cloud_input[indice][0]
            if cloud_input[indice][1] < min_y: min_y = cloud_input[indice][1]
            if cloud_input[indice][2] < min_z: min_z = cloud_input[indice][2]

            if cloud_input[indice][0] > max_x: max_x = cloud_input[indice][0]
            if cloud_input[indice][1] > max_y: max_y = cloud_input[indice][1]
            if cloud_input[indice][2] > max_z: max_z = cloud_input[indice][2]
        print('cluster size:' + str(len(cluster_points)))
        cluster_cloud = pcl.PointCloud()
        cluster_cloud.from_list(cluster_points)
        # mass center
        # mass_center_point = pcl.PointCloud(min_x + (min_x+max_x)/2, min_y + (min_y+max_y)/2, min_z + (min_z+max_z)/2)
        # z_axis = pcl.PointCloud(min_x, min_y, min_z)
        # CLOUD RGB COLOR 
        r = int(cluster_color[j][0])
        g = int(cluster_color[j][1])
        b = int(cluster_color[j][2])
        cluster_pc_color = pcl.pcl_visualization.PointCloudColorHandleringCustom(
            cluster_cloud, r, g, b)
        pcl.save(cluster_cloud, str(j) + '.pcd')
        viewer.AddPointCloud_ColorHandler(cluster_cloud, cluster_pc_color, 'cloud_cluster:' + str(j))
        # viewer.AddCube(min_x, max_x, min_y, max_y, min_z, max_z, 1.0, 1.0, 1.0, 'cloud_cluster:' + str(j))
        # viewer.AddLine(mass_center_point, z_axis, 0.0, 0.0, 1.0, "minor eigen vector")

    v = True
    while v:
        v = not(viewer.WasStopped())
        viewer.SpinOnce()


def gray_visualizer(cloud):
    viewer = pcl.pcl_visualization.PCLVisualizering('3D Viewer')
    pccolor = pcl.pcl_visualization.PointCloudColorHandleringCustom(
        cloud, 255, 255, 255)

    # viewer
    viewer.AddPointCloud_ColorHandler(cloud, pccolor)

    v = True
    while v:
        v = not(viewer.WasStopped())
        viewer.SpinOnce()


if __name__ == "__main__":
    main()
