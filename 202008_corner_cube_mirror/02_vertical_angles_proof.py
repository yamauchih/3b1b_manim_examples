# -*- coding: utf-8; -*-

#
# Vertical angle explanation animation part 02
#    * Proof of the mesures of vertical angles are the same
#
#    (C) 2019-2020 Hitoshi Yamauchi
#
# References: 3Blue1Brown, Theorem of Beethoven (manim tutorial)
#
#  cd data/gitdata/manim
#  source manim-venv/bin/activate
#
# Full resolution
#   python3 -m manim 02_vertical_angles_proof.py VerticalAngleProof01 --resolution 720,1280 -p --high_quality
# Preview resolution
#   python3 -m manim 02_vertical_angles_proof.py VerticalAngleProof01 --resolution 360,640 -pl
#   python3 -m manim 02_vertical_angles_proof.py VerticalAngleProof01 --resolution 360,640 -i --high_quality
# -i as gif


from manimlib.imports import *
import os, copy
import pyclbr

class VerticalAngleProof01(Scene):
    """01. A pair of parallel line
    """
    CONFIG={
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

        all_play  = True
        wait_time = 1

        # language: 0 ... English, 1 ... Deutsch, 2 ... 日本語
        CUR_LANG = 0

        #-- 1. Create 2 lines crossed at both center (0, -1)

        # line ab
        line_ab_start  = ORIGIN
        line_ab_end    = RIGHT * self.line_length
        # The center is moved to origin
        line_ab = Line(line_ab_start, line_ab_end, color=self.line_ab_color).move_to(ORIGIN + DOWN)

        # line_cd
        line_cd_start  = ORIGIN
        line_cd_end    = RIGHT * self.line_length
        line_cd = Line(line_cd_start, line_cd_end, color=self.line_cd_color).move_to(ORIGIN + DOWN)

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

        # point e (rotation center)
        dot_e  = Dot(ORIGIN + DOWN, color=GREEN)
        text_e = TexMobject("E", color=GREEN).next_to(dot_e, DOWN, buff=MED_SMALL_BUFF)

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


        dot_a. add_updater(Glue_obj_side_updater(line_ab, position=LEFT,  buff=0))
        text_a.add_updater(Glue_obj_side_updater(dot_a,   position=LEFT,  buff=MED_SMALL_BUFF))
        dot_b. add_updater(Glue_obj_side_updater(line_ab, position=RIGHT, buff=0))
        text_b.add_updater(Glue_obj_side_updater(dot_b,   position=RIGHT, buff=MED_SMALL_BUFF))

        # add all togather
        self.add(*[line_ab, dot_a, text_a, dot_b, text_b])

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
        # Start with PI/4 rotated position
        self.theta = PI/4
        theta = ValueTracker(self.theta)
        # Use rotate the line instead of set_angle. (due to no about_point)
        def update_angle(obj):
            delta = theta.get_value() - obj.get_angle()
            obj.rotate(delta)

        line_cd.add_updater(update_angle)

        # dot C D update
        dot_c. add_updater(Glue_line_point_edge_rotate_updater(line_cd, position=ORIGIN, where=0))
        dot_d. add_updater(Glue_line_point_edge_rotate_updater(line_cd, position=ORIGIN, where=1))
        text_c.add_updater(Glue_obj_side_updater(dot_c, position=LEFT, buff=MED_SMALL_BUFF))
        text_d.add_updater(Glue_obj_side_updater(dot_d, position=RIGHT, buff=MED_SMALL_BUFF))

        # Start with line cd
        if all_play:
            self.play(*[ShowCreation(obj) for obj in [dot_a, dot_b, dot_e, line_ab]],
                      *[FadeIn(obj)       for obj in [text_a, text_b, text_e]])
            self.wait(wait_time)


        # --- Add angle arc 1, 180 degree
        arc_angle_1 = Arc(
            start_angle = line_ab.get_angle(),
            angle       = PI,
            radius      = self.radius,
            color       = self.radius_color_1,
            arc_center  = self.arc_center_1
        )

        # update function
        def update_arc_1(obj):
            obj.become(
                Arc(
                    start_angle = line_ab.get_angle(),
                    angle       = PI,
                    radius      = self.radius,
                    color       = self.radius_color_1,
                    arc_center  = self.arc_center_1
                )
            )

        # Set update function to arc_angle
        arc_angle_1.add_updater(update_arc_1)
        angle_text_scale = 1.0

        # right arrow and its label angle DEB
        # Vector is ORIGIN to direction
        # arrow_vec_1 = Vector(direction = 1.3 * (-2 * RIGHT + -1 * UP), buff=0).\
        #                                  move_to(arc_angle_bed.get_center() + 1.5 * RIGHT + 0.7 * UP)
        tex_angle_180 = TexMobject( r"180^\circ").scale(angle_text_scale).shift(0.3 * UP + 0.0 * RIGHT)

        # Add angle AED 180 degrees
        if all_play:
            self.play(ShowCreation(arc_angle_1), FadeIn(tex_angle_180))
            self.wait(wait_time)

        # Remove angle AED 180 degrees
        if all_play:
            self.play(FadeOut(arc_angle_1), FadeOut(tex_angle_180))
            self.wait(wait_time)



        #--- Add Line CD, Angle 2 (alpha), Move 180 to the left and 180 - alpha
        if all_play:
            self.play(*[ShowCreation(obj) for obj in [dot_c, dot_d, line_cd]],
                      *[FadeIn(obj)       for obj in [text_c, text_d]],)

            self.wait(wait_time)

        # --- Add angle arc alpha
        arc_angle_deb = Arc(
            start_angle = line_ab.get_angle(),
            angle       = line_cd.get_angle(),
            radius      = self.radius,
            color       = RED, # self.radius_color_2,
            arc_center  = self.arc_center_1
        )
        arc_angle_aed = Arc(
            start_angle = line_ab.get_angle() + PI/4,
            angle       = line_ab.get_angle() + 3 * PI/4,
            radius      = self.radius,
            color       = self.radius_color_2,
            arc_center  = self.arc_center_1
        )

        # left arrow and its label angle AEC
        # arrow_vec_2 = Vector(direction = 1.3 * (2 * RIGHT + 1 * UP), buff=0).\
        #                                  move_to(arc_angle_aec.get_center() + -1.5 * RIGHT + -0.75 * UP)
        deb_shift      = -0.5 * UP + 2.0 * RIGHT
        tex_angle_deb       = TexMobject( r"\angle DEB").scale(angle_text_scale).\
                              shift(deb_shift)
        deb_180m_shift = 0.3 * UP + -1.0 * RIGHT
        tex_angle_180_m_deb = TexMobject(r"180^\circ", r"-", r"\angle DEB").scale(angle_text_scale).\
                              shift(deb_180m_shift)

        if all_play:
            self.play(ShowCreation(arc_angle_deb), FadeIn(tex_angle_deb))
            self.wait(wait_time)
            self.play(ShowCreation(arc_angle_aed), FadeIn(tex_angle_180_m_deb))
            self.wait(wait_time)

        # Copy the figure and move left and right. (Shrinking is a bit
        # trickey, since the scale didn't keep the structure)
        geoms_org = {
            "line_ab": line_ab,
            "line_cd": line_cd,
            "dot_a": dot_a,
            "dot_b": dot_b,
            "dot_c": dot_c,
            "dot_d": dot_d,
            "dot_e": dot_e,
            "text_a": text_a,
            "text_b": text_b,
            "text_c": text_c,
            "text_d": text_d,
            "text_e": text_e,
            "arc_angle_deb": arc_angle_deb,
            "arc_angle_aed": arc_angle_aed,
            "tex_angle_deb": tex_angle_deb,
            "tex_angle_180_m_deb": tex_angle_180_m_deb
        }

        center_offset = 3.4
        geoms_org_list  = [elem for key, geom in geoms_org.items()
                           for elem in [geom.shift, center_offset * RIGHT]]
        geoms_left_copy = copy.deepcopy(geoms_org)
        geoms_left_copy_list = [elem for key, geom in geoms_left_copy.items()
                                for elem in [geom.shift, center_offset * -RIGHT]]

        glist = geoms_org_list
        glist.extend(geoms_left_copy_list)

        if all_play:
            self.play(*glist)
            self.wait(wait_time)


        # Left figure remove line AB, dot A, dot B, texts, and show Angle 180
        if all_play:
            self.play(FadeOut(geoms_left_copy["line_ab"]),
                      FadeOut(geoms_left_copy["dot_a"]),
                      FadeOut(geoms_left_copy["dot_b"]),
                      FadeOut(geoms_left_copy["text_a"]),
                      FadeOut(geoms_left_copy["text_b"]),
                      FadeOut(geoms_left_copy["arc_angle_aed"]),
                      FadeOut(geoms_left_copy["arc_angle_deb"]),
                      FadeOut(geoms_left_copy["tex_angle_deb"]),
                      FadeOut(geoms_left_copy["tex_angle_180_m_deb"]))
            self.wait(wait_time)

        arc_angle_left_180 = Arc(
            start_angle = geoms_left_copy["line_cd"].get_angle(),
            angle       = PI,
            radius      = self.radius,
            color       = self.radius_color_1,
            arc_center  = self.arc_center_1 + center_offset * -RIGHT
        )

        tex_left_angle_180 = TexMobject( r"180^\circ").scale(angle_text_scale).\
                             shift(0.3 * UP + center_offset * -RIGHT)
        geoms_left_copy["arc_angle_180"] = arc_angle_left_180
        geoms_left_copy["tex_angle_180"] = tex_left_angle_180

        if all_play:
            self.play(ShowCreation(geoms_left_copy["arc_angle_180"]),
                      FadeIn(      geoms_left_copy["tex_angle_180"]))
            self.wait(wait_time)

        # Show line AB and show Angle AEC and 180 - AEC
        if all_play:
            self.play(ShowCreation(geoms_left_copy["line_ab"]),
                      ShowCreation(geoms_left_copy["dot_a"]),
                      ShowCreation(geoms_left_copy["dot_b"]),
                      FadeIn(geoms_left_copy["text_a"]),
                      FadeIn(geoms_left_copy["text_b"]))
            self.wait(wait_time)


        aec_shift = -1.5 * UP - 2.0 * RIGHT
        left_tex_angle_aec       = TexMobject( r"\angle AEC").scale(angle_text_scale).\
                                   shift(aec_shift + center_offset * -RIGHT)
        left_tex_angle_180_m_aec = TexMobject(r"180^\circ", r"-", r"\angle AEC").scale(angle_text_scale).\
                                   shift(deb_180m_shift + center_offset * -RIGHT)
        geoms_left_copy["tex_angle_aec"]       = left_tex_angle_aec
        geoms_left_copy["tex_angle_180_m_aec"] = left_tex_angle_180_m_aec

        if all_play:
            self.play(FadeOut(geoms_left_copy["arc_angle_180"]),
                      FadeOut(geoms_left_copy["tex_angle_180"]))
            self.wait(wait_time)


        left_arc_angle_aec = Arc(
            start_angle = line_ab.get_angle() + 4 * PI/4,
            angle       = line_ab.get_angle() + PI/4,
            radius      = self.radius,
            color       = RED, # self.radius_color_2,
            arc_center  = self.arc_center_1 + -center_offset * RIGHT

        )
        left_arc_angle_aed = Arc(
            start_angle = line_ab.get_angle() + PI/4,
            angle       = line_ab.get_angle() + 3 * PI/4,
            radius      = self.radius,
            color       = self.radius_color_2,
            arc_center  = self.arc_center_1 + -center_offset * RIGHT
        )
        geoms_left_copy["arc_angle_aec"] = left_arc_angle_aec
        geoms_left_copy["arc_angle_aed"] = left_arc_angle_aed

        if True:
            self.play(FadeIn(geoms_left_copy["tex_angle_aec"]),
                      ShowCreation(geoms_left_copy["arc_angle_aec"]))
            self.wait(wait_time)
            self.play(FadeIn(geoms_left_copy["tex_angle_180_m_aec"]),
                      ShowCreation(geoms_left_copy["arc_angle_aed"]))
            self.wait(wait_time)

        #
        # Show Side by side AED = 180 - AEC = 180 - DEB, thus both -180 and arrange AEC == DEB
        #
        tex_angle_aed_eq_aed = TexMobject(r"\angle AED", r"=", r"\angle AED").scale(angle_text_scale)
        tex_angle_aed_eq_aed_dst = copy.deepcopy(tex_angle_aed_eq_aed)

        # start with next to the angle
        tex_angle_aed_eq_aed[0].move_to(-5.5 * RIGHT -0.5 * UP)
        tex_angle_aed_eq_aed[2].move_to( 1.5 * RIGHT -0.5 * UP)

        arc_emph_scale = 1.2
        if all_play:
            self.play(FadeIn(tex_angle_aed_eq_aed[0]))
            self.wait(wait_time)
            self.play(FadeIn(tex_angle_aed_eq_aed[2]))
            self.wait(wait_time)
        else:
            self.play(FadeIn(tex_angle_aed_eq_aed[0]),
                      FadeIn(tex_angle_aed_eq_aed[2]))

        if all_play:
            self.play(tex_angle_aed_eq_aed[0].scale,          arc_emph_scale,
                      geoms_left_copy["arc_angle_aed"].scale, arc_emph_scale)
            self.play(tex_angle_aed_eq_aed[0].scale,          1/arc_emph_scale,
                      geoms_left_copy["arc_angle_aed"].scale, 1/arc_emph_scale)
            self.wait(wait_time)
            self.play(tex_angle_aed_eq_aed[2].scale,    arc_emph_scale,
                      geoms_org["arc_angle_aed"].scale, arc_emph_scale)
            self.play(tex_angle_aed_eq_aed[2].scale,    1/arc_emph_scale,
                      geoms_org["arc_angle_aed"].scale, 1/arc_emph_scale)
            self.wait(wait_time)

        # go to up
        eq_pos = 3.0 * RIGHT + 3.0 * UP
        tex_angle_aed_eq_aed_dst.move_to(eq_pos)
        self.play(ReplacementTransform(tex_angle_aed_eq_aed, tex_angle_aed_eq_aed_dst))
        self.wait(wait_time)

        # ---- Equation rearrangement
        # Replace 180 - * to up: AED = AED -> 180 - AEC = 180 - DEB
        self.play(tex_angle_aed_eq_aed_dst.move_to, eq_pos)
        self.play(left_tex_angle_180_m_aec.move_to, eq_pos - 2.0 * RIGHT,
                  FadeOut(tex_angle_aed_eq_aed_dst[0]))
        self.play(tex_angle_180_m_deb.move_to,      eq_pos + 2.0 * RIGHT,
                  FadeOut(tex_angle_aed_eq_aed_dst[2]))

        # Remove 180, rearrange
        #   180 - AEC = 180 - DEB
        #       - AEC =     - DEB
        #       - AEC = - DEB
        self.play(FadeOut(left_tex_angle_180_m_aec[0]),
                  FadeOut(geoms_org["tex_angle_180_m_deb"][0]))

        #   Note: FadeOut object will show up when shift
        self.play(geoms_org["tex_angle_180_m_deb"][1].shift, -1.0 * RIGHT,
                  geoms_org["tex_angle_180_m_deb"][2].shift, -1.0 * RIGHT)

        # Remove '-' both side, rearrange
        #       - AEC =     - DEB
        #         AEC =       DEB
        #         AEC = DEB
        self.play(FadeOut(left_tex_angle_180_m_aec[1]),
                  FadeOut(geoms_org["tex_angle_180_m_deb"][1]))
        self.play(geoms_org["tex_angle_180_m_deb"][2].shift, -0.5 * RIGHT) # final DEB


        # --- Show text
        # To show Japanese, manim/manimlib/constants.py
        # TEX_USE_CTEX = True and update the
        # manimlib/ctex_template.tex
        text_vertical_angle = [
            TextMobject(r"Vertical ", r"angles"),
            TextMobject(r"Scheitelwinkel"),
            TextMobject(r"対頂角"),
        ]
        text_vertical_angle[CUR_LANG].scale(1.6).shift(3 * UP - 4 * RIGHT)
        self.play(FadeIn(text_vertical_angle[CUR_LANG]))
        self.wait(wait_time)


        # Back to the one figure
        center_offset = -3.4

        # Removed fadeout texs and arcs
        del(geoms_org["tex_angle_180_m_deb"])
        del(geoms_left_copy["tex_angle_180_m_deb"])
        del(geoms_left_copy["tex_angle_180_m_aec"])
        del(geoms_left_copy["tex_angle_deb"])
        del(geoms_left_copy["arc_angle_deb"])
        del(geoms_left_copy["arc_angle_180"])
        del(geoms_left_copy["tex_angle_180"])

        geoms_org_list  = [elem for key, geom in geoms_org.items()
                           for elem in [geom.shift, center_offset * RIGHT]]
        geoms_left_copy_list = [elem for key, geom in geoms_left_copy.items()
                                for elem in [geom.shift, center_offset * -RIGHT]]
        glist = geoms_org_list
        glist.extend(geoms_left_copy_list)

        if all_play:
            self.play(*glist)
            self.wait(wait_time)

        # FadeOut left copy and orig DEB
        self.play(FadeOut(geoms_org["arc_angle_aed"]),
                  FadeOut(geoms_left_copy["arc_angle_aed"]))
        self.wait(wait_time)

        # emphasize the vertical anges
        if all_play:
            mag_factor = 1.2
            self.play(geoms_left_copy["tex_angle_aec"].scale, mag_factor,
                      geoms_left_copy["arc_angle_aec"].scale, mag_factor)
            self.play(geoms_left_copy["tex_angle_aec"].scale, 1.0/mag_factor,
                      geoms_left_copy["arc_angle_aec"].scale, 1.0/mag_factor)
            self.wait(wait_time)
            self.play(geoms_org["tex_angle_deb"].scale, mag_factor,
                      geoms_org["arc_angle_deb"].scale, mag_factor)
            self.play(geoms_org["tex_angle_deb"].scale, 1.0/mag_factor,
                      geoms_org["arc_angle_deb"].scale, 1.0/mag_factor)
            self.wait(wait_time)

        self.play(FadeOut(geoms_org["arc_angle_deb"]),
                  FadeOut(geoms_org["tex_angle_deb"]),
                  FadeOut(geoms_left_copy["arc_angle_aec"]),
                  FadeOut(geoms_left_copy["tex_angle_aec"]));
        # FadeOut(geoms_left_copy["arc_angle_deb"]))
        self.wait(wait_time)

        # Add another vertical angle: AED = CEB
        tex_angle_aed_eq_ceb = TexMobject(r"\angle AED", r"=", r"\angle CEB").scale(angle_text_scale)
        arc_angle_ceb = Arc(
            start_angle = line_ab.get_angle() + PI + PI/4,
            angle       = line_ab.get_angle() + 3/4 * PI,
            radius      = self.radius,
            color       = WHITE,
            arc_center  = self.arc_center_1
        )
        geoms_org["arc_angle_aed"].set_color(WHITE)

        tex_angle_aed_eq_ceb[2].move_to(1.0 * RIGHT + -2.2 * UP)

        self.play(ShowCreation(geoms_org["arc_angle_aed"]),
                  FadeIn(tex_angle_aed_eq_ceb[0]))
        self.wait(wait_time)
        self.play(ShowCreation(arc_angle_ceb),
                  FadeIn(tex_angle_aed_eq_ceb[2]))
        self.wait(wait_time)

        # Move to top and show AED = CEB
        tex_angle_aed_eq_ceb[1].move_to(3.0 * RIGHT + 2.0 * UP)
        self.play(ShowCreation(tex_angle_aed_eq_ceb[1]),
                  tex_angle_aed_eq_ceb[0].move_to, 1.8 * RIGHT + 2.0 * UP,
                  tex_angle_aed_eq_ceb[2].move_to, 4.3 * RIGHT + 2.0 * UP)

        self.wait(wait_time)

        self.wait(5)


