"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

from pathlib import Path as path_t

import numpy as nmpy
import skimage.io as skio
from obj_mpp.interface.storage.api import signal_details_h
from skimage.color import rgb2hsv as HSVVersionFromRGB

array_t = nmpy.ndarray


def ImageBySkimage(image_path: path_t | None, /) -> signal_details_h:
    """"""
    if image_path is None:
        return None, None

    return _ImageBySkimage(image_path)


def ImageChannelBySkimage(
    image_path: path_t | None,
    /,
    *,
    channel: str = "gray",
) -> signal_details_h:
    """
    channel (case-insensitive): gray, 0, 1, 2, R, G, B, H, S, V
    """
    if image_path is None:
        return None, None

    image, image_error = ImageBySkimage(image_path)
    if image is None:
        return None, image_error

    if image.ndim == 3:
        if nmpy.all(nmpy.diff(image[..., :3], axis=2) == 0):
            image = image[..., 0]
            return image, image_error

        channel_couple_lst = ((0, 1), (0, 2), (1, 2))
        for channel_couple in channel_couple_lst:
            simultaneously_zero = (
                nmpy.all(image[..., channel_couple[0]] == 0)
                and (image[..., channel_couple[1]] == 0).all()
            )
            if simultaneously_zero:
                image = image[..., {0, 1, 2}.difference(channel_couple)]
                return image, image_error

        # Normally, channel is already a string, but 0, 1, 2 also works.
        channel = channel.__str__().lower()

        if channel == "gray":  # ITU-R 601-2 luma transform.
            image = (
                (0.299 * image[..., 0] + 0.587 * image[..., 1] + 0.114 * image[..., 2])
                .round()
                .astype(image.dtype)
            )
        elif channel in "012":
            image = image[..., int(channel)]
        elif channel in "rgb":
            image = image[..., int("rgb".find(channel))]
        elif channel in "hsv":
            normalized_image = image.astype(nmpy.float64)
            # noinspection PyArgumentList
            image_max = normalized_image.max()
            if image_max > 1.0:
                normalized_image /= image_max  # Normally never zero
            else:
                normalized_image = image
            hsv_image = HSVVersionFromRGB(normalized_image)
            image = hsv_image[..., int("hsv".find(channel))]
        else:
            return None, ValueError(f"{channel}: Invalid channel specification")

    return image, image_error


def _ImageBySkimage(path: path_t, /) -> signal_details_h:
    """"""
    try:
        image = skio.imread(str(path))
        error = None
    except Exception as exception:
        image = None
        error = exception

    return image, error


"""
COPYRIGHT NOTICE

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

This software is being developed by Eric Debreuve, a CNRS employee and
member of team Morpheme.
Team Morpheme is a joint team between Inria, CNRS, and UniCA.
It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
I3S, and Laboratory iBV.

CNRS: https://www.cnrs.fr/index.php/en
Inria: https://www.inria.fr/en/
UniCA: https://univ-cotedazur.eu/
Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
I3S: https://www.i3s.unice.fr/en/
iBV: http://ibv.unice.fr/
Team Morpheme: https://team.inria.fr/morpheme/
"""
