# Auto-generated test for maskdump

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import MaskDump


def test_maskdump(tmp_path, cli_parse_only):

    task = MaskDump(
        debug=False,
        force=False,
        in_file=Nifti1.sample(),
        out_file=None,
    )
    result = task(plugin="serial")
    assert not result.errored
