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
# Activate poetry (venv)
#  cd data/gitdata/manim/community/manim/manim
#  poetry shell
#
# Full resolution
#   python3 -m manim 04_read_bayse.py ReadBayesTheorem01 --resolution 720,1280 -p --high_quality
# Preview resolution
#   python3 -m manim 04_read_bayse.py ReadBayesTheorem01 --resolution 360,640 -p -ql
#

from manim import *
import copy, numpy
import myutil

class ReadBayesTheorem01(Scene):
# class ReadBayesTheorem01(LinearTransformationScene):
    """Read Bayes theorem: how to read the Bayes' theorem

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
        "txt_title_bayes": None,
        "txt_how_to_read": None,
        "col_positive":    RED,
        "col_negative":    BLUE,

        # title scaling factor
        "scale_title_f":    0.9,
        # equation scaling factor
        "scale_eq_f":       1.0,
        # text scaling factor
        "scale_txt_f":      0.8,

        # P(H|E) = {{P(E|H) P(H)} \over P(E)} ... use over instead of frac for coloring (frac cannot be divided)
        "mtex_bayes_simple": None,
        "col_h":             YELLOW,
        "col_e":             BLUE_B,
        "h_indices":         None,
        "e_indices":         None,

        # events notation
        # {E,H,A,B}, 事象 (Event), 病気, 検査+
        "tex_events_eq":   None,
        "txt_events_exp":  None,

        # conditional notation
        "tex_cond_eq":     None, # H|E
        "tex_cond_eq_2":   None, # H|E : animation destination
        "txt_cond_exp_1":  None,
        "txt_cond_exp_2":  None,

        # probability notation
        "tex_prob_eq":     None,
        "txt_prob_exp":    None,

    }

    def create_bayes_eq(self):
        """
        """
        self.txt_title_bayes = Text(r"ベイズの定理").scale(self.scale_title_f)
        myutil.critical_point_move_to(self.txt_title_bayes, LEFT + DOWN, ORIGIN + -6.3 * RIGHT + 3.0 * UP)
        self.txt_how_to_read = Text(r"式の「読み方」").scale(self.scale_txt_f)
        myutil.critical_point_move_to(self.txt_how_to_read, LEFT + DOWN, ORIGIN + -1.0 * RIGHT + 3.0 * UP)

        # simple Bayes form                          # indices for h,e color
        self.mtex_bayes_simple = MathTex(r"P(H|E)",   # e [0,4]  h [0,2]
                                         r"={",       #
                                         r"{P(H)",    #          h [2,2]
                                         r"P(E|H)}",  # e [3,2], h [3,4]
                                         r"\over",    #
                                         r"{P(E)}",   # e [5,2]
                                         r"}",        #
        ).scale(self.scale_eq_f)
        myutil.critical_point_move_to(self.mtex_bayes_simple, LEFT + DOWN, ORIGIN + -5.0 * RIGHT + 1.1 * UP)

        self.h_indices = [[0, 2], [2, 2], [3, 4]]
        for [i,j] in self.h_indices:
            self.mtex_bayes_simple[i][j].set_color(self.col_h)
        self.e_indices = [[0, 4], [3, 2], [5, 2]]
        for [i,j] in self.e_indices:
            self.mtex_bayes_simple[i][j].set_color(self.col_e)

        # events notation
        self.tex_events_eq    = MathTex(r"E", r",", r"H", r", A, B:").scale(self.scale_eq_f)
        self.tex_events_eq[0].set_color(self.col_e)
        self.tex_events_eq[2].set_color(self.col_h)
        self.txt_events_exp = [
            Text(r"事象 (Event): ").scale(self.scale_txt_f),
            Text(r"病気, ").        scale(self.scale_txt_f),
            Text(r"検査＋", t2c={r"＋": self.col_positive},).scale(self.scale_txt_f),
        ]
        myutil.critical_point_move_to(self.tex_events_eq,     LEFT + DOWN, ORIGIN + -6.0 * RIGHT + 0.0 * UP)
        myutil.critical_point_move_to(self.txt_events_exp[0], LEFT + DOWN, ORIGIN + -2.6 * RIGHT + 0.0 * UP)
        for i in range(1, len(self.txt_events_exp)):
            self.txt_events_exp[i].next_to(self.txt_events_exp[i-1], buff=0.2)

        # conditional notation
        self.tex_cond_eq  = MathTex(r"H", r"|", r"E").scale(self.scale_eq_f)
        self.tex_cond_eq[0].set_color(self.col_h)
        self.tex_cond_eq[2].set_color(self.col_e)
        myutil.critical_point_move_to(self.tex_cond_eq, LEFT + DOWN, ORIGIN + -6.0 * RIGHT + -1.0 * UP)

        self.txt_cond_exp_1 = [
            Text(r": Evidence (証拠)").scale(self.scale_txt_f).set_color(self.col_e),
            Text(r"の時,").            scale(self.scale_txt_f),
            Text(r"Hypothesis (仮説)").scale(self.scale_txt_f).set_color(self.col_h),
        ]
        myutil.critical_point_move_to(self.txt_cond_exp_1[0], LEFT + DOWN, ORIGIN + -4.6 * RIGHT + -1.0 * UP)
        for i in range(1, len(self.txt_cond_exp_1)):
            self.txt_cond_exp_1[i].next_to(self.txt_cond_exp_1[i-1], buff=0.2)
        # baseline adjustment of Evidence
        self.txt_cond_exp_1[0].shift(0.05 * UP)

        # Hypothesis given the Evidence
        self.txt_cond_exp_2 = [
            Text(r"Hypothesis").  scale(self.scale_txt_f).set_color(self.col_h),
            Text(r"given").       scale(self.scale_txt_f),
            Text(r"the Evidence").scale(self.scale_txt_f).set_color(self.col_e),
        ]
        myutil.critical_point_move_to(self.txt_cond_exp_2[0], LEFT + DOWN, ORIGIN + -4.2 * RIGHT + -2.0 * UP)
        for i in range(1, len(self.txt_cond_exp_2)):
            self.txt_cond_exp_2[i].next_to(self.txt_cond_exp_2[i-1], buff=0.2)
        # baseline adjustment of the Evidence
        self.txt_cond_exp_2[2].shift(0.05 * UP)

        # animation destination, destination of "Hypothesis of the Evidence"
        self.tex_cond_eq_2 = MathTex(r"H", r"|", r"E").scale(self.scale_eq_f)
        self.tex_cond_eq_2[0].set_color(self.col_h)
        self.tex_cond_eq_2[2].set_color(self.col_e)
        myutil.critical_point_move_to(self.tex_cond_eq_2, LEFT + DOWN,     ORIGIN + -4.2 * RIGHT + -2.0 * UP)


        # probability notation
        self.tex_prob_eq         = [
            MathTex(r"P()").   scale(self.scale_eq_f),
            MathTex(r"P(A)").  scale(self.scale_eq_f),
            MathTex(r"P(", r"H", r"|", r"E", r")").scale(self.scale_eq_f),
        ]
        self.tex_prob_eq[2][1].set_color(self.col_h)
        self.tex_prob_eq[2][3].set_color(self.col_e)

        self.txt_prob_exp = [
            Text(r": 〜の確率 (Probability)").scale(self.scale_txt_f),
            Text(r": A の確率").              scale(self.scale_txt_f),
            Text(r": E の時に H になる確率",
                 t2c={"[1:2]": self.col_e, "[5:6]": self.col_h}
            ). scale(self.scale_txt_f),
            ]

        myutil.critical_point_move_to(self.tex_prob_eq[0], LEFT + DOWN, ORIGIN + -6.0 * RIGHT + -2.0 * UP)
        myutil.critical_point_move_to(self.tex_prob_eq[1], LEFT + DOWN, ORIGIN +  2.0 * RIGHT + -2.0 * UP)
        myutil.critical_point_move_to(self.tex_prob_eq[2], LEFT + DOWN, ORIGIN + -6.0 * RIGHT + -3.0 * UP)
        for i in range(0, len(self.txt_prob_exp)):
            self.txt_prob_exp[i].next_to(self.tex_prob_eq[i])



    def show_only(self):
        """Only add, no animation
        """
        self.add(self.txt_title_bayes,
                 self.mtex_bayes_simple,
                 self.txt_how_to_read,
                 self.tex_events_eq,
                 *self.txt_events_exp,
                 self.tex_cond_eq,
                 *self.txt_cond_exp_1,
                 *self.txt_cond_exp_2,
                 *self.tex_prob_eq,
                 *self.txt_prob_exp,
        )


    def animate_title_equation(self):
        """part 1
        animate title and equation
        """

        # Show title
        self.play(FadeIn(self.txt_title_bayes))
        self.wait(self.time_wait)

        # Show equation
        self.play(FadeIn(self.mtex_bayes_simple))
        self.wait(self.time_wait)

        # How to read
        self.play(FadeInFrom(self.txt_how_to_read, direction=DOWN))
        self.wait(self.time_wait)


    def animate_variable(self):
        """part 2
        animate E, H, A, B: explanation
        """
        # E, H, A, B
        self.play(FadeIn(self.tex_events_eq))
        self.wait(self.time_wait)

        # event, example 1, example 2
        for txt in self.txt_events_exp:
            self.play(FadeIn(txt))
            self.wait(self.time_wait)

        # condition H|E
        self.play(FadeIn(self.tex_cond_eq))
        self.wait(self.time_wait)

        # condition explain
        self.play(*[FadeIn(mobj) for mobj in self.txt_cond_exp_1])
        self.wait(self.time_wait)

        emphasis_factor = 1.3
        self.play(ApplyMethod(self.tex_cond_eq[1].scale,    emphasis_factor),
                  ApplyMethod(self.txt_cond_exp_1[1].scale, emphasis_factor))
        self.play(ApplyMethod(self.tex_cond_eq[1].scale,    1/emphasis_factor),
                  ApplyMethod(self.txt_cond_exp_1[1].scale, 1/emphasis_factor))
        self.wait(self.time_wait)

        # condition explain in English
        self.play(*[FadeIn(mobj) for mobj in self.txt_cond_exp_2])
        self.wait(self.time_wait)

        # Turns out, not a good idea
        # emphasis_factor = 1.3
        # for i in range(0,3):
        #     self.play(ApplyMethod(self.tex_cond_eq[i].scale,    emphasis_factor),
        #               ApplyMethod(self.txt_cond_exp_2[i].scale, emphasis_factor))
        #     self.play(ApplyMethod(self.tex_cond_eq[i].scale,    1/emphasis_factor),
        #               ApplyMethod(self.txt_cond_exp_2[i].scale, 1/emphasis_factor))
        # self.wait(self.time_wait)

        self.play(Transform(self.txt_cond_exp_2[0], self.tex_cond_eq_2[0]))
        self.wait(self.time_wait)
        self.play(Transform(self.txt_cond_exp_2[1], self.tex_cond_eq_2[1]))
        self.wait(self.time_wait)
        self.play(Transform(self.txt_cond_exp_2[2], self.tex_cond_eq_2[2]))
        self.wait(self.time_wait)

        # need to be array dereference, due to transform overwritten
        self.play(FadeOut(self.txt_cond_exp_2[0]), FadeOut(self.txt_cond_exp_2[1]), FadeOut(self.txt_cond_exp_2[2]))
        self.wait(self.time_wait)


    def animate_probablity(self):
        """part 3
        animate P()'s meaning
        """

        # probability notation: reposition
        myutil.critical_point_move_to(self.tex_prob_eq[1], LEFT + DOWN, ORIGIN + -6.0 * RIGHT + -2.0 * UP)
        myutil.critical_point_move_to(self.tex_prob_eq[2], LEFT + DOWN, ORIGIN + -6.0 * RIGHT + -2.0 * UP)
        for i in range(0, len(self.txt_prob_exp)):
            self.txt_prob_exp[i].next_to(self.tex_prob_eq[i], buff=0.2)

        # working memory (Transform(a, b): a = b, a is written
        eq_work  = copy.deepcopy(self.tex_prob_eq[0])

        # P()
        self.play(FadeIn(eq_work))
        self.wait(self.time_wait)

        # P() : 〜の確率
        self.play(FadeIn(self.txt_prob_exp[0]))
        self.wait(self.time_wait)

        # P(A)
        self.play(Transform(eq_work,  self.tex_prob_eq[1]),
                  FadeOut(self.txt_prob_exp[0]))
        self.wait(self.time_wait)

        # P(A): A の確率
        self.play(FadeIn(self.txt_prob_exp[1]))
        self.wait(self.time_wait)

        # P(H|E)
        self.play(Transform(eq_work,  self.tex_prob_eq[2]),
                  FadeOut(self.txt_prob_exp[1]))
        self.wait(self.time_wait)

        # P(H|E): E の時，H となる確率
        self.play(FadeIn(self.txt_prob_exp[2]))
        self.wait(self.time_wait)


    def animate_bayes_rhs(self):
        """part 4 Bayes right hand side
        """
        self.remove(self.mtex_bayes_simple[2],
                    self.mtex_bayes_simple[3],
                    self.mtex_bayes_simple[5])

        self.play(FadeIn(self.mtex_bayes_simple[2]))
        self.wait(self.time_wait)

        self.play(FadeIn(self.mtex_bayes_simple[3]))
        self.wait(self.time_wait)

        self.play(FadeIn(self.mtex_bayes_simple[5]))
        self.wait(self.time_wait)


    def animate_cleanup(self):
        """part 5
        clean up to next animation
        Failed to do. Use video editing
        """
        self.play(
            FadeOut(self.txt_how_to_read),
            FadeOut(self.tex_events_eq),
            *[FadeOut(mobj) for mobj in self.txt_events_exp],
        )


    def construct(self):
        """Read Bayes theorem statement
        """
        self.create_bayes_eq()

        if (self.is_show_only):
            self.show_only()
        else:
            self.animate_title_equation()
            self.animate_variable()
            self.animate_probablity()
            self.animate_bayes_rhs()
            # self.animate_cleanup()

        self.wait(5)
