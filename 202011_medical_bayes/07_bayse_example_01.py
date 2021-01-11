# -*- coding: utf-8; -*-
#
# disease test and Bayes' theorem
#
# 07_bayse_example_01
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
#   python3 -m manim 07_bayse_example_01.py BayesExample01 --resolution 720,1280 -p --high_quality
# Preview resolution
#   python3 -m manim 07_bayse_example_01.py BayesExample01 --resolution 360,640 -p -ql
#

from manim import *
import copy, numpy
import myutil


class BayesExample01(Scene):
# class BayesExample01(LinearTransformationScene):
    """Bayes theorem: example 01: simple concrete example 1
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
        "txt_title_bayes": None,
        "col_positive":    RED,
        "col_negative":    BLUE,
        "col_true_positive":  RED,
        "col_false_positive": WHITE,
        "col_ill_sign":    WHITE,

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

        # person svg figure (use inkscape)
        "svg_people":      None,
        "color_people":   "#bcbbbd",
        "sick_signs":      None,
        "test_positive_signs": None,

        # annotation key list (in order)
        "annot_key": [ "sick", "no_sick", "true_positive", "false_positive", "total_positive"],

        # anotations: line, brace, math tex, text
        "line_annot":  {},
        "brace_annot": {},
        "mtex_annot":  {},
        "text_annot":  {},
    }

    def create_bayes_eq(self):
        """create all mobjects
        """

        self.txt_title_bayes = Text(r"具体例 1").scale(self.scale_title_f)
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

        self.h_indices = [[0, 2], [2, 2], [3, 4], [5, 2], [6, 4], [8, 2], [8, 3], [9, 4], [9, 5]]
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
        self.mtex_event_h = MathTex(r"H").  scale(self.scale_event_eq_f).set_color(self.col_h).\
                            move_to(0.2 * RIGHT + 3.4 * UP)
        self.txt_event_h = Text(r": 病気").scale(self.scale_event_txt_f).\
                           move_to(1.3 * RIGHT + 3.4 * UP)

        # event example E
        self.mtex_event_e = MathTex(r"E").scale(self.scale_event_eq_f).set_color(self.col_e).\
                            move_to(2.7 * RIGHT + 3.37 * UP)
        self.txt_event_e = Text(r": 検査＋", t2c={r"[3:4]": self.col_positive}).\
                                                  scale(self.scale_event_txt_f).move_to(4.0 * RIGHT + 3.37 * UP)

        # show ten people
        person_size = 0.9
        nb_person   = 10
        nb_sick     = 4
        nb_false_positive = 2
        nb_total_positive = nb_sick + nb_false_positive
        people_pos_left   = - 4.5 * RIGHT + -2.5 * UP
        people_delta_dist =   1.0 * RIGHT
        self.svg_people = []
        for i in range(0, nb_person):
            pos = people_pos_left + i * people_delta_dist
            person = SVGMobject("svg/person_silhouette").scale(person_size).move_to(pos).set_color(self.color_people)
            self.svg_people.append(person)

        # 4 real sick people
        sign_scale = 1.0
        sick_sign = Text(r"病").scale(sign_scale).set_color(self.col_ill_sign)
        self.sick_signs = []
        for i in range(0, nb_sick):
            self.sick_signs.append(copy.deepcopy(sick_sign))

        for i in range(0, nb_sick):
            pos = people_pos_left + (i) * people_delta_dist + -0.3 * RIGHT + -0.15 * UP
            myutil.critical_point_move_to(self.sick_signs[i], LEFT + DOWN, pos)

        # 6 test positive
        test_p_sign = Text(r"＋").scale(sign_scale).set_color(self.col_positive)
        self.test_positive_signs = []
        for i in range(0, nb_total_positive):
            self.test_positive_signs.append(copy.deepcopy(test_p_sign))

        for i in range(0, nb_total_positive):
            pos = people_pos_left + (i) * people_delta_dist + -0.25 * RIGHT + +1.0 * UP
            myutil.critical_point_move_to(self.test_positive_signs[i], LEFT + DOWN, pos)

        # lines for brance anotation
        br_up_off   = 1.6 * UP
        br_beg_off  = 0.5 * LEFT
        br_end_off  = 0.5 * RIGHT
        pos_sick_begin = self.svg_people[0         ].get_center() + br_up_off + br_beg_off
        pos_sick_end   = self.svg_people[nb_sick -1].get_center() + br_up_off + br_end_off

        pos_no_sick_begin = self.svg_people[nb_sick      ].get_center() + br_up_off + br_beg_off
        pos_no_sick_end   = self.svg_people[nb_person - 1].get_center() + br_up_off + br_end_off

        pos_false_pos_begin = self.svg_people[nb_sick              ].get_center() + br_up_off+ br_beg_off
        pos_false_pos_end   = self.svg_people[nb_total_positive - 1].get_center() + br_up_off+ br_end_off

        self.line_annot["sick"]           = Line(pos_sick_begin,      pos_sick_end)
        self.line_annot["no_sick"]        = Line(pos_no_sick_begin,   pos_no_sick_end).  set_color(YELLOW)
        self.line_annot["true_positive"]  = Line(pos_sick_begin,      pos_sick_end).     set_color(RED)
        self.line_annot["false_positive"] = Line(pos_false_pos_begin, pos_false_pos_end).set_color(BLUE)
        self.line_annot["total_positive"] = Line(pos_sick_begin,      pos_false_pos_end).set_color(GREEN)

        for key in self.line_annot:
            self.brace_annot[key] = Brace(self.line_annot[key], UP)

        self.mtex_annot["sick"]           = self.brace_annot["sick"].          get_tex(r"H")
        self.mtex_annot["sick"].set_color(self.col_h)

        self.mtex_annot["no_sick"]        = self.brace_annot["no_sick"].       get_tex(r"\lnot", r"H")
        self.mtex_annot["no_sick"][0].set_color(self.col_n)
        self.mtex_annot["no_sick"][1].set_color(self.col_h)

        self.mtex_annot["true_positive"]  = self.brace_annot["true_positive"]. get_tex(r"E", r"|", r"H")
        self.mtex_annot["true_positive"][0].set_color(self.col_e)
        self.mtex_annot["true_positive"][2].set_color(self.col_h)

        self.mtex_annot["false_positive"] = self.brace_annot["false_positive"].get_tex(r"E", r"|", r"\lnot", r" H")
        self.mtex_annot["false_positive"][0].set_color(self.col_e)
        self.mtex_annot["false_positive"][2].set_color(self.col_n)
        self.mtex_annot["false_positive"][3].set_color(self.col_h)

        self.mtex_annot["total_positive"] = self.brace_annot["total_positive"].get_tex(r"E")
        self.mtex_annot["total_positive"].set_color(self.col_e)

        self.text_annot["sick"]           = Text(r"病気").             scale(self.scale_txt_f)
        self.text_annot["no_sick"]        = Text(r"¬病気",             t2c={"[0:1]":  self.col_n}).       scale(self.scale_txt_f)
        self.text_annot["true_positive"]  = Text(r"病気の時，検査＋",  t2c={"[7:8]":  self.col_positive}).scale(self.scale_txt_f)
        self.text_annot["false_positive"] = Text(r"¬病気の時，検査＋", t2c={"[0:1]":  self.col_n,
                                                                             "[8:9]": self.col_positive}).scale(self.scale_txt_f)
        self.text_annot["total_positive"] = Text(r"検査＋",            t2c={"[2:3]":  self.col_positive}).scale(self.scale_txt_f)

        # copy the math tex position to text
        for key in self.annot_key:
            self.text_annot[key].move_to(self.mtex_annot[key].get_center())


    def show_title(self):
        """架空の具体例 1
        """
        # Already shown
        if (self.is_show_only):
            self.add(self.txt_title_bayes)
            self.add(self.mtex_bayes_full)
            self.add(self.mtex_event_e, self.txt_event_e)
            self.add(self.mtex_event_h, self.txt_event_h)
            return

        self.play(FadeIn(self.txt_title_bayes))
        self.wait(self.time_wait)

        self.play(FadeIn(self.mtex_bayes_full),
                  FadeIn(self.mtex_event_e), FadeIn(self.txt_event_e),
                  FadeIn(self.mtex_event_h), FadeIn(self.txt_event_h))
        self.wait(self.time_wait)


    def animate_people(self):
        """10 people example
        """
        if (self.is_show_only):
            self.add(*[mobj for mobj in self.svg_people],
                     *[mobj for mobj in self.sick_signs],
                     *[mobj for mobj in self.test_positive_signs],
                     )
            return

        # There are 10 people

        # store destination positions
        pos_dst_svg_people = []
        for person in self.svg_people:
            pos_dst_svg_people.append(person.get_center())

        # set start position
        pos_src = self.svg_people[0].get_center()
        for person in self.svg_people:
            person.move_to(pos_src)
            self.add(person)
        # Show people from left: appear and slide
        self.play(*[ApplyMethod(self.svg_people[i].move_to, pos_dst_svg_people[i]) for i in range(0,10)])
        self.wait(self.time_wait)

        # 4 people are sick (true posive)
        self.play(*[ApplyMethod(self.svg_people[i].set_color, self.col_true_positive) for i in range(0,4)],
                  *[FadeInFrom(mobj, DOWN) for mobj in self.sick_signs])
        self.wait(self.time_wait)

        # P(E|H) = 1 (no false negative)
        self.play(*[FadeInFrom(self.test_positive_signs[i], DOWN) for i in range(0,4)])
        self.wait(self.time_wait)

        # P(E|\lnot H) = 1/3 (false positive)
        self.play(*[FadeInFrom(self.test_positive_signs[i], DOWN) for i in range(4,6)],
                  *[ApplyMethod(self.svg_people[i].set_color, self.col_false_positive) for i in range(4,6)])
        self.wait(self.time_wait)


    def animate_eq(self):
        """sibstitute right hand side
        """
        if (self.is_show_only):
            # first add [0]
            self.add(self.line_annot ["sick"],
                     self.brace_annot["sick"],
                     self.mtex_annot ["sick"])
            self.wait(1)

            # loop [1,n-1]
            remove_add_key = []
            for i in range(1, len(self.annot_key)):
                remove_add_key.append([self.annot_key[i-1], self.annot_key[i]])

            for [rmkey, addkey] in remove_add_key:
                self.remove(self.line_annot[rmkey],
                            self.brace_annot[rmkey],
                            self.mtex_annot[rmkey])
                self.add(self.line_annot[addkey],
                         self.brace_annot[addkey],
                         self.mtex_annot[addkey])
                self.wait(1)

            # last remove [n]
            self.remove(self.line_annot ["total_positive"],
                        self.brace_annot["total_positive"],
                        self.mtex_annot ["total_positive"])


        # for fraction computation
        numerator_offset   =  0.25 * UP
        denominator_offset = -0.25 * UP

        # P(H) = 4/10
        ph_val_1 = None
        ph_val_2 = None
        if (self.is_show_only):
            # MathTex([0][0]...[0][k], [1][0]...[1][k], ...) ph_val_1, ph_val_2
            ph_val_1 = MathTex(r"4", r"\over", r"10").move_to(self.mtex_bayes_full[2].get_center() + numerator_offset)
            ph_val_2 = MathTex(r"4", r"\over", r"10").move_to(self.mtex_bayes_full[5].get_center() + denominator_offset)
            self.remove(self.mtex_bayes_full[2],
                        self.mtex_bayes_full[5])
            self.add(ph_val_1,
                     ph_val_2)
        else:
            self.play(ShowCreation(self.brace_annot["sick"]),
                      FadeIn(      self.text_annot["sick"]))
            self.wait(self.time_wait)

            self.play(FadeOut(self.text_annot["sick"]),
                      FadeIn( self.mtex_annot["sick"]))
            self.wait(self.time_wait)

            ph = MathTex(r"P(", r"H", r")=", r"{4 \over 10}").move_to(self.mtex_annot["sick"].get_center())
            ph[1].set_color(self.col_h)

            self.play(FadeOut(self.mtex_annot["sick"]),
                      FadeIn (ph))
            self.wait(self.time_wait)
            ph_val_1 = MathTex(r"4", r"\over", r"10").move_to(ph[3].get_center())
            ph_val_2 = MathTex(r"4", r"\over", r"10").move_to(ph[3].get_center())

            self.play(ApplyMethod(ph_val_1.move_to, self.mtex_bayes_full[2].get_center() + numerator_offset),
                      FadeOut(self.mtex_bayes_full[2]),
                      ApplyMethod(ph_val_2.move_to, self.mtex_bayes_full[5].get_center() + denominator_offset),
                      FadeOut(self.mtex_bayes_full[5]),
            )
            self.wait(self.time_wait)
            self.play(FadeOut(ph),
                      FadeOut(self.brace_annot["sick"]))
            self.wait(self.time_wait)


        # P(\lnot H) = 6/10
        p_n_h_val = None
        if (self.is_show_only):
            p_n_h_val = MathTex(r"{6 \over 10}").move_to(self.mtex_bayes_full[8].get_center() + denominator_offset)[0]
            self.remove(self.mtex_bayes_full[8])
            self.add(p_n_h_val)
        else:
            # transwork = self.text_annot["no_sick"]
            self.play(ShowCreation(self.brace_annot["no_sick"]),
                      FadeIn(      self.text_annot["no_sick"]))
            self.wait(self.time_wait)

            self.play(FadeOut(self.text_annot["no_sick"]),
                      FadeIn( self.mtex_annot["no_sick"]))
            self.wait(self.time_wait)

            p_n_h = MathTex(r"P(", r"\lnot H", r")=", r"{6 \over 10}").move_to(self.mtex_annot["no_sick"].get_center())
            p_n_h[1][0].set_color(self.col_n)
            p_n_h[1][1].set_color(self.col_h)

            self.play(FadeOut(self.mtex_annot["no_sick"]),
                      FadeIn(p_n_h))
            self.wait(self.time_wait)
            p_n_h_val = copy.deepcopy(p_n_h[3])

            self.play(ApplyMethod(p_n_h_val.move_to, self.mtex_bayes_full[8].get_center() + denominator_offset),
                      FadeOut(self.mtex_bayes_full[8]))
            self.wait(self.time_wait)

            self.play(FadeOut(p_n_h),
                      FadeOut(self.brace_annot["no_sick"]))
            self.wait(self.time_wait)


        # P(E|H) = 1
        p_t_p_val_1 = None
        p_t_p_val_2 = None
        if (self.is_show_only):
            # [0] dereference for later consistency use
            p_t_p_val_1 = MathTex(r"{4 \over 4}").move_to(self.mtex_bayes_full[3].get_center() + numerator_offset)  [0]
            p_t_p_val_2 = MathTex(r"{4 \over 4}").move_to(self.mtex_bayes_full[6].get_center() + denominator_offset)[0]
            self.remove(self.mtex_bayes_full[3],
                        self.mtex_bayes_full[6])
            self.add(p_t_p_val_1,
                     p_t_p_val_2)
        else:
            self.play(ShowCreation(self.brace_annot["true_positive"]),
                      FadeIn(      self.text_annot["true_positive"]))
            self.wait(self.time_wait)

            self.play(FadeOut(self.text_annot["true_positive"]),
                      FadeIn (self.mtex_annot["true_positive"]))
            self.wait(self.time_wait)

            p_t_p = MathTex(r"P(", r"E", r"|", r"H", r")=", r"{4 \over 4}").move_to(self.text_annot["true_positive"].get_center())
            p_t_p[1].set_color(self.col_e)
            p_t_p[3].set_color(self.col_h)

            self.play(FadeOut(self.mtex_annot["true_positive"]),
                      FadeIn(p_t_p))
            self.wait(self.time_wait)

            p_t_p_val_1 = copy.deepcopy(p_t_p[5])  # copy 4/4, de-reffered the 1st level
            p_t_p_val_2 = copy.deepcopy(p_t_p[5])  # copy 4/4, de-reffered the 1st level

            self.play(ApplyMethod(p_t_p_val_1.move_to, self.mtex_bayes_full[3].get_center() + numerator_offset),
                      FadeOut(self.mtex_bayes_full[3]),
                      ApplyMethod(p_t_p_val_2.move_to, self.mtex_bayes_full[6].get_center() + denominator_offset),
                      FadeOut(self.mtex_bayes_full[6]))
            self.wait(self.time_wait)

            self.play(FadeOut(p_t_p),
                      FadeOut(self.brace_annot["true_positive"]))
            self.wait(self.time_wait)

        # P(E|\lnot H) = 2/6
        p_f_p_val = None
        if (self.is_show_only):
            p_f_p_val = MathTex(r"{2 \over 6}").move_to(self.mtex_bayes_full[9].get_center() + denominator_offset)
            self.remove(self.mtex_bayes_full[9])
            self.add(p_f_p_val)
        else:
            # transwork = self.text_annot["false_positive"]
            self.play(ShowCreation(self.brace_annot["false_positive"]),
                      FadeIn(self.text_annot["false_positive"]))
            self.wait(self.time_wait)

            self.play(FadeOut(self.text_annot["false_positive"]),
                      FadeIn (self.mtex_annot["false_positive"]))
            self.wait(self.time_wait)

            p_f_p = MathTex(r"P(", r"E", r"|", r"\lnot H", r")=", r"{2 \over 6}").\
                                                                move_to(self.text_annot["false_positive"].get_center())
            p_f_p[1].set_color(self.col_e)
            p_f_p[3][0].set_color(self.col_n)
            p_f_p[3][1].set_color(self.col_h)

            self.play(FadeOut(self.mtex_annot["false_positive"]),
                      FadeIn (p_f_p))
            self.wait(self.time_wait)

            p_f_p_val = copy.deepcopy(p_f_p[5]) # copy 2/6
            self.play(ApplyMethod(p_f_p_val.move_to, self.mtex_bayes_full[9].get_center() + denominator_offset),
                      FadeOut(self.mtex_bayes_full[9]))
            self.wait(self.time_wait)

            self.play(FadeOut(p_f_p),
                      FadeOut(self.brace_annot["false_positive"]))
            self.wait(self.time_wait)

        # simplify rhs
        # 4/4 -> 1 -> ''
        to_one_1 = MathTex(r"1").move_to(p_t_p_val_1.get_center())
        to_one_2 = MathTex(r"1").move_to(p_t_p_val_2.get_center())
        if (self.is_show_only):
            # self.add(   to_one_1,    to_one_2)
            self.remove(p_t_p_val_1, p_t_p_val_2)
        else:
            # cross 4/4
            crosses = [myutil.CrossMobj(p_t_p_val_1[0]), myutil.CrossMobj(p_t_p_val_1[2]),
                       myutil.CrossMobj(p_t_p_val_2[0]), myutil.CrossMobj(p_t_p_val_2[2]) ]
            self.play(*[FadeIn(mobj) for mobj in crosses])
            self.wait(self.time_wait)

            self.play(*[FadeOut(mobj) for mobj in crosses],
                      FadeOut(p_t_p_val_1), FadeIn(to_one_1),
                      FadeOut(p_t_p_val_2), FadeIn(to_one_2))
            self.wait(self.time_wait)

            self.play(ApplyMethod(to_one_1.move_to, ph_val_1.get_center() + 0.5 * RIGHT),
                      ApplyMethod(to_one_2.move_to, ph_val_2.get_center() + 0.5 * RIGHT))
            self.play(FadeOut(to_one_1),
                      FadeOut(to_one_2))
            self.wait(self.time_wait)



        # 6/10 (p_f_p_val) * 2/6 (p_n_h_val) ->  2/10
        six_over_10 = MathTex(r"6", r"\over ",r"10").move_to(self.mtex_bayes_full[7].get_center() + denominator_offset)
        if (self.is_show_only):
            self.remove(p_f_p_val, p_n_h_val, ph_val_2, self.mtex_bayes_full[7])
            self.add(six_over_10)
        else:
            self.play(ApplyMethod(p_f_p_val.move_to, p_n_h_val.get_center() + 0.5 * RIGHT))
            self.wait(self.time_wait)

            # cross {6}/10 2/{6}
            crosses = [myutil.CrossMobj(p_f_p_val[2]), myutil.CrossMobj(p_n_h_val[0])]
            self.play(*[FadeIn(mobj) for mobj in crosses])
            self.wait(self.time_wait)

            two_over_10 = MathTex(r"2 \over 10").move_to(p_n_h_val.get_center())
            self.play(*[FadeOut(mobj) for mobj in crosses],
                      FadeOut(p_f_p_val),
                      FadeOut(p_n_h_val),
                      FadeIn(two_over_10))
            self.wait(self.time_wait)

            # 4/10, 2/10 approach to '+' (self.mtex_bayes_full[7])
            pos_denom_plus_org = self.mtex_bayes_full[7].get_center()
            self.play(ApplyMethod(ph_val_2.   move_to, pos_denom_plus_org + denominator_offset + -0.45 * RIGHT),
                      ApplyMethod(two_over_10.move_to, pos_denom_plus_org + denominator_offset + +0.45 * RIGHT),
                      ApplyMethod(self.mtex_bayes_full[7].shift, denominator_offset))
            self.wait(self.time_wait)

            # 4/10 + 2/10 -> 6/10
            self.play(FadeOut(self.mtex_bayes_full[7]),
                      FadeIn(six_over_10),
                      FadeOut(ph_val_2),
                      FadeOut(two_over_10))
            self.wait(self.time_wait)

        # 4/10 / 6/10 -> cross -> 4/6
        crosses = [myutil.CrossMobj(six_over_10[2]), myutil.CrossMobj(ph_val_1[2])]
        self.play(*[FadeIn(mobj) for mobj in crosses])
        self.wait(self.time_wait)

        # - (self.mtex_bayes_full[4]) -> 4/6
        rhs = MathTex(r"4 \over 6").move_to(self.mtex_bayes_full[4].get_center())

        self.play(*[FadeOut(mobj) for mobj in crosses],
                  FadeOut(ph_val_1),     # num.   4/10
                  FadeOut(six_over_10),  # denom. 6/10
                  FadeOut(self.mtex_bayes_full[4]), # \over
                  FadeIn(rhs))
        self.wait(self.time_wait)

        # - align 4/6 to '='
        self.play(ApplyMethod(rhs.move_to, self.mtex_bayes_full[1].get_center() + 0.55 * RIGHT))
        self.wait(self.time_wait)


    def animate_check(self):
        """check lhs and rhs
        """
        # lhs
        # Positive 6, real ill 4 -> 4/6

        dest_4_6 = MathTex(r"4", r"\over", r"6").move_to(self.mtex_bayes_full[0].get_center() + 0.6 * RIGHT)

        # remove P(H|E) add a bar
        self.play(FadeOut(self.mtex_bayes_full[0]),
                  FadeIn(dest_4_6[1]))
        self.wait(self.time_wait)


        # show brace and E
        total_pos_copy = copy.deepcopy(self.mtex_annot["total_positive"])
        self.play(ShowCreation(self.brace_annot["total_positive"]),
                  FadeIn(total_pos_copy))
        self.wait(self.time_wait)

        # E -> 6
        self.play(Transform(total_pos_copy, MathTex(r"6").move_to(total_pos_copy.get_center())))
        self.wait(self.time_wait)

        # 6 to position
        self.play(ApplyMethod(total_pos_copy.move_to, dest_4_6[2].get_center()))
        self.play(FadeOut(self.brace_annot["total_positive"]))
        self.wait(self.time_wait)

        # show brace and H
        sick_pos_copy = copy.deepcopy(self.mtex_annot["sick"])
        self.play(ShowCreation(self.brace_annot["sick"]),
                  FadeIn(sick_pos_copy))
        self.wait(self.time_wait)

        # H -> 4
        self.play(Transform(sick_pos_copy, MathTex(r"4").move_to(sick_pos_copy.get_center())))
        self.wait(self.time_wait)

        # 4 to position
        self.play(ApplyMethod(sick_pos_copy.move_to, dest_4_6[0].get_center()))
        self.play(FadeOut(self.brace_annot["sick"]))
        self.wait(self.time_wait)


    def construct(self):
        """Test and Bayes intro
        """

        self.create_bayes_eq()
        self.show_title()

        self.animate_people()
        self.animate_eq()
        self.animate_check()

        self.wait(5)
