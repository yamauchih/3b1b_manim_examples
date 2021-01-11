# -*- coding: utf-8; -*-
#
# disease test and Bayes' theorem
#
# 10_bayse_repeat_01
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
#   python3 -m manim 10_bayse_repeat_01.py BayesRepeat01 --resolution 720,1280 -p --high_quality
# Preview resolution
#   python3 -m manim 10_bayse_repeat_01.py BayesRepeat01 --resolution 360,640 -p -ql
#

from manim import *
import copy, numpy, random
import myutil


class BayesRepeat01(Scene):
# class BayesRepeat01(LinearTransformationScene):
    """Bayes theorem: repeated test
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
        "time_wait":            4.0,
        "is_show_only":         False,

        #-- shared MObjects
        "txt_title_bayes":    None,
        "col_positive":       RED,
        "col_negative":       BLUE,
        "col_true_positive":  RED,
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

        # event footnote scale for eq: equation, txt: text
        "scale_event_eq_f":  1.0,
        "scale_event_txt_f": 0.8,

        # events example 1
        #   H: really ill
        "mtex_event_h": None,
        "txt_event_h":  None,

        # events example 2
        #   E: test positive
        "mtex_event_e": None,
        "txt_event_e":  None,

        # person svg figure (use inkscape)
        "svg_people":      None,
        "col_people":      "#bcbbbd",
        "sick_signs":      None,
        "test_positive_signs": None,

        #-- people size, pos
        "person_size":       0.9,
        "nb_true_positive":    1,
        "nb_false_positive":  10,
        "people_pos_left":   -5.5 * RIGHT + -2.5 * UP,
        "people_delta_dist":  1.1 * RIGHT,
        "label_shift_up":     1.0,
        "nb_person":          None,

        # True positive, False positive labels
        "scale_label_txt": 0.9,

        #--- True positive label
        #  only 1 person
        "label_true_positive": None,
        # pcoord is person's array index coords
        # "true_positive_pcoords": [[22, 11],],

        # False positive label [10]
        "label_false_positive": None,

        # 11 people probability
        # P(H) nominator term, denominator term
        "p_h_nom":   None,
        "p_h_den":   None,

        # P(E|H) nominator term, denominator
        "p_e_h_nom": None,
        "p_e_h_den": None,

        # P(\lnot H)
        "p_not_h_den":   None,

        # P(E|\lnot H)
        "p_e_not_h_den":   None,

        # repeat rhs
        "rhs": None,

        # effect of repeated test
        "text_repeat": None,

    }


    def get_person_position(self, pcoord):
        """get the position of person of (x, y)"""
        return self.pos_people_min + pcoord[0] * self.people_dx * RIGHT + pcoord[1] * self.people_dy * UP

    def get_person_1d_idx(self, pcoord):
        """get the 1D array index of person of index position coordinates
        pcoord = [ix, iy]
        """
        return pcoord[0] + pcoord[1] * self.nb_people_x

    def gen_false_positive(self):
        """generate:
        * 1  true positive index coords
        * 10 false positive index coords
            [[24, 13],
             [2, 8], [32, 15], [25, 9], [30, 11], [37, 6],
             [32, 4], [18, 4], [48, 3], [39, 8], [34, 19], ],
        """
        random.seed(0)
        for i in range(0, 11):
            print("[{0}, {1}], ".format(random.randint(0,50), random.randint(0,20)))


    def create_bayes_eq(self):
        """create all mobjects
        """

        self.txt_title_bayes = Text(r"再検査の効果").scale(self.scale_title_f)
        myutil.critical_point_move_to(self.txt_title_bayes, LEFT + DOWN, ORIGIN + -6.3 * RIGHT + 3.0 * UP)

        # full Bayes form                                  # indices for h,e color (MathTex removes white space))
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

        # 11 people example values
        self.p_h_nom = MathTex(r"P(H)", r"=", r"0.09").scale(self.scale_eq_f).move_to(-2.0 * RIGHT + +0.5 * UP)
        self.p_h_nom[0][2].set_color(self.col_h)
        self.p_h_den = copy.deepcopy(self.p_h_nom)

        # P(E|H) nominator term, denominator
        self.p_e_h_nom = MathTex(r"P(E|H)", r"=", r"1.0").scale(self.scale_eq_f).move_to(+2.5 * RIGHT + +0.5 * UP)
        self.p_e_h_nom[0][2].set_color(self.col_e)
        self.p_e_h_nom[0][4].set_color(self.col_h)
        self.p_e_h_den = copy.deepcopy(self.p_e_h_nom)

        # P(\lnot H)
        self.p_not_h_den = MathTex(r"P(\lnot H)", r"=", r"0.91").scale(self.scale_eq_f).move_to(-2.2 * RIGHT + -0.5 * UP)
        self.p_not_h_den[0][2].set_color(self.col_n)
        self.p_not_h_den[0][3].set_color(self.col_h)
        # P(E|\lnot H)
        self.p_e_not_h_den = MathTex(r"P(E|\lnot H)", r"=", r"0.01").scale(self.scale_eq_f).move_to(+2.5 * RIGHT + -0.5 * UP)
        self.p_e_not_h_den[0][2].set_color(self.col_e)
        self.p_e_not_h_den[0][4].set_color(self.col_n)
        self.p_e_not_h_den[0][5].set_color(self.col_h)

        # # simple from the figure
        # self.p_h_e_simple = MathTex(r"P(H|E)", r"=", r"{1", r"\over", r"11}", r"\approx", r"0.09").\
        #                                            scale(self.scale_eq_f).move_to(0.0 * RIGHT + +2.0 * UP)
        # self.p_h_e_simple[0][2].set_color(self.col_h)
        # self.p_h_e_simple[0][4].set_color(self.col_e)


        # --- Event examples
        # event example H
        self.mtex_event_h = MathTex(r"H").  scale(self.scale_event_eq_f).set_color(
            self.col_h).move_to(0.2 * RIGHT + 3.2 * UP)
        self.txt_event_h = Text(r": 病気").scale(self.scale_event_txt_f).move_to(1.3 * RIGHT + 3.2 * UP)

        # event example E
        self.mtex_event_e = MathTex(r"E").scale(self.scale_event_eq_f).set_color(
            self.col_e).move_to(2.7 * RIGHT + 3.17 * UP)
        self.txt_event_e = Text(r": 検査＋", t2c={r"[3:4]": self.col_positive}).scale(
            self.scale_event_txt_f).move_to(4.0 * RIGHT + 3.17 * UP)

        # 11 people position
        self.nb_people = self.nb_true_positive + self.nb_false_positive

        # create 11 people
        self.svg_people = []
        for i in range(0, self.nb_people):
            pos = self.people_pos_left + i * self.people_delta_dist
            person = SVGMobject("svg/person_silhouette", fill_opacity=1.0).scale(self.person_size).\
                                                                       move_to(pos).set_color(self.col_false_positive)
            self.svg_people.append(person)

        # true positive color
        self.svg_people[0].set_color(self.col_positive)

        # move true positive label
        self.label_true_positive = myutil.LabeledRectangle(Text(r"真＋",
                                                                t2c={"[0:1]": WHITE,
                                                                     "[1:2]": WHITE}).scale(self.scale_label_txt),
                                                           tip_direction=DOWN,
                                                           color=RED, fill_color=RED, fill_opacity=1.0)
        myutil.critical_point_move_to(self.label_true_positive, DOWN, self.people_pos_left).\
            shift(self.person_size * self.label_shift_up * UP)


        self.label_false_positives = []
        for i in range(0, self.nb_false_positive):
            fpos_dst   = self.people_pos_left + (i + self.nb_true_positive) * self.people_delta_dist
            label_fpos = myutil.LabeledRectangle(Text(r"偽＋".format(i), # i is for debug
                                                      t2c={"[0:1]": BLACK,
                                                           "[1:2]": RED,
                                                           "[2:]":  BLACK}).scale(self.scale_label_txt),
                                                 tip_direction=DOWN, color=WHITE, fill_color=WHITE, fill_opacity=1.0)
            self.label_false_positives.append(label_fpos)
            # move false positive label
            myutil.critical_point_move_to(self.label_false_positives[i], DOWN, fpos_dst).\
                shift(self.person_size * self.label_shift_up * UP)
            if (i % 2 == 0):
                self.label_false_positives[i].shift(self.label_shift_up * UP)


        self.rhs = MathTex(r"\approx", r"0.91").scale(self.scale_eq_f).move_to(-2.4 * RIGHT + 2.0 * UP)

        self.text_repeat = Text(r"独立した再検査によって精度向上").scale(self.scale_txt_f).move_to(-1.0 * RIGHT + 1.0 * UP)


    def show_title_people(self):
        """show selected people
        """
        # Already shown
        self.add(self.txt_title_bayes)
        self.add(self.mtex_event_e, self.txt_event_e)
        self.add(self.mtex_event_h, self.txt_event_h)
        self.add(*self.svg_people)
        self.add(self.label_true_positive)
        self.add(*self.label_false_positives)

        self.wait(self.time_wait)

    def animate_retest_reset(self):
        """reset the test"""

        if (self.is_show_only):
            self.remove(self.label_true_positive,
                        *self.label_false_positives)
            for i in range(1, 11):
                self.svg_people[i].set_color(self.col_people)
            self.wait(self.time_wait)
            return

        self.play(FadeOut(self.label_true_positive),
                  *[FadeOut(mobj) for mobj in self.label_false_positives])
        self.wait(self.time_wait)

        apply_ary = []
        for i in range(1, self.nb_people):
            apply_ary.append(ApplyMethod(self.svg_people[i].set_color, self.col_people))
        self.play(*apply_ary)
        self.wait(self.time_wait)


    def animate_bayes_retest_full(self):
        """
        """
        if (self.is_show_only):
            self.add(self.mtex_bayes_full)
            self.wait(self.time_wait)

            self.add(self.p_h_nom,
                     self.p_e_h_nom,
                     self.p_not_h_den,
                     self.p_e_not_h_den)
            self.wait(self.time_wait)

            return

        self.play(FadeIn(self.mtex_bayes_full))
        self.wait(self.time_wait)

        # P(H)
        self.play(FadeIn(self.p_h_nom))
        self.wait(self.time_wait)

        # P(\lnot H)
        self.play(FadeIn(self.p_not_h_den))
        self.wait(self.time_wait)

        # P(E|H)
        self.play(FadeIn(self.p_e_h_nom))
        self.wait(self.time_wait)

        # P(E|\lnot H)
        self.play(FadeIn(self.p_e_not_h_den))
        self.wait(self.time_wait)


    def animate_bayes_retest_substitute(self):
        """substitute all
        """
        if (self.is_show_only):
            # P(H) nominator
            p_h_nom_t = copy.deepcopy(self.p_h_nom[2])
            p_h_nom_t.move_to(self.mtex_bayes_full[2].get_center())
            self.remove(self.mtex_bayes_full[2])
            self.add(p_h_nom_t)

            # P(H) denominator
            p_h_den_t = copy.deepcopy(self.p_h_den[2])
            p_h_den_t.move_to(self.mtex_bayes_full[5].get_center())
            self.remove(self.mtex_bayes_full[5])
            self.add(p_h_den_t)

            # P(\lnot H)
            p_not_h_den_t = copy.deepcopy(self.p_not_h_den[2])
            p_not_h_den_t.move_to(self.mtex_bayes_full[8].get_center())
            self.remove(self.mtex_bayes_full[8])
            self.add(p_not_h_den_t)

            # P(E|H) nominator
            p_e_h_nom_t = copy.deepcopy(self.p_e_h_nom[2])
            p_e_h_nom_t.move_to(self.mtex_bayes_full[3].get_center())
            self.remove(self.mtex_bayes_full[3])
            self.add(p_e_h_nom_t)

            # P(E|H) denominator
            p_e_h_den_t = copy.deepcopy(self.p_e_h_den[2])
            p_e_h_den_t.move_to(self.mtex_bayes_full[6].get_center())
            self.remove(self.mtex_bayes_full[6])
            self.add(p_e_h_den_t)

            # P(E|\lnot H)
            p_e_not_h_den_t = copy.deepcopy(self.p_e_not_h_den[2])
            p_e_not_h_den_t.move_to(self.mtex_bayes_full[9].get_center())
            self.remove(self.mtex_bayes_full[9])
            self.add(p_e_not_h_den_t)
            self.wait(self.time_wait)

            # show rhs
            self.remove(p_h_nom_t,
                        p_h_den_t,
                        p_not_h_den_t,
                        p_e_h_nom_t,
                        p_e_h_den_t,
                        p_e_not_h_den_t,
                        self.mtex_bayes_full[1],  # =
                        self.mtex_bayes_full[4],  # over
                        self.mtex_bayes_full[7]   # + in the denominator
            )
            self.add(self.rhs)
            self.wait(self.time_wait)

            self.remove(self.p_h_nom,
                        self.p_h_den,
                        self.p_not_h_den,
                        self.p_e_h_nom,
                        self.p_e_h_den,
                        self.p_e_not_h_den,)
            self.wait(self.time_wait)

            return


        # # P(H) nominator, denominator
        # p_h_nom_t = copy.deepcopy(self.p_h_nom[2])
        # p_h_den_t = copy.deepcopy(self.p_h_den[2])
        # self.play(FadeOut(self.mtex_bayes_full[2]),
        #           ApplyMethod(p_h_nom_t.move_to, self.mtex_bayes_full[2].get_center()),
        #           FadeOut(self.mtex_bayes_full[5]),
        #           ApplyMethod(p_h_den_t.move_to, self.mtex_bayes_full[5].get_center()))
        # self.wait(self.time_wait)

        # # P(\lnot H)
        # p_not_h_den_t = copy.deepcopy(self.p_not_h_den[2])
        # self.play(FadeOut(self.mtex_bayes_full[8]),
        #           ApplyMethod(p_not_h_den_t.move_to, self.mtex_bayes_full[8].get_center()))
        # self.wait(self.time_wait)

        # # P(E|H) nominator, denominator
        # p_e_h_nom_t = copy.deepcopy(self.p_e_h_nom[2])
        # p_e_h_den_t = copy.deepcopy(self.p_e_h_den[2])
        # self.play(FadeOut(self.mtex_bayes_full[3]),
        #           ApplyMethod(p_e_h_nom_t.move_to, self.mtex_bayes_full[3].get_center()),
        #           FadeOut(self.mtex_bayes_full[6]),
        #           ApplyMethod(p_e_h_den_t.move_to, self.mtex_bayes_full[6].get_center()))
        # self.wait(self.time_wait)

        # # P(E|\lnot H)
        # p_e_not_h_den_t = copy.deepcopy(self.p_e_not_h_den[2])
        # self.play(FadeOut(self.mtex_bayes_full[9]),
        #           ApplyMethod(p_e_not_h_den_t.move_to, self.mtex_bayes_full[9].get_center()))
        # self.wait(self.time_wait)

        # P(H) nominator, denominator
        p_h_nom_t = copy.deepcopy(self.p_h_nom[2])
        p_h_den_t = copy.deepcopy(self.p_h_den[2])
        p_not_h_den_t = copy.deepcopy(self.p_not_h_den[2])
        p_e_h_nom_t = copy.deepcopy(self.p_e_h_nom[2])
        p_e_h_den_t = copy.deepcopy(self.p_e_h_den[2])
        p_e_not_h_den_t = copy.deepcopy(self.p_e_not_h_den[2])
        self.play(FadeOut(self.mtex_bayes_full[2]),
                  ApplyMethod(p_h_nom_t.move_to, self.mtex_bayes_full[2].get_center()),
                  FadeOut(self.mtex_bayes_full[5]),
                  ApplyMethod(p_h_den_t.move_to, self.mtex_bayes_full[5].get_center()),
                  FadeOut(self.mtex_bayes_full[8]),
                  ApplyMethod(p_not_h_den_t.move_to, self.mtex_bayes_full[8].get_center()),
                  FadeOut(self.mtex_bayes_full[3]),
                  ApplyMethod(p_e_h_nom_t.move_to, self.mtex_bayes_full[3].get_center()),
                  FadeOut(self.mtex_bayes_full[6]),
                  ApplyMethod(p_e_h_den_t.move_to, self.mtex_bayes_full[6].get_center()),
                  FadeOut(self.mtex_bayes_full[9]),
                  ApplyMethod(p_e_not_h_den_t.move_to, self.mtex_bayes_full[9].get_center()))
        self.wait(self.time_wait)


        # (/ 0.09 (+ 0.09 (* 0.91 0.01))) 0.91
        # show rhs
        self.play(FadeOut(p_h_nom_t),
                  FadeOut(p_h_den_t),
                  FadeOut(p_not_h_den_t),
                  FadeOut(p_e_h_nom_t),
                  FadeOut(p_e_h_den_t),
                  FadeOut(p_e_not_h_den_t),
                  FadeOut(self.mtex_bayes_full[1]),  # =
                  FadeOut(self.mtex_bayes_full[4]),  # over
                  FadeOut(self.mtex_bayes_full[7])   # + in the denominator
        )
        self.play(FadeInFrom(self.rhs, direction=DOWN))
        self.wait(self.time_wait)


        self.play(FadeOut(self.p_h_nom),
                  FadeOut(self.p_h_den),
                  FadeOut(self.p_not_h_den),
                  FadeOut(self.p_e_h_nom),
                  FadeOut(self.p_e_h_den),
                  FadeOut(self.p_e_not_h_den))
        self.wait(self.time_wait)


    def animate_bayes_retest_rethink(self):
        """re-think the repeat test meaning
        """
        # P(E|\lnot H) = 0.01
        # False positive probability is 1%, apply to 10 people
        if (self.is_show_only):
            # show one false positive
            self.add(self.label_false_positives[0])
            self.svg_people[1].set_color(self.col_false_positive)
            self.wait(self.time_wait)

            self.remove(self.label_false_positives[0])
            self.svg_people[1].set_color(self.col_people)
            self.wait(self.time_wait)

            self.add(self.label_true_positive)
            self.wait(self.time_wait)

            self.add(self.text_repeat)

            return


        self.play(FadeIn(self.text_repeat))
        self.wait(self.time_wait)

        # show one false positive
        self.play(FadeIn(self.label_false_positives[0]),
                  ApplyMethod(self.svg_people[1].set_color, self.col_false_positive))
        self.wait(self.time_wait)

        self.play(FadeOut(self.label_false_positives[0]),
                  ApplyMethod(self.svg_people[1].set_color, self.col_people))
        self.wait(self.time_wait)

        self.play(FadeIn(self.label_true_positive))
        self.wait(self.time_wait)




    def construct(self):
        """More realistic example (example 2)
        """
        # generate random positions for true positive and false positive
        # self.gen_false_positive()

        self.create_bayes_eq()
        self.show_title_people()

        self.animate_retest_reset()
        self.animate_bayes_retest_full()
        self.animate_bayes_retest_substitute()
        self.animate_bayes_retest_rethink()

        self.wait(5)
