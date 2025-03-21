# Auto-generated test for sh2peaks

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Sh2Peaks


def test_sh2peaks(tmp_path, cli_parse_only):

    task = Sh2Peaks(
        SH=Nifti1.sample(),
        debug=False,
        direction=None,
        fast=False,
        force=False,
        mask=None,
        num=None,
        peaks=None,
        seeds=None,
        threshold=None,
        out_file=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
