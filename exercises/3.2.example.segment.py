#!/usr/bin/env python

import time

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
    
    # cloud_2d = cloud_filtered
    # for i in range(cloud_filtered.size):
    #     cloud_2d[i][1]=0
    # tree = cloud_2d.make_kdtree()
    tree = cloud_filtered.make_kdtree()
    
    segment = cloud_filtered.make_EuclideanClusterExtraction()
    segment.set_ClusterTolerance(0.2)
    segment.set_MinClusterSize(1000)
    segment.set_MaxClusterSize(25000)
    segment.set_SearchMethod(tree)
    cluster_indices = segment.Extract()

    # print(cluster_indices)

    print('cluster_indices : ' + str(len(cluster_indices)) + " count.")
    cluster_color = get_color_list(len(cluster_indices))
    print(cluster_color)

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

    visualizer(cluster_cloud)


def visualizer(cloud):
    viewer = pcl.pcl_visualization.CloudViewing('3D Viewer')
    viewer.ShowColorCloud(cloud)

    v = True
    while v:
        v = not(viewer.WasStopped())
        # viewer.SpinOnce()
        time.sleep(0.01)


if __name__ == "__main__":
    # import cProfile
    # cProfile.run('main()', sort='time')
    main()
