import pytest

import tempfile
import pathlib
import pandas
import numpy

from utils.files import pickle
from . import somethingThatDoesntExist


def test_open_pickle_as_pandas_table_fail(
    somethingThatDoesntExist: str
) -> None:
    # openning a non-existent path
    with pytest.raises(ValueError, match=r"^The path \[.*\] does not exist$"):
        tbl = pickle.openPickleAsPandasTable(somethingThatDoesntExist)
    # openning a folder instead of a file
    with pytest.raises(ValueError, match=r"^The path \[.*\] is not a file$"):
        tbl = pickle.openPickleAsPandasTable(".")


def test_open_pickle_as_pandas_table() -> None:
    tbl = pickle.openPickleAsPandasTable("./data/systems-528n.pkl")
    assert tbl.index[0] == "AU Mic b"
    assert tbl.index[3] == "CoRoT-24 c"


def test_save_pandas_table_as_pickle() -> None:
    rng = numpy.random.default_rng()
    tbl = pandas.DataFrame(
        rng.integers(0, 20, size=(3, 5)),
        index=[1, 2, 3],
        columns=["a", "b", "c", "d", "e"]
    )
    with tempfile.TemporaryDirectory() as tempDir:
        tempFilePath = pathlib.Path(tempDir) / "some.pkl"
        pickle.savePandasTableAsPickle(tbl, tempFilePath)
        assert tempFilePath.exists()
        with pytest.raises(
            ValueError, match=r"^The \[.*\] file already exists$"
        ):
            pickle.savePandasTableAsPickle(tbl, tempFilePath)


def test_merge_pickles_return_as_pandas() -> None:
    tbl = pickle.mergePickles(
        "./data/merge-pickles/",
        None
    )
    assert isinstance(tbl, pandas.DataFrame)
    assert len(tbl) == 6


def test_merge_pickles_save_to_file() -> None:
    with tempfile.TemporaryDirectory() as tempDir:
        tempFilePath = pathlib.Path(tempDir) / "merged.pkl"
        rslt = pickle.mergePickles(
            "./data/merge-pickles/",
            tempFilePath
        )
        assert isinstance(rslt, type(None))
        assert tempFilePath.exists()
