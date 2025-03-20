import numpy as np
import plotly.graph_objects as go


def plot_point_cloud(pts, **kwargs):
    return go.Scatter3d(x=pts[:, 0], y=pts[:, 1], z=pts[:, 2], mode="markers", **kwargs)


def plot_mesh(mesh, pos=None, rot=None, color="lightblue", opacity=1.0, name="mesh", **kwargs):
    verts = mesh.vertices
    if rot is not None:
        verts = np.matmul(rot, verts.T).T
    if pos is not None:
        verts = verts + pos[None]
    return go.Mesh3d(
        x=verts[:, 0],
        y=verts[:, 1],
        z=verts[:, 2],
        i=mesh.faces[:, 0],
        j=mesh.faces[:, 1],
        k=mesh.faces[:, 2],
        color=color,
        opacity=opacity,
        name=name,
        showlegend=True,
    )
