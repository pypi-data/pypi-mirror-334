# Auto-generated test for warpcorrect

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import WarpCorrect


def test_warpcorrect(tmp_path, cli_parse_only):

    task = WarpCorrect(
        debug=False,
        force=False,
        in_=Nifti1.sample(),
        marker=None,
        tolerance=None,
        out=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
