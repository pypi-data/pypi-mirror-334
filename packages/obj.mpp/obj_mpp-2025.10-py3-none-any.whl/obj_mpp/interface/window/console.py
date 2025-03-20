"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import typing as h

from babelwidget.main import backend_t
from babelwidget.main import base_h as library_wgt_h
from babelwidget.main import label_h as label_wgt_h
from babelwidget.main import text_box_h as text_box_wgt_h
from rich.console import Console as rich_console_t
from rich.errors import NotRenderableError
from rich.segment import Segment as segment_t
from rich.terminal_theme import DEFAULT_TERMINAL_THEME

RULE_WIDTH = 80


@d.dataclass(slots=True, repr=False, eq=False)
class qt_console_t:
    backend: d.InitVar[backend_t]

    rich_console: rich_console_t = d.field(init=False)
    library_wgt: library_wgt_h = d.field(init=False)
    contents: text_box_wgt_h = d.field(init=False)
    progress_bar: label_wgt_h = d.field(init=False)
    FlushEvents: h.Callable[[], None] = d.field(init=False)

    def __post_init__(self, backend: backend_t) -> None:
        """"""
        self.rich_console = rich_console_t(highlight=False, force_terminal=True)

        self.library_wgt = backend.base_t()
        self.contents = backend.text_box_t("")
        self.progress_bar = backend.label_t(
            '<font color="orange">... Processing ...</font>'
        )

        self.contents.setReadOnly(True)
        self.contents.setUndoRedoEnabled(False)
        self.contents.setLineWrapMode(backend.LINE_NO_WRAP)
        self.contents.setWordWrapMode(backend.WORD_NO_WRAP)
        self.contents.setStyleSheet("font-family: monospace;")

        self.progress_bar.setVisible(False)
        self.progress_bar.setAlignment(backend.ALIGNED_CENTER)

        # size_policy = wdgt.QSizePolicy()
        # size_policy.setHorizontalPolicy(wdgt.QSizePolicy.Expanding)
        # self.qt_title.setSizePolicy(size_policy)
        # self.contents.setSizePolicy(size_policy)

        layout = backend.vbox_lyt_t()
        layout.addWidget(self.contents)
        layout.addWidget(self.progress_bar)
        self.library_wgt.setLayout(layout)

        self.FlushEvents = backend.qt_core_app_t.processEvents

    # def setWidth(self, width: int, /)-> None:
    #     """"""
    #     self.qt_title.resize(width, self.qt_title.height())
    #     self.contents.resize(width, self.contents.height())

    def StartProgressTracker(self) -> None:
        """"""
        self.progress_bar.setVisible(True)
        self.FlushEvents()

    def StopProgressTracker(self) -> None:
        """"""
        self.progress_bar.setVisible(False)

    def print(self, message: str | h.Iterable[segment_t] | h.Any, /, *_, **__) -> None:
        """"""
        if isinstance(message, str):
            segments = self.rich_console.render(message)
        elif (renderable := getattr(message, "renderable", None)) is None:
            try:
                segments = self.rich_console.render(message)
            except NotRenderableError:
                segments = message
        else:
            segments = self.rich_console.render(renderable)

        if isinstance(segments, h.Iterable):
            # Inspired from the code of: rich.console.export_html.
            html_segments = []
            for text, style, _ in segments:
                if text == "\n":
                    html_segments.append("\n")
                else:
                    if style is not None:
                        style = style.get_html_style(DEFAULT_TERMINAL_THEME)
                        if (style is not None) and (style.__len__() > 0):
                            text = f'<span style="{style}">{text}</span>'
                    html_segments.append(text)
            if html_segments[-1] == "\n":
                html_segments = html_segments[:-1]
        else:
            html_segments = (str(segments),)

        # /!\ For some reason, the widget splits the message into lines, place each line
        # inside a pre tag, and set margin-bottom of the first and list lines to 12px.
        # This can be seen by printing self.contents.toHtml(). To avoid the unwanted
        # extra margins, margin-bottom is set to 0 below.
        self.contents.append(
            "<pre style='margin-bottom:0px'>" + "".join(html_segments) + "</pre>"
        )

        self.FlushEvents()

    def rule(self, *_, **__) -> None:
        """"""
        self.contents.append(
            "<span style='color:green'>" + RULE_WIDTH * "―" + "</span>"
        )
        self.FlushEvents()

    def Clear(self) -> None:
        """"""
        self.contents.clear()


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
