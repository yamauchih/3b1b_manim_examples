# -*- coding: utf-8; -*-
#
# disease test and Bayes' theorem
#
# 07_bayse_example_02
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
#   python3 -m manim 08_bayse_example_02.py BayesExample02 --resolution 720,1280 -p --high_quality
# Preview resolution
#   python3 -m manim 08_bayse_example_02.py BayesExample02 --resolution 360,640 -p -ql
#

from manim import *
import copy, numpy, random
import myutil


class BayesExample02(Scene):
# class BayesExample02(LinearTransformationScene):
    """Bayes theorem: example 02: more realistic concrete example (example 2)
    Equation aniamation.
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
        "time_wait":            5.0,
        "is_show_only":         False,

        #-- shared MObjects
        "txt_title_bayes":    None,
        "col_positive":       RED,
        "col_negative":       BLUE,
        "col_true_positive":  PINK,
        "col_false_positive": WHITE,

        # title scaling factor
        "scale_title_f":    0.9,
        # equation scaling factor
        "scale_eq_f":       1.0,
        # text scaling factor
        "scale_txt_f":      0.8,

        # P(H|E) = {{P(E|H) P(H)} \over {P(E|H)P(H) + P(E|\lnot H)P(\lnot H)}
        # use over instead of frac for coloring (frac cannot be divided)
        "mtex_bayes_full":  None,
        "col_h":            YELLOW,
        "col_e":            BLUE_B,
        "col_n":            RED,
        "h_indices":        None, # for H
        "e_indices":        None, # for E
        "n_indices":        None, # for \lnot

        # events example 1
        #   H: really ill
        "mtex_event_h": None,
        "txt_event_h":  None,

        # event footnote scale for eq: equation, txt: text
        "scale_event_eq_f":  1.0,
        "scale_event_txt_f": 0.8,

        # events example 2
        #   E: test positive
        "mtex_event_e": None,
        "txt_event_e":  None,

        # --- example 2
        "text_p_h": None,
        "mtex_p_h": None,

        "text_p_not_h": None,
        "mtex_p_not_h": None,

        "text_p_e_h": None,
        "mtex_p_e_h": None,

        "text_p_e_not_h": None,
        "mtex_p_e_not_h": None,

        # values
        # P(H) = 0.001
        "p_h_1": None,
        "p_h_2": None,

        # P(\lnot H) = 0.999
        "p_not_h": None,

        # P(E|H) = 1.0
        "p_e_h_1": None,
        "p_e_h_2": None,

        # P(E|\lnot H) = 0.99
        "p_e_not_h": None,

        # P(E|H) result number, and its percent
        "p_e_h": None,
        "p_e_h_percent": None,
    }


    def create_bayes_eq(self):
        """create all mobjects
        """

        self.txt_title_bayes = Text(r"具体例 2").scale(self.scale_title_f)
        myutil.critical_point_move_to(self.txt_title_bayes, LEFT + DOWN, ORIGIN + -6.3 * RIGHT + 3.0 * UP)

        # full Bayes form                                 # indices for h,e color (MathTex removes white space))
        self.mtex_bayes_full = MathTex(r"P(H|E)",          # [0] e [0,4], h [0,2]
                                       r"={",              # [1]
                                       r"{P(H)",           # [2]          h [2,2]
                                       r"P(E|H)}",         # [3] e [3,2], h [3,4]
                                       r"\over",           # [4]
                                       r"{P(H)",           # [5]          h [5,2]
                                       r"P(E|H)}",         # [6] e [6,2], h [6,4]
                                       r"+",               # [7]
                                       r"{P(\lnot H)",     # [8]          h [8,3], n [8,2]
                                       r"P(E |\lnot H)}}", # [9] e [9,2], h [9,5], n [9,4]
        ).scale(self.scale_eq_f)
        myutil.critical_point_move_to(self.mtex_bayes_full, LEFT + DOWN, ORIGIN + -5.0 * RIGHT + 1.4 * UP)

        self.h_indices = [[0, 2], [2, 2], [3, 4], [5, 2], [6, 4], [8, 3], [9, 5]]
        for [i,j] in self.h_indices:
            self.mtex_bayes_full[i][j].set_color(self.col_h)
        self.e_indices = [[0, 4], [3, 2], [6, 2], [9, 2]]
        for [i,j] in self.e_indices:
            self.mtex_bayes_full[i][j].set_color(self.col_e)
        self.n_indices = [[8, 2], [9, 4]]
        for [i,j] in self.n_indices:
            self.mtex_bayes_full[i][j].set_color(self.col_n)

        # --- Event examples
        # event example H
        self.mtex_event_h = MathTex(r"H").  scale(self.scale_event_eq_f).set_color(
            self.col_h).move_to(0.2 * RIGHT + 3.4 * UP)
        self.txt_event_h = Text(r": 病気").scale(self.scale_event_txt_f).move_to(1.3 * RIGHT + 3.4 * UP)

        # event example E
        self.mtex_event_e = MathTex(r"E").scale(self.scale_event_eq_f).set_color(
            self.col_e).move_to(2.7 * RIGHT + 3.37 * UP)
        self.txt_event_e = Text(r": 検査＋", t2c={r"[3:4]": self.col_positive}).scale(
            self.scale_event_txt_f).move_to(4.0 * RIGHT + 3.37 * UP)

        # --- another example (counter intuitive, but more realistic

        # 病気の確率  0.1%: P(H)  = 0.001
        self.text_p_h = [Text(r"病気の確率").scale(self.scale_txt_f),
                         MathTex(r"0.1 \%"). scale(self.scale_eq_f),]
        self.mtex_p_h = MathTex(r"P(H)", r"=", r"0.001").scale(self.scale_eq_f)
        self.mtex_p_h[0][2].set_color(self.col_h)

        # ¬病気の可能性 0.1%: P(¬H) = 0.999
        self.text_p_not_h = [Text(r"¬病気の確率", t2c={"[0:1]": self.col_n}).scale(self.scale_txt_f),
                             MathTex(r"99.9 \%"). scale(self.scale_eq_f),]
        self.mtex_p_not_h = MathTex(r"P(\lnot H)", r"=", r"0.999").scale(self.scale_eq_f)
        self.mtex_p_not_h[0][2].set_color(self.col_n)
        self.mtex_p_not_h[0][3].set_color(self.col_h)

        # 病気の時に検査+ 100%: P(E|H) = 1.0
        self.text_p_e_h = [Text(r"病気の時，検査＋", t2c={"[7:8]": self.col_positive}).scale(self.scale_txt_f),
                           MathTex(r"100 \%").       scale(self.scale_eq_f),]
        self.mtex_p_e_h = MathTex(r"P(E|H)", r"=", r"1.0"). scale(self.scale_eq_f)
        self.mtex_p_e_h[0][2].set_color(self.col_e)
        self.mtex_p_e_h[0][4].set_color(self.col_h)

        # ¬病気の時に検査+  1%: P(E|¬H) = 0.01
        self.text_p_e_not_h = [Text(r"¬病気の時，検査＋",
                                    t2c={"[0:1]": self.col_n, "[8:9]": self.col_positive}).scale(self.scale_txt_f),
                               MathTex(r" 1 \%").         scale(self.scale_eq_f)]
        self.mtex_p_e_not_h = MathTex(r"P(E|\lnot H)", r"=", r"0.01").scale(self.scale_eq_f)
        self.mtex_p_e_not_h[0][2].set_color(self.col_e)
        self.mtex_p_e_not_h[0][4].set_color(self.col_n)
        self.mtex_p_e_not_h[0][5].set_color(self.col_h)

        # text up shift and text right shift
        text_up = [ 0.0, -0.8, -1.6, -2.4]
        text_ri = [-5.5, +0.3]
        text_align = [LEFT, RIGHT]
        for i in range(0, 2):
            myutil.critical_point_move_to(self.text_p_h[i],       text_align[i], text_ri[i] * RIGHT + text_up[0] * UP)
            myutil.critical_point_move_to(self.text_p_not_h[i],   text_align[i], text_ri[i] * RIGHT + text_up[1] * UP)
            myutil.critical_point_move_to(self.text_p_e_h[i],     text_align[i], text_ri[i] * RIGHT + text_up[2] * UP)
            myutil.critical_point_move_to(self.text_p_e_not_h[i], text_align[i], text_ri[i] * RIGHT + text_up[3] * UP)

        mtex_ri = [+3.0, +3.4, +4.2]
        text_align = [RIGHT, LEFT, LEFT]
        for i in range(0, 3):
            myutil.critical_point_move_to(self.mtex_p_h[i],       text_align[i], ORIGIN + mtex_ri[i] * RIGHT + text_up[0] * UP)
            myutil.critical_point_move_to(self.mtex_p_not_h[i],   text_align[i], ORIGIN + mtex_ri[i] * RIGHT + text_up[1] * UP)
            myutil.critical_point_move_to(self.mtex_p_e_h[i],     text_align[i], ORIGIN + mtex_ri[i] * RIGHT + text_up[2] * UP)
            myutil.critical_point_move_to(self.mtex_p_e_not_h[i], text_align[i], ORIGIN + mtex_ri[i] * RIGHT + text_up[3] * UP)


    def show_title(self):
        """より現実的な具体例
        """
        # Already shown
        if (self.is_show_only):
            self.add(self.txt_title_bayes)
            self.add(self.mtex_bayes_full)
            self.add(self.mtex_event_e, self.txt_event_e)
            self.add(self.mtex_event_h, self.txt_event_h)
            self.wait(self.time_wait)
            return


        self.play(FadeIn(self.txt_title_bayes))
        self.wait(self.time_wait)

        self.play(FadeIn(self.mtex_bayes_full),
                  FadeIn(self.mtex_event_e), FadeIn(self.txt_event_e),
                  FadeIn(self.mtex_event_h), FadeIn(self.txt_event_h))
        self.wait(self.time_wait)


    def animate_description(self):
        """description
        """
        if (self.is_show_only):
            self.add(*self.text_p_h,
                     *self.text_p_not_h,
                     *self.text_p_e_h,
                     *self.text_p_e_not_h)
            self.add(self.mtex_p_h,
                     self.mtex_p_not_h,
                     self.mtex_p_e_h,
                     self.mtex_p_e_not_h)
            self.wait(self.time_wait)
            return

        # P(H)
        self.play(FadeIn(self.text_p_h[0]),
                  FadeIn(self.text_p_h[1]))
        self.wait(self.time_wait)

        self.play(FadeIn(    self.mtex_p_h[0]),
                  FadeIn(    self.mtex_p_h[1]),
                  FadeInFrom(self.mtex_p_h[2], direction=DOWN))
        self.wait(self.time_wait)

        # P(\lnot H)
        self.play(FadeIn(self.text_p_not_h[0]),
                  FadeIn(self.text_p_not_h[1]))
        self.wait(self.time_wait)

        self.play(FadeIn(    self.mtex_p_not_h[0]),
                  FadeIn(    self.mtex_p_not_h[1]),
                  FadeInFrom(self.mtex_p_not_h[2], direction=DOWN))
        self.wait(self.time_wait)

        # P(\E|H)
        self.play(FadeIn(self.text_p_e_h[0]),
                  FadeIn(self.text_p_e_h[1]))
        self.wait(self.time_wait)

        self.play(FadeIn(    self.mtex_p_e_h[0]),
                  FadeIn(    self.mtex_p_e_h[1]),
                  FadeInFrom(self.mtex_p_e_h[2], direction=DOWN))
        self.wait(self.time_wait)

        # P(E|\lnot H)
        self.play(FadeIn(self.text_p_e_not_h[0]),
                  FadeIn(self.text_p_e_not_h[1]))
        self.wait(self.time_wait)

        self.play(FadeIn(    self.mtex_p_e_not_h[0]),
                  FadeIn(    self.mtex_p_e_not_h[1]),
                  FadeInFrom(self.mtex_p_e_not_h[2], direction=DOWN))
        self.wait(self.time_wait)


    def animate_substitute(self):
        """simplily fraction
        """
        # copy the values: P(H) = 0.001
        self.p_h_1 = copy.deepcopy(self.mtex_p_h[2])
        self.p_h_2 = copy.deepcopy(self.mtex_p_h[2])

        # copy the values: P(\lnot H) = 0.999
        self.p_not_h = copy.deepcopy(self.mtex_p_not_h[2])

        # copy the values: P(E|H) = 1.0
        self.p_e_h_1 = copy.deepcopy(self.mtex_p_e_h[2])
        self.p_e_h_2 = copy.deepcopy(self.mtex_p_e_h[2])

        # copy the values: P(E|\lnot H) = 0.99
        self.p_e_not_h = copy.deepcopy(self.mtex_p_e_not_h[2])

        if (self.is_show_only):
            self.p_h_1.move_to(self.mtex_bayes_full[2].get_center())
            self.p_h_2.move_to(self.mtex_bayes_full[5].get_center())

            self.p_not_h.move_to(self.mtex_bayes_full[8].get_center())

            self.p_e_h_1.move_to(self.mtex_bayes_full[3].get_center())
            self.p_e_h_2.move_to(self.mtex_bayes_full[6].get_center())

            self.p_e_not_h.move_to(self.mtex_bayes_full[9].get_center())
            self.remove(self.mtex_bayes_full[2],
                        self.mtex_bayes_full[5],
                        self.mtex_bayes_full[8],
                        self.mtex_bayes_full[3],
                        self.mtex_bayes_full[6],
                        self.mtex_bayes_full[9])
            self.add(self.p_h_1,
                     self.p_h_2,
                     self.p_not_h,
                     self.p_e_h_1,
                     self.p_e_h_2,
                     self.p_e_not_h)

            self.wait(self.time_wait)
            return

        # # P(H)
        # self.play(ApplyMethod(self.p_h_1.move_to, self.mtex_bayes_full[2].get_center()),
        #           FadeOut(self.mtex_bayes_full[2]),
        #           ApplyMethod(self.p_h_2.move_to, self.mtex_bayes_full[5].get_center()),
        #           FadeOut(self.mtex_bayes_full[5]))
        # self.wait(self.time_wait)

        # # P(\lnot H)
        # self.play(ApplyMethod(self.p_not_h.move_to, self.mtex_bayes_full[8].get_center()),
        #           FadeOut(self.mtex_bayes_full[8]))
        # self.wait(self.time_wait)

        # # P(E|H)
        # self.play(ApplyMethod(self.p_e_h_1.move_to, self.mtex_bayes_full[3].get_center()),
        #           FadeOut(self.mtex_bayes_full[3]),
        #           ApplyMethod(self.p_e_h_2.move_to, self.mtex_bayes_full[6].get_center()),
        #           FadeOut(self.mtex_bayes_full[6]))
        # self.wait(self.time_wait)

        # # P(E|\lnot H)
        # self.play(ApplyMethod(self.p_e_not_h.move_to, self.mtex_bayes_full[9].get_center()),
        #           FadeOut(self.mtex_bayes_full[9]))
        # self.wait(self.time_wait)

        self.play(ApplyMethod(self.p_h_1.move_to,     self.mtex_bayes_full[2].get_center()),
                  FadeOut(self.mtex_bayes_full[2]),
                  ApplyMethod(self.p_h_2.move_to,     self.mtex_bayes_full[5].get_center()),
                  FadeOut(self.mtex_bayes_full[5]),
                  ApplyMethod(self.p_not_h.move_to,   self.mtex_bayes_full[8].get_center()),
                  FadeOut(self.mtex_bayes_full[8]),
                  ApplyMethod(self.p_e_h_1.move_to,   self.mtex_bayes_full[3].get_center()),
                  FadeOut(self.mtex_bayes_full[3]),
                  ApplyMethod(self.p_e_h_2.move_to,   self.mtex_bayes_full[6].get_center()),
                  FadeOut(self.mtex_bayes_full[6]),
                  ApplyMethod(self.p_e_not_h.move_to, self.mtex_bayes_full[9].get_center()),
                  FadeOut(self.mtex_bayes_full[9]))
        self.wait(self.time_wait)


    def animate_simplify(self):
        """simplily the rhs
        """
        # copy the values: P(H), 0.001 * P(E|H), 1.0 = 0.001

        # first simplify
        #   pos_nomi / (pos_denom_1 + pos_denom_2)
        pos_nom     = 0.5 * (self.p_h_1.  get_center() + self.p_e_h_1.  get_center())

        pos_denom_1 = 0.5 * (self.p_h_2.  get_center() + self.p_e_h_2.  get_center())
        pos_denom_2 = 0.5 * (self.p_not_h.get_center() + self.p_e_not_h.get_center())
        p_not_h_p_e_not_h = MathTex(r"0.989").scale(self.scale_eq_f)

        # second simplify
        #   pos_nomi / pos_denom
        pos_denom = np.array((pos_nom[0], pos_denom_1[1], 0.0))

        p_denom = MathTex(r"0.011").scale(self.scale_eq_f)

        # third (final) simplify
        # (/ 0.001 (+ 0.001 (* 0.999 0.01))) 0.091
        # (/ 0.001 0.011)
        self.p_e_h = MathTex(r"0.091").scale(self.scale_eq_f)

        self.p_e_h_percent = MathTex(r"\approx", r"9 \%").scale(self.scale_eq_f)

        if (self.is_show_only):
            # 1st simplify
            self.p_h_1.move_to(pos_nom)

            self.p_h_2.       move_to(pos_denom_1)
            p_not_h_p_e_not_h.move_to(pos_denom_2)
            self.add(p_not_h_p_e_not_h)

            self.remove(self.p_e_h_1,
                        self.p_e_h_2,
                        self.p_not_h,
                        self.p_e_not_h)
            self.wait(self.time_wait)

            # 2nd denom = 0.011
            p_denom.move_to(pos_denom)
            self.add(p_denom)
            self.remove(self.p_h_2,
                        p_not_h_p_e_not_h,
                        self.mtex_bayes_full[7], # +
            )
            self.wait(self.time_wait)

            # 3rd
            self.p_e_h.next_to(self.mtex_bayes_full[1])
            self.add(self.p_e_h)
            self.remove(self.p_h_1,
                        self.mtex_bayes_full[4], # \over
                        p_denom,
            )
            self.wait(self.time_wait)

            self.p_e_h_percent.next_to(self.p_e_h)
            self.add(self.p_e_h_percent)
            self.wait(self.time_wait)
            return


        # 1st simplify
        p_not_h_p_e_not_h.move_to(pos_denom_2)
        self.play(ApplyMethod(self.p_h_1.move_to, pos_nom),
                  FadeOut(self.p_e_h_1),
                  ApplyMethod(self.p_h_2.move_to, pos_denom_1),
                  FadeOut(self.p_e_h_2))
        self.wait(self.time_wait)

        self.play(FadeOut(self.p_not_h),
                  FadeOut(self.p_e_not_h),
                  FadeIn( p_not_h_p_e_not_h))
        self.wait(self.time_wait)

        # 2nd denom = 0.011
        p_denom.move_to(pos_denom)

        self.play(FadeOut(self.p_h_2),
                  FadeOut(p_not_h_p_e_not_h),
                  FadeOut(self.mtex_bayes_full[7]), # +
                  FadeIn(p_denom))
        self.wait(self.time_wait)

        # 3rd
        self.p_e_h.next_to(self.mtex_bayes_full[1])
        self.play(FadeInFrom(self.p_e_h, direction=RIGHT),
                  FadeOut(self.p_h_1),
                  FadeOut(self.mtex_bayes_full[4]), # \over
                  FadeOut(p_denom)
        )
        self.wait(self.time_wait)

        # 9.1 percent
        self.p_e_h_percent.next_to(self.p_e_h)
        self.play(FadeInFrom(self.p_e_h_percent, direction=RIGHT))
        self.wait(self.time_wait)

        return


    def construct(self):
        """More realistic example (example 2)
        """
        # generate random positions for true positive and false positive
        # self.gen_false_positive()

        self.create_bayes_eq()
        self.show_title()

        self.animate_description()
        self.animate_substitute()
        self.animate_simplify()


        self.wait(5)
