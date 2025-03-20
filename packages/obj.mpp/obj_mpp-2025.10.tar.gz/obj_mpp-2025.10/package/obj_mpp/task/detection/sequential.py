"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import typing as h
from multiprocessing.managers import ListProxy as list_shared_t

from mpss_tools_36.rich_ import progress_t, status_per_task_h
from obj_mpp.type.detection import detection_t
from obj_mpp.type.marked_point.instance.base import description_h
from obj_mpp.type.marked_point.model.mark import mark_h
from obj_mpp.type.marked_point.model.point import coordinate_h
from obj_mpp.type.signal.domain import domain_h
from rich.progress import TaskID as task_id_t


def DetectObjectsInOneChunk(
    detection_or_prm: detection_t | dict[str, h.Any],
    domain: domain_h,
    output: None | list_shared_t | list[tuple[tuple[coordinate_h | mark_h, ...], ...]],
    progress_or_status: progress_t | status_per_task_h,
    task_id: task_id_t,
    /,
    *,
    previous_detection: list[description_h] | None = None,
) -> None:
    """
    When called in sequential mode:
        - detection_or_prm is a detection,
        - domain is the full signal domain,
        - output is None since the detection serves as output,
        - previous_detection is None since the detection has been initialized with the
        history.
    When called in parallel mode:
        - detection_or_prm is a parameter dictionary,
        - domain is a domain chunk,
        - output is a multiprocessing.Manager (shared) list,
        - previous_detection is a list of instance descriptions in the domain chunk, or
        None.
    """
    if output is None:
        detection = detection_or_prm
    else:
        detection = detection_t(**detection_or_prm)
        if previous_detection is not None:
            detection.Initialize(previous_detection)

    if detection.sampler.RestrictPointSampling(domain):
        return

    for i_idx in range(1, detection.n_iterations + 1):
        newly_detected = detection.NewDetections()
        if newly_detected.__len__() == 0:
            continue

        detection.Update(newly_detected)
        detection.Refine()

        progress_t.Update(
            progress_or_status,
            task_id,
            i1=i_idx,
            n_non_blank_its=detection.n_non_blank_its,
            n_instances=detection.__len__(),
            refinement_efficiency=detection.refinement_efficiency,
        )

    detection.FilterOutCropped()

    if output is not None:
        output.append(tuple(_elm.as_tuple for _elm in detection))


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
