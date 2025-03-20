from histpy import HealpixAxis

from astropy.coordinates import SkyCoord
import astropy.units as u

from numpy import array_equal as arr_eq

import numpy as np

import pytest

def test_healpix_axis():

    axis = HealpixAxis(nside = 128,
                       coordsys = 'icrs',
                       label='Foo')

    assert axis.label == 'Foo'

    # find_bin
    assert axis.find_bin(SkyCoord(ra = 1*u.deg, dec = 89.999*u.deg)) == 0

    # find_bin with multiple values
    assert arr_eq(axis.find_bin(SkyCoord(ra=[1,-1] * u.deg, dec=89.999 * u.deg)),
                  [0,3])
    assert arr_eq(axis.find_bin([SkyCoord(ra = 1*u.deg, dec = 89.999*u.deg),
                                 SkyCoord(ra = -1*u.deg, dec = 89.999*u.deg)]),
                                [0, 3])

    # Interp
    pos0 = SkyCoord(ra=0 * u.deg, dec=90 * u.deg)
    pos1 = SkyCoord(ra=0 * u.deg, dec=-90 * u.deg)

    pix, weights = axis.interp_weights(pos0)

    assert np.array_equal(np.sort(pix), [0,1,2,3])

    assert np.allclose(weights, 0.25)

    # Interp with multiples values
    pix, weights = axis.interp_weights([pos0,pos1])

    assert np.array_equal(pix, [[1, 196607], [2, 196604], [3, 196605], [0, 196606]])
    assert np.allclose(weights, 0.25)

    assert pix.shape == (4,2)
    assert weights.shape == (4,2)

    # verify that copy() preserves subclass data
    b = axis.copy()
    assert axis == b

    # verify that replace_edges() preserves subclass data
    old_edges = axis.edges
    new_edges = old_edges[::2]
    b = axis.replace_edges(new_edges)
    b = b.replace_edges(old_edges)
    assert axis == b

    # HealpixAxis does not permit arithmetic
    with pytest.raises(AttributeError):
        c = b * 2

    # HealpixAxis does not permit arithmetic
    with pytest.raises(AttributeError):
        b *= 2

    b = axis[10:20] # specifies *bins*
    assert np.array_equiv(b.edges, axis.edges[10:21]) # one more edge than bins
    # not sure how to test that HealpixMap part is same

    with pytest.raises(ValueError):
        # edge array must be 0..len(edges)
        axis = HealpixAxis(edges = [1,2,3],
                           coordsys = 'icrs',
                           label='Foo')
