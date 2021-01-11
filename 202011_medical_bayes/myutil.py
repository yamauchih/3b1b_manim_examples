# -*- coding: utf-8; -*-
#
# disease test and Bayes' theorem
#
# my utility
#
#    (C) 2020 Hitoshi Yamauchi
#
#

from manim import *
import copy


class CrossMobj(Line):
    """Use Line to cross an mobject.
    Use case: simplifing a fraction
    """

    def __init__(self, mobj=None, color=ORANGE, *args, **kwargs):
        Line.__init__(self, *args, **kwargs)
        self.__ref_mobj = mobj
        self.set_color(color)
        self.set_mobj(self.__ref_mobj)


    def set_mobj(self, mobj):
        """Cross mobj left-bottom to right-up
        """
        if (self.__ref_mobj == None):
            return
        pos_ld = mobj.get_critical_point(LEFT  + DOWN)
        pos_ru = mobj.get_critical_point(RIGHT + UP)
        self.put_start_and_end_on(pos_ld, pos_ru)



class LabeledRectangle(RoundedRectangle):
    """A :class:`LabeledRectangle` containing a label in its center.

    Parameters
    ----------
    label : Union[:class:`str`, :class:`~.SingleStringMathTex`, :class:`~.Text`, :class:`~.Tex`]
        The label of the :class:`Rectangle`. This is rendered as :class:`~.MathTex`
        by default (i.e., when passing a :class:`str`), but other classes
        representing rendered strings like :class:`~.Text` or :class:`~.Tex`
        can be passed as well.

    width : :class:`float`
        The width of the :class:`Rectangle`. If ``None`` (the default), the width
        is calculated based on the size of the ``label``.


    Rectangle, Text, and tip triangle

    * tip_direction == DOWN

    +----------+
    | Text     |
    +----------+   ---
         \/          tip_height
        |  |       ---
          tip_width


    Examples
    --------

    .. manim:: SeveralLabeledRectangle
        :save_last_frame:

        class SeveralLabeledRectangle(Scene):
            def construct(self):
                label_rect_1 = LabeledRectangle(Text(r"真＋", t2c={"[0:1]": BLACK, "[1:2]": RED}).scale(0.9),
                                                tip_direction=DOWN, color=WHITE, fill_opacity=1.0).move_to(2.0 * UP)
                label_rect_2 = LabeledRectangle(Text(r"False ＋", t2c={"[0:5]": BLACK, "[5:6]": RED}).scale(0.9),
                                               tip_direction=RIGHT, color=WHITE, fill_opacity=1.0).move_to(2.0 * RIGHT)
                label_rect_3 = LabeledRectangle(Text(r"False ＋", t2c={"[0:5]": BLACK, "[5:6]": RED}).scale(0.9),
                                                tip_direction=LEFT, color=WHITE, fill_opacity=1.0).move_to(2.0 * LEFT)
                label_rect_4 = LabeledRectangle(Text(r"True −", t2c={"[0:4]": BLACK, "[4:5]": BLUE}).scale(0.9),
                                                tip_direction=UP, color=WHITE, fill_opacity=1.0).move_to(2.0 * DOWN)
                self.add(label_rect_1, label_rect_2, label_rect_3, label_rect_4)

    """

    def __init__(self, label, width=None, height=None,
                 width_buff=0.1, height_buff=0.1, color=WHITE, fill_color=WHITE, fill_opacity=1.0, corner_radius=0.1,
                 tip_direction=None, tip_height=0.3, tip_width=0.3, **kwargs) -> None:
        if isinstance(label, str):
            from manim import MathTex

            rendered_label = MathTex(label, color=BLACK)
        else:
            rendered_label = label

        if width is None:
            width  = (2 * width_buff  + rendered_label.get_width())
        if height is None:
            height = (2 * height_buff + rendered_label.get_height())


        RoundedRectangle.__init__(self, width=width, height=height, color=color, fill_color=fill_color, fill_opacity=fill_opacity, corner_radius=corner_radius, **kwargs)
        rendered_label.move_to(self.get_center())
        self.add(rendered_label)

        if (tip_direction is not None):
            self.set_tip(tip_direction=tip_direction, tip_height=tip_height, tip_width=tip_width, color=color, fill_opacity=fill_opacity, **kwargs)


    def set_tip(self, tip_direction, tip_height=0.3, tip_width=0.3, color=WHITE, fill_opacity=1.0, **kwargs):
        """
        """
        # add a triangle
        v1 = (tip_width / 2) * LEFT
        v2 = (tip_width / 2) * RIGHT
        v3 =  tip_height * UP

        tri = Polygon(v1, v2, v3, color=color, fill_opacity=fill_opacity, **kwargs)

        if ((tip_direction == DOWN).all()):
            tri.rotate(PI)
            tri.shift(self.get_critical_point(DOWN) - tri.get_critical_point(UP))
        elif ((tip_direction == UP).all()):
            tri.shift(self.get_critical_point(UP) - tri.get_critical_point(DOWN))
        elif ((tip_direction == RIGHT).all()):
            tri.rotate(PI/2)
            tri.shift(self.get_critical_point(LEFT) - tri.get_critical_point(RIGHT))
        elif ((tip_direction == LEFT).all()):
            tri.rotate(-PI/2)
            tri.shift(self.get_critical_point(RIGHT) - tri.get_critical_point(LEFT))
        else:
            raise ValueError(
                """LabeledRectangle.set_tip's tip_direction must be one of
                {RIGHT, LEFT, UP, DOWN} only"""
            )

        self.add(tri)



def critical_point_move_to(mobj, critical_point_dir, target_pos):
    """
    Move the critical_point(critical_point_dir) to the target

    +-----------+
    |text C     |
    X-----------+

    Move position X to the target position instead of C (get_center()) position

    @param mobj               mobject
    @param critical_point_dir critical point direction of mobj (e.g., LEFT + DOWN)
    @param target_pos         mobj's critical point target position
    @return mobj
    """
    to_center_from_cp = mobj.get_critical_point(critical_point_dir) - mobj.get_center()
    mobj.move_to(target_pos - to_center_from_cp)
    return mobj



def get_tab_cell_critical_pos(tab_ancher_pos, width_ary, height_ary, cell_idx_x, cell_idx_y, critical_point_dir, show=False):
    """Table position utility function.

    Get a table cell position.
    A table is defined by tab_ancher_pos,  width_ary, height_ary.

    width_ary[k] : variable widths,  e.g., w = [1.0, 1.5, ..,.1.2]
    height_ary[j]: variable heights  e.g., h = [1.0, 2.0, ...,1.1]


    |<- w[0] ->|<- w[1]    ->| ...  |<- w[k-1] ->|
    *----------+-------------+-    -+------------+ --
    | (0,0)    |  (1,0)      |      |  (k-1,0)   |    h[0]
    +----------+-------------+-    -+------------+ --
    |          |             |      |            |
    | (0,1)    |  (1,1)      |      |  (k-1, 1)  |    h[1]
    +----------+-------------+-    -+------------+ --
         ...                                          ...
    +----------+-------------+-    -+------------+ --
    | (0,j-1)  |  (1,j-1)    |      | (k-1,j-1)  |    h[j-1]
    +----------+-------------+-    -+------------+ --

    * is the tab_ancher_pos (table anchor position)


    Position '&' below is the table cell critical position. The
    critical position is the same as manim.

    critical_point_dir = LEFT + UP. (top left)
    &-------------+
    |tab_cell(x,y)|
    +-------------+

    critical_point_dir = ORIGIN (center)
    +-------------+
    |      &      |
    +-------------+

    @param[in] tab_ancher_pos      table anchor position
    @param[in] width_ary           table width length array
    @param[in] height_ary          table height length array
    @param[in] cell_idx_x          table cell index x
    @param[in] cell_idx_y          table cell index y
    @param[in] critical_point_dir  manim style critical point direction
    @param[in] show                (option) print out coordinates when True
    @return    critical point manim coordinate (numpy array)
    """
    # print("x, y: ({0}, {1}), len ({2}, {3})".format(cell_idx_x, cell_idx_y, len(width_ary), len(height_ary)))
    assert(cell_idx_x < len(width_ary))
    assert(cell_idx_y < len(height_ary))
    dx = 0
    cur_cell_w = 0
    for i in range(0, cell_idx_x):
        dx += width_ary[i]
        # print("   dx: {0}".format(dx))
    cur_cell_w = width_ary[cell_idx_x]
    # print("   cur_cell w: {0}".format(width_ary[cell_idx_x]))

    dy = 0
    cur_cell_h = 0
    for j in range(0, cell_idx_y):
        dy += height_ary[j]
    cur_cell_h = height_ary[cell_idx_y]


    # Shift right & down / 2 (relative to the cell anchor point)
    shifted_critical_point_dir = copy.deepcopy(critical_point_dir)
    shifted_critical_point_dir += (RIGHT + DOWN)
    shifted_critical_point_dir *= 0.5
    # print("shifted_critical_point_dir 2: {0}".format(shifted_critical_point_dir))

    cell_anchor_pos = copy.deepcopy(tab_ancher_pos)
    cell_anchor_pos[0] += ( dx + shifted_critical_point_dir[0] * cur_cell_w) # RIGHT direction
    cell_anchor_pos[1] += (-dy + shifted_critical_point_dir[1] * cur_cell_h) # DOWN  direction

    if (show):
        print("x, y: ({0}, {1}), pos{2}".format(cell_idx_x, cell_idx_y, cell_anchor_pos))
    return cell_anchor_pos



def move_src_list_dst(scene, src_mobj_list, dst_mobj):
    """Only move the src and dst, without sideeffect

    Note: if mobject has no __deepcopy__ implemented, no side effect fails.

    src_mobj_list is a list of mobj (multiple source, single destination)


    """
    # element wise deep copy
    move_work_list = []
    for mobj in src_mobj_list:
        move_work_list.append(copy.deepcopy(mobj))
    scene.add(*move_work_list)

    # for i in src_mobj_list:
    #     print(f"src_mobj_list: {i}")
    # for i in move_work_list:
    #     print(f"move_work_list: {i}")


    dst_pos = dst_mobj.get_center()
    apply_list = []
    for mobj in src_mobj_list:
        apply_list.append(ApplyMethod(mobj.move_to, dst_pos))

    scene.play(*apply_list)
    scene.remove(*move_work_list)


def transform_src_dst(scene, src_mobj, dst_mobj):
    """Only move the src and dst, without sideeffect

    Note: if mobject has no __deepcopy__ implemented, no side effect fails.
    """
    src_work = copy.deepcopy(src_mobj)
    dst_work = copy.deepcopy(dst_mobj)
    scene.add(src_work)
    scene.play(Transform(src_work, dst_work))
    scene.remove(src_work, dst_work)
