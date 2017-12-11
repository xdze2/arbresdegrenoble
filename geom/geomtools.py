import numpy as np

from scipy.spatial import Delaunay

import shapely.geometry as geometry
from shapely.ops import cascaded_union, polygonize



def get_coordsarray( points_deg ):
    """ Scale and offset the coords approximately to meter

        :param points_deg: list of tuple, coords (lat, lon) decimal deg
        :return: nd-array (n_points, n_dim), the inverse scaling function
    """
    points_deg = np.array( points_deg )
    center_deg = points_deg.mean( axis = 0 )

    R_Earth =  6371008  # meter
    scale_factor = np.pi/180*R_Earth

    points_m = (points_deg - center_deg)*scale_factor
    scale_back = lambda X: X/scale_factor + center_deg

    return points_m, scale_back



def add_contourpoints( points_list,  n_points = 5, r_cercle = 3 ):
    """ Ajoute des points virtuels autour des points pour donner
        une épaisseur au polygone

        :points_list: list of tuple, or nd-array
        :n_point = 5: int, nombre de points à ajouter
        :r_cercle = 3: float, distance au point centre
        :return: nd-array
    """

    thetas = np.linspace( 0, 2*np.pi, n_points+1 )[:-1]

    added_point = []
    for x, y in points_list:

        x_add = x + r_cercle * np.cos( thetas )
        y_add = y + r_cercle * np.sin( thetas )

        added_point.extend( zip( x_add, y_add ) )

    return np.array( added_point )



def get_polycoords( polygon, scale_back ):
    """ retourne la partie Geométrie du GeoJson pour l'objet polygon
        peut être un simple ou MultiPolygon
        - convertie les coords en degrée décimaux avec la fonction scale_back

        :polygon: Shaply polygon object (mutli or simple)
        :scale_back: scaling function to apply on coords

        :return: polygon type: MultiPolygon  or Polygon
                 list of the coords
    """

    if polygon.geom_type == 'MultiPolygon':

        all_coords = []
        for part in polygon.boundary:
            boundary_coords = part.coords
            boundary_coords = scale_back( np.array(boundary_coords) ).tolist()
            all_coords.append( (boundary_coords, )  ) # supplementary tuple ??

        coordslist = all_coords

    elif polygon.geom_type == 'Polygon':
        boundary_coords = polygon.boundary.coords
        coordslist = scale_back( np.array(boundary_coords) ).tolist()

    return polygon.geom_type, coordslist



def alpha_shape(points, r_critic):
    """ Compute the alpha shape (concave hull) of a set of points.

    the original code come from :
    http://nbviewer.jupyter.org/github/dwyerk/boundaries/blob/master/concave_hulls.ipynb
    https://github.com/dwyerk/boundaries

    # Rq: Delaunay ne marche pas avec les coords en degrée dec. ...

    @param points: Iterable container of points. ( (x1, y1), (x2, y2), ... )
    @param r_critic: critical radius (alpha value) to influence the gooeyness
                  of the border. Smaller numbers don't fall inward as much
                  as larger numbers. Too large, and you lose everything!
    """
    if len(points) < 4:
        # When you have a triangle, there is no sense in computing an alpha
        # shape.
        return geometry.MultiPoint(list(points)).convex_hull

    def add_edge(edges, edge_points, coords, i, j):
        """Add a line between the i-th and j-th points, if not in the list already"""
        if (i, j) in edges or (j, i) in edges:
            # already added
            return
        edges.add( (i, j) )
        edge_points.append(coords[ [i, j] ])

    coords = np.array( points )

    tri = Delaunay(coords)
    edges = set()
    edge_points = []
    # loop over triangles:
    # ia, ib, ic = indices of corner points of the triangle
    for ia, ib, ic in tri.vertices:
        pa = coords[ia]
        pb = coords[ib]
        pc = coords[ic]

        # Lengths of sides of triangle
        a = np.sqrt((pa[0]-pb[0])**2 + (pa[1]-pb[1])**2)
        b = np.sqrt((pb[0]-pc[0])**2 + (pb[1]-pc[1])**2)
        c = np.sqrt((pc[0]-pa[0])**2 + (pc[1]-pa[1])**2)

        # Semiperimeter of triangle
        s = (a + b + c)/2.0

        # Area of triangle by Heron's formula
        area = np.sqrt(s*(s-a)*(s-b)*(s-c))
        circum_r = a*b*c/(4.0*area)

        # Here's the radius filter.
        #print circum_r
        if circum_r < r_critic:
            add_edge(edges, edge_points, coords, ia, ib)
            add_edge(edges, edge_points, coords, ib, ic)
            add_edge(edges, edge_points, coords, ic, ia)

    m = geometry.MultiLineString(edge_points)
    triangles = list(polygonize(m))
    return cascaded_union(triangles), edge_points




from descartes import PolygonPatch
import matplotlib.pyplot as plt

def plot_polygon(polygon):
    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(111)
    margin = .3

    x_min, y_min, x_max, y_max = polygon.bounds

    ax.set_xlim([x_min-margin, x_max+margin])
    ax.set_ylim([y_min-margin, y_max+margin])
    patch = PolygonPatch(polygon, fc='#999999', ec='#000000', fill=True, zorder=-1)
    ax.add_patch(patch)
    return fig
