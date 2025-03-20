from .axis import Axis

from mhealpy import HealpixBase

import numpy as np

from astropy.coordinates import (SkyCoord,
                                 BaseRepresentation,
                                 UnitSphericalRepresentation)
from astropy.coordinates import concatenate_representations
from astropy.coordinates import concatenate as concatenate_coords

import astropy.units as u

class HealpixAxis(Axis, HealpixBase):
    """
    2D spherical axis using a HEALPix grid

    Args:
        nside (int): Alternatively, you can specify the edges for all pixels.
        scheme (str): Healpix scheme. Either 'RING', 'NESTED'.
        edges (array): List of bin edges in terms of HEALPix pixels. Must be integers. Default:
            all pixels, one pixel per bin.
        coordsys (BaseFrameRepresentation or str): Instrinsic coordinates of the map.
            Either ‘G’ (Galactic), ‘E’ (Ecliptic) , ‘C’ (Celestial = Equatorial) or any other
            coordinate frame recognized by astropy.
    """

    def __init__(self,
                 nside = None,
                 scheme='ring',
                 edges=None,
                 coordsys = None,
                 *args, **kwargs):

        if nside is None and edges is not None:

            edges = np.asarray(edges)

            npix = len(edges)-1

            if not np.array_equal(edges, np.arange(npix + 1)):
                raise ValueError("If you don't specify nside, edges must include all pixels. Use integers.")

            HealpixBase.__init__(self,
                                 npix = npix,
                                 scheme = scheme,
                                 coordsys = coordsys)

        else:

            if nside is None:
                raise ValueError("Specify either nside or edges")

            HealpixBase.__init__(self,
                                 nside = nside,
                                 scheme = scheme,
                                 coordsys = coordsys)

            if edges is None:
                # Default to full map
                edges = np.arange(self.npix + 1)

        super().__init__(edges, *args, **kwargs)

        # additional sanity checks specific to HealpixAxis edges
        self._validate_healpix_edges(self.edges)

    def _copy(self, edges=None, copy_edges=True):
        """Make a deep copy of a HealpixAxis, optionally
        replacing edge array. (The superclass's _copy
        method handles edge replacement.)
        """

        new = super()._copy(edges, copy_edges)

        if edges is not None: # extra sanity checks
            self._validate_healpix_edges(new._edges)

        HealpixBase.__init__(new,
                             nside = self.nside,
                             scheme = self.scheme,
                             coordsys = self.coordsys)

        return new

    def _validate_healpix_edges(self, edges):

        super()._validate_edges(edges)

        # Check it corresponds to pixels
        if edges.dtype.kind not in 'ui':
            raise ValueError("HeapixAxis needs integer edges")

        if edges[0] < 0 or edges[-1] > self.npix+1:
            raise ValueError("Edges must lie between 0 and total number of pixels")

    def __eq__(self, other):
        return super().__eq__(other) and self.conformable(other)

    def __getitem__(self, key):

        new = super().__getitem__(key)

        HealpixBase.__init__(new,
                             nside = self.nside,
                             scheme = self.scheme,
                             coordsys = self.coordsys)

        return new

    def find_bin(self, value):
        """
        Find the bin number that corresponds to a given pixel or coordinate.

        Args:
            value (int, SkyCoord, BaseRepresentation): Pixel or coordinate

        Returns:
            int
        """

        value = self._standardize_skycoord_array(value)

        if isinstance(value, (SkyCoord, BaseRepresentation)):
            # Transform first from coordinates to pixel
            value = self.ang2pix(value)

        return super().find_bin(value)

    def _standardize_skycoord_array(self, value):
        """
        Transform arrays of astropy's SkyCoords or BaseRepresentation
        to individual objects with arrays inside
        """

        # Standardize arrays of SkyCoord or BaseRepresentation to
        # classes with arrays as internal elements
        if isinstance(value, (np.ndarray, tuple, list)):

            # Astropy's concatenation function doesn't work with
            # single elements for some reason
            if isinstance(value, np.ndarray) and not value.shape:
                # Singleton
                value = value.item()

            elif np.shape(value) == (1,):
                # Single element. Keep same shape inside
                value = np.reshape(value[0], (1,))

            elif isinstance(value[0], SkyCoord):
                # Multiple SkyCoord
                value = concatenate_coords(value)

            elif isinstance(value[0], BaseRepresentation):
                # Multiple BaseRepresentation
                value = concatenate_representations(value)

        return value

    def interp_weights(self, value):
        """
        Return the 4 closest pixels on the two rings above and below
        the location and corresponding weights. Weights are provided
        for bilinear interpolation along latitude and longitude

        Args:
        value (int, SkyCoord, BaseRepresentation):
           Coordinate to interpolate. When passing an integer, the
           center of the corresponding pixel will be used.

        Returns:
        bins (int array):
            Array of bins to be interpolated
        weights (float array):
            Corresponding weights.

        """

        value = self._standardize_skycoord_array(value)

        # Interp
        if isinstance(value, (SkyCoord, BaseRepresentation)):

            # Specific location

            pixels, weights = self.get_interp_weights(value)

            return self.find_bin(pixels), weights

        else:

            # Pixel. Get the center.

            if self.coordsys is None:
                lon, lat = self.pix2ang(value, lonlat = True)

                value = UnitSphericalRepresentation(lon = lon*u.deg,
                                                    lat = lat*u.deg)

            else:
                value = self.pix2skycoord(value)

            return self.interp_weights(value)

    def _operation(self, other, operation):
        raise AttributeError("HealpixAxis doesn't support operations")

    def _ioperation(self, other, operation):
        raise AttributeError("HealpixAxis doesn't support operations")

    def _write(self, axes_group, name):

        """
        Save all needed information to recreate Axis into
        a HDF5 group.  Subclasses may override

        Returns: dataset holding axis
        """

        axis_set = super()._write(axes_group, name)

        axis_set.attrs['nside'] = self.nside
        axis_set.attrs['scheme'] = self.scheme

        if self.coordsys is not None:
            axis_set.attrs['coordsys'] = str(self.coordsys.name)

        return axis_set

    @classmethod
    def _open(cls, dataset):
        """
        Create HealpixAxis from HDF5 dataset
        """

        new = super()._open(dataset)

        nside = dataset.attrs['nside']
        scheme = dataset.attrs['scheme']

        coordsys = None
        if 'coordsys' in dataset.attrs:
            coordsys = dataset.attrs['coordsys']

        HealpixBase.__init__(new,
                             nside = nside,
                             scheme = scheme,
                             coordsys = coordsys)

        return new
