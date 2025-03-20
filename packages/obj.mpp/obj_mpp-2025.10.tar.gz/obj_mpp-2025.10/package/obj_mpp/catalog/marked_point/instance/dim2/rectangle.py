"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import math
from ctypes import c_double, c_size_t, c_void_p

import numpy as nmpy
from obj_mpp.catalog.marked_point.instance.c_extension import RegionImplementationInC
from obj_mpp.interface.console.marked_point import FormattedAngle
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
        c_void_p,
    ),
)

_HALF_SMALL_LENGTH, _LARGE_SMALL_RATIO, _ANGLE = range(3)


class rectangle_t(_base_t):

    @property
    def educated_marks(self) -> tuple[mark_h, ...]:
        """"""
        return (
            self.marks[_HALF_SMALL_LENGTH],
            self.marks[_HALF_SMALL_LENGTH] * self.marks[_LARGE_SMALL_RATIO],
            self.marks[_ANGLE],
            self.marks[_ANGLE] * 180.0 / math.pi,
        )

    def _CoarseBoundingBoxHalfLengths(self) -> tuple[int, ...]:
        """"""
        return CoarseBoundingBoxHalfLengths(*self.marks)

    def _Region(self) -> array_t:
        """"""
        return Region(*self.marks, self.point, self.bbox.domain)

    def Normals(self) -> tuple[tuple[array_t, ...] | None, array_t | None]:
        """"""
        cache_entry = self.Normals.__name__

        if cache_entry not in self._cache:
            self._cache[cache_entry] = Normals(
                self.marks[_LARGE_SMALL_RATIO],
                self.marks[_ANGLE],
                self.point,
                self.bbox.min_s,
                self.crosses_border,
                self.Contour(),
            )

        return self._cache[cache_entry]

    def _RadiusForSimilarPoints(self, /, *, fraction: float = 0.1) -> float:
        """"""
        return (
            0.5
            * fraction
            * self.marks[_HALF_SMALL_LENGTH]
            * (1.0 + self.marks[_LARGE_SMALL_RATIO])
        )

    def FormattedMarks(self) -> str:
        """"""
        half_small_length = self.marks[_HALF_SMALL_LENGTH]
        half_large_length = half_small_length * self.marks[_LARGE_SMALL_RATIO]
        return (
            f"[red]{half_small_length:.2f}x{half_large_length:.2f}[/]"
            + FormattedAngle(self.marks[_ANGLE])
        )


def CoarseBoundingBoxHalfLengths(
    semi_minor_axis: float, major_minor_ratio: float, angle: float, /
) -> tuple[int, ...]:
    """"""
    s_min_a_2 = semi_minor_axis
    s_maj_a_2 = s_min_a_2 * major_minor_ratio

    abs_cos = abs(math.cos(angle))
    abs_sin = abs(math.sin(angle))

    half_length_row = math.ceil(s_min_a_2 * abs_cos + s_maj_a_2 * abs_sin).__int__()
    half_length_col = math.ceil(s_min_a_2 * abs_sin + s_maj_a_2 * abs_cos).__int__()

    return half_length_row, half_length_col


def Region(
    semi_minor_axis: float,
    major_minor_ratio: float,
    angle: float,
    point: point_h,
    domain: domain_indexer_h,
    /,
) -> array_t:
    """"""
    grid_sites = SIGNAL_CONTEXT.grid_sites
    if _Region_C is None:
        centered_rows = grid_sites[0][domain] - point[0]
        centered_cols = grid_sites[1][domain] - point[1]

        cos = math.cos(angle)
        sin = math.sin(angle)
        rotated_rows = sin * centered_cols + cos * centered_rows
        rotated_cols = cos * centered_cols - sin * centered_rows

        semi_major_axis = semi_minor_axis * major_minor_ratio
        sq_1_level_map = nmpy.fmax(
            nmpy.fabs(rotated_rows * (1.0 / semi_minor_axis)),
            nmpy.fabs(rotated_cols * (1.0 / semi_major_axis)),
        )
        region = sq_1_level_map <= 1.0
    else:
        bbox_grid_rows = nmpy.array(
            grid_sites[0][domain], dtype=nmpy.float64, order="C"
        )
        bbox_grid_cols = nmpy.array(
            grid_sites[1][domain], dtype=nmpy.float64, order="C"
        )
        region = nmpy.empty_like(bbox_grid_rows, dtype=nmpy.bool_)
        _Region_C(
            bbox_grid_rows.ctypes.data,
            bbox_grid_cols.ctypes.data,
            bbox_grid_rows.size,
            *point,
            semi_minor_axis,
            major_minor_ratio,
            angle,
            region.ctypes.data,
        )

    return region


def Normals(
    major_minor_ratio: float,
    angle: float,
    point: point_h,
    min_s: tuple[int, ...],
    crosses_border: bool,
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
    site_norms = nmpy.sqrt((un_rotated_sites**2).sum(axis=1))
    if crosses_border:
        # The line below is useless in general. It is necessary when the shape is
        # partially outside the image domain, with its center on the border. In this
        # case, the analytical normal expression is evaluated at (0,0), which results in
        # a null normal.
        site_norms[site_norms == 0.0] = 1.0

    site_angles = nmpy.arccos(un_rotated_sites[:, 0] / site_norms)
    limit_angle = math.atan(major_minor_ratio)
    col_edges = nmpy.logical_or(
        site_angles < limit_angle, site_angles > math.pi - limit_angle
    )
    row_edges = nmpy.logical_not(col_edges)

    normals = nmpy.empty_like(un_rotated_sites)
    normals[col_edges, 0] = nmpy.sign(un_rotated_sites[col_edges, 0])
    normals[col_edges, 1] = 0.0
    normals[row_edges, 0] = 0.0
    normals[row_edges, 1] = nmpy.sign(un_rotated_sites[row_edges, 1])

    normals = normals @ rotation.transpose()

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
