# Auto-generated test for mrhistmatch

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import MrHistmatch


def test_mrhistmatch(tmp_path, cli_parse_only):

    task = MrHistmatch(
        bins=None,
        debug=False,
        force=False,
        in_file=Nifti1.sample(),
        mask_input=None,
        mask_target=None,
        target=Nifti1.sample(),
        type="scale",
        out_file=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
