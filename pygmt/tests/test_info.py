"""
Tests for gmtinfo
"""
import os

import numpy as np
import numpy.testing as npt
import pandas as pd
import pytest
import xarray as xr

from .. import info
from ..exceptions import GMTInvalidInput

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
POINTS_DATA = os.path.join(TEST_DATA_DIR, "points.txt")


def test_info():
    "Make sure info works on file name inputs"
    output = info(table=POINTS_DATA)
    expected_output = (
        f"{POINTS_DATA}: N = 20 "
        "<11.5309/61.7074> "
        "<-2.9289/7.8648> "
        "<0.1412/0.9338>\n"
    )
    assert output == expected_output


def test_info_dataframe():
    "Make sure info works on pandas.DataFrame inputs"
    table = pd.read_csv(POINTS_DATA, sep=" ", header=None)
    output = info(table=table)
    expected_output = (
        "<matrix memory>: N = 20 <11.5309/61.7074> <-2.9289/7.8648> <0.1412/0.9338>\n"
    )
    assert output == expected_output


def test_info_2d_array():
    "Make sure info works on 2D numpy.ndarray inputs"
    table = np.loadtxt(POINTS_DATA)
    output = info(table=table)
    expected_output = (
        "<matrix memory>: N = 20 <11.5309/61.7074> <-2.9289/7.8648> <0.1412/0.9338>\n"
    )
    assert output == expected_output


def test_info_1d_array():
    "Make sure info works on 1D numpy.ndarray inputs"
    output = info(table=np.arange(20))
    expected_output = "<matrix memory>: N = 20 <0/19>\n"
    assert output == expected_output


def test_info_per_column():
    "Make sure the per_column option works"
    output = info(table=POINTS_DATA, per_column=True)
    npt.assert_allclose(
        actual=output, desired=[11.5309, 61.7074, -2.9289, 7.8648, 0.1412, 0.9338]
    )


def test_info_spacing():
    "Make sure the spacing option works"
    output = info(table=POINTS_DATA, spacing=0.1)
    npt.assert_allclose(actual=output, desired=[11.5, 61.8, -3, 7.9])


def test_info_spacing_bounding_box():
    "Make sure the spacing option for writing a bounding box works"
    output = info(table=POINTS_DATA, spacing="b")
    npt.assert_allclose(
        actual=output,
        desired=[
            [11.5309, -2.9289],
            [61.7074, -2.9289],
            [61.7074, 7.8648],
            [11.5309, 7.8648],
            [11.5309, -2.9289],
        ],
    )


def test_info_per_column_spacing():
    "Make sure the per_column and spacing options work together"
    output = info(table=POINTS_DATA, per_column=True, spacing=0.1)
    npt.assert_allclose(actual=output, desired=[11.5, 61.8, -3, 7.9, 0.1412, 0.9338])


def test_info_nearest_multiple():
    "Make sure the nearest_multiple option works"
    output = info(table=POINTS_DATA, nearest_multiple=0.1)
    npt.assert_allclose(actual=output, desired=[11.5, 61.8, 0.1])


def test_info_fails():
    """
    Make sure info raises an exception if not given either a file name, pandas
    DataFrame, or numpy ndarray
    """
    with pytest.raises(GMTInvalidInput):
        info(table=xr.DataArray(21))
