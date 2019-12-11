#!/usr/bin/env python

import time
import math

import numpy as np
import pcl
import pcl.pcl_visualization

from pcl_helper import get_color_list
from pcl_helper import rgb_to_float

def main():
    cloud = pcl.load('/python-pcl/apollo_scape_pcd/333.pcd')
    print("cloud points : " + str(cloud.size))

    LEAF_SIZE = 0.09

    vg = cloud.make_voxel_grid_filter()
    vg.set_leaf_size(LEAF_SIZE, LEAF_SIZE, LEAF_SIZE)
    cloud_filtered = vg.filter()
    print('point size after voxel_grid_filter: ' + str(cloud_filtered.size))
    # cloud_filtered = pcl.PointCloud(cloud_filtered_blob.to_array())
    # print('PointCloud after filtering: ' +
    #       str(cloud_filtered.width * cloud_filtered.height) + ' data points.')
    
    points = []
    for i in range(cloud_filtered.size):
        # Radius filter
        r = math.sqrt(cloud_filtered[i][0]*cloud_filtered[i][0] + cloud_filtered[i][1]*cloud_filtered[i][1])
        # Passthrough filter
        if cloud_filtered[i][2] > -1.5 and cloud_filtered[i][2] < 2.0 and r < 13.0:
            points.append([cloud_filtered[i][0], cloud_filtered[i][1], cloud_filtered[i][2]])

    cloud_2d = pcl.PointCloud()
    cloud_2d.from_list(points)
    # gray_visualizer(cloud_2d)

    print("cloud_2d points : " + str(cloud_2d.size))
    # pcl.save(cloud_2d, '/python-pcl/cloud_2d.pcd')
    # exit(0)

    tree = cloud_2d.make_kdtree()
    # tree = cloud_filtered.make_kdtree()
    
    segment = cloud_2d.make_EuclideanClusterExtraction()
    segment.set_ClusterTolerance(0.25)
    segment.set_MinClusterSize(750)
    segment.set_MaxClusterSize(3000)
    segment.set_SearchMethod(tree)
    cluster_indices = segment.Extract()

    print('cluster_indices : ' + str(len(cluster_indices)) + " count.")
    cluster_color = get_color_list(len(cluster_indices))

    color_cluster_point_list = []
    for j, indices in enumerate(cluster_indices):
        for i, indice in enumerate(indices):
            color_cluster_point_list.append([cloud_filtered[indice][0],
                                            cloud_filtered[indice][1],
                                            cloud_filtered[indice][2],
                                            rgb_to_float(cluster_color[j])
                                           ])

    #Create new cloud containing all clusters, each with unique color
    cluster_cloud = pcl.PointCloud_PointXYZRGB()
    cluster_cloud.from_list(color_cluster_point_list)

    if cluster_cloud.size > 0:
        color_visualizer(cluster_cloud)


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
