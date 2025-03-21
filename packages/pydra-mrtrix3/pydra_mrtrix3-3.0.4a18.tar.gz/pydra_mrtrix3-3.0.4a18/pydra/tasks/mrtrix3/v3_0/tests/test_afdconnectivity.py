# Auto-generated test for afdconnectivity

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import AfdConnectivity


def test_afdconnectivity(tmp_path, cli_parse_only):

    task = AfdConnectivity(
        all_fixels=False,
        debug=False,
        force=False,
        image_=Nifti1.sample(),
        tracks=Tracks.sample(),
        wbft=None,
        afd_map=None,
    )
    result = task(plugin="serial")
    assert not result.errored
