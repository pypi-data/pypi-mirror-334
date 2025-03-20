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
from obj_mpp.type.marked_point.instance.base3 import instance_t as _base_t
from obj_mpp.type.marked_point.model.mark import mark_h

array_t = nmpy.ndarray

_Region_C = RegionImplementationInC(
    __file__,
    (
        c_void_p,
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
        c_double,
        c_void_p,
    ),
)

_SEMI_MINOR_AXIS, _MAJOR_MINOR_RATIO, _THIRD_MINOR_RATIO, _RC_ANGLE, _RD_ANGLE = range(
    5
)


class ellipsoid_t(_base_t):
    # TODO: The sampling is probably not uniform due to absence of constraint on
    #     third_minor_ratio.

    @property
    def educated_marks(self) -> tuple[mark_h, ...]:
        """"""
        return (
            self.marks[_SEMI_MINOR_AXIS],
            self.marks[_SEMI_MINOR_AXIS] * self.marks[_MAJOR_MINOR_RATIO],
            self.marks[_SEMI_MINOR_AXIS] * self.marks[_THIRD_MINOR_RATIO],
            self.marks[_RC_ANGLE],
            self.marks[_RC_ANGLE] * 180.0 / math.pi,
            self.marks[_RD_ANGLE],
            self.marks[_RD_ANGLE] * 180.0 / math.pi,
        )

    def _CoarseBoundingBoxHalfLengths(self) -> tuple[int, ...]:
        """"""
        semi_major_axis = math.ceil(
            self.marks[_SEMI_MINOR_AXIS] * self.marks[_MAJOR_MINOR_RATIO]
        ).__int__()
        semi_third_axis = math.ceil(
            self.marks[_SEMI_MINOR_AXIS] * self.marks[_THIRD_MINOR_RATIO]
        ).__int__()
        radius = max(semi_major_axis, semi_third_axis)

        return radius, radius, radius

    def _Region(self) -> array_t:
        """"""
        grid_sites = SIGNAL_CONTEXT.grid_sites
        if _Region_C is None:
            centered_rows = grid_sites[0][self.bbox.domain] - self.point[0]
            centered_cols = grid_sites[1][self.bbox.domain] - self.point[1]
            centered_deps = grid_sites[2][self.bbox.domain] - self.point[2]

            cos_rc = math.cos(self.marks[_RC_ANGLE])
            sin_rc = math.sin(self.marks[_RC_ANGLE])
            rotated_rows = sin_rc * centered_cols + cos_rc * centered_rows

            cos_rd = math.cos(self.marks[_RD_ANGLE])
            sin_rd = math.sin(self.marks[_RD_ANGLE])
            re_rotated_rows = sin_rd * centered_deps + cos_rd * rotated_rows
            re_rotated_cols = cos_rc * centered_cols - sin_rc * centered_rows
            re_rotated_deps = cos_rd * centered_deps - sin_rd * rotated_rows

            semi_minor_axis = self.marks[_SEMI_MINOR_AXIS]
            semi_major_axis = semi_minor_axis * self.marks[_MAJOR_MINOR_RATIO]
            semi_third_axis = semi_minor_axis * self.marks[_THIRD_MINOR_RATIO]
            sq_1_level_map = (
                re_rotated_rows**2 * (1.0 / semi_minor_axis**2)
                + re_rotated_cols**2 * (1.0 / semi_major_axis**2)
                + re_rotated_deps**2 * (1.0 / semi_third_axis**2)
            )
            region = sq_1_level_map <= 1.0
        else:
            bbox_grid_rows = nmpy.array(
                grid_sites[0][self.bbox.domain], dtype=nmpy.float64, order="C"
            )
            bbox_grid_cols = nmpy.array(
                grid_sites[1][self.bbox.domain], dtype=nmpy.float64, order="C"
            )
            bbox_grid_deps = nmpy.array(
                grid_sites[2][self.bbox.domain], dtype=nmpy.float64, order="C"
            )
            region = nmpy.empty_like(bbox_grid_rows, dtype=nmpy.bool_)
            _Region_C(
                bbox_grid_rows.ctypes.data,
                bbox_grid_cols.ctypes.data,
                bbox_grid_deps.ctypes.data,
                bbox_grid_rows.size,
                *self.point,
                self.marks[_SEMI_MINOR_AXIS],
                self.marks[_MAJOR_MINOR_RATIO],
                self.marks[_THIRD_MINOR_RATIO],
                self.marks[_RC_ANGLE],
                self.marks[_RD_ANGLE],
                region.ctypes.data,
            )

        return region

    def Normals(self) -> tuple[tuple[array_t, ...] | None, array_t | None]:
        """"""
        cache_entry = self.Normals.__name__

        if cache_entry not in self._cache:
            contour = self.Contour()
            sites = contour.nonzero()

            if sites[0].size > 0:
                rd_rotation = nmpy.zeros((3, 3), dtype=nmpy.float64, order="C")
                rd_rotation[0, 0] = nmpy.cos(self.marks[_RD_ANGLE])
                rd_rotation[2, 0] = nmpy.sin(self.marks[_RD_ANGLE])
                rd_rotation[0, 2] = -rd_rotation[2, 0]
                rd_rotation[2, 2] = rd_rotation[0, 0]
                rd_rotation[1, 1] = 1.0

                rc_rotation = nmpy.zeros((3, 3), dtype=nmpy.float64, order="C")
                rc_rotation[0, 0] = nmpy.cos(self.marks[_RC_ANGLE])
                rc_rotation[1, 0] = nmpy.sin(self.marks[_RC_ANGLE])
                rc_rotation[0, 1] = -rc_rotation[1, 0]
                rc_rotation[1, 1] = rc_rotation[0, 0]
                rc_rotation[2, 2] = 1.0

                rotation = rd_rotation @ rc_rotation

                un_rotated_sites = (
                    nmpy.transpose(sites).astype(nmpy.float64)
                    + [
                        [
                            self.bbox.min_s[0] - self.point[0],
                            self.bbox.min_s[1] - self.point[1],
                            self.bbox.min_s[2] - self.point[2],
                        ]
                    ]
                ) @ rotation

                normals = un_rotated_sites
                normals[:, 0] /= self.marks[_SEMI_MINOR_AXIS] ** 2
                normals[:, 1] /= (
                    self.marks[_SEMI_MINOR_AXIS] * self.marks[_MAJOR_MINOR_RATIO]
                ) ** 2
                normals[:, 2] /= (
                    self.marks[_SEMI_MINOR_AXIS] * self.marks[_THIRD_MINOR_RATIO]
                ) ** 2

                normals = normals @ rotation.transpose()
                normal_norms = nmpy.sqrt((normals**2).sum(axis=1, keepdims=True))
                # When the analytical normal expression is evaluated at (0,0), it results in a null normal. This
                # occurs whenever the contour "passes through the center" (very thick contour and/or very thin object).
                normal_norms[normal_norms == 0.0] = 1.0
                normals /= normal_norms
            else:
                sites = normals = None

            self._cache[cache_entry] = (sites, normals)

        return self._cache[cache_entry]

    def _RadiusForSimilarPoints(self, /, *, fraction: float = 0.1) -> float:
        """"""
        return (
            0.34
            * fraction
            * self.marks[_SEMI_MINOR_AXIS]
            * (1.0 + self.marks[_MAJOR_MINOR_RATIO] + self.marks[_THIRD_MINOR_RATIO])
        )

    def FormattedMarks(self) -> str:
        """"""
        semi_minor_axis = self.marks[_SEMI_MINOR_AXIS]
        semi_major_axis = semi_minor_axis * self.marks[_MAJOR_MINOR_RATIO]
        semi_third_axis = semi_minor_axis * self.marks[_THIRD_MINOR_RATIO]
        return (
            f"[red]{semi_minor_axis:.2f}x{semi_major_axis:.2f}x{semi_third_axis:.2f}[/]"
            + FormattedAngle(self.marks[_RC_ANGLE])
            + FormattedAngle(self.marks[_RD_ANGLE])
        )


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
