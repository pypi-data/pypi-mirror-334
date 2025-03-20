"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import sys as sstm

import numpy as n
from conf_ini_g.api.functional import config_t as config_definition_t
from conf_ini_g.api.functional import config_typed_h
from conf_ini_g.api.visual import config_t as config_visual_t
from logger_36 import L
from logger_36.api.exception import OverrideExceptionFormat
from logger_36.api.handler import AddGenericHandler
from obj_mpp.app.config import AddINIPathToHistory, LoadedConfig
from obj_mpp.app.detection_cli import Config
from obj_mpp.app.detection_cli import MainRaw as MainRawCLI
from obj_mpp.config.app import APP_NAME
from obj_mpp.config.color import COLOR_CONTOUR
from obj_mpp.constant.config.definition import DEFINITION
from obj_mpp.interface.window.feedback import FeedbackWidget
from obj_mpp.runtime.backend import BACKEND
from obj_mpp.task.analysis.illustration import ContourMapOfDetection
from skimage.io import imread as ImageLoadedBySkimageFrom

event_loop = BACKEND.event_loop_t(sstm.argv)
feedback_wgt, qt_console, qt_image = FeedbackWidget(BACKEND)


def MainRaw(
    title: str,
    config_definition: config_definition_t,
    advanced_mode: bool,
    /,
) -> None:
    """"""
    _, history = LoadedConfig()
    config_scr = config_visual_t.New(
        title,
        config_definition,
        BACKEND,
        history=history,
        UpdateHistory=AddINIPathToHistory,
        action=("Run Detection", lambda _arg: _RunDetection(_arg)),
        advanced_mode=advanced_mode,
    )
    config_scr.SyncWithFunctional()
    config_scr.show()

    layout = BACKEND.hbox_lyt_t()
    layout.addWidget(config_scr.library_wgt)
    layout.addWidget(feedback_wgt)

    window = BACKEND.base_t()
    window.setWindowTitle("Obj.MPP Detector")
    window.setLayout(layout)
    config_scr.ReassignCloseButtonTarget()
    window.show()
    end_status = event_loop.Run()
    sstm.exit(end_status)


def _RunDetection(config: config_typed_h, /) -> None:
    """"""
    qt_console.Clear()
    qt_image.SetImage(n.ones((1, 1), dtype=n.uint8))

    qt_console.StartProgressTracker()
    all_mkpts = MainRawCLI(config, called_from_cli=False)
    qt_console.StopProgressTracker()

    if all_mkpts.__len__() == 0:
        return

    last_path = tuple(all_mkpts.keys())[-1]
    mkpts = all_mkpts[last_path]
    if mkpts.__len__() == 0:
        return

    try:
        image = ImageLoadedBySkimageFrom(last_path)
    except Exception as exception:
        image = None
        qt_image.library_wgt.setText(str(exception))
    if image is not None:
        contour_map = ContourMapOfDetection(mkpts) > 0
        contour_points = contour_map.nonzero()
        qt_image.SetImage(image)
        qt_image.library_wgt.DrawPoints(contour_points, COLOR_CONTOUR)


def Main() -> None:
    """"""
    OverrideExceptionFormat()
    AddGenericHandler(L, qt_console.print)

    (
        specification_,
        advanced_mode_,
    ) = Config(APP_NAME, DEFINITION)
    MainRaw(
        APP_NAME,
        specification_,
        advanced_mode_,
    )


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
