#!/usr/bin/env python

import time
import math

import numpy as np
import pcl
import pcl.pcl_visualization

from pcl_helper import get_color_list
from pcl_helper import rgb_to_float
from filtering_helper import do_ransac_plane_segmentation
from clustering import get_clusters

def main():
    cloud_filtered = pcl.load('/python-pcl/apollo_scape_pcd/333.pcd')
    print("cloud points : " + str(cloud_filtered.size))

    LEAF_SIZE = 0.09

    # vg = cloud_filtered.make_voxel_grid_filter()
    # vg.set_leaf_size(LEAF_SIZE, LEAF_SIZE, LEAF_SIZE)
    # cloud_filtered = vg.filter()
    # print('point size after voxel_grid_filter: ' + str(cloud_filtered.size))
    # cloud_filtered = pcl.PointCloud(cloud_filtered_blob.to_array())
    # print('PointCloud after filtering: ' +
    #       str(cloud_filtered.width * cloud_filtered.height) + ' data points.')

    stat_filter = cloud_filtered.make_statistical_outlier_filter()
    stat_filter.set_mean_k(100)
    stat_filter.set_std_dev_mul_thresh(2.0)
    cloud_filtered = stat_filter.filter()
    print('point size after statistical_outlier_filter: ' + str(cloud_filtered.size))

    points = []
    for i in range(cloud_filtered.size):
        # Radius filter
        r = math.sqrt(cloud_filtered[i][0]*cloud_filtered[i][0] + cloud_filtered[i][1]*cloud_filtered[i][1])
        # ROI filter Passthrough filter
        if cloud_filtered[i][2] > -1.55 and cloud_filtered[i][2] < 2.5 and r < 10.0:
            points.append([cloud_filtered[i][0], cloud_filtered[i][1], cloud_filtered[i][2]])

    cloud_2d = pcl.PointCloud()
    cloud_2d.from_list(points)

    # ransac plane segmentation
    # plane_cloud, cloud_2d = do_ransac_plane_segmentation(cloud_2d, max_distance = 0.01)

    # print('object_cloud size %s' % cloud_2d.size)
    # print('plane_cloud size %s' % plane_cloud.size)

    # gray_visualizer(cloud_2d)
    # gray_visualizer(plane_cloud)

    print("cloud_2d points : " + str(cloud_2d.size))
    # pcl.save(cloud_2d, 'cloud_2d'+str(time.time())+'.pcd')
    # exit(0)

    cluster_indices = get_clusters(cloud_2d, tolerance = 0.65, min_size = 50, max_size = 3500)

    print('cluster_indices : ' + str(len(cluster_indices)) + ' count.')
    cluster_color = get_color_list(len(cluster_indices))
    print(cluster_color)

    color_cluster_point_list = []
    for j, indices in enumerate(cluster_indices):
        cluster_points = []
        for i, indice in enumerate(indices):
            cluster_points.append([
                cloud_2d[indice][0],
                cloud_2d[indice][1],
                cloud_2d[indice][2],
                rgb_to_float(cluster_color[j])
                ])

        print('cluster size:' + str(len(cluster_points)))
        # cluster_cloud = pcl.PointCloud_PointXYZRGB()
        # cluster_cloud.from_list(cluster_points)
        # pcl.save(cluster_cloud, str(j) + '.pcd')
        color_cluster_point_list.append(cluster_points)

    #Create new cloud containing all clusters, each with unique color
    print('color_cluster_point_list size :' + str(len(color_cluster_point_list)))

    # if len(color_cluster_point_list) > 0:
    #     viewer = pcl.pcl_visualization.CloudViewing('3D Viewer')
    #     cluster_cloud = pcl.PointCloud_PointXYZRGB()
    #     for cluster_index, j in enumerate(color_cluster_point_list):
    #         cluster_cloud.resize(0)
    #         cluster_cloud.from_list(j)
    #         pcl.save(cluster_cloud, str(cluster_index) + '.pcd')
    #         viewer.ShowColorCloud(cluster_cloud,  b'cloud')

    #     v = True
    #     while v:
    #         v = not(viewer.WasStopped())
            # viewer.SpinOnce()


def color_visualizer(cloud):
    if isinstance(cloud, pcl.PointCloud):
        viewer = pcl.pcl_visualization.PCLVisualizering('3D Viewer')
        pccolor = pcl.pcl_visualization.PointCloudColorHandleringCustom(
        cloud, 255, 255, 255)
        # viewer
        viewer.AddPointCloud_ColorHandler(cloud, pccolor)
    elif isinstance(cloud, pcl.PointCloud_PointXYZRGB):
        viewer = pcl.pcl_visualization.CloudViewing('3D Viewer')
        viewer.ShowColorCloud(cloud)

    v = True
    while v:
        v = not(viewer.WasStopped())
        # viewer.SpinOnce()
        time.sleep(0.01)


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
        # sleep(0.01)


if __name__ == "__main__":
    # import cProfile
    # cProfile.run('main()', sort='time')
    main()
