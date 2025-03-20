"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import typing as h

import numpy as nmpy
from logger_36 import L
from obj_mpp.extension.type import number_h
from obj_mpp.runtime.model import MARKED_POINT_MODEL
from obj_mpp.runtime.signal import SIGNAL_CONTEXT
from obj_mpp.type.marked_point.model.point import point_h
from obj_mpp.type.signal.domain import domain_h, domain_precision_h

array_t = nmpy.ndarray
number_sampler_t = nmpy.random.Generator


@d.dataclass(slots=True, repr=False, eq=False)
class point_sampler_t:
    """
    precision:
        - Currently, used only for domain sampling.
        - None="infinite".
    """

    sampler: d.InitVar[number_sampler_t]
    #
    _IntegerSamples: h.Callable | None = None
    _RealSamples: h.Callable | None = None

    def __post_init__(self, sampler: number_sampler_t) -> None:
        """"""
        self._IntegerSamples = sampler.integers
        self._RealSamples = sampler.uniform

    @classmethod
    def New(
        cls,
        constraint: domain_precision_h | array_t,
        sampler: number_sampler_t,
        /,
    ) -> h.Self | None:
        """
        Note that the returned sampler is not usable until RestrictSampling has been
        called.

        constraint: None, precision, per-axis precisions, validity map, or pdf.
        """
        if SIGNAL_CONTEXT.domain is None:
            L.error(
                "Point sampling cannot be used "
                "until signal context has been initialized."
            )
            return None

        dimension = MARKED_POINT_MODEL.dimension

        if isinstance(constraint, array_t):
            if constraint.ndim != dimension:
                L.Log(
                    f"Invalid center map or PDF dimension.",
                    actual=constraint.ndim,
                    expected=dimension,
                )
                return None

            unique_values = nmpy.unique(constraint)
            if unique_values.size > 2:
                sampling_pdf = constraint.astype(nmpy.float64)
                return _pdf_t(pdf=sampling_pdf, sampler=sampler)

            sampling_map = constraint == unique_values[1]
            return _map_t(map=sampling_map, sampler=sampler)

        if constraint is None:
            precisions = dimension * (None,)
        elif isinstance(constraint, number_h):
            precisions = dimension * (float(constraint),)
        else:  # tuple[point_precision_h, ...].
            precisions = []
            for element in constraint:
                if element is None:
                    precisions.append(None)
                else:
                    precisions.append(float(element))
            precisions = tuple(precisions)

        return _domain_t(precisions=precisions, sampler=sampler)

    def SimilarSamples(
        self, reference: point_h, radius: float, n_samples: int, /
    ) -> tuple[array_t, ...]:
        """
        Note that the (optional) precision is ignored.
        """
        output = []

        for center, (first, last) in zip(reference, SIGNAL_CONTEXT.domain, strict=True):
            first = max(center - radius, first)
            last = min(center + radius, last)
            last = nmpy.nextafter(last, last + 1.0)
            local_output = self._RealSamples(low=first, high=last, size=n_samples)
            output.append(local_output)

        indexer = self._ValidityBIndexer(output)

        return tuple(_elm[indexer] for _elm in output)

    def RestrictSampling(self, restricted_domain: domain_h, /) -> bool:
        """
        The returned value has a "restriction is empty" meaning. Consequently, any
        current procedure should abort.
        """
        raise NotImplementedError

    def Samples(self, n_samples: int, /) -> tuple[array_t, ...]:
        """"""
        raise NotImplementedError

    def _ValidityBIndexer(self, samples: h.Sequence[array_t], /) -> array_t:
        """
        Used only in SimilarSamples.
        """
        raise NotImplementedError


@d.dataclass(slots=True, repr=False, eq=False)
class _domain_t(point_sampler_t):
    precisions: tuple[float | None, ...] | None = None
    restricted_domain: domain_h | None = None
    _maxes: tuple[int | None, ...] | None = None

    def RestrictSampling(self, restricted_domain: domain_h, /) -> bool:
        """"""
        self.restricted_domain = restricted_domain
        self._maxes = tuple(
            None if _prc is None else int((_lst - _fst) / _prc)
            for (_fst, _lst), _prc in zip(
                restricted_domain, self.precisions, strict=True
            )
        )

        return False

    def Samples(self, n_samples: int, /) -> tuple[array_t, ...]:
        """"""
        output = []

        for (first, last), precision, maximum in zip(
            self.restricted_domain, self.precisions, self._maxes, strict=True
        ):
            if precision is None:
                last = nmpy.nextafter(last, last + 1.0)
                local_output = self._RealSamples(low=first, high=last, size=n_samples)
            else:
                local_output = (
                    precision
                    * self._IntegerSamples(0, high=maximum + 1, size=n_samples)
                    + first
                )
            output.append(local_output)

        return tuple(output)

    def _ValidityBIndexer(self, samples: h.Sequence[array_t], /) -> array_t:
        """"""
        interval, *remaining = self.restricted_domain

        output = nmpy.logical_and(samples[0] >= interval[0], samples[0] <= interval[1])
        for d_idx, (first, last) in enumerate(remaining, start=1):
            local_output = nmpy.logical_and(
                samples[d_idx] >= first, samples[d_idx] <= last
            )
            output = nmpy.logical_and(output, local_output)

        return output


@d.dataclass(slots=True, repr=False, eq=False)
class _map_t(point_sampler_t):
    map: array_t | None = None
    _valid_indices: array_t | None = None
    _n_valid_indices: int = 0

    def RestrictSampling(self, restricted_domain: domain_h, /) -> bool:
        """"""
        slices = tuple(slice(_fst, _lst + 1) for _fst, _lst in restricted_domain)
        restricted_map = nmpy.zeros_like(self.map)
        restricted_map[slices] = self.map[slices]

        if nmpy.any(restricted_map):
            self._valid_indices = nmpy.flatnonzero(restricted_map)
            self._n_valid_indices = self._valid_indices.size

            return False

        return True

    def Samples(self, n_samples: int, /) -> tuple[array_t, ...]:
        """"""
        return nmpy.unravel_index(
            self._valid_indices[
                self._IntegerSamples(0, high=self._n_valid_indices, size=n_samples)
            ],
            SIGNAL_CONTEXT.lengths,
        )

    def _ValidityBIndexer(
        self,
        samples: h.Sequence[array_t],
        /,
    ) -> array_t:
        """"""
        if nmpy.issubdtype(samples[0].dtype, nmpy.floating):
            samples = tuple(nmpy.around(_elm).astype(nmpy.uint64) for _elm in samples)

        return nmpy.fromiter(
            map(
                lambda _arg: _arg in self._valid_indices,
                nmpy.ravel_multi_index(samples, SIGNAL_CONTEXT.lengths),
            ),
            dtype=nmpy.bool_,
            count=samples[0].__len__(),
        )


@d.dataclass(slots=True, repr=False, eq=False)
class _pdf_t(point_sampler_t):
    pdf: array_t | None = None
    _cdf: array_t | None = None

    def RestrictSampling(self, restricted_domain: domain_h, /) -> bool:
        """"""
        slices = tuple(slice(_fst, _lst + 1) for _fst, _lst in restricted_domain)
        restricted_pdf = nmpy.zeros_like(self.pdf)
        restricted_pdf[slices] = self.pdf[slices]

        self._cdf = restricted_pdf.cumsum()
        self._cdf /= self._cdf[-1]

        return False

    def Samples(self, n_samples: int, /) -> tuple[array_t, ...]:
        """"""
        uniform_samples = self._RealSamples(size=n_samples)
        indices = nmpy.searchsorted(self._cdf, uniform_samples)

        return tuple(_elm[indices] for _elm in SIGNAL_CONTEXT.grid_sites_flat)

    def _ValidityBIndexer(
        self,
        samples: h.Sequence[array_t],
        /,
    ) -> array_t:
        """"""
        return nmpy.array(samples[0].size * (True,), dtype=nmpy.bool_, order="C")


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
