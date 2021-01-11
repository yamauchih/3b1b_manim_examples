# -*- coding: utf-8; -*-
#
# disease test and Bayes' theorem
#
# 08_bayse_example_03
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
#   python3 -m manim 09_bayse_example_03.py BayesExample03 --resolution 720,1280 -p --high_quality
# Preview resolution
#   python3 -m manim 09_bayse_example_03.py BayesExample03 --resolution 360,640 -p -ql
#

from manim import *
import copy, numpy, random
import myutil


class BayesExample03(Scene):
# class BayesExample03(LinearTransformationScene):
    """Bayes theorem: example 03: more realistic concrete example (example 2)
    People figure animation
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
        "mtex_event_e":  None,
        "txt_event_e":  None,

        # person svg figure (use inkscape)
        "svg_people":      None,
        "color_people":   "#bcbbbd",
        "sick_signs":      None,
        "test_positive_signs": None,

        #-- people array info
        #  svg person size
        "size_person_1000":    0.08,
        #  array nb_people_x * nb_people_y
        "nb_people_x":    50,
        "nb_people_y":    20,
        #  positions
        "pos_people_min": -6.2 * RIGHT + -3.5 * UP,
        "pos_people_max":  6.2 * RIGHT +  0.5 * UP,

        # each delta
        "people_dx": None,
        "people_dy": None,

        # True positive, False positive labels
        "scale_label_txt": 0.9,

        #--- True positive
        #  only 1 person
        "label_true_positive": None,
        # pcoord is person's array index coords
        "true_positive_pcoords": [[22, 11],],

        # False positive [10]
        "label_false_positive": None,

        # False positive random position by gen_false_positive() and adjusted
        # pcoord is person's array index coords
        "false_positive_pcoords": [[2, 8], [32, 15], [10, 1], [35, 11], [5, 16],
                                   [32, 4], [18, 4], [48, 3], [39, 8],  [41, 15], ],

        # person animation scale factor
        "person_scale_factor": 10.0,

        # 1000 people probability

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

        # P(H|E) simple
        "p_h_e_simple": None,

        # explain
        "mtex_exp": None,
        "text_exp": None,
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

        self.txt_title_bayes = Text(r"具体例 2").scale(self.scale_title_f)
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

        # 1000 people example values
        self.p_h_nom = MathTex(r"0.001").scale(self.scale_eq_f).move_to(self.mtex_bayes_full[2].get_center())
        self.p_h_den = MathTex(r"0.001").scale(self.scale_eq_f).move_to(self.mtex_bayes_full[5].get_center())

        # P(E|H) nominator term, denominator
        self.p_e_h_nom = MathTex(r"1.0").scale(self.scale_eq_f).move_to(self.mtex_bayes_full[3].get_center())
        self.p_e_h_den = MathTex(r"1.0").scale(self.scale_eq_f).move_to(self.mtex_bayes_full[6].get_center())

        # P(\lnot H)
        self.p_not_h_den = MathTex(r"0.999").scale(self.scale_eq_f).move_to(self.mtex_bayes_full[8].get_center())

        # P(E|\lnot H)
        self.p_e_not_h_den = MathTex(r"0.01").scale(self.scale_eq_f).move_to(self.mtex_bayes_full[9].get_center())

        # simple from the figure
        self.p_h_e_simple = MathTex(r"P(H|E)", r"=", r"{1", r"\over", r"11}", r"\approx", r"0.09").\
                                                   scale(self.scale_eq_f).move_to(-3.0 * RIGHT + +2.0 * UP)
        self.p_h_e_simple[0][2].set_color(self.col_h)
        self.p_h_e_simple[0][4].set_color(self.col_e)

        self.mtex_exp = MathTex(r"P(H)", r"\ll", r"P(E|\lnot H)").\
                        scale(self.scale_eq_f).move_to(2.0 * RIGHT + +2.0 * UP)
        self.mtex_exp[0][2].set_color(self.col_h)
        self.mtex_exp[2][2].set_color(self.col_e)
        self.mtex_exp[2][4].set_color(self.col_n)
        self.mtex_exp[2][5].set_color(self.col_h)
        self.text_exp = Text(r"1% 間違える方法で 0.1% を見つける難しさ").scale(self.scale_txt_f).\
                        move_to(0.0 * RIGHT + +1.1 * UP)

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

        # show 1000 people
        self.people_dx      = (self.pos_people_max[0] - self.pos_people_min[0]) / (self.nb_people_x - 1)
        self.people_dy      = (self.pos_people_max[1] - self.pos_people_min[1]) / (self.nb_people_y - 1)
        self.svg_people = []
        for iy in range(0, self.nb_people_y):
            for ix in range(0, self.nb_people_x):
                pos    = self.get_person_position([ix, iy])
                person = SVGMobject("svg/person_silhouette", fill_opacity=1.0).scale(self.size_person_1000).\
                         move_to(pos).set_color(self.color_people)
                self.svg_people.append(person)


        # true positive label
        pos = self.get_person_position(self.true_positive_pcoords[0])
        self.label_true_positive = myutil.LabeledRectangle(Text(r"真＋",
                                                                t2c={"[0:1]": WHITE,
                                                                     "[1:2]": WHITE}).scale(self.scale_label_txt),
                                                           tip_direction=DOWN,
                                                           color=RED, fill_color=RED, fill_opacity=1.0)
        myutil.critical_point_move_to(self.label_true_positive, DOWN, pos).shift(self.size_person_1000 * 0.8 * UP)

        # false positive label
        idx = 0
        self.label_false_positive = []
        for pcoord in self.false_positive_pcoords:
            lr = myutil.LabeledRectangle(Text(r"偽＋".format(idx),
                                              t2c={"[0:1]": BLACK,
                                                   "[1:2]": RED,
                                                   "[2:]":  BLACK}).scale(self.scale_label_txt),
                                         tip_direction=DOWN, color=WHITE, fill_color=WHITE, fill_opacity=1.0)
            pos = self.get_person_position(pcoord)
            myutil.critical_point_move_to(lr, DOWN, pos).shift(self.size_person_1000 * 0.8 * UP)
            self.label_false_positive.append(lr)
            idx += 1


    def show_title(self):
        """より現実的な具体例
        """
        # Already shown
        self.add(self.txt_title_bayes)
        # self.add(self.mtex_bayes_full)
        self.add(self.mtex_event_e, self.txt_event_e)
        self.add(self.mtex_event_h, self.txt_event_h)
        self.wait(self.time_wait)

        # if (self.is_show_only):
        #     self.remove(self.mtex_bayes_full[2], self.mtex_bayes_full[5], self.mtex_bayes_full[3],
        #                 self.mtex_bayes_full[6], self.mtex_bayes_full[8], self.mtex_bayes_full[9])
        #     self.add(self.p_h_nom,  self.p_h_den,     self.p_e_h_nom,
        #              self.p_e_h_den,self.p_not_h_den, self.p_e_not_h_den)
        #     self.wait(self.time_wait)

        #     self.add(self.mtex_bayes_full[2], self.mtex_bayes_full[5], self.mtex_bayes_full[3],
        #              self.mtex_bayes_full[6], self.mtex_bayes_full[8], self.mtex_bayes_full[9])
        #     self.remove(self.p_h_nom,  self.p_h_den,     self.p_e_h_nom,
        #                 self.p_e_h_den,self.p_not_h_den, self.p_e_not_h_den)



    def animate_people_populate(self):
        """1000 people example
        """
        if (self.is_show_only):
            self.add(*[mobj for mobj in self.svg_people])
            return

        # store the destination positions
        pos_dst_people = []
        for person in self.svg_people:
            pos_dst_people.append(person.get_center())

        # deep copy the first person
        first_person = copy.deepcopy(self.svg_people[0])
        first_person.move_to(ORIGIN).scale(1.0 / self.size_person_1000) # original
        self.play(FadeInFrom(first_person, direction=DOWN))
        self.wait(self.time_wait)

        # Move to [0,0] position with transform
        self.play(Transform(first_person, self.svg_people[0]))
        self.wait(self.time_wait)

        # add the bottom row
        first_person_pos = self.svg_people[0].get_center()
        for ix in range(0, self.nb_people_x):
            idx = self.get_person_1d_idx([ix, 0])
            self.svg_people[idx].move_to(first_person_pos)
            self.add(self.svg_people[idx])

        # swap first_person with the people
        self.remove(first_person)
        self.add(self.svg_people[0])

        # First bottom row
        self.play(*[ApplyMethod(self.svg_people[idx].move_to, pos_dst_people[idx]) for idx in range(0, self.nb_people_x)])
        self.wait(self.time_wait)

        # up to 1000 add
        apply_array = []
        for iy in range(1, self.nb_people_y):
            for ix in range(0, self.nb_people_x):
                src_idx = self.get_person_1d_idx([ix,  0])
                dst_idx = self.get_person_1d_idx([ix, iy])
                self.svg_people[dst_idx].move_to(self.svg_people[src_idx].get_center())
                self.add(self.svg_people[dst_idx])
                dst_pos = self.get_person_position([ix, iy])
                apply_array.append(ApplyMethod(self.svg_people[dst_idx].move_to, dst_pos))

        self.play(*apply_array)
        self.wait(self.time_wait)


    def animate_true_positive(self):
        """Show true positive person and probability
        """
        if (self.is_show_only):
            self.add(self.label_true_positive)
            for pcoord in self.true_positive_pcoords:
                one_d_idx = self.get_person_1d_idx(pcoord)
                self.svg_people[one_d_idx].set_color(self.col_positive)
            return

        one_d_idx = self.get_person_1d_idx(self.true_positive_pcoords[0])

        # remove and add to show it in the front (otherwise, draw at back)
        self.remove(self.svg_people[one_d_idx])
        self.add(self.svg_people[one_d_idx])

        self.play(ApplyMethod(self.svg_people[one_d_idx].set_color, self.col_positive))
        self.play(ApplyMethod(self.svg_people[one_d_idx].scale, self.person_scale_factor))
        self.play(ApplyMethod(self.svg_people[one_d_idx].scale, 1 / self.person_scale_factor))
        self.wait(self.time_wait)

        self.play(FadeIn(self.label_true_positive))
        self.wait(self.time_wait)



    def animate_false_positive(self):
        if (self.is_show_only):
            for ix, iy in self.false_positive_pcoords:
                one_d_idx = self.get_person_1d_idx([ix, iy])
                self.svg_people[one_d_idx].set_color(self.col_false_positive)
            self.add(*self.label_false_positive)
            return

        apply_color = []
        apply_scale_1 = []
        apply_scale_2 = []
        for ix, iy in self.false_positive_pcoords:
            one_d_idx = self.get_person_1d_idx([ix, iy])
            # remove and add to draw in front
            self.remove(self.svg_people[one_d_idx])
            self.add(self.svg_people[one_d_idx])

            # keep person the apply list to animate
            apply_color.append(ApplyMethod(self.svg_people[one_d_idx].set_color, self.col_false_positive))
            apply_scale_1.append(ApplyMethod(self.svg_people[one_d_idx].scale, self.person_scale_factor))
            apply_scale_2.append(ApplyMethod(self.svg_people[one_d_idx].scale, 1.0 / self.person_scale_factor))


        self.play(*apply_color)
        self.play(*apply_scale_1)
        self.play(*apply_scale_2)
        self.play(*[FadeIn(mobj) for mobj in self.label_false_positive])
        self.wait(self.time_wait)


    def animate_positive_only(self):
        """Get positive only
        """
        people_negative_xy_idx = []
        for iy in range(0, self.nb_people_y):
            for ix in range(0, self.nb_people_x):
                if ([ix, iy] in self.true_positive_pcoords):
                    # skip true positive
                    continue
                if ([ix, iy] in self.false_positive_pcoords):
                    # skip false positive
                    continue
                people_negative_xy_idx.append([ix, iy])

        people_negative = []
        for pcoord in people_negative_xy_idx:
            people_negative.append(self.svg_people[self.get_person_1d_idx(pcoord)])

        person_size       = 0.9
        nb_person         = 11
        nb_true_positive  =  1
        people_pos_left   = - 5.5 * RIGHT + -2.5 * UP
        people_delta_dist =   1.1 * RIGHT
        label_shift_up    =   1.0

        if (self.is_show_only):
            # remove people negative
            self.remove(*people_negative)

            # move true positive
            tpos_idx = self.get_person_1d_idx(self.true_positive_pcoords[0])
            tpos_dst = people_pos_left
            self.svg_people[tpos_idx].scale(person_size * (1.0 / self.size_person_1000)).move_to(tpos_dst)

            # move true positive label
            myutil.critical_point_move_to(self.label_true_positive, DOWN, tpos_dst).\
                shift(person_size * label_shift_up * UP)

            for i in range(0, len(self.false_positive_pcoords)):
                fpos_idx = self.get_person_1d_idx(self.false_positive_pcoords[i])
                # move false positive
                fpos_dst = people_pos_left + (i + nb_true_positive) * people_delta_dist
                self.svg_people[fpos_idx].scale(person_size * (1.0 / self.size_person_1000)).move_to(fpos_dst)
                # move false positive label
                myutil.critical_point_move_to(self.label_false_positive[i], DOWN, fpos_dst).\
                    shift(person_size * label_shift_up * UP)
                if (i % 2 == 0):
                    self.label_false_positive[i].shift(label_shift_up * UP)


            return

        # remove people negative
        self.play(*[FadeOut(mobj) for mobj in people_negative])

        # move true positive
        tpos_idx = self.get_person_1d_idx(self.true_positive_pcoords[0])
        tpos_dst = people_pos_left

        # make true positive front
        self.remove(self.svg_people[tpos_idx], self.label_true_positive)
        self.add(   self.svg_people[tpos_idx], self.label_true_positive)

        # move true positive label (create a dummy and use for the destination position calculation)
        tpos_label_dst_tmp = copy.deepcopy(self.label_true_positive)
        myutil.critical_point_move_to(tpos_label_dst_tmp, DOWN, tpos_dst).shift(person_size * label_shift_up * UP)

        # create a dummy dstination copy
        tpos_person_dst_tmp = copy.deepcopy(self.svg_people[tpos_idx])
        tpos_person_dst_tmp.scale(person_size * (1.0 / self.size_person_1000)).move_to(tpos_dst)
        self.play(Transform(self.svg_people[tpos_idx],          tpos_person_dst_tmp),
                  ApplyMethod(self.label_true_positive.move_to, tpos_label_dst_tmp.get_center()))
        self.wait(self.time_wait)

        # Same as the true positive people and labels
        fpos_trans = []
        label_move = []
        for i in range(0, len(self.false_positive_pcoords)):
            fpos_idx = self.get_person_1d_idx(self.false_positive_pcoords[i])
            fpos_dst = people_pos_left + (i + nb_true_positive) * people_delta_dist

            ptmp = copy.deepcopy(self.svg_people[fpos_idx])
            ptmp.scale(person_size * (1.0 / self.size_person_1000)).move_to(fpos_dst)
            fpos_trans.append(Transform(self.svg_people[fpos_idx], ptmp))

            ltmp = copy.deepcopy(self.label_false_positive[i])
            myutil.critical_point_move_to(ltmp, DOWN, fpos_dst).shift(person_size * label_shift_up * UP)
            if (i % 2 == 0):
                ltmp.shift(label_shift_up * UP)
            label_move.append(ApplyMethod(self.label_false_positive[i].move_to, ltmp.get_center()))

        self.play(*fpos_trans,
                  *label_move)
        self.wait(self.time_wait)



    def animate_positive_only_eq(self):
        """P(H|E) 11 out of 1
        """
        if (self.is_show_only):
            self.add(self.p_h_e_simple)
            return

        # P(H|E) =
        self.play(FadeIn(self.p_h_e_simple[0]), FadeIn(self.p_h_e_simple[1]))
        self.wait(self.time_wait)

        # 1/11 (In Japanese, one says the denominator first)
        positive_people = []
        tpos_idx = self.get_person_1d_idx(self.true_positive_pcoords[0])
        positive_people.append(self.svg_people[tpos_idx])
        for i in range(0, len(self.false_positive_pcoords)):
            fpos_idx = self.get_person_1d_idx(self.false_positive_pcoords[i])
            positive_people.append(self.svg_people[fpos_idx])

        scale_f = 1.3
        self.play(FadeIn(self.p_h_e_simple[4]),
                  *[ApplyMethod(mobj.scale, scale_f) for mobj in positive_people]),
        self.play(*[ApplyMethod(mobj.scale, 1.0 / scale_f) for mobj in positive_people])
        self.wait(self.time_wait)

        # 1/
        self.play(FadeIn(self.p_h_e_simple[2]),
                  FadeIn(self.p_h_e_simple[3]),
                  ApplyMethod(self.svg_people[tpos_idx].scale, scale_f))
        self.play(ApplyMethod(self.svg_people[tpos_idx].scale, 1.0 / scale_f))
        self.wait(self.time_wait)

        # appropos 0.09
        self.play(FadeIn(self.p_h_e_simple[5]), FadeIn(self.p_h_e_simple[6]))
        self.wait(self.time_wait)



    def animate_one_reason(self):
        """Explain this specific case
        """
        if (self.is_show_only):
            self.add(self.mtex_exp)
            self.add(self.text_exp)
            return

        self.play(FadeIn(self.mtex_exp))
        self.wait(self.time_wait)

        self.play(FadeIn(self.text_exp))
        self.wait(self.time_wait)




    def construct(self):
        """More realistic example (example 2)
        """
        # generate random positions for true positive and false positive
        # self.gen_false_positive()

        self.create_bayes_eq()
        self.show_title()

        self.animate_people_populate()
        self.animate_true_positive()
        self.animate_false_positive()
        self.animate_positive_only()
        self.animate_positive_only_eq()

        self.animate_one_reason()

        self.wait(5)
