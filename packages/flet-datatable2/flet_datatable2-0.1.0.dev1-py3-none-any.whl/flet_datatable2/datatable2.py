from typing import Any, List, Optional, Union

from flet.core.alignment import Alignment
from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.border import Border, BorderSide
from flet.core.box import BoxDecoration
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber
from flet.core.gradients import Gradient
from flet.core.ref import Ref
from flet.core.text_style import TextStyle
from flet.core.theme import CheckboxTheme
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    BorderRadiusValue,
    ClipBehavior,
    ColorEnums,
    ColorValue,
    ControlStateValue,
    DurationValue,
    IconEnums,
    IconValue,
    OffsetValue,
    OptionalControlEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)

from flet_datatable2.datacolumn2 import DataColumn2
from flet_datatable2.datarow2 import DataRow2


class DataTable2(ConstrainedControl):
    """In-place replacement of standard Flet [DataTable](https://flet.dev/docs/controls/datatable).

    Has the header row always fixed and core of the table (with data rows) scrollable and stretching to max width/height of it's container.
    By using [DataColumn2](datacolumn2.md) instead of [DataColumn](https://flet.dev/docs/controls/datatable#datacolumn) it is possible to control relative column sizes (setting them to S, M and L).
    [DataRow2](datarow2.md) provides row-level tap event handlers.
    """

    def __init__(
        self,
        columns: List[DataColumn2],
        rows: Optional[List[DataRow2]] = None,
        empty: Optional[Control] = None,
        bottom_margin: OptionalNumber = None,
        lm_ratio: OptionalNumber = None,
        sm_ratio: OptionalNumber = None,
        fixed_left_columns: Optional[int] = None,
        fixed_top_rows: Optional[int] = None,
        fixed_columns_color: Optional[ColorValue] = None,
        fixed_corner_color: Optional[ColorValue] = None,
        min_width: OptionalNumber = None,
        sort_ascending: Optional[bool] = None,
        show_checkbox_column: Optional[bool] = None,
        show_heading_checkbox: Optional[bool] = None,
        heading_checkbox_theme: Optional[CheckboxTheme] = None,
        data_row_checkbox_theme: Optional[CheckboxTheme] = None,
        sort_column_index: Optional[int] = None,
        sort_arrow_icon: Optional[IconValue] = None,
        sort_arrow_animation_duration: Optional[DurationValue] = None,
        show_bottom_border: Optional[bool] = None,
        is_horizontal_scroll_bar_visible: Optional[bool] = None,
        is_vertical_scroll_bar_visible: Optional[bool] = None,
        border: Optional[Border] = None,
        border_radius: Optional[BorderRadiusValue] = None,
        horizontal_lines: Optional[BorderSide] = None,
        vertical_lines: Optional[BorderSide] = None,
        checkbox_horizontal_margin: OptionalNumber = None,
        checkbox_alignment: Optional[Alignment] = None,
        column_spacing: OptionalNumber = None,
        data_row_color: ControlStateValue[ColorValue] = None,
        data_row_height: OptionalNumber = None,
        # data_row_min_height: OptionalNumber = None,
        # data_row_max_height: OptionalNumber = None,
        data_text_style: Optional[TextStyle] = None,
        bgcolor: Optional[ColorValue] = None,
        gradient: Optional[Gradient] = None,
        divider_thickness: OptionalNumber = None,
        heading_row_color: ControlStateValue[ColorValue] = None,
        heading_row_height: OptionalNumber = None,
        heading_text_style: Optional[TextStyle] = None,
        heading_row_decoration: Optional[BoxDecoration] = None,
        horizontal_margin: OptionalNumber = None,
        clip_behavior: Optional[ClipBehavior] = None,
        on_select_all: OptionalControlEventCallable = None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: Optional[RotateValue] = None,
        scale: Optional[ScaleValue] = None,
        offset: Optional[OffsetValue] = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: Optional[AnimationValue] = None,
        animate_size: Optional[AnimationValue] = None,
        animate_position: Optional[AnimationValue] = None,
        animate_rotation: Optional[AnimationValue] = None,
        animate_scale: Optional[AnimationValue] = None,
        animate_offset: Optional[AnimationValue] = None,
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: Optional[TooltipValue] = None,
        badge: Optional[BadgeValue] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.columns = columns
        self.rows = rows
        self.empty = empty
        self.fixed_left_columns = fixed_left_columns
        self.fixed_top_rows = fixed_top_rows
        self.fixed_columns_color = fixed_columns_color
        self.fixed_corner_color = fixed_corner_color
        self.bottom_margin = bottom_margin
        self.lm_ration = lm_ratio
        self.sm_ratio = sm_ratio
        self.min_width = min_width
        self.border = border
        self.border_radius = border_radius
        self.horizontal_lines = horizontal_lines
        self.is_horizontal_scroll_bar_visible = is_horizontal_scroll_bar_visible
        self.is_vertical_scroll_bar_visible = is_vertical_scroll_bar_visible
        self.vertical_lines = vertical_lines
        self.bgcolor = bgcolor
        self.gradient = gradient
        self.divider_thickness = divider_thickness
        self.checkbox_horizontal_margin = checkbox_horizontal_margin
        self.checkbox_alignment = checkbox_alignment
        self.heading_checkbox_theme = heading_checkbox_theme
        self.data_row_checkbox_theme = data_row_checkbox_theme
        self.column_spacing = column_spacing
        self.data_row_color = data_row_color
        # self.data_row_min_height = data_row_min_height
        # self.data_row_max_height = data_row_max_height
        self.data_row_height = data_row_height
        self.data_text_style = data_text_style
        self.heading_row_color = heading_row_color
        self.heading_row_height = heading_row_height
        self.heading_text_style = heading_text_style
        self.horizontal_margin = horizontal_margin
        self.show_bottom_border = show_bottom_border
        self.show_checkbox_column = show_checkbox_column
        self.show_heading_checkbox = show_heading_checkbox
        self.sort_ascending = sort_ascending
        self.sort_column_index = sort_column_index
        self.on_select_all = on_select_all
        self.clip_behavior = clip_behavior
        self.sort_arrow_icon = sort_arrow_icon
        self.sort_arrow_animation_duration = sort_arrow_animation_duration
        self.heading_row_decoration = heading_row_decoration

    def _get_control_name(self):
        return "datatable2"

    def __contains__(self, item):
        return item in self.__columns or item in self.__rows

    def before_update(self):
        super().before_update()
        visible_columns = list(filter(lambda column: column.visible, self.__columns))
        visible_rows = list(filter(lambda row: row.visible, self.__rows))
        assert (
            len(visible_columns) > 0
        ), "columns must contain at minimum one visible DataColumn"
        assert all(
            len(list(filter(lambda c: c.visible, row.cells))) == len(visible_columns)
            for row in visible_rows
        ), f"each visible DataRow must contain exactly as many visible DataCells as there are visible DataColumns ({len(visible_columns)})"
        # assert (
        #     self.data_row_min_height is None
        #     or self.data_row_max_height is None
        #     or (self.data_row_min_height <= self.data_row_max_height)
        # ), "data_row_min_height must be less than or equal to data_row_max_height"
        assert (
            self.divider_thickness is None or self.divider_thickness >= 0
        ), "divider_thickness must be greater than or equal to 0"
        assert self.sort_column_index is None or (
            0 <= self.sort_column_index < len(visible_columns)
        ), f"sort_column_index must be greater than or equal to 0 and less than the number of columns ({len(visible_columns)})"
        self._set_attr_json("border", self.__border)
        self._set_attr_json("gradient", self.__gradient)
        self._set_attr_json("borderRadius", self.__border_radius)
        self._set_attr_json("horizontalLines", self.__horizontal_lines)
        self._set_attr_json("verticalLines", self.__vertical_lines)
        self._set_attr_json("dataRowColor", self.__data_row_color)
        self._set_attr_json("headingRowColor", self.__heading_row_color)
        self._set_attr_json("dataTextStyle", self.__data_text_style)
        self._set_attr_json("headingTextStyle", self.__heading_text_style)
        self._set_attr_json("headingCheckboxTheme", self.__heading_checkbox_theme)
        self._set_attr_json("dataRowCheckboxTheme", self.__data_row_checkbox_theme)
        self._set_attr_json(
            "sortArrowAnimationDuration", self.__sort_arrow_animation_duration
        )
        self._set_attr_json("checkboxAlignment", self.__checkbox_alignment)
        self._set_attr_json("headingRowDecoration", self.__heading_row_decoration)

    def _get_children(self):
        children = self.__columns + self.__rows

        if isinstance(self.__empty, Control):
            self.__empty._set_attr_internal("n", "empty")
            children.append(self.__empty)
        return children

    # empty
    @property
    def empty(self) -> Control:
        """
        **NEW**

        Placeholder control which is displayed whenever the data rows are empty. The widget will be displayed below heading row.
        """
        return self.__empty

    @empty.setter
    def empty(self, value: Control):
        self.__empty = value

    # columns
    @property
    def columns(self) -> List[DataColumn2]:
        """
        A list of [DataColumn2](datacolumn2.md) controls describing table columns.
        """
        return self.__columns

    @columns.setter
    def columns(self, value: List[DataColumn2]):
        assert all(
            isinstance(column, DataColumn2) for column in value
        ), "columns must contain only DataColumn instances"
        self.__columns = value

    # rows
    @property
    def rows(self) -> Optional[List[DataRow2]]:
        """
        A list of [DataRow2](datarow2.md) controls defining table rows.
        """
        return self.__rows

    @rows.setter
    def rows(self, value: Optional[List[DataRow2]]):
        self.__rows = value if value is not None else []
        assert all(
            isinstance(row, DataRow2) for row in self.__rows
        ), "rows must contain only DataRow instances"

    # fixed_left_columns
    @property
    def fixed_left_columns(self) -> Optional[int]:
        """
        **NEW**

        The number of sticky columns fixed at the left side of the table. Check box column (if enabled) is also counted.
        """
        return self._get_attr("fixedLeftColumns")

    @fixed_left_columns.setter
    def fixed_left_columns(self, value: Optional[int]):
        self._set_attr("fixedLeftColumns", value)

    # fixed_top_rows
    @property
    def fixed_top_rows(self) -> Optional[int]:
        """
        **NEW**

        The number of sticky rows fixed at the top of the table. The heading row is counted/included.
        By defult the value is 1 which means header row is fixed.
        Set to 0 in order to unstick the header, set to >1 in order to fix data rows (i.e. in order to fix both header and the first data row use value of 2).
        """
        return self._get_attr("fixedTopRows")

    @fixed_top_rows.setter
    def fixed_top_rows(self, value: Optional[int]):
        self._set_attr("fixedTopRows", value)

    # fixed_columns_color
    @property
    def fixed_columns_color(self) -> Optional[ColorValue]:
        """
        **NEW**

        Backgound color of the sticky columns fixed via `fixed_left_columns`.
        """
        return self.__fixed_columns_color

    @fixed_columns_color.setter
    def fixed_columns_color(self, value: Optional[ColorValue]):
        self.__fixed_columns_color = value
        self._set_enum_attr("fixedColumnsColor", value, ColorEnums)

    # fixed_corner_color
    @property
    def fixed_corner_color(self) -> Optional[ColorValue]:
        """
        **NEW**

        Backgound color of the top left corner which is fixed when both `fixed_top_rows` and `fixed_left_columns` are greater than 0.
        """
        return self.__fixed_corner_color

    @fixed_corner_color.setter
    def fixed_corner_color(self, value: Optional[ColorValue]):
        self.__fixed_corner_color = value
        self._set_enum_attr("fixedCornerColor", value, ColorEnums)

    # bottom_margin
    @property
    def bottom_margin(self) -> OptionalNumber:
        """
        **NEW**

        If set, the table will have empty space added after the the last row.
        """
        return self._get_attr("bottomMargin")

    @bottom_margin.setter
    def bottom_margin(self, value: OptionalNumber):
        self._set_attr("bottomMargin", value)

    # sort_arrow_icon
    @property
    def sort_arrow_icon(self):
        """
        **NEW**

        Icon to be displayed when sorting is applied to a column. If not set, the default icon is `Icons.ARROW_UPWARD`.
        """
        return self.__sort_arrow_icon

    @sort_arrow_icon.setter
    def sort_arrow_icon(self, value):
        self.__sort_arrow_icon = value
        self._set_enum_attr("sortArrowIcon", value, IconEnums)

    # sort_arrow_animation_duration
    @property
    def sort_arrow_animation_duration(self) -> Optional[DurationValue]:
        """
        **NEW**

        When changing sort direction an arrow icon in the header is rotated clockwise. The value defines the duration of the rotation animation.
        If not set, the default animation duration is 150 ms.
        """
        return self.__sort_arrow_animation_duration

    @sort_arrow_animation_duration.setter
    def sort_arrow_animation_duration(self, value: Optional[DurationValue]):
        self.__sort_arrow_animation_duration = value

    # lm_ratio
    @property
    def lm_ratio(self) -> OptionalNumber:
        """
        **NEW**

        Determines ratio of Large column's width to Medium column's width. I.e. 2.0 means that Large column is twice wider than Medium column.

        The default value is `1.2`.
        """
        return self._get_attr("lmRatio")

    @lm_ratio.setter
    def lm_ratio(self, value: OptionalNumber):
        self._set_attr("lmRatio", value)

    # sm_ratio
    @property
    def sm_ratio(self) -> OptionalNumber:
        """
        **NEW**

        Determines ratio of Small column's width to Medium column's width. I.e. 0.5 means that Small column is twice narrower than Medium column.

        The default value is `0.67`.
        """
        return self._get_attr("smRatio")

    @sm_ratio.setter
    def sm_ratio(self, value: OptionalNumber):
        self._set_attr("smRatio", value)

    # min_width
    @property
    def min_width(self) -> OptionalNumber:
        """
        **NEW**

        If set, the table will stop shrinking below the threshold and provide horizontal scrolling.
        Useful for the cases with narrow screens (e.g. portrait phone orientation) and lots of columns.
        """
        return self._get_attr("minWidth")

    @min_width.setter
    def min_width(self, value: OptionalNumber):
        self._set_attr("minWidth", value)

    # border
    @property
    def border(self) -> Optional[Border]:
        """
        See DataTable [border](https://flet.dev/docs/controls/datatable#border).
        """
        return self.__border

    @border.setter
    def border(self, value: Optional[Border]):
        self.__border = value

    # border_radius
    @property
    def border_radius(self) -> Optional[BorderRadiusValue]:
        """
        See DataTable [border_radius](https://flet.dev/docs/controls/datatable#border_radius).
        """
        return self.__border_radius

    @border_radius.setter
    def border_radius(self, value: Optional[BorderRadiusValue]):
        self.__border_radius = value

    # horizontal_lines
    @property
    def horizontal_lines(self) -> Optional[BorderSide]:
        """
        See DataTable [horizontal_lines](https://flet.dev/docs/controls/datatable#horizontal_lines).
        """
        return self.__horizontal_lines

    @horizontal_lines.setter
    def horizontal_lines(self, value: Optional[BorderSide]):
        self.__horizontal_lines = value

    # vertical_lines
    @property
    def vertical_lines(self) -> Optional[BorderSide]:
        """
        See DataTable [vertical_lines](https://flet.dev/docs/controls/datatable#vertical_lines).
        """
        return self.__vertical_lines

    @vertical_lines.setter
    def vertical_lines(self, value: Optional[BorderSide]):
        self.__vertical_lines = value

    # checkbox_horizontal_margin
    @property
    def checkbox_horizontal_margin(self) -> OptionalNumber:
        """
        See DataTable [checkbox_horizontal_margin](https://flet.dev/docs/controls/datatable#checkbox_horizontal_margin).
        """
        return self._get_attr("checkboxHorizontalMargin")

    @checkbox_horizontal_margin.setter
    def checkbox_horizontal_margin(self, value: OptionalNumber):
        self._set_attr("checkboxHorizontalMargin", value)

    # checkbox_alignment
    @property
    def checkbox_alignment(self) -> Optional[Alignment]:
        """
        **NEW**

        Alignment of the checkbox if it is displayed. Defaults to the `alignment.center`.
        """
        return self.__checkbox_alignment

    @checkbox_alignment.setter
    def checkbox_alignment(self, value: Optional[Alignment]):
        self.__checkbox_alignment = value

    # heading_checkbox_theme
    @property
    def heading_checkbox_theme(self) -> Optional[CheckboxTheme]:
        """
        **NEW**

        Overrides theme of the checkbox that is displayed in the top left corner of the heading (if checkboxes are enabled).
        Value is an instance of [CheckboxTheme](https://flet.dev/docs/reference/types/checkboxtheme).
        """
        return self.__heading_checkbox_theme

    @heading_checkbox_theme.setter
    def heading_checkbox_theme(self, value: Optional[CheckboxTheme]):
        self.__heading_checkbox_theme = value

    # data_row_checkbox_theme
    @property
    def data_row_checkbox_theme(self) -> Optional[CheckboxTheme]:
        """
        **NEW**

        Overrides theme of the checkboxes that are displayed in the checkbox column in each data row (if checkboxes are enabled).
        Value is an instance of [CheckboxTheme](https://flet.dev/docs/reference/types/checkboxtheme).
        """
        return self.__data_row_checkbox_theme

    @data_row_checkbox_theme.setter
    def data_row_checkbox_theme(self, value: Optional[CheckboxTheme]):
        self.__data_row_checkbox_theme = value

    # column_spacing
    @property
    def column_spacing(self) -> OptionalNumber:
        """
        See DataTable [column_spacing](https://flet.dev/docs/controls/datatable#column_spacing).
        """
        return self._get_attr("columnSpacing")

    @column_spacing.setter
    def column_spacing(self, value: OptionalNumber):
        self._set_attr("columnSpacing", value)

    # divider_thickness
    @property
    def divider_thickness(self) -> float:
        """
        See DataTable [divider_thickness](https://flet.dev/docs/controls/datatable#divider_thickness).
        """
        return self._get_attr("dividerThickness", data_type="float", def_value=1.0)

    @divider_thickness.setter
    def divider_thickness(self, value: OptionalNumber):
        self._set_attr("dividerThickness", value)

    # horizontal_margin
    @property
    def horizontal_margin(self) -> OptionalNumber:
        """
        See DataTable [horizontal_margin](https://flet.dev/docs/controls/datatable#horizontal_margin).
        """
        return self._get_attr("horizontalMargin")

    @horizontal_margin.setter
    def horizontal_margin(self, value: OptionalNumber):
        self._set_attr("horizontalMargin", value)

    # heading_row_decoration
    @property
    def heading_row_decoration(self) -> Optional[BoxDecoration]:
        """
        **NEW**

        Decoration to be applied to the heading row.
        Value is an instance of [BoxDecoration](https://flet.dev/docs/reference/types/boxdecoration).

        When both `heading_row_color` and 'heading_row_decoration' are provided:

        * `heading_row_decoration` takes precedence if there're 0 or 1 fixed rows
        * `headeing_row_color` is applied to fixed top starting from the second row.
        * When there're both fixed top rows and fixed left columns with `fixed_corner_color` provided, this decoration overrides top left corner cell color.

        """
        return self.__heading_row_decoration

    @heading_row_decoration.setter
    def heading_row_decoration(self, value: Optional[BoxDecoration]):
        self.__heading_row_decoration = value

    # data_row_color
    @property
    def data_row_color(self) -> ControlStateValue[str]:
        """
        See DataTable [data_row_color](https://flet.dev/docs/controls/datatable#data_row_color).
        """
        return self.__data_row_color

    @data_row_color.setter
    def data_row_color(self, value: ControlStateValue[str]):
        self.__data_row_color = value

    # data_row_height
    @property
    def data_row_height(self) -> OptionalNumber:
        """
        **NEW**
        The height of each row (excluding the row that contains column headings).

        Note that, unlike in Flet [DataTable](https://flet.dev/docs/controls/datatable), there's no capability to define min/max height of a row. This is an implementation tradeoff making it possible to have performant sticky columns.
        """
        return self._get_attr("dataRowHeight")

    @data_row_height.setter
    def data_row_height(self, value: OptionalNumber):
        self._set_attr("dataRowHeight", value)

    # data_text_style
    @property
    def data_text_style(self) -> Optional[TextStyle]:
        """
        See DataTable [data_text_style](https://flet.dev/docs/controls/datatable#data_text_style).
        """
        return self.__data_text_style

    @data_text_style.setter
    def data_text_style(self, value: Optional[TextStyle]):
        self.__data_text_style = value

    # bgcolor
    @property
    def bgcolor(self) -> Optional[ColorValue]:
        """
        See DataTable [bgcolor](https://flet.dev/docs/controls/datatable#bgcolor).
        """
        return self.__bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[ColorValue]):
        self.__bgcolor = value
        self._set_enum_attr("bgColor", value, ColorEnums)

    # gradient
    @property
    def gradient(self) -> Optional[Gradient]:
        """
        See DataTable [gradient](https://flet.dev/docs/controls/datatable#gradient).
        """
        return self.__gradient

    @gradient.setter
    def gradient(self, value: Optional[Gradient]):
        self.__gradient = value

    # heading_row_color
    @property
    def heading_row_color(self) -> ControlStateValue[str]:
        """
        See DataTable [heading_row_color](https://flet.dev/docs/controls/datatable#heading_row_color).
        """
        return self.__heading_row_color

    @heading_row_color.setter
    def heading_row_color(self, value: ControlStateValue[str]):
        self.__heading_row_color = value

    # heading_row_height
    @property
    def heading_row_height(self) -> OptionalNumber:
        """
        See DataTable [heading_row_height](https://flet.dev/docs/controls/datatable#heading_row_height).
        """
        return self._get_attr("headingRowHeight")

    @heading_row_height.setter
    def heading_row_height(self, value: OptionalNumber):
        self._set_attr("headingRowHeight", value)

    # heading_text_style
    @property
    def heading_text_style(self) -> Optional[TextStyle]:
        """
        See DataTable [heading_text_style](https://flet.dev/docs/controls/datatable#heading_text_style).
        """
        return self.__heading_text_style

    @heading_text_style.setter
    def heading_text_style(self, value: Optional[TextStyle]):
        self.__heading_text_style = value

    # show_bottom_border
    @property
    def show_bottom_border(self) -> bool:
        """
        See DataTable [show_bottom_border](https://flet.dev/docs/controls/datatable#show_bottom_border).
        """
        return self._get_attr("showBottomBorder", data_type="bool", def_value=False)

    @show_bottom_border.setter
    def show_bottom_border(self, value: Optional[bool]):
        self._set_attr("showBottomBorder", value)

    # show_checkbox_column
    @property
    def show_checkbox_column(self) -> bool:
        """
        See DataTable [show_checkbox_column](https://flet.dev/docs/controls/datatable#show_checkbox_column).
        """
        return self._get_attr("showCheckboxColumn", data_type="bool", def_value=False)

    @show_checkbox_column.setter
    def show_checkbox_column(self, value: Optional[bool]):
        self._set_attr("showCheckboxColumn", value)

    # show_heading_checkbox
    @property
    def show_heading_checkbox(self) -> bool:
        """
        **NEW**

        Whether to display heading checkbox or not, if the checkbox column is present. Defaults to `True`.
        """
        return self._get_attr("showHeadingCheckbox", data_type="bool", def_value=False)

    @show_heading_checkbox.setter
    def show_heading_checkbox(self, value: Optional[bool]):
        self._set_attr("showHeadingCheckbox", value)

    # sort_ascending
    @property
    def sort_ascending(self) -> bool:
        """
        See DataTable [sort_ascending](https://flet.dev/docs/controls/datatable#sort_ascending).
        """
        return self._get_attr("sortAscending", data_type="bool", def_value=False)

    @sort_ascending.setter
    def sort_ascending(self, value: Optional[bool]):
        self._set_attr("sortAscending", value)

    # is_horizontal_scroll_bar_visible
    @property
    def is_horizontal_scroll_bar_visible(self) -> bool:
        """
        **NEW**

        Determines whether the horizontal scroll bar is visible.
        """
        return self._get_attr("isHorizontalScrollBarVisible", data_type="bool")

    @is_horizontal_scroll_bar_visible.setter
    def is_horizontal_scroll_bar_visible(self, value: Optional[bool]):
        self._set_attr("isHorizontalScrollBarVisible", value)

    # is_vertical_scroll_bar_visible
    @property
    def is_vertical_scroll_bar_visible(self) -> bool:
        """
        **NEW**

        Determines whether the vertical scroll bar is visible.
        """
        return self._get_attr(
            "isVerticalScrollBarVisible", data_type="bool", def_value=False
        )

    @is_vertical_scroll_bar_visible.setter
    def is_vertical_scroll_bar_visible(self, value: Optional[bool]):
        self._set_attr("isVerticalScrollBarVisible", value)

    # sort_column_index
    @property
    def sort_column_index(self) -> Optional[int]:
        """
        See DataTable [sort_column_index](https://flet.dev/docs/controls/datatable#sort_column_index).
        """
        return self._get_attr("sortColumnIndex")

    @sort_column_index.setter
    def sort_column_index(self, value: Optional[int]):
        self._set_attr("sortColumnIndex", value)

    # clip_behavior
    @property
    def clip_behavior(self) -> Optional[ClipBehavior]:
        """
        See DataTable [clip_behavior](https://flet.dev/docs/controls/datatable#clip_behavior).
        """
        return self.__clip_behavior

    @clip_behavior.setter
    def clip_behavior(self, value: Optional[ClipBehavior]):
        self.__clip_behavior = value
        self._set_enum_attr("clipBehavior", value, ClipBehavior)

    # on_select_all
    @property
    def on_select_all(self) -> OptionalControlEventCallable:
        """
        See DataTable [on_select_all](https://flet.dev/docs/controls/datatable#on_select_all).
        """
        return self._get_event_handler("select_all")

    @on_select_all.setter
    def on_select_all(self, handler: OptionalControlEventCallable):
        self._add_event_handler("select_all", handler)
        self._set_attr("onSelectAll", True if handler is not None else None)


# class Item(Control):
#     def __init__(self, obj):
#         Control.__init__(self)
#         assert obj, "obj cannot be empty"
#         self.obj = obj

#     def _set_attr(self, name, value, dirty=True):
#         if value is None:
#             return

#         orig_val = self._get_attr(name)
#         if orig_val is not None:
#             if isinstance(orig_val, bool):
#                 value = str(value).lower() == "true"
#             elif isinstance(orig_val, float):
#                 value = float(str(value))

#         self._set_attr_internal(name, value, dirty=False)
#         if isinstance(self.obj, dict):
#             self.obj[name] = value
#         else:
#             setattr(self.obj, name, value)

#     def _fetch_attrs(self):
#         # reflection
#         obj = self.obj if isinstance(self.obj, dict) else vars(self.obj)

#         for name, val in obj.items():
#             data_type = (
#                 type(val).__name__ if isinstance(val, (bool, float)) else "string"
#             )
#             orig_val = self._get_attr(name, data_type=data_type)

#             if val != orig_val:
#                 self._set_attr_internal(name, val, dirty=True)

#     def _get_control_name(self):
#         return "item"
