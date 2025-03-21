# Auto-generated test for sh2amp

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Sh2Amp


def test_sh2amp(tmp_path, cli_parse_only):

    task = Sh2Amp(
        datatype=None,
        debug=False,
        directions=File.sample(),
        force=False,
        fslgrad=None,
        grad=None,
        in_file=Nifti1.sample(),
        nonnegative=False,
        strides=None,
        out_file=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
