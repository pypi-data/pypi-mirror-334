"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import time

import obj_mpp.task.detection.parallel as prll
from logger_36 import L
from logger_36.api.content import LINE_INDENT
from mpss_tools_36.rich_ import NewTextColumn, progress_t
from obj_mpp.runtime.signal import SIGNAL_CONTEXT
from obj_mpp.task.detection.sequential import DetectObjectsInOneChunk
from obj_mpp.task.sampling.marked_point import sampler_t
from obj_mpp.type.config.algorithm import config_t as algorithm_config_t
from obj_mpp.type.detection import detection_t
from obj_mpp.type.marked_point.instance.base import instance_t
from rich.progress import BarColumn as column_bar_t
from rich.progress import TimeRemainingColumn as column_time_remaining_t


def DetectedObjects(
    instance_tt: type[instance_t],
    sampler: sampler_t,
    min_quality: float,
    algorithm_cfg: algorithm_config_t,
    /,
    *,
    max_overlap: float = 0.0,
    only_un_cropped: bool = True,
    previous_detection: list[instance_t] | None = None,
    called_from_cli: bool = True,
) -> list[instance_t]:
    """
    Pre-requisites:
        - SIGNAL_CONTEXT.SetSignals(?) or SIGNAL_CONTEXT.LazySignalDetails()
        - QUALITY_CONTEXT.SetSignal(?); Typically, ?=SIGNAL_CONTEXT.signal_for_qty
    """
    n_workers = prll.NParallelWorkers(algorithm_cfg.main["n_parallel_workers"])
    in_parallel = n_workers > 1
    n_new_per_iteration = algorithm_cfg.main["n_new_per_iteration"] // n_workers
    if n_new_per_iteration == 0:
        L.StageIssue(
            "Number of generated marked points in each chunk per iteration is zero."
        )
        return []

    detection_prm = {
        "instance_tt": instance_tt,
        "sampler": sampler,
        "max_overlap": max_overlap,
        "min_quality": min_quality,
        "only_un_cropped": only_un_cropped,
        "n_iterations": algorithm_cfg.main["n_iterations"],
        "n_new_per_iteration": n_new_per_iteration,
        "refinement_interval": algorithm_cfg.refinement["interval"],
        "n_new_per_refinement": algorithm_cfg.refinement["n_attempts"],
        "max_refinement_variation": algorithm_cfg.refinement["max_variation"],
    }
    detection = detection_t(**detection_prm)

    columns = (
        NewTextColumn("description", factory="description", markup=False),
        column_bar_t(),
        NewTextColumn(
            "n_non_blank_its / completed",
            factory="completed",
            extra="n_non_blank_its",
            justify="right",
            markup=False,
        ),
        NewTextColumn(
            "#n_instances[refinement_efficiency%]",
            extra=("n_instances", "refinement_efficiency"),
            markup=False,
        ),
        column_time_remaining_t(elapsed_when_finished=True),
    )
    progress_tracker = progress_t.New(
        *columns, for_several_processes=in_parallel, with_overall_progress=None
    )
    if not called_from_cli:
        progress_tracker.disable = True

    start_time = time.time_ns()

    if in_parallel:
        chunked_bounds = prll.ChunkedBounds(
            SIGNAL_CONTEXT.lengths, SIGNAL_CONTEXT.domain, n_workers
        )
        output = progress_tracker.sharing_manager.list()
        prll.DetectObjectsInAllChunks(
            detection_prm,
            chunked_bounds,
            output,
            previous_detection,
            progress_tracker,
        )

        detection.Initialize(output[0])
        for from_chunk in output[1:]:
            if from_chunk.__len__() == 0:
                continue
            detection.Update(from_chunk, live_mode=False)
    else:
        task_id = progress_tracker.NewTask(
            f"{LINE_INDENT}Progress",
            n_iterations=detection.n_iterations,
            n_non_blank_its=0,
            n_instances=0,
            refinement_efficiency=0,
        )
        if previous_detection is not None:
            detection.Initialize(previous_detection)
        DetectObjectsInOneChunk(
            detection, SIGNAL_CONTEXT.domain, None, progress_tracker, task_id
        )
        progress_tracker.Close()

    L.info(f"Detection time: {(time.time_ns() - start_time) / 1e9:.3f}s")

    return detection.AsListWithDecreasingQualities()


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
