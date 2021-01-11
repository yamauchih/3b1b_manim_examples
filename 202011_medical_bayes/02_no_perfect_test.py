# -*- coding: utf-8; -*-
#
# disease test and Bayes' theorem
#
# 02_no_perfect_test
#
#    (C) 2020 Hitoshi Yamauchi
#
# Using community manim: 28a733e9
#
# New BSD License
#
# Activate poetry (venv)
#  cd data/gitdata/manim/community/manim/manim
#  poetry shell
#
# Full resolution
#   python3 -m manim 02_no_perfect_test.py NoPerfectTest01 --resolution 720,1280 -p --high_quality
# Preview resolution
#   python3 -m manim 02_no_perfect_test.py NoPerfectTest01 --resolution 360,640 -p -ql
#

from manim import *
import copy, numpy
import myutil

class NoPerfectTest01(Scene):
# class NoPerfectTest01(LinearTransformationScene):
    """Test and Bayes 02: test cases
    """
    CONFIG={
        # BEGIN: Linear transformation scene config
        # "camera_config": {"background_color": RED},
        "include_background_plane": True,
        "include_foreground_plane": True,
        "background_plane_kwargs": {
            "color": GREY,
            "axis_config": {
                "stroke_color": LIGHT_GREY,
            },
            "axis_config": {
                "color": GREY,
            },
            "background_line_style": {
                "stroke_color": GREY,
                "stroke_width": 1,
            },
        },
        "show_coordinates": False,
        "show_basis_vectors": True,
        "basis_vector_stroke_width": 6,
        "i_hat_color": GREEN_C, # X_COLOR: this is defined in vector_space_scene.py, but not works
        "j_hat_color": RED_C,   # Y_COLOR: this is defined in vector_space_scene.py, but not works
        "leave_ghost_vectors": False,
        "t_matrix": [[3, 0], [1, 2]],
        # END: Linear transformation scene config

        #-- shared variables
        "time_wait":            4,
        "is_show_only":         False,

        #-- shared MObjects
        # time parameter t and its value tracker

        # title scaling factor
        "scale_title_f":    0.8,
        # equation scaling factor
        "scale_eq_f":       1.0,
        # text scaling factor
        "scale_txt_f":      0.8,

        # top text
        "txt_assumption":      None,
        "txt_no_perfect_test": None,
        "txt_handle_non_perfect": None,
        "txt_not_pre":         None,
        "mtex_not_1":          None,
        "txt_not_ja":          None,

        # color for \lnot
        "col_n":               RED,

        # not example
        "txt_ill":             None,
        "mtex_not_2":           None,
        "txt_not_ill":         None,

        # table
        "line_tab":              None,
        "color_tab_line":        WHITE,
        "stroke_width_tab_line": 4.0,
        "pos_tab_origin":        ORIGIN + -4.0 * RIGHT + +1.5 * UP,

        #
        # Position *: pos_tab_origin
        #
        # |<--------         \sum  width_trow               --------->|
        # *---------------=---+-------------------+-------------------+ ---
        # |<- width_trow[0] ->|<- width_trow[1] ->|<- width_trow[2] ->|  | height_tcol[0]
        # +-------------------+-------------------+-------------------+ ---
        # |                   |                   |                   |  | height_tcol[1]
        # +-------------------+-------------------+-------------------+ ---
        # | tab_cell(0,2)     |                   |                   |  | height_tcol[2]
        # +-------------------+-------------------+-------------------+ ---
        # | tab_cell(0,3)     | tab_cell(1,3)     |                   |  | height_tcol[3]
        # +-------------------+-------------------+-------------------+ ---
        #
        "width_trow":         [3.0, 2.5, 2.5,],
        "height_tcol":        [1.0, 1.0, 1.0, 1.0],


        "line_tab_hline": None,
        "line_tab_vline": None,
        "txt_tab_column_title": None,
        "txt_tab_test_title":   None,
        "txt_tab_ill_title":    None,
        "color_positive":  RED, # '#e53125',
        "color_negative":  BLUE,

        "txt_tab_true_pn":  None,
        "txt_tab_false_pn": None,

    }

    def create_title(self):
        """
        """
        self.txt_assumption = Text(r"前提:"           ).scale(self.scale_title_f)
        self.txt_no_perfect = Text(r"完璧な検査はない").scale(self.scale_title_f)
        myutil.critical_point_move_to(self.txt_assumption, LEFT + DOWN, ORIGIN + -6 * RIGHT +  2.8 * UP)
        self.txt_no_perfect.next_to(self.txt_assumption)

        self.txt_handle_non_perfect = Text(r"不確実を扱う道具の話").scale(self.scale_txt_f)
        myutil.critical_point_move_to(self.txt_handle_non_perfect, LEFT + DOWN, ORIGIN + -5.5 * RIGHT +  2.0 * UP)


        self.txt_not_pre = Text(r"記号"     ).   scale(self.scale_txt_f)
        self.mtex_not_1  = MathTex(r"\lnot").    scale(1.0).set_color(self.col_n)
        self.txt_not_ja  = Text(r": 〜ではない").scale(self.scale_txt_f)
        # It seems Text and MathTex don't share the positioning. Use other Text
        myutil.critical_point_move_to(self.txt_not_pre, LEFT + DOWN, ORIGIN + +0.2 * RIGHT +  3.0 * UP)
        self.mtex_not_1.next_to(self.txt_not_pre)
        self.txt_not_ja.next_to(self.mtex_not_1)

        self.mtex_not_2  = MathTex(r"\lnot").      scale(self.scale_eq_f).set_color(self.col_n)
        self.txt_ill     = Text(r"病気").          scale(self.scale_txt_f)
        self.txt_not_ill = Text(r": 病気ではない").scale(self.scale_txt_f)
        myutil.critical_point_move_to(self.mtex_not_2, LEFT + DOWN, ORIGIN + + 0.24 * RIGHT +  2.5 * UP)
        self.txt_ill.next_to(self.mtex_not_2)
        self.txt_not_ill.next_to(self.txt_ill)



    def animate_title(self):
        """
        """
        if (self.is_show_only):
            self.add(
                self.txt_assumption,      # 前提
                self.txt_no_perfect,      # 完璧な検査はない
                self.txt_handle_non_perfect,
                self.txt_not_pre,
                self.mtex_not_1,
                self.txt_not_ja,
                self.mtex_not_2,     # ¬
                self.txt_ill,        # 病気
                self.txt_not_ill,    # : 病気ではない
            )
            self.wait(self.time_wait)

            self.remove(self.txt_handle_non_perfect)
            self.wait(self.time_wait)

            return

        # 前提
        self.play(FadeIn(self.txt_assumption))
        self.wait(self.time_wait)

        # 完璧な検査はない
        self.play(FadeIn(self.txt_no_perfect))
        self.wait(self.time_wait)

        # 不確実さを扱う道具の話
        self.play(FadeIn(self.txt_handle_non_perfect))
        self.wait(self.time_wait)

        self.play(FadeOut(self.txt_handle_non_perfect))
        self.wait(self.time_wait)

        # 記法
        self.play(FadeIn(self.txt_not_pre), FadeIn(self.mtex_not_1))
        self.wait(self.time_wait)

        self.play(FadeIn(self.txt_not_ja))
        self.wait(self.time_wait)

        self.play(FadeInFrom(self.mtex_not_2, direction=DOWN),
                  FadeInFrom(self.txt_ill,    direction=DOWN))
        self.wait(self.time_wait)

        self.play(FadeInFrom(self.txt_not_ill, direction=DOWN))
        self.wait(self.time_wait)




    def get_tab_cell_anchor_pos(self, px, py, show=False):
        """
        Position * is the table cell anchor position
        *-------------+
        |tab_cell(x,y)|
        +-------------+
        """
        is_show = show
        cell_pos = myutil.get_tab_cell_critical_pos(self.pos_tab_origin,
                                                    self.width_trow, self.height_tcol,
                                                    px, py, LEFT + UP, show=is_show)

        return cell_pos



    def get_tab_width(self):
        """table total width
        """
        tab_width = 0.0
        for w in self.width_trow:
            tab_width += w
        return tab_width


    def get_tab_height(self):
        """table total height
        """
        tab_height = 0.0
        for h in self.height_tcol:
            tab_height += h
        return tab_height


    def create_table(self):
        # horizontal lines
        tab_width = self.get_tab_width()
        self.line_tab_hline = []
        for hidx in range(0, len(self.height_tcol)):
            anchor_pos = self.get_tab_cell_anchor_pos(0, hidx)
            self.line_tab_hline.append(
                Line(anchor_pos, anchor_pos + tab_width * RIGHT,
                     color=self.color_tab_line, stroke_width=self.stroke_width_tab_line))
        # append the last hline
        hsize = len(self.height_tcol)
        print("hsize: {0}".format(hsize))
        last_h_anchor_pos = self.get_tab_cell_anchor_pos(0, hsize - 1) + self.height_tcol[hsize - 1] * DOWN
        self.line_tab_hline.append(
            Line(last_h_anchor_pos, last_h_anchor_pos + tab_width * RIGHT,
                 color=self.color_tab_line, stroke_width=self.stroke_width_tab_line))


        # (0,2) vline is one level shorter
        tab_height = self.get_tab_height()
        self.line_tab_vline = []
        self.line_tab_vline.append(
            Line(self.get_tab_cell_anchor_pos(0, 0), self.get_tab_cell_anchor_pos(0, 0) + tab_height * DOWN,
                 color=self.color_tab_line, stroke_width=self.stroke_width_tab_line))
        self.line_tab_vline.append(
            Line(self.get_tab_cell_anchor_pos(1, 0), self.get_tab_cell_anchor_pos(1, 0) + tab_height * DOWN,
                 color=self.color_tab_line, stroke_width=self.stroke_width_tab_line))
        # [2] vline is one level (self.height_tcol[0]) shorter
        self.line_tab_vline.append(
            Line(self.get_tab_cell_anchor_pos(2, 1),
                 self.get_tab_cell_anchor_pos(2, 1) + (tab_height - self.height_tcol[0]) * DOWN,
                 color=self.color_tab_line, stroke_width=self.stroke_width_tab_line))

        # append the last vline
        vsize = len(self.width_trow)
        last_v_anchor_pos = self.get_tab_cell_anchor_pos(vsize - 1, 0) + self.width_trow[vsize - 1] * RIGHT
        self.line_tab_vline.append(
            Line(last_v_anchor_pos, last_v_anchor_pos + tab_height * DOWN,
                 color=self.color_tab_line, stroke_width=self.stroke_width_tab_line))

        debug_show_all_cell_position = False
        if (debug_show_all_cell_position):
            # Show cell positions
            anchor_txt = []
            for x in range(0, len(self.width_trow)):
                for y in range(0, len(self.height_tcol)):
                    anchor_txt.append(Text("({0},{1})".format(x, y)).move_to(
                        myutil.get_tab_cell_critical_pos(self.pos_tab_origin,
                                                         self.width_trow, self.height_tcol,
                                                         x, y, ORIGIN, show=True)))
                    self.add(*anchor_txt)


        # text column title
        scale_col_title_txt = 1.0
        self.txt_tab_column_title = [
            Text(r"検査結果").scale(scale_col_title_txt),
            Text(r"実際"    ).scale(scale_col_title_txt)
        ]

        myutil.critical_point_move_to(self.txt_tab_column_title[0], ORIGIN,
                                      myutil.get_tab_cell_critical_pos(self.pos_tab_origin,
                                                                       self.width_trow, self.height_tcol,
                                                                       0, 0, ORIGIN, show=False))
        table_row_2_adjust = (self.width_trow[2] / 2)
        myutil.critical_point_move_to(self.txt_tab_column_title[1], ORIGIN,
                                      myutil.get_tab_cell_critical_pos(self.pos_tab_origin,
                                                                       self.width_trow, self.height_tcol,
                                                                       1, 0, ORIGIN, show=False)
                                      + table_row_2_adjust * RIGHT)



        # test row title (+,-)
        scale_row_title_txt = 1.2
        self.txt_tab_test_title = [
            Text(r"＋", font="sans-serif", color=self.color_positive).scale(scale_row_title_txt),
            Text(r"−", font="sans-serif", color=self.color_negative).scale(scale_row_title_txt)
        ]

        # '+' is localted at (0,2)
        myutil.critical_point_move_to(self.txt_tab_test_title[0], ORIGIN,
                                      myutil.get_tab_cell_critical_pos(self.pos_tab_origin,
                                                                       self.width_trow, self.height_tcol,
                                                                       0, 2, ORIGIN, show=False))
        # '-' is localted at (0,3)
        myutil.critical_point_move_to(self.txt_tab_test_title[1], ORIGIN,
                                      myutil.get_tab_cell_critical_pos(self.pos_tab_origin,
                                                                       self.width_trow, self.height_tcol,
                                                                       0, 3, ORIGIN, show=False))


        # ill, not ill title
        scale_row_title_txt = 1.0
        not_ill = VGroup()
        tex_not = MathTex(r"\lnot").scale(scale_row_title_txt).set_color(self.col_n)
        txt_ill = Text(r"病気"       ).       scale(scale_row_title_txt).next_to(tex_not)
        not_ill.add(tex_not, txt_ill)

        self.txt_tab_ill_title    = [
            Text(r"病気").  scale(scale_col_title_txt),
            not_ill,
        ]
        myutil.critical_point_move_to(self.txt_tab_ill_title[0], ORIGIN,
                                      myutil.get_tab_cell_critical_pos(self.pos_tab_origin,
                                                                       self.width_trow, self.height_tcol,
                                                                       1, 1, ORIGIN, show=False))
        myutil.critical_point_move_to(self.txt_tab_ill_title[1], ORIGIN,
                                      myutil.get_tab_cell_critical_pos(self.pos_tab_origin,
                                                                       self.width_trow, self.height_tcol,
                                                                       2, 1, ORIGIN, show=False))


        # table contents
        self.txt_tab_true_pn  = [
            Text(r"真＋", font="sans-serif",
                 t2c = {"＋": self.color_positive}), # t2w = {"＋": BOLD} doesn't work
            Text(r"真−", font="sans-serif",
                 t2c = {"−": self.color_negative}), # t2w = {"−": ULTRABOLD} doesn't work
        ]
        myutil.critical_point_move_to(self.txt_tab_true_pn[0], ORIGIN,
                                      myutil.get_tab_cell_critical_pos(self.pos_tab_origin,
                                                                       self.width_trow, self.height_tcol,
                                                                       1, 2, ORIGIN, show=False))
        myutil.critical_point_move_to(self.txt_tab_true_pn[1], ORIGIN,
                                      myutil.get_tab_cell_critical_pos(self.pos_tab_origin,
                                                                       self.width_trow, self.height_tcol,
                                                                       2, 3, ORIGIN, show=False))

        self.txt_tab_false_pn = [
            Text(r"偽＋", font="sans-serif", t2c = {"＋": self.color_positive}),
            Text(r"偽−", font="sans-serif", t2c = {"−": self.color_negative}),
        ]
        myutil.critical_point_move_to(self.txt_tab_false_pn[0], ORIGIN,
                                      myutil.get_tab_cell_critical_pos(self.pos_tab_origin,
                                                                       self.width_trow, self.height_tcol,
                                                                       2, 2, ORIGIN, show=False))
        myutil.critical_point_move_to(self.txt_tab_false_pn[1], ORIGIN,
                                      myutil.get_tab_cell_critical_pos(self.pos_tab_origin,
                                                                       self.width_trow, self.height_tcol,
                                                                       1, 3, ORIGIN, show=False))




    def animate_table(self):
        if (self.is_show_only):
            self.add(*self.line_tab_hline)
            self.add(*self.line_tab_vline)
            self.add(*self.txt_tab_column_title)
            self.add(*self.txt_tab_test_title)
            self.add(*self.txt_tab_ill_title)
            self.add(*self.txt_tab_true_pn)
            self.add(*self.txt_tab_false_pn)
            return

        self.play(*[ShowCreation(mobj) for mobj in self.line_tab_hline],
                  *[ShowCreation(mobj) for mobj in self.line_tab_vline])
        self.wait(self.time_wait)

        self.play(FadeIn(self.txt_tab_column_title[0])) # Test: 検査結果
        self.wait(self.time_wait)

        self.play(FadeIn(self.txt_tab_column_title[1])) # Reality: 実際
        self.wait(self.time_wait)

        self.play(FadeIn(self.txt_tab_test_title[0])) # result positive: +
        self.wait(self.time_wait)

        self.play(FadeIn(self.txt_tab_test_title[1])) # result negative: -
        self.wait(self.time_wait)

        self.play(FadeIn(self.txt_tab_ill_title[0])) # ill: 病気
        self.wait(self.time_wait)

        self.play(FadeIn(self.txt_tab_ill_title[1])) # not ill; ¬病気
        self.wait(self.time_wait)

        each_duration = 6
        self.play(FadeIn(self.txt_tab_true_pn[0])) # true positive: 真+
        self.wait(each_duration)

        self.play(FadeIn(self.txt_tab_true_pn[1])) # true negative: 真-
        self.wait(each_duration)

        self.play(FadeIn(self.txt_tab_false_pn[0])) # false positive: 偽+
        self.wait(each_duration)

        self.play(FadeIn(self.txt_tab_false_pn[1])) # false negative: 偽-
        self.wait(each_duration)

        # emphasize true cases
        emp_factor = 1.4
        self.play(ApplyMethod(self.txt_tab_true_pn[0].scale, emp_factor),
                  ApplyMethod(self.txt_tab_true_pn[1].scale, emp_factor))
        self.play(ApplyMethod(self.txt_tab_true_pn[0].scale, 1.0/emp_factor),
                  ApplyMethod(self.txt_tab_true_pn[1].scale, 1.0/emp_factor))
        self.wait(self.time_wait)

        # emphasize false cases
        emp_factor = 1.4
        self.play(ApplyMethod(self.txt_tab_false_pn[0].scale, emp_factor),
                  ApplyMethod(self.txt_tab_false_pn[1].scale, emp_factor))
        self.play(ApplyMethod(self.txt_tab_false_pn[0].scale, 1.0/emp_factor),
                  ApplyMethod(self.txt_tab_false_pn[1].scale, 1.0/emp_factor))
        self.wait(self.time_wait)



    def construct(self):
        """Test and Bayes intro
        """
        self.create_title()
        self.animate_title()
        self.wait(self.time_wait)

        self.create_table()
        self.animate_table()
        self.wait(self.time_wait)


        self.wait(5)
