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
#   python3 -m manim 03_no_perfect_and_bayse.py NoPerfectBayes01 --resolution 720,1280 -p --high_quality
# Preview resolution
#   python3 -m manim 03_no_perfect_and_bayse.py NoPerfectBayes01 --resolution 360,640 -p -ql
#

from manim import *
import copy, numpy
import myutil

class NoPerfectBayes01(Scene):
# class NoPerfectBayes01(LinearTransformationScene):
    """Test and Bayes 03: What do we want to know when the test is not perfect?

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
        "time_wait":            5,
        "is_show_only":         False,

        # title scaling factor
        "scale_title_f":    0.9,
        # equation scaling factor
        "scale_eq_f":       1.0,
        # text scaling factor
        "scale_txt_f":      0.8,


        #-- shared MObjects
        # time parameter t and its value tracker

        # top text
        "txt_want_to_know":  None,
        "txt_test_positive": None,
        "txt_test_negative": None,
        "txt_bayes_1":       None,
        "txt_bayes_2":       None,
        "txt_bayes_3":       None,

        # color for \lnot
        "col_n":               RED,

        "col_positive":    RED, # '#e53125',
        "col_negative":    BLUE,

        "line_cond":         None,
        "line_possibility":  None,
        "line_color_when":   YELLOW,
        "line_color_cond":   GREEN,
        "line_stroke_when":  6,
        "line_down_offset":  0.1, # underline offset to DOWN

        # evidence changes probablity of hypothesis
        "txt_e_changes_h":   None,

    }

    def create_text(self):
        """
        """
        self.txt_want_to_know  = Text(r"検査が不完全な時に知りたいこと").scale(self.scale_title_f)
        myutil.critical_point_move_to(self.txt_want_to_know, LEFT + DOWN, ORIGIN + -6.0 * RIGHT + 2.5 * UP)

        self.txt_test_positive = [
            Text(r"1.検査結果").                 scale(self.scale_txt_f),
            Text(r"＋", color=self.col_positive).scale(self.scale_txt_f),
            Text(r"の時").                       scale(self.scale_txt_f),
            Text(r"，実際に病気").               scale(self.scale_txt_f),
            Text(r"の可能性").                   scale(self.scale_txt_f),]

        self.txt_test_negative = [
            Text(r"2.検査結果").                 scale(self.scale_txt_f),
            Text(r"−", color=self.col_negative).scale(self.scale_txt_f),
            Text(r"の時").                       scale(self.scale_txt_f),
            Text(r"，実際に¬病気", t2c={"[4:5]":self.col_n}).scale(self.scale_txt_f),
            Text(r"の可能性").                   scale(self.scale_txt_f),]

        myutil.critical_point_move_to(self.txt_test_positive[0], LEFT + DOWN, ORIGIN + -5.0 * RIGHT + 1.5 * UP)
        myutil.critical_point_move_to(self.txt_test_negative[0], LEFT + DOWN, ORIGIN + -5.0 * RIGHT + 0.5 * UP)
        for i in range(1, len(self.txt_test_positive)):
            self.txt_test_positive[i].next_to(self.txt_test_positive[i-1], buff=0.1)
            self.txt_test_negative[i].next_to(self.txt_test_negative[i-1], buff=0.1)

        # Underlines
        pos_when_beg = [
            self.txt_test_positive[2].get_critical_point(LEFT  + DOWN) + self.line_down_offset * DOWN, # の時 0
            self.txt_test_negative[2].get_critical_point(LEFT  + DOWN) + self.line_down_offset * DOWN, # の時 1
            self.txt_test_positive[4].get_critical_point(LEFT  + DOWN) + self.line_down_offset * DOWN, # の可能性 0
            self.txt_test_negative[4].get_critical_point(LEFT  + DOWN) + self.line_down_offset * DOWN, # の可能性 1
        ]
        pos_when_end = [
            self.txt_test_positive[2].get_critical_point(RIGHT + DOWN) + self.line_down_offset * DOWN, # の時 0
            self.txt_test_negative[2].get_critical_point(RIGHT + DOWN) + self.line_down_offset * DOWN, # の時 1
            self.txt_test_positive[4].get_critical_point(RIGHT + DOWN) + self.line_down_offset * DOWN, # の可能性 0
            self.txt_test_negative[4].get_critical_point(RIGHT + DOWN) + self.line_down_offset * DOWN, # の可能性 1
        ]
        self.line_cond = [
            Line(pos_when_beg[0], pos_when_end[0], color=self.line_color_when, stroke_width=self.line_stroke_when),
            Line(pos_when_beg[1], pos_when_end[1], color=self.line_color_when, stroke_width=self.line_stroke_when)
        ]
        self.line_possibility = [
            Line(pos_when_beg[2], pos_when_end[2], color=self.line_color_cond, stroke_width=self.line_stroke_when),
            Line(pos_when_beg[3], pos_when_end[3], color=self.line_color_cond, stroke_width=self.line_stroke_when)
        ]

        # ベイズの定理 (Bayes theorem)
        self.txt_bayes_1       = Text(r"ベイズの定理 (Bayes theorem)").scale(self.scale_txt_f)
        myutil.critical_point_move_to(self.txt_bayes_1,    LEFT + DOWN, ORIGIN + -6.0 * RIGHT + -1.0 * UP)

        # E の時，H の可能性
        self.txt_bayes_2       = [
            Text(r"E ").      scale(self.scale_txt_f),
            Text(r"の時").    scale(self.scale_txt_f),
            Text(r"，H ").    scale(self.scale_txt_f),
            Text(r"の可能性").scale(self.scale_txt_f),
            Text(r"→").      scale(self.scale_txt_f),
            Text(r"E ", color=YELLOW).scale(self.scale_txt_f),
        ]

        myutil.critical_point_move_to(self.txt_bayes_2[0], LEFT + DOWN, ORIGIN + -5.0 * RIGHT + -2.0 * UP)
        for i in range(1, len(self.txt_bayes_2)):
            self.txt_bayes_2[i].next_to(self.txt_bayes_2[i-1], buff=0.1)

        # repeat E の時，H の可能性
        self.txt_bayes_3       = [
            Text(r"E ").      scale(self.scale_txt_f),
            Text(r"の時").    scale(self.scale_txt_f),
            Text(r"，H ").    scale(self.scale_txt_f),
            Text(r"の可能性").scale(self.scale_txt_f),
        ]
        myutil.critical_point_move_to(self.txt_bayes_3[0], LEFT + DOWN, ORIGIN + -5.0 * RIGHT + -3.0 * UP)
        for i in range(1, len(self.txt_bayes_3)):
            self.txt_bayes_3[i].next_to(self.txt_bayes_3[i-1], buff=0.1)

        self.txt_e_changes_h = Text(r"証拠により可能性が変化")


    def animate_text(self):
        """
        """
        if (self.is_show_only):
            self.add(self.txt_want_to_know,
                     *self.txt_test_positive,
                     *self.txt_test_negative,
                     self.txt_bayes_1,
                     *self.txt_bayes_2,
                     *self.line_cond,
                     *self.line_possibility,)
            return

        self.play(FadeIn(self.txt_want_to_know))
        self.wait(self.time_wait)

        self.play(*[FadeIn(mobj) for mobj in self.txt_test_positive])
        self.wait(self.time_wait)

        self.play(*[FadeIn(mobj) for mobj in self.txt_test_negative])
        self.wait(self.time_wait)

        self.play(*[ShowCreation(mobj) for mobj in self.line_cond])
        self.wait(self.time_wait)

        self.play(*[ShowCreation(mobj) for mobj in self.line_possibility])
        self.wait(self.time_wait)

        # move の時 & の可能性
        # duplicate moving texts twice from the destination (の時)
        txt_when = [
            copy.deepcopy(self.txt_bayes_2[1]),
            copy.deepcopy(self.txt_bayes_2[1])# same twice since two sources
        ]
        # set source position
        txt_when[0].move_to(self.txt_test_positive[2].get_center())
        txt_when[1].move_to(self.txt_test_negative[2].get_center())

        # duplicate underlines (の時) for animation, already at the source position.
        line_when = copy.deepcopy(self.line_cond)

        # duplicate moving texts twice from the destination (の可能性)
        txt_possibility = [
            copy.deepcopy(self.txt_bayes_2[3]),
            copy.deepcopy(self.txt_bayes_2[3])# same twice since two sources
        ]
        # set source position
        txt_possibility[0].move_to(self.txt_test_positive[4].get_center())
        txt_possibility[1].move_to(self.txt_test_negative[4].get_center())

        # duplicate underlines (の可能性) for animation, already at the source position
        line_possibility = copy.deepcopy(self.line_possibility)

        # Add underlines for animation
        self.add(*txt_when,
                 *line_when,
                 *txt_possibility,
                 *line_possibility)

        dest_line_when        = self.txt_bayes_2[1].get_critical_point(DOWN) + self.line_down_offset * DOWN
        dest_line_possibility = self.txt_bayes_2[3].get_critical_point(DOWN) + self.line_down_offset * DOWN

        # self.add(self.txt_bayes_2[1], self.txt_bayes_2[3])
        self.play(ApplyMethod(txt_when[0].move_to,   self.txt_bayes_2[1].get_center()),
                  ApplyMethod(line_when[0].move_to,  dest_line_when),
                  ApplyMethod(txt_when[1].move_to,   self.txt_bayes_2[1].get_center()),
                  ApplyMethod(line_when[1].move_to,  dest_line_when))
        self.wait(self.time_wait)

        self.play(ApplyMethod(txt_possibility[0].move_to,   self.txt_bayes_2[3].get_center()),
                  ApplyMethod(line_possibility[0].move_to,  dest_line_possibility),
                  ApplyMethod(txt_possibility[1].move_to,   self.txt_bayes_2[3].get_center()),
                  ApplyMethod(line_possibility[1].move_to,  dest_line_possibility))

        self.wait(self.time_wait)

        # remove copies, add txt_bayes
        self.remove(*txt_when,
                    *txt_possibility)
        self.add(self.txt_bayes_2[1],
                 self.txt_bayes_2[3])

        # complete the sentense
        self.play(FadeIn(self.txt_bayes_2[0]),
                  FadeIn(self.txt_bayes_2[2]))
        self.wait(self.time_wait)

        # Show Bayes theorem title
        self.play(FadeIn(self.txt_bayes_1))
        self.wait(self.time_wait)

        # remove underlines, show -> A, show copy
        self.remove(line_when[1], line_possibility[1]) # remove the duplication first
        self.play(FadeOut(line_when[0]),               # now fade out
                  FadeOut(line_possibility[0]),        # now fade out
                  FadeIn(self.txt_bayes_2[4]),
                  FadeIn(self.txt_bayes_2[5]),
                  *[FadeIn(mobj) for mobj in self.txt_bayes_3])
        self.wait(self.time_wait)

        # transform the line to A
        bayse_2_copy   = copy.deepcopy(self.txt_bayes_2)
        bayse_3_a_copy = copy.deepcopy(self.txt_bayes_3[0])
        bayse_3_a_copy.set_color(YELLOW)
        self.add(bayse_2_copy[0])
        self.play(Transform(bayse_2_copy[0], bayse_3_a_copy),
                  Transform(bayse_2_copy[1], bayse_3_a_copy),
                  Transform(bayse_2_copy[2], bayse_3_a_copy),
                  Transform(bayse_2_copy[3], bayse_3_a_copy))
        self.wait(self.time_wait)







    def construct(self):
        """Test and Bayes intro
        """

        self.create_text()
        self.animate_text()
        self.wait(self.time_wait)

        self.wait(5)
