import cv2
import numpy as np
from shapely.geometry import box, Polygon
from scipy.spatial import transform as scipy_transform

from calib3d import Calib as Calib3d
from calib3d import Point3D, Point2D, compute_rotation_matrix
from calib3d.draw import visible_segment

class Calib(Calib3d):
    def definition(self, distance):
        return self.K[0,0]/distance

    def visible_edge(self, edge):
        return visible_segment(self, edge[0], edge[1])

    def displacement_map(self):
        w, h = self.width, self.height
        points2D = Point2D(np.stack(np.meshgrid(np.arange(w), np.arange(h))).reshape(2, w*h))
        return np.linalg.norm(points2D - self.rectify(points2D), axis=0).reshape(h, w)

    def definition_map(self, distance):
        """ Returns a map of definition [px/<distance-unit>] at a given distance from the camera
        """
        w, h = self.width+2, self.height+2
        assert w < 5000 and h < 5000, "Invalid image dimensions"
        points2D = Point2D(np.stack(np.meshgrid(np.arange(w)-1, np.arange(h)-1)).reshape(2, w*h))
        X = Point2D(self.Kinv@self.rectify(points2D).H).reshape(2, h, w)*distance
        dist_v = (X[:, :-2, 1:-1]-X[:, 2:, 1:-1])/2
        dist_h = (X[:, 1:-1, :-2]-X[:, 1:-1, 2:])/2
        return 2/(np.linalg.norm(dist_h, axis=0) + np.linalg.norm(dist_v, axis=0))

    def get_region_visible_corners_2d(self, points_3d: Point3D, approximate_curve_by_N_segments=10):
        """Return a list of corner points defining the 2D boundaries of a specific 3D region on the image space

        Args:
            points_3d ([type]): [description]
            approximate_curve_by_N_segments (int, optional): [description]. Defaults to 10.

        Returns:
            List[Tuple(int, int)]: a list of 2D coordinates of the corner points of a specific 3D region on the image space
        """

        # Construct the polygon defining the boundaries of the 3D region and projects it, considering the lens distorsion (3D straight lines might be curves on the image)
        region_3d_coords = points_3d.close().linspace(approximate_curve_by_N_segments+1)
        region_2d_coords = self.project_3D_to_2D(region_3d_coords)
        any_coord_outside_img_boundaries = np.any(region_2d_coords < 0) or \
                                           np.any(region_2d_coords.x >= self.width) or \
                                           np.any(region_2d_coords.y >= self.height)
        if not any_coord_outside_img_boundaries:
            return region_2d_coords

        # Restrict the 2D region polygon to the image space boundaries
        img_corners = box(minx=0, miny=0, maxx=self.width, maxy=self.height)
        region_corners = Polygon([r.to_int_tuple() for r in region_2d_coords])
        region_polygon_restricted_to_img_space = region_corners.intersection(img_corners)

        if region_polygon_restricted_to_img_space:
            return Point2D(np.array(region_polygon_restricted_to_img_space.exterior.coords).T)
        else:
            return Point2D(np.empty(shape=(2, 0), dtype=float))

def crop_around_center(image, width, height):
    """ Given a NumPy / OpenCV 2 image, crops it to the given width and height,
        around it's centre point
    """

    image_size = (image.shape[1], image.shape[0])
    image_center = (int(image_size[0] * 0.5), int(image_size[1] * 0.5))

    if width > image_size[0]:
        width = image_size[0]

    if height > image_size[1]:
        height = image_size[1]

    x1 = int(image_center[0] - width * 0.5)
    x2 = int(image_center[0] + width * 0.5)
    y1 = int(image_center[1] - height * 0.5)
    y2 = int(image_center[1] + height * 0.5)

    return image[y1:y2, x1:x2]


class PanoramicStitcher():
    def __init__(self, calibs, output_shape, f=1000, target=None):
        w, h = output_shape
        C = np.mean([calib.C for calib in calibs], axis=0)
        if target is not None:
            R = compute_rotation_matrix(target, C)
        else:
            q = np.mean([scipy_transform.Rotation.from_matrix(calib.R).as_quat() for calib in calibs], axis=0)
            R = scipy_transform.Rotation.from_quat(q/np.linalg.norm(q)).as_matrix()

        T = -R@C
        K = np.array([[f, 0, w/2],
                      [0, f, h/2],
                      [0, 0,  1 ]])
        self.camera = Calib(K=K, T=T, R=R, width=w, height=h)
        self.calibs = calibs

        self.width, self.height = w, h = self.camera.width, self.camera.height
        points2D = Point2D(np.stack(np.meshgrid(np.arange(w),np.arange(h))).reshape((2,w*h)))
        points3D = self.camera.project_2D_to_3D(points2D, Y=0)

        def lookuptable(calib, points3D):
            corners = self.camera.project_3D_to_2D(calib.project_2D_to_3D(Point2D([calib.w, calib.w, 0, 0], [calib.h, 0, 0, calib.h]), Y=0))
            center = self.camera.project_3D_to_2D(calib.project_2D_to_3D(Point2D([calib.w/2], [calib.h/2]), Y=0))
            max_radius = max(np.linalg.norm(corners-center, axis=0))

            output_indices = np.where(np.all([
                calib.projects_in(points3D),
                np.linalg.norm(points2D - center, axis=0) <= max_radius # prevents strong distortion to project to the other side of the image
            ], axis=0))[0] # indices of output pixels that project to calib (and not further than radius away from center of projection)
            input_indices = calib.project_3D_to_2D(points3D[:,output_indices]).astype(np.int32) # output pixels that project to calib
            ih, iw = calib.height, calib.width
            distances = np.min(np.stack(np.meshgrid(iw//2-np.abs(np.arange(-iw//2, iw//2)), ih//2-np.abs(np.arange(-ih//2, ih//2)))), axis=0)
            return input_indices, output_indices, distances[input_indices.y, input_indices.x]
        self.lookuptables = [lookuptable(calib, points3D) for calib in self.calibs]

    def __call__(self, images):
        assert len(set([(shape:=image.shape) for image in images])) == 1, "All images must have the same shape"
        assert len(set([(dtype:=image.dtype) for image in images])) == 1, "All images must have the same dtype"
        c = shape[-1] if len(shape) == 3 else 1

        outputs = np.zeros((len(images), self.height*self.width, c))
        weights = np.zeros((len(images), self.height*self.width))
        for i, (input_indices, output_indices, weight) in enumerate(self.lookuptables):
            outputs[i, output_indices] = np.reshape(images[i][input_indices.y, input_indices.x], (-1, c))
            weights[i, output_indices] = weight

        mask = np.any(weights != 0, axis=0)
        weights[:,mask] = weights[:,mask]/np.sum(weights[:,mask], axis=0)
        result = np.ones((self.height*self.width, c))*np.nan
        result[mask] = np.sum(outputs[:, mask]*weights[:,mask,None], axis=0)
        return np.squeeze((result.reshape((self.height, self.width, c))).astype(dtype))

