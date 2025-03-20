"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d

import numpy as n
from babelwidget.main import backend_t
from babelwidget.main import image_h as image_wgt_h

array_t = n.ndarray


@d.dataclass(slots=True, repr=False, eq=False)
class qt_image_t:
    backend: d.InitVar[backend_t]

    library_wgt: image_wgt_h = d.field(init=False)
    array: array_t = d.field(init=False, default=None)

    def __post_init__(self, backend: backend_t) -> None:
        """"""
        self.library_wgt = backend.image_t()
        self.library_wgt.setAlignment(backend.ALIGNED_CENTER)

    def SetImage(self, image: array_t, /) -> None:
        """"""
        if (image.ndim == 2) or ((image.ndim == 3) and (image.shape[2] in (3, 4))):
            # The 4th channel is assumed to be transparency.
            self.array = image.copy()
            self.ResetImage()
        else:
            self.library_wgt.setText(
                f"Can display only 2-D images with 1 (grayscale), 3 (rgb), "
                f"or 4 (rgb+alpha) channels. Passed image has size {image.shape}."
            )

    def ResetImage(self) -> None:
        """"""
        # No need to copy as it will automatically point to a new image below.
        image = self.array
        if image.ndim == 2:
            rgb_image = n.dstack((image, image, image))
        else:
            rgb_image = image[..., :3]
        img_min = n.min(rgb_image)
        dynamic = n.max(rgb_image) - img_min
        if dynamic > 0:
            rgb_image = (255.0 / dynamic) * (rgb_image.astype(n.float64) - img_min)
        else:
            rgb_image[...] = 0
        rgb_image = n.rint(rgb_image).astype(n.uint8)

        self.library_wgt.SetImage(rgb_image)

    def RowColFromEventXY(self, evt_x: int, evt_y: int, /) -> tuple[int, int]:
        """"""
        lengths = self.array.shape
        row = round(lengths[0] * evt_y / self.library_wgt.height())
        col = round(lengths[1] * evt_x / self.library_wgt.width())

        return row, col


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
