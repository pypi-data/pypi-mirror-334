"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

"""
This module is in a subfolder to hide it from catalog exploration.
"""

import logging as lggg
import typing as h

import numpy as nmpy
from logger_36 import L
from obj_mpp.type.marked_point.instance.base import instance_t

array_t = nmpy.ndarray


def BackgroundIsValid(image: array_t, expected_dim: int, /) -> bool:
    """"""
    if (image.ndim == expected_dim) or (
        (image.ndim == expected_dim + 1) and (image.shape[-1] == 3)
    ):
        return True

    L.Log(
        "Invalid background dimension; Displaying/Saving cancelled",
        level=lggg.WARNING,
        actual=image.ndim,
        expected=f"{expected_dim}for grayscale or {expected_dim+1} for color",
    )

    return False


def ColorOutputImage(background: array_t, image_dim: int, /) -> array_t:
    """"""
    if background.ndim == image_dim:
        output = nmpy.empty((*background.shape, 3), dtype=nmpy.float64)
        for channel in range(3):
            output[..., channel] = background
    else:
        # Returns a copy, as desired
        output = background.astype(nmpy.float64)

    # noinspection PyArgumentList
    normalization_factor = background.max()
    if normalization_factor > 0.0:
        output /= normalization_factor

    return output


def DrawMarkedPoints(
    image: array_t,
    labeled_map: array_t | None,
    instances: h.Sequence[instance_t],
    quality_details: dict[str, h.Any],
    in_color: bool,
    on_channel: int,
    off_channel: int,
    plot_thickness: int,
    /,
) -> None:
    """"""
    qualities = quality_details["pushed_against_1"]

    if in_color:
        target_image = image[..., on_channel]
    else:
        target_image = image

    for i_idx, (instance, quality) in enumerate(
        zip(instances, qualities, strict=True), start=1
    ):
        instance.DrawInArray(target_image, thickness=plot_thickness, level=quality)
        if in_color:
            instance.DrawInArray(
                image[..., off_channel], thickness=plot_thickness, level=0.0
            )

        if labeled_map is not None:
            labeled_map[instance.bbox.domain][instance.region] = i_idx


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
