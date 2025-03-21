# Auto-generated test for mrthreshold

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import MrThreshold


def test_mrthreshold(tmp_path, cli_parse_only):

    task = MrThreshold(
        abs=None,
        allvolumes=False,
        bottom=None,
        comparison=None,
        debug=False,
        force=False,
        ignorezero=False,
        in_file=Nifti1.sample(),
        invert=False,
        mask=None,
        nan=False,
        out_masked=False,
        percentile=None,
        top=None,
        out_file=None,
    )
    result = task(plugin="serial")
    assert not result.errored
