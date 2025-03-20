"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import sys as sstm
import typing as h
from pathlib import Path as path_t

import obj_mpp.interface.storage.save.detection as svdt
from conf_ini_g.api.console import CommandLineConfig, CommandLineParser
from conf_ini_g.api.functional import config_definition_h as config_raw_h
from conf_ini_g.api.functional import config_t as config_definition_t
from conf_ini_g.api.functional import config_typed_h
from conf_ini_g.api.storage import INIConfig, SaveConfigToINIDocument
from logger_36 import L
from logger_36.api.system import LogSystemDetails
from logger_36.api.time import TimeStamp
from obj_mpp.config.app import APP_NAME
from obj_mpp.constant.catalog import (
    I_CATALOG_SECTION,
    MPI_CATALOG_SECTION,
    MPM_CATALOG_SECTION,
    O_CATALOG_SECTION,
    Q_CATALOG_SECTION,
)
from obj_mpp.constant.config.definition import DEFINITION
from obj_mpp.constant.config.label import label_e
from obj_mpp.interface.console.detection import ReportDetectedMarkedPoints
from obj_mpp.interface.storage.load.detection import PreviousDetection
from obj_mpp.interface.storage.save.generic import CreateOutputFolder, OutputDocument
from obj_mpp.runtime.model import MARKED_POINT_MODEL
from obj_mpp.runtime.quality import QUALITY_CONTEXT
from obj_mpp.runtime.signal import SIGNAL_CONTEXT
from obj_mpp.task.catalog.importer import ImportedElement
from obj_mpp.task.catalog.specifier import (
    SpecifyCatalogMarkedPoints,
    SpecifyCatalogQualities,
)
from obj_mpp.task.detection.main import DetectedObjects
from obj_mpp.task.sampling.marked_point import sampler_t
from obj_mpp.task.validation.interface import (
    CheckLoadingFunction,
    CheckOutputFunction,
    CheckRequestedOutputs,
)
from obj_mpp.task.validation.point import CheckPointConstraint
from obj_mpp.type.config.algorithm import config_t as algorithm_config_t
from obj_mpp.type.config.marked_point import config_t as marked_point_config_t
from obj_mpp.type.config.output import config_t as output_config_t
from obj_mpp.type.config.signal import config_t as signal_config_t
from obj_mpp.type.marked_point.instance.base import instance_t as base_instance_t


def MainRaw(
    config: config_typed_h, /, *, called_from_cli: bool = True
) -> dict[path_t, list[base_instance_t]]:
    """"""
    L.ResetEventCounts()

    time_tag = TimeStamp()
    algorithm_cfg, marked_point_cfg, signal_cfg, output_cfg = _ConfigSections(config)

    # --- CLASS and FUNCTION IMPORT
    #
    model_t = ImportedElement(marked_point_cfg.main["definition"], MPM_CATALOG_SECTION)
    instance_t = ImportedElement(
        marked_point_cfg.main["definition"], MPI_CATALOG_SECTION
    )

    quality_context_t = ImportedElement(
        marked_point_cfg.quality["definition"], Q_CATALOG_SECTION
    )
    if quality_context_t is not None:
        quality_context_t = quality_context_t[0]

    SignalLoading_fct = ImportedElement(
        signal_cfg.main["loading_function"], I_CATALOG_SECTION
    )
    CheckLoadingFunction(SignalLoading_fct, signal_cfg.loading_prm)

    if output_cfg.main["output_function"] is None:
        SignalOutput_fct = None
    else:
        SignalOutput_fct = ImportedElement(
            output_cfg.main["output_function"], O_CATALOG_SECTION
        )
        CheckOutputFunction(SignalOutput_fct, output_cfg.output_prm)
    requested_outputs = output_cfg.main["what"]
    if requested_outputs is None:
        requested_outputs = ()
    else:
        requested_outputs = tuple(map(str.strip, requested_outputs.split(",")))
        CheckRequestedOutputs(requested_outputs)

    # --- ERROR REPORT
    #
    if L.has_staged_issues:
        L.CommitIssues()
        if called_from_cli:
            sstm.exit(1)
        else:
            return {}

    # --- RUNTIME INITIALIZATION
    #
    MARKED_POINT_MODEL.Initialize(model_t)
    dimension = MARKED_POINT_MODEL.dimension

    if MARKED_POINT_MODEL.AreMarkRangesValid(marked_point_cfg.mark_ranges):
        normalized_mark_ranges = MARKED_POINT_MODEL.NormalizedMarkRanges(
            marked_point_cfg.mark_ranges
        )
    else:
        normalized_mark_ranges = None

    QUALITY_CONTEXT.Initialize(
        quality_context_t,
        q_kwargs=marked_point_cfg.quality_prm,
        s_kwargs=signal_cfg.processing_prm,
    )

    point_constraint = marked_point_cfg.main["center"]
    CheckPointConstraint(point_constraint, dimension)
    SIGNAL_CONTEXT.Initialize(
        signal_cfg.main["path"],
        point_constraint,
        SignalLoading_fct,
        dimension,
        **signal_cfg.loading_prm,
    )

    output_folder = output_cfg.main["base_folder"]
    if output_folder is not None:
        output_folder = CreateOutputFolder(output_folder / time_tag)

    # --- ERROR REPORT
    #
    if L.has_staged_issues:
        L.CommitIssues()
        if called_from_cli:
            sstm.exit(1)
        else:
            return {}

    # --- DETECTION PROCEDURE
    #
    output = {}

    sampler = sampler_t(seed=algorithm_cfg.main["seed"])
    sampler.SetPointMode(point_constraint)
    sampler.SetMarkParameters(normalized_mark_ranges, MARKED_POINT_MODEL.mark_types)

    SaveDetection = dict(
        zip(
            ("contour", "region", "region_numpy"),
            (
                svdt.SaveDetectionAsContourImage,
                svdt.SaveDetectionAsRegionImage,
                svdt.SaveDetectionAsRegionNumpyArray,
            ),
            strict=True,
        )
    )

    for signal_idx, (signal_path, signal_id) in enumerate(
        SIGNAL_CONTEXT.LazySignalDetails(), start=1
    ):
        if signal_id is None:
            continue

        L.DisplayRule()
        L.info(f"Signal#{signal_idx}: {signal_path}+{SIGNAL_CONTEXT.map_or_pdf_is_new}")

        if QUALITY_CONTEXT.SetSignal(SIGNAL_CONTEXT.signal_for_qty):
            L.error("Signal skipped by quality context.")
            continue

        if sampler.point_is_map_or_pdf:
            if SIGNAL_CONTEXT.map_or_pdf_is_new:
                sampler.SetPointParameters(SIGNAL_CONTEXT.map_or_pdf)
        else:  # To adapt to current signal shape.
            sampler.SetPointParameters(point_constraint)
        if not sampler.is_point_ready:
            # This can happen if the point constraint is a path to a map or PDF file
            # (but not a folder), and the file loading fails, so that the first
            # iteration is "empty" (see "continue" above). On the next iteration, there
            # will be no new map or PDF, and the point sampler will not be ready.
            continue

        previous_detection = PreviousDetection(
            algorithm_cfg.main["use_history"],
            algorithm_cfg.main["fixed_history"],
            output_folder,
            signal_id,
        )

        local_output = DetectedObjects(
            instance_t,
            sampler,
            marked_point_cfg.quality["min_value"],
            algorithm_cfg,
            max_overlap=marked_point_cfg.constraints["max_overlap"],
            only_un_cropped=marked_point_cfg.main["only_un_cropped"],
            previous_detection=previous_detection,
            called_from_cli=called_from_cli,
        )
        output[signal_path] = local_output

        if L.has_staged_issues:
            L.CommitIssues()
            continue

        # --- --- DETECTION OUTPUT
        #
        if local_output.__len__() == 0:
            continue

        if output_cfg.main["console"]:
            ReportDetectedMarkedPoints(local_output)

        if output_folder is not None:
            SaveConfigToINIDocument(
                config, OutputDocument(output_folder, "config", "ini", signal_id)
            )
            if "csv" in requested_outputs:
                svdt.SaveDetectionInCSVFormat(
                    local_output,
                    signal_id,
                    output_folder,
                    sep=output_cfg.main["marks_separator"],
                )
            if "json" in requested_outputs:
                svdt.SaveDetectionInJSONFormat(local_output, signal_id, output_folder)
            for what in requested_outputs:
                if what not in ("csv", "json"):
                    SaveDetection[what](
                        dimension, local_output, signal_id, output_folder
                    )

        # Leave here so that in case it contains blocking instructions (like matplotlib
        # show()), it does not delay saving to files above.
        if called_from_cli and isinstance(SignalOutput_fct, h.Callable):
            SignalOutput_fct(
                local_output,
                SIGNAL_CONTEXT.signal_original,
                output_folder,
                signal_id=signal_id,
                **output_cfg.output_prm,
            )

    return output


def Config(title: str, definition_raw: config_raw_h, /) -> tuple[
    config_definition_t,
    bool,
]:
    """"""
    definition = config_definition_t(definition_raw)
    SpecifyCatalogMarkedPoints(definition)
    SpecifyCatalogQualities(definition)

    parser = CommandLineParser(title, definition)
    config_cmdline, advanced_mode, ini_path = CommandLineConfig(parser)

    if (config_cmdline.__len__() == 0) and (ini_path is None):
        raise RuntimeError(
            "No Configuration passed, either as an INI file or "
            "as command-line arguments."
        )

    issues = definition.UpdateFromINI(ini_path)
    issues.extend(definition.UpdateFromDict(config_cmdline))
    if issues.__len__() > 0:
        L.critical("!!!!\n" + "\n".join(issues) + "\n!!!!")
        sstm.exit(1)

    return (
        definition,
        advanced_mode,
    )


def _ConfigSections(
    config: config_typed_h, /
) -> tuple[algorithm_config_t, marked_point_config_t, signal_config_t, output_config_t]:
    """"""
    algorithm_cfg = algorithm_config_t(
        main=config[label_e.sct_mpp.value],
        refinement=config[label_e.sct_refinement.value],
        feedback=config[label_e.sct_feedback.value],
    )
    marked_point_cfg = marked_point_config_t(
        main=config[label_e.sct_object.value],
        mark_ranges=config[label_e.sct_mark_ranges.value],
        quality=config[label_e.sct_quality.value],
        quality_prm=config[label_e.sct_quality_prm.value],
        constraints=config[label_e.sct_constraints.value],
    )
    signal_cfg = signal_config_t(
        main=config[label_e.sct_signal.value],
        loading_prm=config[label_e.sct_signal_loading_prm.value],
        processing_prm=config[label_e.sct_signal_processing_prm.value],
    )
    output_cfg = output_config_t(
        main=config[label_e.sct_output.value],
        output_prm=config[label_e.sct_output_prm.value],
    )

    return algorithm_cfg, marked_point_cfg, signal_cfg, output_cfg


def Main() -> None:
    """"""
    L.MakeMonochrome()
    LogSystemDetails()

    config_, *_ = Config(APP_NAME, DEFINITION)
    _ = MainRaw(config_.active_as_typed_dict)


if __name__ == "__main__":
    #
    Main()


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
