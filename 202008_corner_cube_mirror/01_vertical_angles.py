# -*- coding: utf-8; -*-
#
# Vertical angle explanation animation part 01
#    * What is vertical angle?
#    * What is the construction?
#    * Which angles are the same measure?
#
#    (C) 2019-2020 Hitoshi Yamauchi
#
# References: 3Blue1Brown, Theorem of Beethoven (manim tutorial)
#
# Full resolution
#   python3 -m manim 01_vertical_angles.py VerticalAngle01  --resolution 720,1280 -p --high_quality
# Preview resolution
#   python3 -m manim 01_vertical_angles.py VerticalAngle01  --resolution 360,640 -pl
#   python3 -m manim 01_vertical_angles.py VerticalAngle01  --resolution 360,640 -i --high_quality
# -i as gif


from manimlib.imports import *
import os
# import pyclbr

class VerticalAngle01(Scene):
    """01. A pair of parallel line
    """
    CONFIG={
        "wait_time":    1,
        "line_ab_color":YELLOW,
        "line_cd_color":BLUE,
        "line_length": 5,
        "theta": 0,
        "increment_theta":PI/2,
        "final_theta":PI,
        "radius":0.7,
        "radius_color_1": WHITE,
        "radius_color_2": YELLOW,
        "arc_center_1":   ORIGIN + DOWN,
    }
    def construct(self):

        # language: 0 ... English, 1 ... Deutsch, 2 ... 日本語
        CUR_LANG = 0
        #-- 1. Create 2 lines

        # line ab
        line_ab_start  = ORIGIN
        line_ab_end    = RIGHT * self.line_length
        # The center is moved to origin
        line_ab = Line(line_ab_start, line_ab_end, color=self.line_ab_color).move_to(ORIGIN).shift(UP)

        # line_cd
        line_cd_start  = ORIGIN
        line_cd_end    = RIGHT * self.line_length
        line_cd = Line(line_cd_start, line_cd_end, color=self.line_cd_color).move_to(ORIGIN).shift(DOWN)

        # dots
        dot_a = Dot(ORIGIN, color=YELLOW).next_to(line_ab, LEFT,  buff=0)
        dot_b = Dot(ORIGIN, color=YELLOW).next_to(line_ab, RIGHT, buff=0)
        dot_c = Dot(ORIGIN, color=BLUE).  next_to(line_cd, LEFT,  buff=0)
        dot_d = Dot(ORIGIN, color=BLUE).  next_to(line_cd, RIGHT,  buff=0)

        # label text
        text_a = TexMobject("A", color=YELLOW).next_to(dot_a, LEFT,  buff=MED_SMALL_BUFF)
        text_b = TexMobject("B", color=YELLOW).next_to(dot_b, RIGHT, buff=MED_SMALL_BUFF)
        text_c = TexMobject("C", color=BLUE).  next_to(dot_c, LEFT,  buff=MED_SMALL_BUFF)
        text_d = TexMobject("D", color=BLUE).  next_to(dot_d, RIGHT, buff=MED_SMALL_BUFF)

        # Show the objects
        self.play(*[ShowCreation(obj) for obj in [dot_a, dot_b, dot_c, dot_d, line_ab, line_cd]],
                  *[FadeIn(obj)       for obj in [text_a, text_b, text_c, text_d]])

        #-- 2. Move CD to AB

        # put aside (up) A, B
        #   Note: I don't know why just UP doesn't work. adjusted with 0.5
        self.play(text_a.shift, 0.5 * UP, text_b.shift, 0.5 * UP)

        self.wait(self.wait_time)

        class Glue_obj_side_updater(object):
            """
            Glue two objects for updater
            """
            def __init__(self, main_obj, position = LEFT, buff = MED_SMALL_BUFF):
                """
                param[in] main_obj the main object, follower object will follow this main object via updater
                param[in] position next_to position
                param[in] buf      buffer between main_obj and follower

                """
                self.__main_obj = main_obj
                self.__position = position
                self.__buff     = buff

            def __call__(self, follower):
                """
                add_updater receives a function. This object behaves a function with this method.
                (Note: A closure will work, too.) See Effective python: Item 15, Item 23.

                """
                follower.next_to(self.__main_obj, self.__position, self.__buff)


        dot_a. add_updater(Glue_obj_side_updater(line_ab, position=LEFT,     buff=0))
        text_a_updater = Glue_obj_side_updater(dot_a,   position=LEFT+UP,  buff=MED_SMALL_BUFF)
        text_a.add_updater(text_a_updater)
        dot_b. add_updater(Glue_obj_side_updater(line_ab, position=RIGHT,    buff=0))
        text_b_updater = Glue_obj_side_updater(dot_b,   position=RIGHT+UP, buff=MED_SMALL_BUFF)
        text_b.add_updater(text_b_updater)

        # add all and play line_ab to down.
        self.add(*[line_ab, dot_a, text_a, dot_b, text_b])
        self.play(line_ab.shift, 2 * DOWN)

        self.wait(self.wait_time)

        #-- 3. Add point e and rotate around e
        dot_e  = Dot(ORIGIN + DOWN, color=GREEN)
        text_e = TexMobject("E", color=GREEN).next_to(dot_e, DOWN, buff=MED_SMALL_BUFF)
        self.play(*[ShowCreation(obj) for obj in [dot_e]],
                  *[FadeIn(obj)       for obj in [text_e]])

        self.wait(self.wait_time)

        # --- rotate without angle arc

        class Glue_line_point_edge_rotate_updater(object):
            """
            Glue two objects (a point at the edge of a line) for updater
            """
            def __init__(self, main_line, position = LEFT, where = 0):
                """
                param[in] main_line the main object but a line, follower object will follow this main line object via updater
                param[in] position  next_to position
                param[in] where     0 ... start, 1 ... end

                """
                self.__main_line     = main_line
                self.__position      = position
                self.__where         = where

            def __call__(self, follower):
                """
                add_updater receives a function. This object behaves a function with this method.
                (Note: A closure will work, too.) See Effective python: Item 15, Item 23.

                """
                # delta = self.__value_tracker.get_value() - self.__main_line.get_angle()
                # self.__main_line.rotate(delta)
                if (self.__where == 0):
                    follower.move_to(self.__main_line.get_start() + self.__position)
                elif(self.__where == 1):
                    follower.move_to(self.__main_line.get_end()   + self.__position)
                else:
                    raise AssertionError("whwre should be {0, 1}")


        # FIXME this value update should be also in a group
        theta = ValueTracker(self.theta)
        # Use rotate the line instead of set_angle. (due to no about_point)
        def update_angle(obj):
            delta = theta.get_value() - obj.get_angle()
            obj.rotate(delta)

        line_cd.add_updater(update_angle)

        # dot c update
        dot_c. add_updater(Glue_line_point_edge_rotate_updater(line_cd, position=ORIGIN, where=0))
        dot_d. add_updater(Glue_line_point_edge_rotate_updater(line_cd, position=ORIGIN, where=1))
        text_c.add_updater(Glue_obj_side_updater(dot_c, position=LEFT, buff=MED_SMALL_BUFF))
        text_d.add_updater(Glue_obj_side_updater(dot_d, position=RIGHT, buff=MED_SMALL_BUFF))


        self.play(theta.increment_value,  PI/2 + PI/4) # 3/4 PI
        self.wait(self.wait_time)

        self.play(theta.increment_value, -PI/2)        # 1/4 PI

        # --- Add angle arc 1 (right), an arrow and \angle BED
        arc_angle_bed = Arc(
            start_angle = line_ab.get_angle(),
            angle       = line_cd.get_angle(),
            radius      = self.radius,
            color       = self.radius_color_1,
            arc_center  = self.arc_center_1
        )

        # update function
        def update_arc_1(obj):
            obj.become(
                Arc(
                    start_angle = line_ab.get_angle(),
                    angle       = line_cd.get_angle(),
                    radius      = self.radius,
                    color       = self.radius_color_1,
                    arc_center  = self.arc_center_1
                )
            )

        # Set update function to arc_angle
        arc_angle_bed.add_updater(update_arc_1)

        angle_text_scale = 1.0

        # right arrow and its label angle DEB
        # Vector is ORIGIN to direction
        arrow_vec_1 = Vector(direction = 1.3 * (-2 * RIGHT + -1 * UP), buff=0).\
                                         move_to(arc_angle_bed.get_center() + 1.5 * RIGHT + 0.7 * UP)
        tex_angle_deb = TexMobject( r"\angle DEB").scale(angle_text_scale).shift( 1.0 * UP + 4.4 * RIGHT)

        self.play(ShowCreation(arc_angle_bed), ShowCreation(arrow_vec_1), FadeIn(tex_angle_deb))
        self.wait(self.wait_time)

        # --- Add angle arc 2 (left)
        arc_angle_aec = Arc(
            start_angle = line_ab.get_angle() + PI,
            angle       = line_cd.get_angle(),
            radius      = self.radius,
            color       = self.radius_color_2,
            arc_center  = self.arc_center_1
        )

        # update function
        def update_arc_2(obj):
            obj.become(
                Arc(
                    start_angle = line_ab.get_angle() + PI,
                    angle       = line_cd.get_angle(),
                    radius      = self.radius,
                    color       = self.radius_color_2,
                    arc_center  = self.arc_center_1
                )
            )
        arc_angle_aec.add_updater(update_arc_2)
        self.add(line_ab, line_cd, arc_angle_bed, arc_angle_aec, dot_a, text_a, dot_b, text_b)

        # left arrow and its label angle AEC
        arrow_vec_2 = Vector(direction = 1.3 * (2 * RIGHT + 1 * UP), buff=0).\
                                         move_to(arc_angle_aec.get_center() + -1.5 * RIGHT + -0.75 * UP)
        tex_angle_aec = TexMobject( r"\angle AEC").scale(angle_text_scale).shift(-2.9 * UP - 4.3 * RIGHT)
        self.play(ShowCreation(arc_angle_aec), ShowCreation(arrow_vec_2), FadeIn(tex_angle_aec))

        self.wait(self.wait_time)

        # --- Remove arrows
        self.play(FadeOut(arrow_vec_1), FadeOut(arrow_vec_2))

        # --- move angle deb and angle aec to equal
        eq_deb_aec_h_shift = -3 * RIGHT
        eq_deb_aec_v_shift =  2.0 * UP
        eq_abs_h_offset    =  1.2 * RIGHT
        tex_angle_deb_eq_aec = TexMobject(r"\angle DEB", r"=", r"\angle AEC").scale(angle_text_scale).\
                                                             shift(eq_deb_aec_v_shift + eq_deb_aec_h_shift)
        # Test the '=' position
        # self.play(Write(tex_angle_deb_eq_aec[1]))

        # Doesn't give the position at here
        # print("deb: {0}, aec: {1}".format(tex_angle_deb_eq_aec[0].get_center(), tex_angle_deb_eq_aec[1].get_center()))

        self.play(FadeIn(tex_angle_deb_eq_aec[1]),
                  tex_angle_deb.move_to,  eq_deb_aec_v_shift + eq_deb_aec_h_shift + eq_abs_h_offset,
                  tex_angle_aec.move_to,  eq_deb_aec_v_shift + eq_deb_aec_h_shift - eq_abs_h_offset)

        # --- rotate with angle arc
        self.play(theta.increment_value, -PI/4)         # back to 0
        self.play(theta.increment_value,  PI/2 + PI/3)  # 5/6 PI
        self.play(theta.increment_value, -PI/2)         # 1/3 PI

        # --- Show text
        # When showing Japanese text below, manim/manimlib/constants.py
        # TEX_USE_CTEX = True and update the
        # manimlib/ctex_template.tex
        text_vertical_angle = [
            TextMobject(r"Vertical ", r"angles"),
            TextMobject(r"Scheitelwinkel ßöäü"),
            TextMobject(r"対頂角"),
        ]
        text_vertical_angle[CUR_LANG].scale(1.6).shift(3 * UP - 4 * RIGHT)
        self.play(FadeIn(text_vertical_angle[CUR_LANG]))
        self.wait(self.wait_time)

        self.play(FadeOut(arc_angle_bed), FadeOut(arc_angle_aec))

        arc_angle_aed = Arc(
            start_angle = line_cd.get_angle(),
            angle       = PI - line_cd.get_angle(),
            radius      = self.radius,
            color       = self.radius_color_2,
            arc_center  = self.arc_center_1
        )
        arc_angle_bec = Arc(
            start_angle = line_cd.get_angle() + PI,
            angle       = PI - line_cd.get_angle(),
            radius      = self.radius,
            color       = self.radius_color_2,
            arc_center  = self.arc_center_1
        )

        # arc, angle label (angle aed, angle ceb)
        eq_aed_ceb_h_shift      =  2.0 * RIGHT
        eq_aed_ceb_v_shift      =  2.0 * UP
        eq_aed_ceb_abs_h_offset =  1.2 * RIGHT
        tex_angle_aed_eq_ceb = TexMobject(r"\angle AED", r"=", r"\angle CEB").scale(angle_text_scale).\
                                                             move_to(eq_aed_ceb_v_shift + eq_aed_ceb_h_shift)
        tex_angle_aed = tex_angle_aed_eq_ceb[0].move_to(-1.2 * RIGHT + 0.2 * UP)
        tex_angle_ceb = tex_angle_aed_eq_ceb[2].move_to( 1.0 * RIGHT - 2.0 * UP)

        self.play(ShowCreation(arc_angle_aed),
                  ShowCreation(arc_angle_bec),
                  FadeIn(tex_angle_aed),
                  FadeIn(tex_angle_ceb))

        self.play(FadeIn(tex_angle_aed_eq_ceb[1]),
                  tex_angle_aed.move_to,  eq_aed_ceb_v_shift + eq_aed_ceb_h_shift - eq_aed_ceb_abs_h_offset,
                  tex_angle_ceb.move_to,  eq_aed_ceb_v_shift + eq_aed_ceb_h_shift + eq_aed_ceb_abs_h_offset)


        # remove the arcs
        self.play(FadeOut(arc_angle_aed), FadeOut(arc_angle_bec))

        # Remove the updater to move A and B
        text_a.remove_updater(text_a_updater)
        text_b.remove_updater(text_b_updater)

        self.play(text_a.shift, 0.5 * DOWN, text_b.shift, 0.5 * DOWN)
        self.play(FadeOut(text_c), FadeOut(text_d),
                  FadeOut(dot_c),  FadeOut(dot_d),
                  FadeOut(line_cd))

        self.wait(5)


