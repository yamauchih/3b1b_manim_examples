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
#   python3 -m manim 05_bayse_event_example_01.py BayesEventExample01 --resolution 720,1280 -p --high_quality
# Preview resolution
#   python3 -m manim 05_bayse_event_example_01.py BayesEventExample01 --resolution 360,640 -p -ql
#

from manim import *
import copy, numpy
import myutil

class BayesEventExample01(Scene):
# class BayesEventExample01(LinearTransformationScene):
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
        "time_wait":            2,
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
        "mtex_bayes_simple": None,
        "mtex_bayes_full":   None,
        "col_h":             YELLOW,
        "col_e":             BLUE_B,
        "col_n":             RED,
        "h_indices":         None,
        "e_indices":         None,
        "n_indices":         None,

        # events example 1
        #   H: really ill
        "mtex_event_h":  None,
        "txt_event_h":   None,

        # events example 2
        #   E: test positive
        "mtex_event_e":  None,
        "txt_event_e":   None,

        # events example 3
        #   H|E: when e, H
        "mtex_event_h_b_e":  None,
        "txt_event_h_b_e":   None,

        # events example 4
        #   P(H|E): P(when e, H)
        "mtex_event_prob_h_b_e": None,
        "txt_event_prob_h_b_e":  None,

        # events example 5
        #   P(H)
        "mtex_event_prob_h":  None,
        "txt_event_prob_h":   None,

        # events example 6
        #   P(E|H)
        "mtex_event_prob_e_b_h": None,
        "txt_event_prob_e_b_h":  None,

        # events example 7
        #   P(E)
        "mtex_event_prob_e": None,
        "txt_event_prob_e":  None,

        # Example event explanation line
        "pos_line_3": None,
        "pos_line_4": None,

        #---------
        # conditional notation
        # "mtex_cond_eq":    None,
        # "txt_cond_exp_1":  None,
        # "txt_cond_exp_2":  None,

        # probability notation
        # "tex_prob_eq":     None,
        # "txt_prob_exp":    None,

        # E's description (検査結果+)
        # "e_desc":          None,

        # H's description (病気+)
        # "h_desc":          None,

        # person svg figure (use inkscape)
        # "svg_people":      None,
        # "color_people":   "#bcbbbd",
        # "sick_signs":      None,
        # "test_positive_signs": None,

        # "tex_test": None,
    }

    def create_bayes_eq(self):
        """
        """
        self.txt_title_bayes = Text(r"ベイズの定理").scale(self.scale_title_f)
        myutil.critical_point_move_to(self.txt_title_bayes, LEFT + DOWN, ORIGIN + -6.3 * RIGHT + 3.0 * UP)

        # simple Bayes form (3b1b form, cond later)  # indices for h,e color
        self.mtex_bayes_simple = MathTex(r"P(H|E)",   # [0] e [0,4]  h [0,2]
                                         r"={",       # [1]
                                         r"{P(H)",    # [2]         h [2,2]
                                         r"P(E|H)}",  # [3] e [3,2], h [3,4]
                                         r"\over",    # [4]
                                         r"{P(E)}",   # [5] e [5,2]
                                         r"}",        # [6]
        ).scale(self.scale_eq_f)
        myutil.critical_point_move_to(self.mtex_bayes_simple, LEFT + DOWN, ORIGIN + -5.0 * RIGHT + 1.4 * UP)

        self.h_indices = [[0, 2], [2, 2], [3, 4]]
        for [i,j] in self.h_indices:
            self.mtex_bayes_simple[i][j].set_color(self.col_h)
        self.e_indices = [[0, 4], [3, 2], [5, 2]]
        for [i,j] in self.e_indices:
            self.mtex_bayes_simple[i][j].set_color(self.col_e)

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
        var_buff = 0.2
        self.mtex_event_h = MathTex(r"H").scale(self.scale_eq_f).set_color(self.col_h)
        self.txt_event_h  = Text(r": 病気").scale(self.scale_txt_f)
        myutil.critical_point_move_to(self.mtex_event_h, RIGHT + DOWN, ORIGIN + -4.0 * RIGHT +  0.2 * UP)
        self.txt_event_h.next_to(self.mtex_event_h, buff=var_buff)

        # event example E
        self.mtex_event_e = MathTex(r"E").scale(self.scale_eq_f).set_color(self.col_e)
        self.txt_event_e  = Text(r": 検査＋", t2c={r"[3:4]": self.col_positive}).scale(self.scale_txt_f)
        myutil.critical_point_move_to(self.mtex_event_e, RIGHT + DOWN, ORIGIN + -4.0 * RIGHT + -0.6 * UP)
        self.txt_event_e.next_to(self.mtex_event_e, buff=var_buff)

        # event example H|E
        self.pos_line_3 = ORIGIN + -4.0 * RIGHT +  -1.5 * UP
        self.pos_line_4 = ORIGIN + -4.0 * RIGHT +  -2.3 * UP
        self.mtex_event_h_b_e = MathTex(r"H", r"|", r"E").scale(self.scale_eq_f)
        self.mtex_event_h_b_e[0].set_color(self.col_h)
        self.mtex_event_h_b_e[2].set_color(self.col_e)
        self.txt_event_h_b_e = Text(r": E (検査＋) の時に H (病気)",
                                    t2c={r"[1:2]":   self.col_e,
                                         r"[5:6]": self.col_positive,
                                         r"[10:11]": self.col_h,}).scale(self.scale_txt_f)
        myutil.critical_point_move_to(self.mtex_event_h_b_e, RIGHT + DOWN, self.pos_line_3)
        self.txt_event_h_b_e.next_to(self.mtex_event_h_b_e, buff=var_buff)
        # event example P(H|E)

        self.mtex_event_prob_h_b_e = MathTex(r"P(", r"H", r"|", r"E", r")").scale(self.scale_eq_f)
        self.mtex_event_prob_h_b_e[1].set_color(self.col_h)
        self.mtex_event_prob_h_b_e[3].set_color(self.col_e)
        self.txt_event_prob_h_b_e = Text(r": E (検査＋) の時に H (病気) の確率",
                                         t2c={r"[1:2]":   self.col_e,
                                              r"[5:6]": self.col_positive,
                                              r"[10:11]": self.col_h}).scale(self.scale_txt_f)
        myutil.critical_point_move_to(self.mtex_event_prob_h_b_e, RIGHT + DOWN, self.pos_line_4)
        self.txt_event_prob_h_b_e.next_to(self.mtex_event_prob_h_b_e, buff=var_buff)

        # event example 5 P(H)
        self.mtex_event_prob_h = MathTex(r"P(", r"H", r")").scale(self.scale_eq_f)
        self.mtex_event_prob_h[1].set_color(self.col_h)
        self.txt_event_prob_h = Text(r": H (病気) の確率",
                                     t2c={r"[1:2]":   self.col_h} ).scale(self.scale_txt_f)
        myutil.critical_point_move_to(self.mtex_event_prob_h, RIGHT + DOWN, self.pos_line_3)
        self.txt_event_prob_h.next_to(self.mtex_event_prob_h, buff=var_buff)


        # event example 6 P(E|H)
        self.mtex_event_prob_e_b_h = MathTex(r"P(", r"E", r"|", r"H", r")").scale(self.scale_eq_f)
        self.mtex_event_prob_e_b_h[1].set_color(self.col_e)
        self.mtex_event_prob_e_b_h[3].set_color(self.col_h)
        self.txt_event_prob_e_b_h = Text(r": H (病気) の時に，E (検査＋) の確率",
                                         t2c={r"[1:2]": self.col_h,
                                              r"[10:11]": self.col_e,
                                              r"[14:15]": self.col_positive,}).scale(self.scale_txt_f)
        myutil.critical_point_move_to(self.mtex_event_prob_e_b_h, RIGHT + DOWN, self.pos_line_3)
        self.txt_event_prob_e_b_h.next_to(self.mtex_event_prob_e_b_h, buff=var_buff)

        # event example 7 P(E)
        self.mtex_event_prob_e = MathTex(r"P(", r"E", r")").scale(self.scale_eq_f)
        self.mtex_event_prob_e[1].set_color(self.col_e)
        self.txt_event_prob_e = Text(r": E (検査＋) の確率",
                                     t2c={r"[1:2]": self.col_e,
                                          r"[5:6]": self.col_positive,}).scale(self.scale_txt_f)
        myutil.critical_point_move_to(self.mtex_event_prob_e, RIGHT + DOWN, self.pos_line_3)
        self.txt_event_prob_e.next_to(self.mtex_event_prob_e, buff=var_buff)


    def show_title(self):
        """ベイズの定理
        """
        if (self.is_show_only):
            self.add(self.txt_title_bayes)
            return

        self.play(FadeIn(self.txt_title_bayes))
        self.wait(self.time_wait)


    def animate_bayes_simple_full(self):
        """1st show
        """
        if (self.is_show_only):
            self.add(self.mtex_bayes_simple)
            self.add(self.mtex_event_e, self.txt_event_e)
            self.add(self.mtex_event_h, self.txt_event_h)
            self.wait(1)
            return

        # Show equation
        self.play(FadeIn(self.mtex_bayes_simple))
        self.wait(self.time_wait)

        # H: 病気
        self.play(FadeIn(self.mtex_event_h), FadeIn(self.txt_event_h))
        self.wait(self.time_wait)

        # E: 検査 +
        self.play(FadeIn(self.mtex_event_e), FadeIn(self.txt_event_e))
        self.wait(self.time_wait)


    def animate_bayes_simple_lhs(self):
        """Read P(H|E)
        """
        if (self.is_show_only):
            self.add(self.txt_event_h_b_e,
                     self.mtex_event_h_b_e,
                     self.txt_event_prob_h_b_e)
            self.wait(1)
            self.remove(self.txt_event_h_b_e,
                        self.mtex_event_h_b_e,
                        self.txt_event_prob_h_b_e)
            self.wait(1)
            return

        # Move lhs P(H|E)
        phe = copy.deepcopy(self.mtex_bayes_simple[0])   # animation temp phe
        self.add(phe)

        # move P(H|E), simple equation fade out
        self.play(ApplyMethod(phe.move_to, self.mtex_event_prob_h_b_e.get_center()),
                  FadeOut(self.mtex_bayes_simple[0]),
                  FadeOut(self.mtex_bayes_simple[2]),
                  FadeOut(self.mtex_bayes_simple[3]),
                  FadeOut(self.mtex_bayes_simple[5]))
        self.wait(self.time_wait)

        # extract H|E, move to start position at P(H|E)
        h_b_e =  copy.deepcopy(self.mtex_event_h_b_e)    # animation temp h_b_e
        h_b_e.move_to(phe.get_center() + 0.29 * RIGHT)
        self.add(h_b_e)
        self.play(ApplyMethod(h_b_e.move_to, self.mtex_event_h_b_e.get_center()))

        self.add(self.mtex_event_h_b_e)                  # show non temp h_b_e
        self.remove(h_b_e)                              # remove animation temp h_b_e
        self.wait(self.time_wait)

        # explanation H|E
        self.play(FadeIn(self.txt_event_h_b_e))
        self.wait(self.time_wait)

        # explanation P(H|E)
        self.play(FadeIn(self.txt_event_prob_h_b_e))
        self.wait(self.time_wait)

        # move back P(H|E) to the equation
        self.play(ApplyMethod(phe.move_to, self.mtex_bayes_simple[0].get_center()))
        self.add(self.mtex_bayes_simple[0])
        self.remove(phe)                                # animation temp phe))
        self.wait(self.time_wait)

        # fadeout P(H|E) explanation related
        self.play(FadeOut(self.txt_event_h_b_e),
                  FadeOut(self.mtex_event_h_b_e),
                  FadeOut(self.txt_event_prob_h_b_e))
        self.wait(self.time_wait)


    def animate_bayes_simple_rhs(self):
        """P(H)P(E|H) \over P(E)
        """
        if (self.is_show_only):
            self.add(   self.mtex_event_prob_h, self.txt_event_prob_h)
            self.wait(1)
            self.remove(self.mtex_event_prob_h,     self.txt_event_prob_h)
            self.add(   self.mtex_event_prob_e_b_h, self.txt_event_prob_e_b_h)
            self.wait(1)
            self.remove(self.mtex_event_prob_e_b_h, self.txt_event_prob_e_b_h)
            self.wait(1)
            self.add(   self.mtex_event_prob_e, self.txt_event_prob_e)
            self.wait(1)
            self.remove(self.mtex_event_prob_e, self.txt_event_prob_e)
            self.wait(1)
            return

        # P(H)
        dest_pos_h = self.mtex_bayes_simple[2].get_center()
        self.mtex_bayes_simple[2].move_to(self.mtex_event_prob_h.get_center())
        self.play(FadeIn(self.mtex_bayes_simple[2]),
                  FadeIn(self.txt_event_prob_h))
        self.wait(self.time_wait)
        self.play(ApplyMethod(self.mtex_bayes_simple[2].move_to, dest_pos_h))
        self.wait(self.time_wait)
        self.play(FadeOut(self.txt_event_prob_h))
        self.wait(self.time_wait)

        # DELETEME self.mtex_bayes_simple[2].set_color(RED)

        # P(E|H)
        dest_pos_e_b_h = self.mtex_bayes_simple[3].get_center()
        self.mtex_bayes_simple[3].move_to(self.mtex_event_prob_e_b_h.get_center())
        self.play(FadeIn(self.mtex_bayes_simple[3]),
                  FadeIn(self.txt_event_prob_e_b_h))
        self.wait(self.time_wait)
        self.play(ApplyMethod(self.mtex_bayes_simple[3].move_to, dest_pos_e_b_h))
        self.wait(self.time_wait)
        self.play(FadeOut(self.txt_event_prob_e_b_h))
        self.wait(self.time_wait)

        # P(E)
        dest_pos_e = self.mtex_bayes_simple[5].get_center()
        self.mtex_bayes_simple[5].move_to(self.mtex_event_prob_e.get_center())
        self.play(FadeIn(self.mtex_bayes_simple[5]),
                  FadeIn(self.txt_event_prob_e))
        self.wait(self.time_wait)
        self.play(ApplyMethod(self.mtex_bayes_simple[5].move_to, dest_pos_e))
        self.wait(self.time_wait)

        self.play(FadeOut(self.txt_event_prob_e))
        self.wait(self.time_wait)


    def animate_bayes_simple_to_full(self):
        """Transit Bayes simple forma to full form
        """
        if (self.is_show_only):
            self.remove(self.mtex_bayes_simple)
            self.add(   self.mtex_bayes_full)
            self.wait(1)
            return

        # replace with working copy. move P(E) to down
        # Note: self.remove(self.mtex_bayes_simple) does not work, seems objects are implicitly copied.
        # self.remove(self.mtex_bayes_simple[0],
        #             self.mtex_bayes_simple[1],
        #             self.mtex_bayes_simple[2],
        #             self.mtex_bayes_simple[3],
        #             self.mtex_bayes_simple[4],
        #             self.mtex_bayes_simple[5],
        # )

        eq_simple_dest = copy.deepcopy(self.mtex_bayes_simple)
        # self.add(eq_simple_dest)

        # destination: P(E) = P(H)P(E|H) + P(\lnot H)P(E|\lnot H)
        tex_e_full = MathTex(r"P(E)",          # [0] e [0,2]
                             r"=",             # [1]
                             r"P(H)",          # [2]         h [2,2]
                             r"P(E|H)",        # [3] e [3,2] h [3,4]
                             r"+",             # [4]
                             r"P(\lnot H)",    # [5]         h [5,3] n [5, 2]
                             r"P(E|\lnot H)"   # [6] e [6,2] h [6,5] n [6, 4]
        ).scale(self.scale_eq_f)

        h_indices = [[2, 2], [3, 4], [5, 3], [6, 5]]
        for [i,j] in h_indices:
            tex_e_full[i][j].set_color(self.col_h)
        e_indices = [[0, 2], [3, 2], [6, 2]]
        for [i,j] in e_indices:
            tex_e_full[i][j].set_color(self.col_e)
        n_indices = [[5, 2], [6, 4]]
        for [i,j] in n_indices:
            tex_e_full[i][j].set_color(self.col_n)


        # push original position
        pushd_src_pos = eq_simple_dest[5].get_center()

        # get the dest position (based on critical point)
        # Note 1: 'RIGHT + DOWN' of the 0-th element! not 'LEFT + DOWN'
        # Thus re-adjuetment whole by LEFT + DOWN
        # Note 2: myutil.critical_point_move_to(tex[0], ...) creates
        # object copy of tex[0], derefernce by tex failed.
        car_tex_e_full = copy.deepcopy(tex_e_full[0])
        myutil.critical_point_move_to(car_tex_e_full, RIGHT + DOWN, self.pos_line_3)
        pos_ld_car_tex_e_full = car_tex_e_full.get_critical_point(LEFT + DOWN)
        myutil.critical_point_move_to(tex_e_full, LEFT + DOWN, pos_ld_car_tex_e_full)
        pushd_dst_pos = tex_e_full[0].get_center()

        # move to the src
        tex_e_full[0].move_to(pushd_src_pos)

        # denominator P(E) moves to explanation
        self.play(ApplyMethod(tex_e_full[0].move_to, pushd_dst_pos))
        self.wait(self.time_wait)

        # Explain P(E) '= '
        self.play(FadeIn(tex_e_full[1]))
        self.wait(self.time_wait)

        # Explain P(E) = 'P(H)'
        self.play(FadeIn(tex_e_full[2]))
        self.wait(self.time_wait)

        # Explain P(E) = P(H)           'P(\lnot H)'
        self.play(FadeIn(tex_e_full[5]))
        self.wait(self.time_wait)

        # Explain P(E) = P(H)'P(E|H)'     P(\lnot H)
        self.play(FadeIn(tex_e_full[3]))
        self.wait(self.time_wait)

        # Explain P(E) = P(H)P(E|H)     P(\lnot H)'P(E|\lnot H)'
        self.play(FadeIn(tex_e_full[6]))
        self.wait(self.time_wait)

        # Explain P(E) = P(H)P(E|H) '+' P(\lnot H)P(E|\lnot H)
        self.play(FadeIn(tex_e_full[4]))
        self.wait(self.time_wait)

        # update to eq to full, keep denominator empty
        self.add(self.mtex_bayes_full[0],
                 self.mtex_bayes_full[1])
        self.remove(eq_simple_dest[0],
                    eq_simple_dest[1],
                    eq_simple_dest[2],
                    eq_simple_dest[3])
        # these seems implicitly copied
        self.remove(self.mtex_bayes_simple[0],
                    self.mtex_bayes_simple[1],
                    self.mtex_bayes_simple[2],
                    self.mtex_bayes_simple[3],
                    self.mtex_bayes_simple[4])

        # P(H)P(E|H) in eq to move, transform the fraction bar
        pos_src_p_h     = self.mtex_bayes_simple[2].get_center()
        pos_src_p_e_b_h = self.mtex_bayes_simple[3].get_center()
        pos_dst_p_h     = self.mtex_bayes_full[2].  get_center()
        pos_dst_p_e_b_h = self.mtex_bayes_full[3].  get_center()

        self.mtex_bayes_full[2].move_to(pos_src_p_h)
        self.mtex_bayes_full[3].move_to(pos_src_p_e_b_h)
        self.play(ApplyMethod(self.mtex_bayes_full[2].move_to, pos_dst_p_h),
                  ApplyMethod(self.mtex_bayes_full[3].move_to, pos_dst_p_e_b_h),
                  Transform(eq_simple_dest[4], self.mtex_bayes_full[4]))
        self.wait(self.time_wait)

        # move the right hand side of P(E) = P(H)P{E|H) + P(\lnot H)P{E|\lnot H)
        # self.play(FadeOut(self.mtex_bayes_simple[5]))
        self.remove(self.mtex_bayes_simple[5]) # This seems implicitly copied
        self.play(FadeOut(eq_simple_dest[5]))
        self.wait(self.time_wait)

        # partal zip?
        self.play(FadeOut(    tex_e_full[0]),
                  FadeOut(    tex_e_full[1]),
                  ApplyMethod(tex_e_full[2].move_to, self.mtex_bayes_full[5].get_center()),
                  ApplyMethod(tex_e_full[3].move_to, self.mtex_bayes_full[6].get_center()),
                  ApplyMethod(tex_e_full[4].move_to, self.mtex_bayes_full[7].get_center()),
                  ApplyMethod(tex_e_full[5].move_to, self.mtex_bayes_full[8].get_center()),
                  ApplyMethod(tex_e_full[6].move_to, self.mtex_bayes_full[9].get_center()))
        self.wait(self.time_wait)

        # replace work equation to shared full beyes equation
        self.remove(tex_e_full)
        self.add(self.mtex_bayes_full)
        self.wait(self.time_wait)


    def animate_event_annotation(self):
        """Save H: ill, and E: test positive to the upper right
        """
        if (self.is_show_only):
            self.mtex_event_h.scale(1.0 / self.scale_eq_f)
            self.txt_event_h.scale( 0.8 / self.scale_txt_f)
            self.mtex_event_e.scale(1.0 / self.scale_eq_f)
            self.txt_event_e.scale( 0.8 / self.scale_txt_f)
            myutil.critical_point_move_to(self.mtex_event_h, LEFT + DOWN, ORIGIN + 0.0 * RIGHT + 3.0 * UP)
            print(self.mtex_event_h.get_center())
            self.txt_event_h.next_to(self.mtex_event_h)
            print(self.txt_event_h.get_center())

            myutil.critical_point_move_to(self.mtex_event_e, LEFT + DOWN, ORIGIN + 2.5 * RIGHT + 3.0 * UP)
            print(self.mtex_event_e.get_center())
            self.txt_event_e.next_to(self.mtex_event_e)
            print(self.txt_event_e.get_center())
            return

        self.play(ApplyMethod(self.txt_event_h.scale,   1.0 / self.scale_eq_f),
                  ApplyMethod(self.txt_event_h.scale,   0.8 / self.scale_txt_f),
                  ApplyMethod(self.txt_event_e.scale,   1.0 / self.scale_eq_f),
                  ApplyMethod(self.txt_event_e.scale,   0.8 / self.scale_txt_f))
        self.play(ApplyMethod(self.mtex_event_h.move_to, ORIGIN + 0.2 * RIGHT + 3.2  * UP),
                  ApplyMethod(self.txt_event_h.move_to,  ORIGIN + 1.3 * RIGHT + 3.2  * UP),
                  ApplyMethod(self.mtex_event_e.move_to, ORIGIN + 2.7 * RIGHT + 3.17 * UP),
                  ApplyMethod(self.txt_event_e.move_to,  ORIGIN + 4.0 * RIGHT + 3.17 * UP))
        self.wait(self.time_wait)



    def construct(self):
        """Test and Bayes intro
        """

        self.create_bayes_eq()
        self.show_title()
        self.animate_bayes_simple_full()
        self.animate_bayes_simple_lhs()
        self.animate_bayes_simple_rhs()
        self.animate_bayes_simple_to_full()
        self.animate_event_annotation()

        self.wait(5)
