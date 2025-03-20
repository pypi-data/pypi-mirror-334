"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
from pathlib import Path as path_t

import numpy as nmpy
from logger_36 import L
from obj_mpp.task.sampling.mark import mark_sampler_t
from obj_mpp.task.sampling.point import point_sampler_t
from obj_mpp.type.marked_point.model.mark import (
    mark_h,
    mark_interval_h,
    mark_precision_h,
)
from obj_mpp.type.signal.domain import domain_h, domain_precision_h

array_t = nmpy.ndarray
number_sampler_t = nmpy.random.Generator


@d.dataclass(slots=True, repr=False, eq=False)
class sampler_t(dict[str, point_sampler_t | mark_sampler_t]):
    """
    The choice of a dict is to allow adding samplers for marks accessible through the
    mark names.
    A valid signal_context_t is required starting from the call to FromSeed.
    """

    seed: int | None = None
    number_sampler: number_sampler_t = d.field(init=False)
    point_is_map_or_pdf: bool | None = d.field(init=False, default=None)
    mark_names: list[str] = d.field(init=False, default_factory=list)

    @property
    def is_point_ready(self) -> bool:
        """"""
        return "point" in self

    @property
    def is_mark_ready(self) -> bool:
        """"""
        if "point" in self:
            return self.__len__() > 1
        return self.__len__() > 0

    def __post_init__(self) -> None:
        """"""
        if self.seed is None:
            self.number_sampler = nmpy.random.default_rng()
        else:
            self.number_sampler = nmpy.random.default_rng(seed=self.seed)

    def Reset(self) -> None:
        """"""
        self.__post_init__()

    def SetPointMode(
        self,
        constraint: domain_precision_h | path_t | str,
        /,
    ) -> None:
        """
        path_t | str: only for pre-signal-loading, partial setting useful to
        distinguish early between domain sampling and map-or-pdf sampling.
        """
        if self.point_is_map_or_pdf is None:
            self.point_is_map_or_pdf = isinstance(constraint, path_t | str)

    def SetPointParameters(
        self,
        constraint: domain_precision_h | array_t,
        /,
    ) -> None:
        """
        Do not pass an array_t to specify a size or domain. It is reserved to map and
        PDF.
        """
        sampler = point_sampler_t.New(constraint, self.number_sampler)
        if sampler is not None:
            self["point"] = sampler

    def RestrictPointSampling(self, restricted_domain: domain_h, /) -> bool:
        """"""
        return self["point"].RestrictSampling(restricted_domain)

    def SetMarkParameters(
        self,
        ranges: dict[str, tuple[mark_interval_h, mark_precision_h]],
        types: dict[str, type[mark_h]],
        /,
    ) -> None:
        """"""
        for name, value in ranges.items():
            if name == "point":
                L.error('Mark name "point" is reserved for point sampling.')
                continue

            self[name] = mark_sampler_t.New(
                value[0], value[1], types[name], self.number_sampler
            )
            self.mark_names.append(name)

    def MarkSamples(self, n_samples: int, /) -> tuple[array_t, ...]:
        """"""
        return tuple(self[_elm].Samples(n_samples) for _elm in self.mark_names)

    def SimilarMarkSamples(
        self,
        references: tuple[mark_h, ...],
        n_samples: int,
        /,
        *,
        fraction: float = 0.1,
    ) -> tuple[array_t, ...]:
        """"""
        return tuple(
            self[_mrk].SimilarSamples(_ref, fraction, n_samples)
            for _ref, _mrk in zip(references, self.mark_names, strict=True)
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
