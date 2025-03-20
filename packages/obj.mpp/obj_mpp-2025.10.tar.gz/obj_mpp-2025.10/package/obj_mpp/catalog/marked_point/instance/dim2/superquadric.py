"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import math
import typing as h
from ctypes import c_double, c_size_t, c_void_p

import numpy as nmpy
from obj_mpp.catalog.marked_point.instance.c_extension import RegionImplementationInC
from obj_mpp.interface.console.marked_point import FormattedAngle, FormattedExponent
from obj_mpp.runtime.signal import SIGNAL_CONTEXT
from obj_mpp.type.marked_point.instance.base2 import instance_t as _base_t
from obj_mpp.type.marked_point.model.mark import mark_h
from obj_mpp.type.marked_point.model.point import point_h
from obj_mpp.type.signal.domain import domain_indexer_h

array_t = nmpy.ndarray

_Region_C = RegionImplementationInC(
    __file__,
    (
        c_void_p,
        c_void_p,
        c_size_t,
        c_double,
        c_double,
        c_double,
        c_double,
        c_double,
        c_double,
        c_double,
        c_void_p,
    ),
)


_SEMI_MINOR_AXIS, _MAJOR_MINOR_RATIO, _MINOR_EXPONENT, _MAJOR_EXPONENT, _ANGLE = range(
    5
)


class superquadric_t(_base_t):

    @property
    def educated_marks(self) -> tuple[mark_h, ...]:
        """"""
        return (
            self.marks[_SEMI_MINOR_AXIS],
            self.marks[_SEMI_MINOR_AXIS] * self.marks[_MAJOR_MINOR_RATIO],
            self.marks[_MINOR_EXPONENT],
            self.marks[_MAJOR_EXPONENT],
            self.marks[_ANGLE],
            self.marks[_ANGLE] * 180.0 / math.pi,
        )

    def _CoarseBoundingBoxHalfLengths(self) -> tuple[int, ...]:
        """"""
        semi_major_axis = math.ceil(
            self.marks[_SEMI_MINOR_AXIS] * self.marks[_MAJOR_MINOR_RATIO]
        ).__int__()

        return semi_major_axis, semi_major_axis

    def _Region(self) -> array_t:
        """
        Alternative, faster or not, implementation: compute only in the first quadrant,
        then copy 2 times by flipping, then rotate with scipy.ndimage.rotate or
        skimage.transform.rotate. Put max value in pixels outside the domain. This
        alternative is valid because the bbox is a square corresponding to the unrotated
        superquadric. (Does it change anything to the management of out-of-domain
        pixels?)
        """
        return Region(
            self.marks[_SEMI_MINOR_AXIS],
            self.marks[_MAJOR_MINOR_RATIO],
            self.marks[_MINOR_EXPONENT],
            self.marks[_MAJOR_EXPONENT],
            self.marks[_ANGLE],
            self.point,
            self.bbox.domain,
            _Region_C,
        )

    def Normals(self) -> tuple[tuple[array_t, ...] | None, array_t | None]:
        """"""
        cache_entry = self.Normals.__name__

        if cache_entry not in self._cache:
            self._cache[cache_entry] = Normals(
                self.marks[_SEMI_MINOR_AXIS],
                self.marks[_MAJOR_MINOR_RATIO],
                self.marks[_MINOR_EXPONENT],
                self.marks[_MAJOR_EXPONENT],
                self.marks[_ANGLE],
                self.point,
                self.bbox.min_s,
                self.Contour(),
            )

        return self._cache[cache_entry]

    def _RadiusForSimilarPoints(self, /, *, fraction: float = 0.1) -> float:
        """"""
        return (
            0.5
            * fraction
            * self.marks[_SEMI_MINOR_AXIS]
            * (1.0 + self.marks[_MAJOR_MINOR_RATIO])
        )

    def FormattedMarks(self) -> str:
        """"""
        semi_minor_axis = self.marks[_SEMI_MINOR_AXIS]
        semi_major_axis = semi_minor_axis * self.marks[_MAJOR_MINOR_RATIO]
        return (
            f"[red]{semi_minor_axis:.2f}x{semi_major_axis:.2f}[/]"
            + FormattedExponent(self.marks[_MINOR_EXPONENT])
            + FormattedExponent(self.marks[_MAJOR_EXPONENT])
            + FormattedAngle(self.marks[_ANGLE])
        )


def Region(
    semi_minor_axis: float,
    major_minor_ratio: float | None,
    minor_exponent: float | None,
    major_exponent: float | None,
    angle: float | None,
    point: point_h,
    domain: domain_indexer_h,
    Region_C: h.Callable | None,
    /,
) -> array_t:
    """"""
    grid_sites = SIGNAL_CONTEXT.grid_sites
    if Region_C is None:
        centered_rows = grid_sites[0][domain] - point[0]
        centered_cols = grid_sites[1][domain] - point[1]

        if angle is None:
            # Circle.
            sq_1_level_map = (centered_rows**2 + centered_cols**2) * (
                1.0 / semi_minor_axis**2
            )
        else:
            cos = math.cos(angle)
            sin = math.sin(angle)
            rotated_rows = sin * centered_cols + cos * centered_rows
            rotated_cols = cos * centered_cols - sin * centered_rows

            if minor_exponent is None:
                # Ellipse.
                semi_major_axis = semi_minor_axis * major_minor_ratio
                sq_1_level_map = rotated_rows**2 * (
                    1.0 / semi_minor_axis**2
                ) + rotated_cols**2 * (1.0 / semi_major_axis**2)
            else:
                minor_power = nmpy.power(nmpy.fabs(rotated_rows), minor_exponent)
                major_power = nmpy.power(nmpy.fabs(rotated_cols), major_exponent)
                minor_factor = 1.0 / semi_minor_axis**minor_exponent
                major_factor = (
                    1.0 / (semi_minor_axis * major_minor_ratio) ** major_exponent
                )

                sq_1_level_map = minor_power * minor_factor + major_power * major_factor

        region = sq_1_level_map <= 1.0
    else:
        bbox_grid_rows = nmpy.array(
            grid_sites[0][domain], dtype=nmpy.float64, order="C"
        )
        bbox_grid_cols = nmpy.array(
            grid_sites[1][domain], dtype=nmpy.float64, order="C"
        )
        region = nmpy.empty_like(bbox_grid_rows, dtype=nmpy.bool_)
        if angle is None:
            # Circle.
            Region_C(
                bbox_grid_rows.ctypes.data,
                bbox_grid_cols.ctypes.data,
                bbox_grid_rows.size,
                *point,
                semi_minor_axis,
                region.ctypes.data,
            )
        elif minor_exponent is None:
            # Ellipse.
            Region_C(
                bbox_grid_rows.ctypes.data,
                bbox_grid_cols.ctypes.data,
                bbox_grid_rows.size,
                *point,
                semi_minor_axis,
                major_minor_ratio,
                angle,
                region.ctypes.data,
            )
        else:
            Region_C(
                bbox_grid_rows.ctypes.data,
                bbox_grid_cols.ctypes.data,
                bbox_grid_rows.size,
                *point,
                semi_minor_axis,
                major_minor_ratio,
                minor_exponent,
                major_exponent,
                angle,
                region.ctypes.data,
            )

    return region


def Normals(
    semi_minor_axis: float,
    major_minor_ratio: float,
    minor_exponent: float | None,
    major_exponent: float | None,
    angle: float,
    point: point_h,
    min_s: tuple[int, ...],
    contour: array_t,
    /,
) -> tuple[tuple[array_t, ...] | None, array_t | None]:
    """"""
    sites = contour.nonzero()
    if sites[0].size == 0:
        return None, None

    rotation = nmpy.empty((2, 2), dtype=nmpy.float64, order="C")
    rotation[0, 0] = nmpy.cos(angle)
    rotation[1, 0] = nmpy.sin(angle)
    rotation[0, 1] = -rotation[1, 0]
    rotation[1, 1] = rotation[0, 0]

    un_rotated_sites = (
        nmpy.transpose(sites).astype(nmpy.float64)
        + [
            [
                min_s[0] - point[0],
                min_s[1] - point[1],
            ]
        ]
    ) @ rotation

    normals = un_rotated_sites
    if minor_exponent is None:
        normals[:, 0] /= semi_minor_axis**2
        normals[:, 1] /= (semi_minor_axis * major_minor_ratio) ** 2
    else:
        row_signs = nmpy.sign(normals[:, 0])
        col_signs = nmpy.sign(normals[:, 1])
        normals[:, 0] = (
            nmpy.power(nmpy.fabs(normals[:, 0]), minor_exponent - 1.0) * row_signs
        )
        normals[:, 1] = (
            nmpy.power(nmpy.fabs(normals[:, 1]), major_exponent - 1.0) * col_signs
        )
        normals[:, 0] *= minor_exponent / semi_minor_axis**minor_exponent
        normals[:, 1] *= (
            major_exponent / (semi_minor_axis * major_minor_ratio) ** major_exponent
        )

    normals = normals @ rotation.transpose()
    normal_norms = nmpy.sqrt((normals**2).sum(axis=1, keepdims=True))
    # When the analytical normal expression is evaluated at (0,0), it
    # results in a null normal. This occurs whenever the contour "passes
    # through the center" (very thick contour and/or very thin object).
    normal_norms[normal_norms == 0.0] = 1.0
    normals /= normal_norms

    return sites, normals


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
