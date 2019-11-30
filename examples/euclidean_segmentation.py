# -*- coding: utf-8 -*-
import pcl
import numpy as np
import pcl.pcl_visualization


def main():
    cloud = pcl.load(
            './examples/pcldata/tutorials/table_scene_lms400.pcd')
    print("cloud points : " + str(cloud.size))

    vg = cloud.make_voxel_grid_filter()
    vg.set_leaf_size(0.01, 0.01, 0.01)
    cloud_filtered = vg.filter()
    tree = cloud_filtered.make_kdtree()

    segment = cloud_filtered.make_EuclideanClusterExtraction()
    segment.set_ClusterTolerance(0.02)
    segment.set_MinClusterSize(100)
    segment.set_MaxClusterSize(25000)
    segment.set_SearchMethod(tree)
    cluster_indices = segment.Extract()

    cloud_cluster = pcl.PointCloud()

    # print('cluster_indices : ' + str(cluster_indices.count) + " count.")
    cloud_cluster = pcl.PointCloud()
    for j, indices in enumerate(cluster_indices):
        # print('indices = ' + str(len(indices)))
        points = np.zeros((len(indices), 3), dtype=np.float32)
        for i, indice in enumerate(indices):
            points[i][0] = cloud_filtered[indice][0]
            points[i][1] = cloud_filtered[indice][1]
            points[i][2] = cloud_filtered[indice][2]

        cloud_cluster.from_array(points)



if __name__ == "__main__":
    # import cProfile
    # cProfile.run('main()', sort='time')
    main()
