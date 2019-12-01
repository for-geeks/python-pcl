# -*- coding: utf-8 -*-
import pcl
import numpy as np
import pcl.pcl_visualization


def main():
    cloud = pcl.load('/python-pcl/examples/pcldata/tutorials/table_scene_lms400.pcd')
    print("cloud points : " + str(cloud.size))

    vg = cloud.make_voxel_grid_filter()
    vg.set_leaf_size(0.0029, 0.0029, 0.0029)
    cloud_filtered = vg.filter()
    print('point size after voxel_grid_filter: ' + str(cloud_filtered.size))
    # cloud_filtered = pcl.PointCloud(cloud_filtered_blob.to_array())
    # print('PointCloud after filtering: ' +
    #       str(cloud_filtered.width * cloud_filtered.height) + ' data points.')
    tree = cloud_filtered.make_kdtree()

    segment = cloud_filtered.make_EuclideanClusterExtraction()
    segment.set_ClusterTolerance(0.005)
    segment.set_MinClusterSize(100)
    segment.set_MaxClusterSize(25000)
    segment.set_SearchMethod(tree)
    cluster_indices = segment.Extract()

    # print(cluster_indices)

    print('cluster_indices : ' + str(len(cluster_indices)) + " count.")
    cloud_cluster = pcl.PointCloud()
    for j, indices in enumerate(cluster_indices):
        # print('indices = ' + str(len(indices)))
        points = np.zeros((len(indices), 3), dtype=np.float32)
        for i, indice in enumerate(indices):
            points[i][0] = cloud_filtered[indice][0]
            points[i][1] = cloud_filtered[indice][1]
            points[i][2] = cloud_filtered[indice][2]

        cloud_cluster.from_array(points)
        # print(points)

    # print(cloud_cluster)

    # for point in enumerate(cloud_cluster):
        # print(point)



if __name__ == "__main__":
    # import cProfile
    # cProfile.run('main()', sort='time')
    main()
