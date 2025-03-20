"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import sys as sstm
import typing as h
from csv import writer as csv_saver_t
from pathlib import Path as path_t

import numpy as nmpy
from json_any.api.storage import StoreAsJSON
from logger_36 import L
from obj_mpp.constant.interface.storage import JSON_BASE_NAME
from obj_mpp.interface.storage.save.generic import OutputDocument
from obj_mpp.runtime.model import MARKED_POINT_MODEL
from obj_mpp.task.analysis.illustration import (
    ContourMapOfDetection,
    RegionMapOfDetection,
)
from obj_mpp.task.analysis.signal import (
    SignalStatisticsInBackground,
    SignalStatisticsInMarkedPoint,
)
from obj_mpp.type.marked_point.instance.base import instance_t

import imageio as mgio


def SaveDetectionInCSVFormat(
    instances: h.Sequence[instance_t],
    signal_id: str | None,
    base_path: path_t,
    /,
    *,
    sep: str = ",",
) -> None:
    """
    Originally, the code used __class__ and isinstance. But this does not always work as
    expected!
    See https://stackoverflow.com/questions/10582774/python-why-can-isinstance-return-false-when-it-should-return-true
    for example.
    """
    if instances.__len__() == 0:
        return

    class_name = type(instances[0]).__name__
    if any(_elm.__class__.__name__ != class_name for _elm in instances[1:]):
        types = set(_elm.__class__.__name__ for _elm in instances)
        L.warning(f"Types: Mixed types in mkpt list in CSV output: {types}")

    path = OutputDocument(base_path, "marked-points", "csv", signal_id)
    with open(path, "w", encoding=sstm.getfilesystemencoding()) as csv_accessor:
        csv_writer = csv_saver_t(csv_accessor, delimiter=sep)

        csv_writer.writerow(
            MARKED_POINT_MODEL.DescriptionHeader(educated_version=True)
            + SignalStatisticsInMarkedPoint(instances[0], header_instead=True)
            + SignalStatisticsInBackground(None)
        )

        bck_stat = SignalStatisticsInBackground(instances)
        for instance in instances:
            csv_writer.writerow(
                instance.AsTuple(educated_version=True)
                + SignalStatisticsInMarkedPoint(instance)
                + bck_stat
            )


def SaveDetectionInJSONFormat(
    instances: h.Sequence[instance_t], signal_id: str | None, base_path: path_t, /
) -> None:
    """"""
    if instances.__len__() == 0:
        return

    path = OutputDocument(base_path, JSON_BASE_NAME, "json", signal_id)
    StoreAsJSON(instances, path, should_continue_on_error=True)


def SaveDetectionAsContourImage(
    dimension: int,
    instances: h.Sequence[instance_t],
    signal_id: str | None,
    base_path: path_t,
    /,
) -> None:
    """"""
    if instances.__len__() == 0:
        return

    contour_map = ContourMapOfDetection(instances)
    if dimension == 2:
        path = OutputDocument(base_path, "contour", "png", signal_id)
        mgio.imwrite(path, contour_map)
    elif dimension == 3:
        path = OutputDocument(base_path, "contour", "tif", signal_id)
        mgio.volwrite(path, contour_map)
    else:
        L.warning(f"Contour output in {dimension}-D not implemented")


def SaveDetectionAsRegionImage(
    dimension: int,
    instances: h.Sequence[instance_t],
    signal_id: str | None,
    base_path: path_t,
    /,
) -> None:
    """"""
    if instances.__len__() == 0:
        return

    region_map = RegionMapOfDetection(instances)
    if dimension == 2:
        path = OutputDocument(base_path, "region", "png", signal_id)
        mgio.imwrite(path, region_map)
    elif dimension == 3:
        path = OutputDocument(base_path, "region", "tif", signal_id)
        mgio.volwrite(path, region_map)
    else:
        L.warning(f"Region output in {dimension}-D not implemented")


def SaveDetectionAsRegionNumpyArray(
    _: int,
    instances: h.Sequence[instance_t],
    signal_id: str | None,
    base_path: path_t,
    /,
) -> None:
    """"""
    if instances.__len__() == 0:
        return

    region_map = RegionMapOfDetection(instances)
    path = OutputDocument(base_path, "region", "npz", signal_id)
    nmpy.savez_compressed(path, detection=region_map)


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
