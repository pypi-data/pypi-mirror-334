"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import typing as h

import networkx as ntwx
import numpy as nmpy
from obj_mpp.constant.signal import INFINITY_NUMPY_FLOAT
from obj_mpp.runtime.quality import QUALITY_CONTEXT
from obj_mpp.task.sampling.marked_point import sampler_t
from obj_mpp.type.marked_point.instance.base import description_h, instance_t

array_t = nmpy.ndarray


@d.dataclass(slots=True, repr=False, eq=False)
class detection_t(list[instance_t]):

    instance_tt: type[instance_t]
    sampler: sampler_t
    max_overlap: float
    min_quality: float
    only_un_cropped: bool
    #
    n_iterations: int
    n_new_per_iteration: int
    refinement_interval: int | None
    n_new_per_refinement: int
    max_refinement_variation: float
    #
    n_non_blank_its: int = 0
    n_refinement_attempts: int = 0
    n_refinement_successes: int = 0

    def __post_init__(self) -> None:
        """"""
        if self.refinement_interval is None:
            self.refinement_interval = self.n_iterations + 1

    @property
    def refinement_efficiency(self) -> int:
        """"""
        return int(
            round(
                100.0 * self.n_refinement_successes / max(1, self.n_refinement_attempts)
            )
        )

    def NewDetections(self) -> list[instance_t]:
        """
        Returns a list of non-intersecting marked point candidates.

        Note that a list, as opposed to a tuple, must be returned (see Update: addition
        with self). This list can be empty due to min_quality filtering.

        One can also visualize the sampling with (sampling_map being initially all 0's):
        sites = tuple(nmpy.rint(_elm).astype(nmpy.int64, copy=False) for _elm in points)
        sampling_map[sites] += 1
        """
        output = []

        points = self.sampler["point"].Samples(self.n_new_per_iteration)
        marks = self.sampler.MarkSamples(self.n_new_per_iteration)

        dimension = points.__len__()
        for point_and_marks in zip(*points, *marks, strict=True):
            new_sample = self.instance_tt(
                point_and_marks[:dimension],
                point_and_marks[dimension:],
            )
            if new_sample.area == 0:
                continue

            # Assumption: intersection computation costs less than quality computation.
            # Hence the order of the tests below.
            for sample in output:
                if new_sample.Intersects(sample, self.max_overlap):
                    break
            else:
                quality = QUALITY_CONTEXT.Quality(new_sample)
                if quality >= self.min_quality:
                    new_sample.quality = quality
                    output.append(new_sample)

        return output

    def Initialize(
        self,
        instances: h.Sequence[instance_t | description_h],
        /,
    ) -> None:
        """
        Must not be used on a non-empty detection, but no check is performed.
        """
        if instances.__len__() == 0:
            return

        if not isinstance(instances[0], self.instance_tt):
            NewFromTuple = self.instance_tt.NewFromTuple
            instances = map(NewFromTuple, instances)

        self.extend(instances)

    def Update(
        self,
        newly_detected: list[instance_t] | tuple[description_h, ...],
        /,
        *,
        live_mode: bool = True,
    ) -> None:
        """"""
        if not isinstance(newly_detected[0], self.instance_tt):
            NewFromTuple = self.instance_tt.NewFromTuple
            newly_detected = list(map(NewFromTuple, newly_detected))

        graph = ntwx.Graph()
        for new_instance in newly_detected:
            # sfr=so far
            sfr_w_intersection = tuple(
                _elm for _elm in self if new_instance.Intersects(_elm, self.max_overlap)
            )
            if sfr_w_intersection.__len__() == 0:
                continue

            for sfr_instance in sfr_w_intersection:
                if sfr_instance not in graph:
                    graph.add_edge(
                        "SO_FAR", sfr_instance, capacity=sfr_instance.quality
                    )
                    graph.add_edge("NEW", sfr_instance, capacity=-sfr_instance.quality)
                # From the documentation of ntwx.minimum_cut: "Edges of the graph are
                # expected to have an attribute called ‘capacity’. If this attribute is
                # not present, the edge is considered to have infinite capacity." So, in
                # principle, setting capacity to INFINITY_NUMPY_FLOAT is useless. But...
                graph.add_edge(
                    new_instance, sfr_instance, capacity=INFINITY_NUMPY_FLOAT
                )

            graph.add_edge("SO_FAR", new_instance, capacity=-new_instance.quality)
            graph.add_edge("NEW", new_instance, capacity=new_instance.quality)

        if graph.number_of_nodes() > 0:
            isolated = set(self + newly_detected).difference(graph.nodes())

            # Note: do not write self = ... since it will leave the original list
            # unchanged, assigning to a new, local list. Hence the deletions below.
            _, (so_far_better, new_better) = ntwx.minimum_cut(graph, "SO_FAR", "NEW")
            for idx in range(self.__len__() - 1, -1, -1):
                if self[idx] not in so_far_better:
                    del self[idx]
            self.extend(_elm for _elm in newly_detected if _elm in new_better)
            self.extend(isolated)

            # The below sorting is useful when seeding pseudo-random number generation.
            # Indeed, in that case, the object detection is requested to be
            # reproducible. However, either "ntwx.minimum_cut" or "set" above (or both)
            # does not return sequences in deterministic order.
            self.sort(key=lambda _arg: _arg.as_sortable)
        else:
            self.extend(newly_detected)

        if live_mode:
            for instance in self:
                instance.age += 1

            self.n_non_blank_its += 1

    def Refine(self) -> None:
        """"""
        # Since self can change (in some way; see below) inside the loop, it might be
        # preferable not to use enumerate below. However, it does not change length, so
        # that "range on length" should be ok.
        for idx in range(self.__len__()):
            instance = self[idx]
            if instance.age >= self.refinement_interval:
                # Reset its age so that the algorithm does not try to improve it at each
                # next iteration (if it is not replaced by the refinement).
                instance.age = 0
                self._RefineInstance(instance, idx)

    def _RefineInstance(
        self,
        instance: instance_t,
        index: int,
        /,
    ) -> None:
        """"""
        self.n_refinement_attempts += 1

        samples = instance.SimilarSamples(
            self.sampler,
            self.n_new_per_refinement,
            fraction=self.max_refinement_variation,
        )
        qualities = []
        for sample in samples:
            quality = QUALITY_CONTEXT.Quality(sample)
            qualities.append(quality)
            sample.quality = quality

        from_high_to_low = nmpy.flipud(nmpy.argsort(qualities))
        for qty_idx in from_high_to_low:
            if qualities[qty_idx] <= instance.quality:
                break

            better = samples[qty_idx]
            for so_far in self:
                if so_far is instance:
                    continue
                if better.Intersects(so_far, self.max_overlap):
                    break
            else:
                self[index] = better
                self.n_refinement_successes += 1

    def FilterOutCropped(self) -> None:
        """
        Cropped instances were initially not considered at all (filtered out in
        NewDetections and SimilarSamples). However, this can lead to bad (but still
        "good" enough) instances touching or almost touching a border. Instead, the
        cropped instances are now kept to prevent such bad, border-touching instances,
        and removed only at the end here.
        """
        if self.only_un_cropped:
            for idx in range(self.__len__() - 1, -1, -1):
                if self[idx].crosses_border:
                    del self[idx]

    def PropertiesExtrema(
        self, /, *, formatted: bool = False
    ) -> tuple[tuple[float, ...], tuple[float, ...]] | str | None:
        """"""
        return PropertiesExtrema(self, formatted=formatted)

    def NormalizedQualities(self) -> dict[str, array_t]:
        """"""
        return NormalizedQualities(self)

    def AsListWithDecreasingQualities(self) -> list[instance_t]:
        """"""
        return sorted(self, key=lambda _arg: _arg.quality, reverse=True)


def PropertiesExtrema(
    instances: h.Sequence[instance_t] | detection_t, /, *, formatted: bool = False
) -> tuple[tuple[float, ...], tuple[float, ...]] | str | None:
    """"""
    if instances.__len__() == 0:
        return None

    instance = instances[0]
    dimension = instance.point.__len__()
    n_properties = dimension + instance.marks.__len__() + 2
    min_s = nmpy.full(n_properties, INFINITY_NUMPY_FLOAT, dtype=nmpy.float64)
    max_s = nmpy.full(n_properties, -INFINITY_NUMPY_FLOAT, dtype=nmpy.float64)
    for instance in instances:
        properties = (*instance.point, *instance.marks, instance.quality, instance.age)
        nmpy.minimum(min_s, properties, out=min_s)
        nmpy.maximum(max_s, properties, out=max_s)

    if formatted:
        output = []
        for minimum, maximum in zip(min_s, max_s, strict=True):
            if minimum.is_integer():
                minimum = int(minimum)
                format_min = "d"
            else:
                format_min = ".3f"
            if maximum.is_integer():
                maximum = int(maximum)
                format_max = "d"
            else:
                format_max = ".3f"
            output.append(f"[{minimum:{format_min}}, {maximum:{format_max}}]")
        return (
            "Center:  "
            + "x".join(output[:dimension])
            + "\nMark(s): "
            + " ".join(output[dimension:-2])
            + f"\nQuality: {output[-2]}\nAge:     {output[-1]}"
        )

    return tuple(min_s), tuple(max_s)


def NormalizedQualities(
    instances: h.Sequence[instance_t] | detection_t, /
) -> dict[str, array_t]:
    """"""
    output = {}

    qualities = nmpy.array(tuple(_elm.quality for _elm in instances))
    output["original"] = qualities.copy()

    where_infinite = nmpy.isinf(qualities)
    if where_infinite.all():
        qualities[qualities == -INFINITY_NUMPY_FLOAT] = 0.0
        qualities[qualities == INFINITY_NUMPY_FLOAT] = 1.0

        min_quality = min(qualities)
        max_quality = max(qualities)
        q_extent = max_quality - min_quality
    elif where_infinite.any():
        non_inf_qualities = qualities[nmpy.logical_not(where_infinite)]
        min_quality = min(non_inf_qualities)
        max_quality = max(non_inf_qualities)
        if max_quality == min_quality:
            quality_margin = 1.0
            q_extent = 2.0 * quality_margin
        else:
            q_extent = max_quality - min_quality
            # If qualities.size == 1.0, then max_quality == min_quality,
            # so the previous code path is taken instead.
            quality_margin = q_extent / (qualities.size - 1.0)
            q_extent += 2.0 * quality_margin

        qualities[qualities == -INFINITY_NUMPY_FLOAT] = min_quality - quality_margin
        qualities[qualities == INFINITY_NUMPY_FLOAT] = max_quality + quality_margin

        min_quality -= quality_margin
        max_quality += quality_margin
    else:
        min_quality, max_quality = min(qualities), max(qualities)
        q_extent = max_quality - min_quality

    if q_extent == 0.0:
        q_extent = 1.0
        # Hence, (qualities[idx] - min_quality) / q_extent == 1
        min_quality -= 1.0

    output["un_infinite_ized"] = qualities
    output["normalized"] = (qualities - min_quality) / q_extent
    output["pushed_against_1"] = 0.7 * output["normalized"] + 0.3

    return output


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
