# -*- coding: utf-8; -*-
#
# disease test and Bayes' theorem
#
# 06_why_bayse_01
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
#   python3 -m manim 06_why_bayse_01.py WhyBayes01 --resolution 720,1280 -p --high_quality
# Preview resolution
#   python3 -m manim 06_why_bayse_01.py WhyBayes01 --resolution 360,640 -p -ql
#

from manim import *
import copy, numpy
import myutil


class WhyBayes01(Scene):
# class WhyBayes01(LinearTransformationScene):
    """Bayes theorem: event example 01: test positive/negative and really ill
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
        "col_positive":    RED,
        "col_negative":    BLUE,

        # title scaling factor
        "scale_title_f":    0.9,
        # equation scaling factor
        "scale_eq_f":       1.0,
        # text scaling factor
        "scale_txt_f":      0.8,

        # P(H|E) = {{P(E|H) P(H)} \over P(E)} ... use over instead of frac for coloring (frac cannot be divided)
        # DELETEME "tex_bayes_simple": None,
        "tex_bayes_full":   None,
        "col_h":            YELLOW,
        "col_e":            BLUE_B,
        "col_n":            RED,
        "h_indices":        None,
        "e_indices":        None,

        # events example 1
        #   H: really ill
        "mtex_event_h":  None,
        "txt_event_h":  None,

        # events example 2
        #   E: test positive
        "mtex_event_e":  None,
        "txt_event_e":  None,

        # P(H|E): 検査+ の時に実際に病気である確率。(不明，知りたいこと)
        "mtex_event_prob_h_b_e":  None,
        "txt_event_prob_h_b_e":  None,

        # P(H): 実際に病気である確率。(難しい。推定可能，検査で改善可能)
        "mtex_event_prob_h":  None,
        "txt_event_prob_h":  None,

        # P(\lnot H): 実際に病気でない確率。H の補集合，P(H) がわかればわかる
        "mtex_event_prob_not_h":  None,
        "txt_event_prob_not_h":  None,

        # P(E|H): 実際に病気の時に検査+ の確率: 検査キットの性能, (測定可能，既知)
        "mtex_event_prob_e_b_h":  None,
        "txt_event_prob_e_b_h":  None,

        # P(E|\lnot H): 実際に病気でない時に検査+ の確率: 検査キットの性能 (測定可能，既知)
        "mtex_event_prob_e_b_not_h":  None,
        "txt_event_prob_e_b_not_h":  None,
    }

    def create_bayes_eq(self):
        """
        """
        self.txt_title_bayes = Text(r"何故ベイズの定理?").scale(self.scale_title_f)
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
                                       r"{P(\lnot H)",     # [8]          h [8,3] n [8,2]
                                       r"P(E |\lnot H)}}", # [9] e [9,2], h [9,5] n [9,4]
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
        var_buff = 0.2
        self.mtex_event_h = MathTex(r"H").scale(self.scale_eq_f).set_color(self.col_h)
        self.txt_event_h = Text(r": 病気").scale(self.scale_txt_f)
        myutil.critical_point_move_to(self.mtex_event_h, RIGHT + DOWN, ORIGIN + -4.0 * RIGHT +  0.2 * UP)
        self.txt_event_h.next_to(self.mtex_event_h, buff=var_buff)

        # event example E
        self.mtex_event_e = MathTex(r"E").scale(self.scale_eq_f).set_color(self.col_e)
        self.txt_event_e = Text(r": 検査＋", t2c={r"[3:4]": self.col_positive}).scale(self.scale_txt_f)
        myutil.critical_point_move_to(self.mtex_event_e, RIGHT + DOWN, ORIGIN + -4.0 * RIGHT + -0.6 * UP)
        self.txt_event_e.next_to(self.mtex_event_e, buff=var_buff)

        # P(H|E): 検査+ の時に実際に病気である確率。(不明，知りたいこと)
        self.mtex_event_prob_h_b_e = MathTex(r"P(", r"H", r"|", r"E", r")").scale(self.scale_eq_f)
        self.mtex_event_prob_h_b_e[1].set_color(self.col_h)
        self.mtex_event_prob_h_b_e[3].set_color(self.col_e)
        self.txt_event_prob_h_b_e = [
            Text(r": 検査＋の時に実際に病気の確率",
                 t2c={r"[3:4]": self.col_positive,}).scale(self.scale_txt_f),
            Text(r": 「知りたいこと」",).scale(self.scale_txt_f),
            Text(r"(未知)",).scale(self.scale_txt_f).set_color(RED),
        ]
        myutil.critical_point_move_to(self.mtex_event_prob_h_b_e, RIGHT + DOWN, -3.0 * RIGHT + 0.5 * UP)
        self.txt_event_prob_h_b_e[0].next_to(self.mtex_event_prob_h_b_e, buff=var_buff)
        self.txt_event_prob_h_b_e[1].next_to(self.mtex_event_prob_h_b_e, buff=var_buff)
        myutil.critical_point_move_to(self.txt_event_prob_h_b_e[2], LEFT + DOWN, 3.5 * RIGHT + 0.5 * UP)

        # P(H): 実際に病気である確率。(難しい。推定可能，検査で改善可能)
        self.mtex_event_prob_h = MathTex(r"P(", r"H", r")").scale(self.scale_eq_f)
        self.mtex_event_prob_h[1].set_color(self.col_h)
        self.txt_event_prob_h = [
            Text(r": 実際に病気の確率",).scale(self.scale_txt_f),
            Text(r": 推定，改善可能",).scale(self.scale_txt_f),
            Text(r"(既知)",).scale(self.scale_txt_f),
        ]
        myutil.critical_point_move_to(self.mtex_event_prob_h, RIGHT + DOWN,     -3.0 * RIGHT + -0.4 * UP)
        self.txt_event_prob_h[0].next_to(self.mtex_event_prob_h, buff=var_buff)
        self.txt_event_prob_h[1].next_to(self.mtex_event_prob_h, buff=var_buff)
        myutil.critical_point_move_to(self.txt_event_prob_h[2], LEFT + DOWN,     3.5 * RIGHT + -0.4 * UP)

        # P(\lnot H): 実際に病気でない確率。H の補集合，P(H) がわかればわかる
        self.mtex_event_prob_not_h = MathTex(r"P(", r"\lnot", r"H", r")").scale(self.scale_eq_f)
        self.mtex_event_prob_not_h[1].set_color(self.col_n)
        self.mtex_event_prob_not_h[2].set_color(self.col_h)
        self.txt_event_prob_not_h = [
            Text(r": 実際に病気でない確率",).scale(self.scale_txt_f),
            Text(r": H の補集合",).scale(self.scale_txt_f),
            Text(r"(既知)",).scale(self.scale_txt_f),
        ]
        myutil.critical_point_move_to(self.mtex_event_prob_not_h, RIGHT + DOWN,  -3.0 * RIGHT + -1.3 * UP)
        self.txt_event_prob_not_h[0].next_to(self.mtex_event_prob_not_h, buff=var_buff)
        self.txt_event_prob_not_h[1].next_to(self.mtex_event_prob_not_h, buff=var_buff)
        myutil.critical_point_move_to(self.txt_event_prob_not_h[2], LEFT + DOWN,  3.5 * RIGHT + -1.3 * UP)

        # P(E|H): 実際に病気の時に検査+ の確率: 検査キットの性能, (測定可能，既知)
        self.mtex_event_prob_e_b_h = MathTex(r"P(", r"E", r"|", r"H", r")").scale(self.scale_eq_f)
        self.mtex_event_prob_e_b_h[1].set_color(self.col_e)
        self.mtex_event_prob_e_b_h[3].set_color(self.col_h)
        self.txt_event_prob_e_b_h = [
            Text(r": 実際に病気の時に，検査＋の確率",
                 t2c={r"[12:13]": self.col_positive,}).scale(self.scale_txt_f),
            Text(r": 検査の性能: 感度",).scale(self.scale_txt_f),
            Text(r"(既知)",).scale(self.scale_txt_f),
        ]
        myutil.critical_point_move_to(self.mtex_event_prob_e_b_h, RIGHT + DOWN, -3.0 * RIGHT + -2.2 * UP)
        self.txt_event_prob_e_b_h[0].next_to(self.mtex_event_prob_e_b_h, buff=var_buff)
        self.txt_event_prob_e_b_h[1].next_to(self.mtex_event_prob_e_b_h, buff=var_buff)
        myutil.critical_point_move_to(self.txt_event_prob_e_b_h[2], LEFT + DOWN, 3.5 * RIGHT + -2.2 * UP)

        # P(E|\lnot H): 実際に病気でない時に検査+ の確率: 検査キットの性能 (測定可能，既知)
        self.mtex_event_prob_e_b_not_h = MathTex(r"P(", r"E", r"|", r"\lnot", r"H", r")").scale(self.scale_eq_f)
        self.mtex_event_prob_e_b_not_h[1].set_color(self.col_e)
        self.mtex_event_prob_e_b_not_h[3].set_color(self.col_n)
        self.mtex_event_prob_e_b_not_h[4].set_color(self.col_h)
        self.txt_event_prob_e_b_not_h = [
            Text(r": 実際に病気でない時に，検査＋の確率",
                 t2c={r"[14:15]": self.col_positive,}).scale(self.scale_txt_f),
            Text(r": 検査の性能: 1 - 特異度",).scale(self.scale_txt_f),
            Text(r"(既知)",).scale(self.scale_txt_f),
        ]
        myutil.critical_point_move_to(self.mtex_event_prob_e_b_not_h, RIGHT + DOWN, -3.0 * RIGHT + -3.1 * UP)
        self.txt_event_prob_e_b_not_h[0].next_to(self.mtex_event_prob_e_b_not_h, buff=var_buff)
        self.txt_event_prob_e_b_not_h[1].next_to(self.mtex_event_prob_e_b_not_h, buff=var_buff)
        myutil.critical_point_move_to(self.txt_event_prob_e_b_not_h[2], LEFT + DOWN, 3.5 * RIGHT + -3.1 * UP)


    def show_title(self):
        """何故ベイズの定理?
        """
        if (self.is_show_only):
            self.add(self.txt_title_bayes)
            return

        self.play(FadeIn(self.txt_title_bayes))
        self.wait(self.time_wait)



    def show_bayes(self):
        """ベイズの定理
        """

        # E: 検査+， H: 病気
        self.mtex_event_h.scale(1.0 / self.scale_eq_f)
        self.txt_event_h.scale(0.8 / self.scale_txt_f)
        self.mtex_event_e.scale(1.0 / self.scale_eq_f)
        self.txt_event_e.scale(0.8 / self.scale_txt_f)
        myutil.critical_point_move_to(self.mtex_event_h, LEFT + DOWN, ORIGIN + 0.0 * RIGHT + 3.0 * UP)
        self.txt_event_h.next_to(self.mtex_event_h)
        myutil.critical_point_move_to(self.mtex_event_e, LEFT + DOWN, ORIGIN + 2.5 * RIGHT + 3.0 * UP)
        self.txt_event_e.next_to(self.mtex_event_e)

        if (self.is_show_only):
            self.add(self.mtex_bayes_full)
            self.add(self.mtex_event_e, self.txt_event_e)
            self.add(self.mtex_event_h, self.txt_event_h)
            return

        self.play(FadeIn(self.mtex_bayes_full),
                  FadeIn(self.mtex_event_e), FadeIn(self.txt_event_e),
                  FadeIn(self.mtex_event_h), FadeIn(self.txt_event_h))
        self.wait(self.time_wait)


    def copy_move_term_explain(self, src_term_list, dst_term, dst_exp):
        """convenient function for unknown and known explanation
        """
        work_list = copy.deepcopy(src_term_list)
        myutil.move_src_list_dst(self, work_list, dst_term)
        self.remove(*work_list)
        self.add(dst_term)
        self.wait(self.time_wait)

        self.play(FadeIn(dst_exp[0]))    # literal meaning
        self.wait(self.time_wait)

        self.play(FadeOut(dst_exp[0]),   # interpretation meaning
                  FadeIn( dst_exp[1]))
        self.wait(self.time_wait)

        self.play(FadeIn( dst_exp[2]))   # 既知，未知
        self.wait(self.time_wait)



    def animate_why(self):
        """why bayes?
        """
        if (self.is_show_only):
            # P(H|E): 検査+ の時に実際に病気である確率。(不明，知りたいこと)
            self.add(self.mtex_event_prob_h_b_e, self.txt_event_prob_h_b_e[0])

            # P(H): 実際に病気である確率。(難しい。推定可能，検査で改善可能)
            self.add(self.mtex_event_prob_h, self.txt_event_prob_h[0])

            # P(\lnot H): 実際に病気でない確率。H の補集合，P(H) がわかればわかる
            self.add(self.mtex_event_prob_not_h, self.txt_event_prob_not_h[0])

            # P(E|H): 実際に病気の時に検査+ の確率: 検査キットの性能, (測定可能，既知)
            self.add(self.mtex_event_prob_e_b_h, self.txt_event_prob_e_b_h[0])

            # P(E|\lnot H): 実際に病気でない時に検査+ の確率: 検査キットの性能 (測定可能，既知)
            self.add(self.mtex_event_prob_e_b_not_h, self.txt_event_prob_e_b_not_h[0])

            self.wait(self.time_wait)

            self.remove(self.txt_event_prob_h_b_e[0],
                        self.txt_event_prob_h[0],
                        self.txt_event_prob_not_h[0],
                        self.txt_event_prob_e_b_h[0],
                        self.txt_event_prob_e_b_not_h[0])
            self.add(self.txt_event_prob_h_b_e[1],
                     self.txt_event_prob_h[1],
                     self.txt_event_prob_not_h[1],
                     self.txt_event_prob_e_b_h[1],
                     self.txt_event_prob_e_b_not_h[1])
            self.wait(self.time_wait)

            self.add(self.txt_event_prob_h_b_e[2],
                     self.txt_event_prob_h[2],
                     self.txt_event_prob_not_h[2],
                     self.txt_event_prob_e_b_h[2],
                     self.txt_event_prob_e_b_not_h[2])


        # P(H|E): 検査+ の時に実際に病気である確率。(不明，知りたいこと)
        wlist = [self.mtex_bayes_full[0]]
        self.copy_move_term_explain(wlist,
                                    self.mtex_event_prob_h_b_e, self.txt_event_prob_h_b_e)
        self.wait(self.time_wait)

        # P(H): 実際に病気である確率。(難しい。推定可能，検査で改善可能)
        wlist = [self.mtex_bayes_full[2], self.mtex_bayes_full[5]]
        self.copy_move_term_explain(wlist,
                                    self.mtex_event_prob_h, self.txt_event_prob_h)
        self.wait(self.time_wait)

        # P(\lnot H): 実際に病気でない確率。H の補集合，P(H) がわかればわかる
        wlist = [self.mtex_bayes_full[8]]
        self.copy_move_term_explain(wlist,
                                    self.mtex_event_prob_not_h, self.txt_event_prob_not_h)
        self.wait(self.time_wait)

        # P(E|H): 実際に病気の時に検査+ の確率: 検査キットの性能, (測定可能，既知)
        wlist = [self.mtex_bayes_full[3], self.mtex_bayes_full[6]]
        self.copy_move_term_explain(wlist,
                                    self.mtex_event_prob_e_b_h, self.txt_event_prob_e_b_h)
        self.wait(self.time_wait)

        # P(E|\lnot H): 実際に病気でない時に検査+ の確率: 検査キットの性能 (測定可能，既知)
        wlist = [self.mtex_bayes_full[9]]
        self.copy_move_term_explain(wlist,
                                    self.mtex_event_prob_e_b_not_h, self.txt_event_prob_e_b_not_h)
        self.wait(self.time_wait)


    def construct(self):
        """Test and Bayes intro
        """
        self.create_bayes_eq()
        self.show_title()
        self.show_bayes()
        self.animate_why()

        self.wait(5)
