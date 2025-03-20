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
from PIL import Image, ImageDraw, ImageFont

import imageio as mgio
from matplotlib import pyplot as pplt

array_t = nmpy.ndarray


def Output2DObjects(
    instances: h.Sequence[instance_t],
    background: array_t,
    result_folder: path_t,
    /,
    *,
    signal_id: str = "",
    plot_thickness: int = 1,
    with_annotations: bool = False,
    show_figure: bool = True,
    img_basename: str | None = None,
) -> None:
    """
    Must accept instances and image as first 2 arguments, and date_as_str as optional
    argument.
    """
    if not BackgroundIsValid(background, 2):
        return

    normalized_qualities = NormalizedQualities(instances)
    mkpt_lmp = nmpy.zeros(background.shape[:2], dtype=nmpy.uint16)
    output = ColorOutputImage(background, 2)
    DrawMarkedPoints(
        output, mkpt_lmp, instances, normalized_qualities, True, 0, 1, plot_thickness
    )

    # Plot here so that output is not altered with legend (see below)
    if show_figure:
        figure = detection_window_t.NewFor2D(output, instances, mkpt_lmp)
        figure.Plot2DImage(output)
        figure.AddColorbar(normalized_qualities, 2)
        if with_annotations:
            figure.PlotAnnotations()
        # But do not block with show() here to let saving below occur right away
    else:
        figure = None

    if (img_basename is not None) and (img_basename != ""):
        if with_annotations:
            _DrawAnnotationsInArray(output, instances)

        mgio.imwrite(
            OutputDocument(result_folder, img_basename, "png", signal_id),
            nmpy.around(255.0 * output).astype("uint8"),
        )

    if show_figure:
        pplt.show()
        pplt.close(figure.root)


def _DrawAnnotationsInArray(
    image: array_t, instances: h.Sequence[instance_t], /
) -> None:
    """"""
    font_size = 11

    for instance in instances:
        bbox = instance.bbox
        array_w_text = _ArrayWithText(str(id(instance)), size=font_size)
        array_w_text = list(nmpy.nonzero(array_w_text))
        array_w_text[0] += (
            bbox.min_s[0] + bbox.max_s[0] + font_size
        ) // 2 - array_w_text[0].max()
        array_w_text[1] += bbox.min_s[1] + font_size // 2 - array_w_text[1].min()

        out_of_domain = nmpy.logical_or(array_w_text[0] < 0, array_w_text[1] < 0)
        out_of_domain = nmpy.logical_or(
            out_of_domain, array_w_text[0] >= image.shape[0]
        )
        out_of_domain = nmpy.logical_or(
            out_of_domain, array_w_text[1] >= image.shape[1]
        )
        within_domain = nmpy.logical_not(out_of_domain)

        array_w_text = (array_w_text[0][within_domain], array_w_text[1][within_domain])

        image[..., 0][array_w_text] = 1.0


def _ArrayWithText(text: str, /, *, size: int = 10) -> array_t:
    """"""
    font = ImageFont.truetype("arial.ttf", size)

    image = Image.new(mode="1", size=(size * (text.__len__() + 1), 2 * size))
    drawer = ImageDraw.Draw(image)
    drawer.text((size // 2, size // 2), text, font=font, fill=1)

    output = nmpy.asarray(image, dtype=nmpy.bool_)

    n_rows, n_cols = output.shape
    row_projection = output.any(axis=1)
    col_projection = output.any(axis=0)
    row_start = row_projection.argmax()
    row_end_p_1 = n_rows - row_projection[::-1].argmax()
    col_start = col_projection.argmax()
    col_end_p_1 = n_cols - col_projection[::-1].argmax()

    return output[row_start:row_end_p_1, col_start:col_end_p_1]


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
