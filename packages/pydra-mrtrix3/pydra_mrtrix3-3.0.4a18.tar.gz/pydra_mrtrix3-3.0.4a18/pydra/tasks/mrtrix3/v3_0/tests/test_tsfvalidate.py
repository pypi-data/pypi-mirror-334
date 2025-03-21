# Auto-generated test for tsfvalidate

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import TsfValidate


def test_tsfvalidate(tmp_path, cli_parse_only):

    task = TsfValidate(
        debug=False,
        force=False,
        tracks=File.sample(),
        tsf=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
