"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import multiprocessing as prll
import typing as h
from multiprocessing.managers import ListProxy as list_shared_t

from logger_36.api.content import LINE_INDENT
from mpss_tools_36.process import CloseSubtasks, NewTrackedTask
from mpss_tools_36.rich_ import progress_t
from obj_mpp.task.detection.sequential import DetectObjectsInOneChunk
from obj_mpp.type.marked_point.instance.base import instance_t
from obj_mpp.type.marked_point.model.mark import mark_h
from obj_mpp.type.marked_point.model.point import coordinate_h
from obj_mpp.type.signal.domain import chunked_bounds_h, domain_h, interval_h


def DetectObjectsInAllChunks(
    detection_prm: dict[str, h.Any],
    chunked_bounds: chunked_bounds_h,
    output: list_shared_t | list[tuple[tuple[coordinate_h | mark_h, ...], ...]],
    previous_detection: list[instance_t] | None,
    progress_tracker: progress_t,
    /,
) -> None:
    """"""
    before, chunks, after = chunked_bounds
    descriptions = progress_t.DescriptionsForChunks(
        "", tuple((_stt, _end + 1) for _stt, _end in chunks)
    )

    if previous_detection is None:
        chunked_previous = chunks.__len__() * (None,)
    else:
        chunked_previous = []
        already_in = []
        for chunk in chunks:
            sub_domain = before + (chunk,) + after
            local_previous = [
                _elm.as_tuple
                for _elm in previous_detection
                if (_elm not in already_in) and _elm.In(sub_domain)
            ]
            chunked_previous.append(local_previous)
            already_in.extend(local_previous)

    # Alternative: ProcessPoolExecutor + executor.submit + as_completed + .result().
    tasks = []
    for c_idx, (local_previous, chunk, description) in enumerate(
        zip(chunked_previous, chunks, descriptions, strict=True), start=1
    ):
        task = NewTrackedTask(
            f"{LINE_INDENT}{c_idx}: {description}",
            DetectObjectsInOneChunk,
            chunk[0],
            chunk[1] + 1,
            progress_tracker,
            t_args=(
                detection_prm,
                before + (chunk,) + after,
                output,
            ),
            t_kwargs={"previous_detection": local_previous},
            p_kwargs={
                "n_non_blank_its": 0,
                "n_instances": 0,
                "refinement_efficiency": 0,
            },
        )
        tasks.append(task)

    progress_tracker.TrackUpdates()
    CloseSubtasks(tasks)


def NParallelWorkers(hint: int, /) -> int:
    """"""
    if (hint != 1) and (prll.get_start_method(allow_none=False) == "fork"):
        if hint > 0:
            output = hint
        else:
            output = (3 * prll.cpu_count()) // 2
    else:
        # Disables parallel computation if requested or if using Windows, since pickle
        # cannot handle it.
        output = 1

    return output


def ChunkedBounds(
    lengths: tuple[int, ...], domain: domain_h, n_workers: int, /
) -> chunked_bounds_h:
    """"""
    max_length = max(lengths)
    where = lengths.index(max_length)
    chunks = _ChunksForLength(n_workers, max_length)

    return domain[:where], chunks, domain[(where + 1) :]


def _ChunksForLength(n_workers: int, length: int, /) -> tuple[interval_h, ...]:
    """"""
    if n_workers < length:
        chunk_size = length // n_workers
        remainder = length % n_workers
        chunk_sizes = n_workers * [chunk_size]
        for chunk_idx in range(remainder):
            chunk_sizes[chunk_idx] += 1
    else:
        chunk_sizes = length * [1]

    output = [(0, chunk_sizes[0] - 1)]
    for chunk_idx, chunk_size in enumerate(chunk_sizes[1:]):
        last = output[chunk_idx][1]
        output.append((last + 1, last + chunk_size))

    return tuple(output)


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
