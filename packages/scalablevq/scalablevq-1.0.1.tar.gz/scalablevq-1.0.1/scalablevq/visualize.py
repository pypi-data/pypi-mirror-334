from typing import List, Tuple
import open3d as o3d
import numpy as np
import torch


def build_geometries(cluster_centers: torch.Tensor, layerized_cluster_centers: torch.Tensor, cluster_tree: List[Tuple[int, int]]):
    pcd_cluster_centers = o3d.geometry.PointCloud()
    pcd_cluster_centers.points = o3d.utility.Vector3dVector(cluster_centers)
    pcd_cluster_centers.colors = o3d.utility.Vector3dVector(np.array([[0, 0, 0]]*cluster_centers.shape[0]))

    leaf_n = cluster_centers.shape[0]
    lines = [(i+leaf_n, t[0]) for i, t in enumerate(cluster_tree)] + [(i+leaf_n, t[1]) for i, t in enumerate(cluster_tree)]
    line_set_layerized_cluster_centers = o3d.geometry.LineSet(
        points=o3d.utility.Vector3dVector(layerized_cluster_centers),
        lines=o3d.utility.Vector2iVector(lines),
    )
    geometries = [
        pcd_cluster_centers,
        line_set_layerized_cluster_centers
    ]
    return geometries


def visualize_layers(cluster_centers: torch.Tensor, layerized_cluster_centers: torch.Tensor, cluster_tree: List[Tuple[int, int]], data: torch.Tensor = None):
    geometries = build_geometries(cluster_centers, layerized_cluster_centers, cluster_tree)
    if data is not None:
        pcd_data = o3d.geometry.PointCloud()
        pcd_data.points = o3d.utility.Vector3dVector(data)
        pcd_data.colors = o3d.utility.Vector3dVector(data)
        geometries.append(pcd_data)
    o3d.visualization.draw_geometries(geometries)
