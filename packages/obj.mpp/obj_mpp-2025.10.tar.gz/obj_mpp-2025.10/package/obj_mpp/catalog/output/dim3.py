"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import typing as h
from pathlib import Path as path_t

import numpy as nmpy
from obj_mpp.catalog.output.generic.dim_any import (
    BackgroundIsValid,
    ColorOutputImage,
    DrawMarkedPoints,
)
from obj_mpp.interface.storage.save.generic import OutputDocument
from obj_mpp.interface.window.detection import detection_window_t
from obj_mpp.type.detection import NormalizedQualities
from obj_mpp.type.marked_point.instance.base import instance_t

import imageio as mgio
from matplotlib import pyplot as pplt

array_t = nmpy.ndarray


def Output3DObjects(
    instances: h.Sequence[instance_t],
    background: array_t,
    result_folder: path_t,
    /,
    *,
    signal_id: str = "",
    plot_thickness: int = 2,
    with_annotations: bool = False,
    show_figure: bool = True,
    img_basename: str | None = None,
) -> None:
    """
    Must accept instances and image as first 2 arguments, and date_as_str as optional argument.
    """
    if not BackgroundIsValid(background, 3):
        return

    normalized_qualities = NormalizedQualities(instances)

    if (img_basename is not None) and (img_basename != ""):
        background_color = ColorOutputImage(background, 3)
        DrawMarkedPoints(
            background_color,
            None,
            instances,
            normalized_qualities,
            True,
            0,
            1,
            plot_thickness,
        )

        mgio.volwrite(
            OutputDocument(result_folder, img_basename, "tif", signal_id),
            nmpy.around(255.0 * background_color).astype("uint8"),
        )

    if show_figure:
        background_grayscale = nmpy.zeros(background.shape[:3], dtype=nmpy.float64)
        DrawMarkedPoints(
            background_grayscale, None, instances, normalized_qualities, False, 0, 0, 0
        )

        figure = detection_window_t.NewFor3D(background_grayscale, instances)
        figure.PlotIsoSurface(background_grayscale)
        figure.AddColorbar(normalized_qualities, 3)

        pplt.show()
        pplt.close(figure.root)


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
