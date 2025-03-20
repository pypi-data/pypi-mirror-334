"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import typing as h

import numpy as nmpy
import scipy.ndimage as spim
import skimage.measure as msre
from obj_mpp.extension.type import number_h
from obj_mpp.interface.console.marked_point import (
    FormattedAge,
    FormattedPoint,
    FormattedQuality,
)
from obj_mpp.runtime.ball import BALL
from obj_mpp.runtime.model import MARKED_POINT_MODEL
from obj_mpp.runtime.signal import SIGNAL_CONTEXT
from obj_mpp.task.sampling.marked_point import sampler_t
from obj_mpp.type.marked_point.instance.bbox import bbox_t
from obj_mpp.type.marked_point.model.mark import mark_h
from obj_mpp.type.marked_point.model.point import coordinate_h, point_h
from obj_mpp.type.signal.domain import domain_h, domain_indexer_h

array_t = nmpy.ndarray
dilated_region_h = tuple[array_t, tuple]
description_h = tuple[point_h, tuple[mark_h, ...], int, float | None]


class instance_t:
    """
    quality: Cached but computed externally and accessed directly (hence, no _ prefix).
    It must be None by default (see mp_quality in obj_mpp.type.quality.definition).
    cropping_indicator: top, bottom, left, right, [front, back] (i.e., row, col, dep).
    """

    __slots__ = (
        "point",
        "marks",
        "bbox",
        "region",
        "cropping_indicator",
        "crosses_border",
        "age",
        "quality",
        "_cache",
    )

    point: point_h
    marks: tuple[mark_h, ...]
    bbox: bbox_t
    region: array_t
    cropping_indicator: tuple[bool, ...]
    crosses_border: bool
    #
    age: int
    quality: float | None
    _cache: dict[str, h.Any]

    def __init__(
        self, point: h.Sequence[coordinate_h], marks: h.Sequence[mark_h], /
    ) -> None:
        """"""
        self.point = tuple(point)
        self.marks = tuple(marks)

        half_lengths = self._CoarseBoundingBoxHalfLengths()
        self._ComputeBoundingBox(half_lengths)
        self.region = self._Region()

        self.age = 0
        self.quality = None
        self._cache = {}

    @property
    def educated_name(self) -> str:
        """
        Could be a class method, but property "prefers" methods.
        """
        return type(self).__name__[:-2].capitalize()

    @property
    def as_tuple(self) -> description_h:
        """
        Marked-point should be re-buildable from the returned tuple.
        """
        return self.point, self.marks, self.age, self.quality

    @property
    def as_sortable(self) -> tuple[coordinate_h | mark_h, ...]:
        """
        Computes a unique marked point instance identifier.

        An easy solution would be to use id(self). However, the only serious use of this
        uid is in sorting mkpts to guarantee reproducibility of the detection (for
        debugging for example). Hence, the uid cannot depend on runtime-dependent
        quantities.
        A float representation can be (costly) computed as:
        hex(nmpy.float64(real).view(nmpy.uint64).item())
        """
        return *self.point, *self.marks

    @property
    def area(self) -> int:
        """"""
        cache_entry = "area"  # self.[...].__name__ cannot be used with properties.

        if cache_entry not in self._cache:
            self._cache[cache_entry] = nmpy.count_nonzero(self.region)

        return self._cache[cache_entry]

    # --- INSTANTIATE

    @classmethod
    def NewFromTuple(cls, as_tuple: description_h, /) -> h.Self:
        """"""
        output = cls(as_tuple[0], as_tuple[1])
        output.age = as_tuple[2]
        output.quality = as_tuple[3]
        return output

    # --- COMPUTE

    def _ComputeBoundingBox(self, un_cropped_half_lengths: tuple[int, ...], /) -> None:
        """
        Compute the rectangle just big enough to contain the marked point and set the
        appropriate member variables.
        """
        domain_lengths = SIGNAL_CONTEXT.lengths

        min_s = []
        max_s = []
        cropping_indicator = 2 * domain_lengths.__len__() * [False]

        ci_idx = 0
        for coordinate, un_cropped_half_length, domain_length in zip(
            self.point, un_cropped_half_lengths, domain_lengths, strict=True
        ):
            min_coord = coordinate - un_cropped_half_length
            if min_coord < 0:
                min_coord = 0
                cropping_indicator[ci_idx] = True
            else:
                min_coord = int(nmpy.floor(min_coord))

            max_coord = coordinate + un_cropped_half_length
            if max_coord > domain_length - 1:
                max_coord = domain_length - 1
                cropping_indicator[ci_idx + 1] = True
            else:
                max_coord = int(nmpy.ceil(max_coord))

            min_s.append(min_coord)
            max_s.append(max_coord)
            ci_idx += 2

        self.bbox = bbox_t(min_s, max_s)
        self.cropping_indicator = tuple(cropping_indicator)
        self.crosses_border = any(self.cropping_indicator)

    def Contour(self, /, *, thickness: int = 1) -> array_t:
        """"""
        cache_entry = self.Contour.__name__

        if cache_entry not in self._cache:
            self._cache[cache_entry] = {}

        if thickness not in self._cache[cache_entry]:
            region = self.region
            ball = BALL.OfDimensionAndRadius(MARKED_POINT_MODEL.dimension, thickness)
            contour = nmpy.logical_xor(
                region, spim.binary_erosion(region, structure=ball)
            )

            self._cache[cache_entry][thickness] = contour

        return self._cache[cache_entry][thickness]

    def DilatedRegion(self, dilation: int, /) -> array_t | dilated_region_h:
        """
        Returns the boolean map of the dilated marked-point and the slices for each bbox
        dimension. Dilation can be negative (erosion then).
        """
        cache_entry = self.DilatedRegion.__name__

        if cache_entry not in self._cache:
            self._cache[cache_entry] = {}

        if dilation not in self._cache[cache_entry]:
            ball = BALL.OfDimensionAndRadius(
                MARKED_POINT_MODEL.dimension, abs(dilation)
            )
            if dilation > 0:
                padded_region = nmpy.pad(self.region, dilation)
                dilated_region = spim.binary_dilation(padded_region, structure=ball)
                sub_domain = MARKED_POINT_MODEL.dimension * [slice(0)]
                for axis, length in enumerate(SIGNAL_CONTEXT.lengths):
                    start = max(dilation - self.bbox.domain[axis].start, 0)
                    stop = dilated_region.shape[axis] - max(
                        self.bbox.domain[axis].stop + dilation - length, 0
                    )
                    sub_domain[axis] = slice(start, stop)
                dilated_region = dilated_region[tuple(sub_domain)]
                dilated_domain = self.bbox.SlicesOfDilated(dilation)
            else:
                dilated_region = spim.binary_erosion(self.region, structure=ball)
                dilated_domain = self.bbox.domain

            self._cache[cache_entry][dilation] = (dilated_region, dilated_domain)

        return self._cache[cache_entry][dilation]

    def InnerDistanceMap(self) -> array_t:
        """"""
        return spim.distance_transform_edt(self.region)

    def Property(self, name: str, /) -> h.Any:
        """"""
        py_path_entry = f"{msre.__name__}.{msre.regionprops.__name__}"
        cache_entry = f"{py_path_entry}.{name}"

        if cache_entry not in self._cache:
            if py_path_entry not in self._cache:
                self._cache[py_path_entry] = msre.regionprops(
                    self.region.astype(nmpy.uint8)
                )[0]

            self._cache[cache_entry] = self._cache[py_path_entry][name]

        return self._cache[cache_entry]

    # --- GENERATE

    def SimilarSamples(
        self, sampler: sampler_t, n_similar: int, /, *, fraction: float = 0.1
    ) -> tuple[h.Self, ...]:
        """"""
        radius = self._RadiusForSimilarPoints(fraction=fraction)
        points = sampler["point"].SimilarSamples(self.point, radius, n_similar)
        marks = sampler.SimilarMarkSamples(
            self.marks, points[0].__len__(), fraction=fraction
        )
        dimension = points.__len__()

        return tuple(
            self.__class__(_elm[:dimension], _elm[dimension:])
            for _elm in zip(*points, *marks, strict=True)
        )

    # --- ANALYZE

    def In(self, domain: domain_h, /) -> bool:
        """"""
        return all(
            _fst <= _crd <= _lst
            for _crd, (_fst, _lst) in zip(self.point, domain, strict=True)
        )

    def _RegionIntersects(
        self,
        domain_1: domain_indexer_h,
        region_2: array_t,
        domain_2: domain_indexer_h,
        area_2: int,
        max_overlap: float,
        /,
    ) -> bool:
        """"""
        region_1_inter = self.region[domain_1]
        region_2_inter = region_2[domain_2]
        intersection_area = nmpy.count_nonzero(
            nmpy.logical_and(region_1_inter, region_2_inter)
        )

        if intersection_area == 0:
            return False

        min_area = min(self.area, area_2)
        if intersection_area == min_area:
            # Total inclusion
            return True

        # Always true when max_overlap = 0
        return 100.0 * intersection_area / min_area > max_overlap

    # --- REPORT

    def __str__(self) -> str:
        """"""
        return str(self.AsTuple())

    def AsTuple(
        self,
        /,
        *,
        educated_version: bool = False,
        header: tuple[str, ...] | None = None,
    ) -> tuple[str | coordinate_h | mark_h | number_h, ...]:
        """"""
        output = [self.educated_name]

        output.extend(self.point)

        if educated_version:
            output.extend(self.educated_marks)
            output.append(self.area)
        else:
            output.extend(self.marks)

        if self.quality is None:
            output.append(nmpy.nan)
        else:
            output.append(self.quality)

        output.append(self.age)

        if header is not None:
            for idx, (name, value) in enumerate(zip(header, output, strict=True)):
                output[idx] = f"{name}={value}"

        return tuple(output)

    def AsFormattedString(self) -> str:
        """"""
        return (
            f"{type(self).__name__[0].upper()}"
            + FormattedPoint(self.point)
            + "_"
            + self.FormattedMarks()
            + FormattedQuality(self.quality)
            + FormattedAge(self.age)
        )

    def DrawInArray(
        self,
        array: array_t,
        /,
        *,
        level: number_h = 255,
        thickness: int = 2,
        bbox_level: number_h = -1,
    ) -> None:
        """"""
        bbox = self.bbox

        if bbox_level >= 0:
            slices = list(bbox.domain)
            for d_idx in range(MARKED_POINT_MODEL.dimension):
                domain_for_dim = slices[d_idx]

                slices[d_idx] = bbox.min_s[d_idx]
                array[tuple(slices)] = bbox_level

                slices[d_idx] = bbox.max_s[d_idx]
                array[tuple(slices)] = bbox_level

                slices[d_idx] = domain_for_dim

        if thickness > 0:
            array[bbox.domain][self.Contour(thickness=thickness)] = level
        else:
            array[bbox.domain][self.region] = level

    # --- JSON
    def __DescriptionForJSON__(self) -> description_h:
        """"""
        return self.as_tuple

    @classmethod
    def __NewFromJsonDescription__(cls, description: description_h, /) -> h.Self:
        """"""
        return cls.NewFromTuple(description)

    # --- MISSING MANDATORY

    def _CoarseBoundingBoxHalfLengths(self) -> tuple[int, ...]:
        """"""
        raise NotImplementedError

    def _Region(self) -> array_t:
        """
        Must include the marked point frontier.
        """
        raise NotImplementedError

    def Intersects(self, other: h.Self, max_overlap: float, /) -> bool:
        """"""
        raise NotImplementedError

    # --- MISSING OPTIONAL

    @property
    def educated_marks(self) -> tuple[mark_h, ...]:
        """"""
        raise NotImplementedError

    def Normals(self) -> tuple[tuple[array_t, ...] | None, array_t | None]:
        """"""
        raise NotImplementedError

    def _RadiusForSimilarPoints(self, /, *, fraction: float = 0.1) -> float:
        """
        Necessary for refinement, but optional since refinement is optional.
        """
        raise NotImplementedError

    def FormattedMarks(self) -> str:
        """"""
        raise NotImplementedError


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
