"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import typing as h
from pathlib import Path as path_t

import matplotlib.cm as clmp
import matplotlib.colors as clrs
import matplotlib.pyplot as pypl
import matplotlib.widgets as wdgt
import numpy as nmpy
import obj_mpp.interface.storage.save.detection as save
import scipy.ndimage as spim
import skimage.measure as msre
from matplotlib.backend_bases import Event as event_t
from matplotlib.backend_bases import FigureCanvasBase as canvas_t
from matplotlib.backend_bases import MouseEvent as event_mouse_t
from matplotlib.backend_bases import RendererBase as renderer_t
from matplotlib.text import Annotation as base_annotation_t
from matplotlib.text import Text as text_t
from mpl_toolkits.axes_grid1.inset_locator import inset_axes as inset_axes_t
from mpl_toolkits.mplot3d import Axes3D as axes_3d_t
from mpl_toolkits.mplot3d import proj3d as prj3
from obj_mpp.extension.type import number_h
from obj_mpp.runtime.model import MARKED_POINT_MODEL
from obj_mpp.type.exception import ShouldNeverHappenException
from obj_mpp.type.marked_point.instance.base import instance_t
from skimage.io import imsave as SaveImageWithSkimage

_CSV_SEPARATORS = (",", ".", ";", ":", "/", "|", "\\")

_ANNOTATION_TEXT_STYLE = {"fc": "yellow", "boxstyle": "round,pad=0.5", "alpha": 0.5}
_ANNOTATION_ARROW_STYLE = {"arrowstyle": "->", "connectionstyle": "arc3,rad=0"}
_ANNOTATION_STYLE = {
    "textcoords": "offset pixels",
    "fontsize": 9,
    "horizontalalignment": "center",
    "verticalalignment": "bottom",
    "bbox": _ANNOTATION_TEXT_STYLE,
    "arrowprops": _ANNOTATION_ARROW_STYLE,
}


array_t = nmpy.ndarray

button_press_event_t = h.TypeVar("button_press_event_t", bound=event_t | event_mouse_t)
button_release_event_t = h.TypeVar(
    "button_release_event_t", bound=event_t | event_mouse_t
)


@d.dataclass(slots=True, repr=False, eq=False)
class detection_window_t:
    instances: h.Sequence[instance_t]

    image: d.InitVar[array_t]

    root: pypl.Figure = d.field(init=False)
    grid: pypl.GridSpec = d.field(init=False)
    main_axes: pypl.Axes = d.field(init=False)
    buttons: tuple[wdgt.Button, ...] = d.field(init=False)
    sep_slider: wdgt.Slider = d.field(init=False)
    instances_lmp: array_t = d.field(init=False)
    viewpoint_3D_status: text_t = d.field(init=False)
    click_3D_position: tuple[int, int] = d.field(init=False)

    def __post_init__(self, image: array_t) -> None:
        """"""
        root = pypl.figure()
        root.set_layout_engine("constrained")
        root.get_layout_engine().set(wspace=0, hspace=0)
        self.root = root

        grid = root.add_gridspec(nrows=3, ncols=6, height_ratios=[0.8, 0.17, 0.03])
        self.grid = grid

        self._AddSaveButtonsForImage(image, self.instances)
        self._AddSeparatorSlider()

    @classmethod
    def NewFor2D(
        cls,
        image: array_t,
        instances: h.Sequence[instance_t],
        instances_lmp: array_t,
        /,
    ) -> h.Self:
        """"""
        output = cls(instances=instances, image=image)
        output.instances_lmp = instances_lmp

        output.main_axes = output.root.add_subplot(output.grid[0, :], label="main")
        # Only to lighten code below
        axes = output.main_axes

        axes.xaxis.tick_top()
        axes.set_ylabel("Row")
        axes.format_coord = lambda x, y: f"R:{int(y + 0.5)},C:{int(x + 0.5)}"

        _ = output.root.canvas.mpl_connect(
            "button_press_event", output._On2DButtonPress
        )

        return output

    @classmethod
    def NewFor3D(cls, image: array_t, instances: h.Sequence[instance_t], /) -> h.Self:
        """"""
        output = cls(instances=instances, image=image)

        output.main_axes = output.root.add_subplot(
            output.grid[0, :], label="main", projection=axes_3d_t.name
        )

        axes = output.main_axes

        axes.set_xlim(left=0, right=image.shape[0])
        axes.set_ylim(bottom=0, top=image.shape[1])
        axes.set_zlim(bottom=0, top=image.shape[2])

        coords = ("x", "y", "z")
        labels = ("X=Row", "Y=Col", "Z=Depth")
        colors = ("red", "green", "blue")
        for axis_lbl, label, color in zip(coords, labels, colors, strict=True):
            labeling_fct = getattr(axes, f"set_{axis_lbl}label")
            axis = getattr(axes, axis_lbl + "axis")

            labeling_fct(label)
            axis.label.set_color(color)
            axis.line.set_color(color)
            axes.tick_params(axis_lbl, colors=color)

        output.viewpoint_3D_status = axes.text2D(
            0, 1, f"Az={axes.azim}, El={axes.elev}", transform=axes.transAxes
        )

        canvas = output.root.canvas
        _ = canvas.mpl_connect("button_press_event", output._On3DButtonPress)
        _ = canvas.mpl_connect("button_release_event", output._On3DButtonRelease)

        return output

    def _AddSaveButtonsForImage(
        self, image: array_t, instances: h.Sequence[instance_t] | None, /
    ) -> None:
        """"""
        pypl.rc("font", size=8)

        all_arguments = (
            ("Save\nImage\nas PNG", "save image as png", image),
            ("Save\nImage\nas NPZ", "save image as npz", image),
            ("Save\nContour\nImage", "save contour image", instances),
            ("Save\nRegion\nImage", "save region image", instances),
            ("Save\nMarks\nas CSV", "save marks as csv", instances),
            ("Save\nMarked\nPoints", "save marked points", instances),
        )

        # Another Matplotlib nicety: despite countless attempts, this is the best I found to factorize button creation!
        if (instances is not None) and (MARKED_POINT_MODEL.dimension == 2):
            btn_save_0 = self._NewSaveButton(0, all_arguments[0])
        else:
            btn_save_0 = None
        btn_save_1 = self._NewSaveButton(1, all_arguments[1])
        if instances is None:
            btn_save_2 = btn_save_3 = btn_save_4 = btn_save_5 = None
        else:
            btn_save_2 = self._NewSaveButton(2, all_arguments[2])
            btn_save_3 = self._NewSaveButton(3, all_arguments[3])
            btn_save_4 = self._NewSaveButton(4, all_arguments[4])
            btn_save_5 = self._NewSaveButton(5, all_arguments[5])

        # Only to keep a reference so that buttons remain responsive (see Button documentation)
        self.buttons = (
            btn_save_0,
            btn_save_1,
            btn_save_2,
            btn_save_3,
            btn_save_4,
            btn_save_5,
        )

    def _NewSaveButton(
        self, position: int, arguments: tuple[str, str, h.Any], /
    ) -> wdgt.Button:
        """"""
        button_room = self.root.add_subplot(self.grid[1, position], label=arguments[1])
        output = wdgt.Button(button_room, arguments[0])
        output.on_clicked(
            lambda _: _OnSaveButtonClicked(arguments[1], arguments[2], self.sep_slider)
        )

        return output

    def _AddSeparatorSlider(self) -> None:
        """"""
        slider_room = self.root.add_subplot(self.grid[2, :], label="sep_slider")
        self.sep_slider = wdgt.Slider(
            slider_room,
            "CSV Sep.",
            0,
            _CSV_SEPARATORS.__len__() - 1,
            valinit=0.0,
            valstep=1.0,
            valfmt="%d",
        )
        slider_room.xaxis.set_visible(True)
        slider_room.set_xticks(range(_CSV_SEPARATORS.__len__()))
        slider_room.set_xticklabels(_CSV_SEPARATORS)
        slider_room.tick_params(
            axis="x", direction="in", bottom=True, top=True, labelsize=12
        )

    def Plot2DImage(self, image: array_t, /) -> None:
        """"""
        # matshow cannot be used since image is normally RGB here.
        self.main_axes.imshow(image)

    def PlotVoxels(self, image: array_t, /) -> None:
        """"""
        self.main_axes.voxels(image, facecolors="#1f77b430")

    def PlotIsoSurface(self, image: array_t, /) -> None:
        """"""
        binary_map = (image > 0.0).astype(nmpy.float16)
        vertices, faces, _, _ = msre.marching_cubes(binary_map, 0.5)

        dilated_image = spim.grey_dilation(image, size=(3, 3, 3))
        rounded_vertices = nmpy.around(vertices).astype(nmpy.uint16)
        one_v_per_f = rounded_vertices[faces[:, 0], :]
        face_values = dilated_image[tuple(one_v_per_f[:, _idx] for _idx in range(3))]
        ValueToColor = clmp.get_cmap("gist_rainbow")
        face_colors = ValueToColor(face_values)

        poly_collection = self.main_axes.plot_trisurf(
            vertices[:, 0],
            vertices[:, 1],
            faces,
            vertices[:, 2],
            edgecolor="k",
            linewidth=0.15,
        )
        # Passing facecolors to plot_trisurf does not work!
        poly_collection.set_facecolors(face_colors)

    def PlotAnnotations(self) -> None:
        """"""
        font_dct = {"family": "monospace", "color": "red", "size": 8, "va": "center"}

        # https://matplotlib.org/api/text_api.html#matplotlib.text.Text.get_window_extent
        for instance in self.instances:
            h_offset = (instance.bbox.max_s[1] - instance.bbox.min_s[1] + 1) // 4
            self.main_axes.text(
                instance.point[1] - h_offset,
                instance.point[0],
                str(id(instance)),
                fontdict=font_dct,
            )

    def AddColorbar(self, quality_details: dict[str, h.Any], dimension: int, /) -> None:
        """"""
        max_n_ticks = 7

        un_infinite_ized = nmpy.sort(quality_details["un_infinite_ized"])
        pushed_against_1 = quality_details["pushed_against_1"]

        n_un_infinite_ized = un_infinite_ized.__len__()
        if n_un_infinite_ized < 2:
            return

        if dimension == 2:
            colors = nmpy.zeros((pushed_against_1.__len__(), 4), dtype=nmpy.float64)
            colors[:, 3] = 1.0
            colors[:, 0] = pushed_against_1[::-1]
            colormap = clrs.ListedColormap(colors)
            container = inset_axes_t(
                self.main_axes,
                width="5%",
                height="100%",
                loc="right",
                bbox_to_anchor=(0.075, 0, 1, 1),
                bbox_transform=self.main_axes.transAxes,
                borderpad=0,
            )
            axes = None
        else:
            ValueToColor = clmp.get_cmap("gist_rainbow")
            colormap = clrs.ListedColormap(ValueToColor(pushed_against_1[::-1]))
            container = None
            axes = self.main_axes

        if n_un_infinite_ized > max_n_ticks:
            step = (n_un_infinite_ized - 1) / (max_n_ticks - 1)
            kept_idc = nmpy.fromiter(
                (round(_elm * step) for _elm in range(max_n_ticks)),
                dtype=nmpy.uint64,
            )
            ticks = un_infinite_ized[nmpy.unique(kept_idc)]
        else:
            ticks = un_infinite_ized

        if n_un_infinite_ized > 1:
            centers = (
                0.5
                * (un_infinite_ized[: (n_un_infinite_ized - 1)] + un_infinite_ized[1:])
            ).tolist()
            normalization = clrs.BoundaryNorm(
                [un_infinite_ized[0]] + centers + [un_infinite_ized[-1]],
                n_un_infinite_ized,
            )
        else:
            normalization = clrs.NoNorm(
                vmin=un_infinite_ized.item(0), vmax=un_infinite_ized.item(-1)
            )

        # The creation of axes for the colorbar disturbs the layout, regardless of
        # use_gridspec. In 3D, this does not make much of a difference, but in 2D the
        # layout becomes ugly. Hence the container hack in 2D.
        colorbar = self.root.colorbar(
            clmp.ScalarMappable(cmap=colormap, norm=normalization),
            cax=container,
            ax=axes,
            ticks=ticks,
            spacing="proportional",
            label="Quality",
        )
        colorbar.set_ticks(ticks)
        colorbar.ax.tick_params(axis="y", direction="inout")
        # This is necessary only because of the container hack
        colorbar.ax.zorder = -10

    def _On2DButtonPress(self, event: button_press_event_t, /) -> None:
        """"""
        if event.inaxes == self.main_axes:
            row = int(event.ydata + 0.5)
            col = int(event.xdata + 0.5)
            label = self.instances_lmp[row, col].item()

            if label > 0:
                instance = self.instances[label - 1]
                text, reference, offset = _MKPTAnnotation(instance)
                self.main_axes.annotate(
                    text, xy=reference, xytext=offset, **_ANNOTATION_STYLE
                )
                event.canvas.draw_idle()

                return

        self._RemoveAllAnnotations(event.canvas)

    def _On3DButtonPress(self, event: button_press_event_t, /) -> None:
        """"""
        self.click_3D_position = (event.x, event.y)

    def _On3DButtonRelease(self, event: button_release_event_t, /) -> None:
        """"""
        if (event.x, event.y) == self.click_3D_position:
            idx_o_closest = self._MKPTClosestToEvent(event)
            if idx_o_closest is None:
                self._RemoveAllAnnotations(event.canvas)
            else:
                self._Annotate3DMKPT(event.canvas, idx_o_closest)
        else:
            self.viewpoint_3D_status.set_text(
                f"Az={int(round(self.main_axes.azim))}, El={int(round(self.main_axes.elev))}"
            )
            event.canvas.draw_idle()

    def _Annotate3DMKPT(self, canvas: canvas_t, index: int, /) -> None:
        """"""
        text, reference, offset = _MKPTAnnotation(self.instances[index])
        annotation = annotation_t(
            text,
            self.main_axes.get_proj(),
            xyz=reference,
            xytext=offset,
            **_ANNOTATION_STYLE,
        )
        self.main_axes.add_artist(annotation)

        canvas.draw_idle()

    def _RemoveAllAnnotations(self, canvas: canvas_t, /) -> None:
        """"""
        any_removed = False
        for child in self.main_axes.get_children():
            # Leave base_annotation_t here (as opposed to annotation_t) so that it works for both 2-D and 3-D
            if isinstance(child, base_annotation_t):
                child.remove()
                any_removed = True
        if any_removed:
            canvas.draw_idle()

    def _MKPTClosestToEvent(self, event: button_release_event_t, /) -> int | None:
        """"""
        sq_distances = tuple(
            self._EventToPointSqDistance(event, _elm.point) for _elm in self.instances
        )
        min_sq_distance = min(sq_distances)
        output = nmpy.argmin(sq_distances).item()

        half_sq_lengths = (
            (_elm / 2) ** 2 for _elm in self.instances[output].bbox.lengths
        )
        if min_sq_distance > max(half_sq_lengths):
            return None

        return output

    def _EventToPointSqDistance(
        self, event: button_release_event_t, point_3D: h.Sequence[number_h], /
    ) -> float:
        """"""
        x2_01, y2_01, _ = prj3.proj_transform(*point_3D, self.main_axes.get_proj())
        x2, y2 = self.main_axes.transData.transform((x2_01, y2_01))

        return (x2 - event.x) ** 2 + (y2 - event.y) ** 2


class annotation_t(base_annotation_t):
    """
    Ideally, this class should not be necessary, but somehow, something working when
    outside a custom figure class (rotation of annotations with axes) does not work
    here.
    """

    def __init__(
        self,
        text: str,
        projection_matrix: array_t,
        /,
        *,
        xyz: tuple[number_h, ...] | None = None,
        **kwargs,
    ):
        """"""
        super().__init__(text, xy=(0, 0), **kwargs)
        self._verts3d = xyz
        self.__projection_matrix__ = projection_matrix

    def draw(self, renderer: renderer_t, /) -> None:
        """
        The projection matrix used to be passed as: renderer.M.
        It is now self.__projection_matrix__.
        It could also be: self.axes.M.
        """
        xs, ys, _ = prj3.proj_transform(*self._verts3d, self.__projection_matrix__)
        self.xy = (xs, ys)
        super().draw(renderer)


def _MKPTAnnotation(
    instance: instance_t, /
) -> tuple[str, tuple[number_h, ...], tuple[number_h, ...]]:
    """"""
    bbox_lengths = instance.bbox.lengths

    if bbox_lengths.__len__() == 2:
        reference = tuple(reversed(instance.point))
        offset = (0.5 * bbox_lengths[1] + 10, 0.5 * bbox_lengths[0] + 15)
    else:
        reference = instance.point
        single_offset = 3 * max(tuple(0.5 * _elm + 5 for _elm in bbox_lengths))
        offset = 2 * (single_offset,)

    pos_as_str = ", ".join(f"{_elm:.2f}" for _elm in instance.point)
    marks_as_str = "/".join(map(str, instance.marks))
    annotation = f"Q={instance.quality:.3f}\n" f"{pos_as_str}\n" f"{marks_as_str}"

    return annotation, reference, offset


def _OnSaveButtonClicked(
    operation: str, data: h.Any, sep_slider: wdgt.Slider, /
) -> None:
    """"""
    if operation == "save image as png":
        img_path = _SavePath("Image", "Image", "Image", "png")
        if img_path is not None:
            SaveImageWithSkimage(img_path, nmpy.around(255.0 * data).astype("uint8"))
    elif operation == "save image as npz":
        img_path = _SavePath("Image Array", "Image Array", "Numpy", "npz")
        if img_path is not None:
            nmpy.savez_compressed(img_path, data)
    elif operation == "save contour image":
        dimension = MARKED_POINT_MODEL.dimension
        if dimension == 2:
            extension = "png"
        else:
            extension = "tif"
        img_path = _SavePath("Contour Image", "Contour Image", "Image", extension)
        if img_path is not None:
            save.SaveDetectionAsContourImage(dimension, data, None, img_path)
    elif operation == "save region image":
        dimension = MARKED_POINT_MODEL.dimension
        if dimension == 2:
            extension = "png"
        else:
            extension = "tif"
        img_path = _SavePath("Region Image", "Region Image", "Image", extension)
        if img_path is not None:
            save.SaveDetectionAsRegionImage(dimension, data, None, img_path)
    elif operation == "save marks as csv":
        csv_path = _SavePath("Marks", "Marks", "CSV", "csv")
        if csv_path is not None:
            save.SaveDetectionInCSVFormat(
                data, None, csv_path, sep=_CSV_SEPARATORS[int(sep_slider.val)]
            )
    elif operation == "save marked points":
        json_path = _SavePath("Marked Points", "Marked Points", "JSON", "json")
        if json_path is not None:
            save.SaveDetectionInJSONFormat(data, None, json_path)
    else:
        raise ShouldNeverHappenException(f'Unknown operation "{operation}"')


def _SavePath(
    for_title: str, for_message: str, for_filter: str, extension: str, /
) -> path_t | None:
    """"""
    # TODO: To be changed.
    return path_t("/tmp") / f"{for_title}.{extension}"


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
