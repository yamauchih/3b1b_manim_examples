# -*- coding: utf-8; -*-
#
# Section 3: Corresponding angles
#
#    (C) 2020 Hitoshi Yamauchi
#
# References: 3Blue1Brown, Theorem of Beethoven (manim tutorial)
#
#  cd data/gitdata/manim
#  source manim-venv/bin/activate
#
# Full resolution
#   python3 -m manim 03_corresponding_angles.py CorrespondingAngles01 --resolution 720,1280 -p --high_quality
# Preview resolution
#   python3 -m manim 03_corresponding_angles.py CorrespondingAngles01 --resolution 360,640 -pl
#   python3 -m manim 03_corresponding_angles.py CorrespondingAngles01 --resolution 360,640 -i --high_quality
# -i as gif


from manimlib.imports import *
import os, copy
import pyclbr


class Glue_obj_side_updater(object):
    """
    Glue two objects (horizontal side) updater.
    Put an object next to the main_obj using next_to().

    follower_obj(left) -- main_obj -- follwer_obj(right)

    This uses next_to(), not move_to()

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



class Glue_line_point_edge_rotate_updater(object):
    """
    Glue two objects (a point at the edge of a line) for updater
    Put an follower object next to the end point of a line.

                                    + follower(right(where = 1))
                                   /
                                  /
                                 / line
                                /
                               /
    follower(left(where = 0)) +

    This uses move_to() instead of next_to().

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


class Intersection_point_e_updater_by_line_position(object):
    """
    Intersection point e position updater.
    The point e is an intersection point on line AB and line CD.

    This follows the ab's position change.

    Currently, assume m_ab is constant and = 0 (horizontal line)
    (TODO: m_ab is constant but can be non-zero)

    Where
      * the line AB: y = m_ab x + o_ab
      * the line CD: y = m_cd x + o_cd

    line AB
      * m_ab: slope of line AB
      * O_ab: origin, the center point, of the line segment AB (O_ab_x, O_ab_y, 0.0)

    line CD
      * m_cd: slope of line CD
      * O_cd: origin, the center point, of the line segment CD (O_cd_x, O_cd_y, 0.0)


    line AB1: y = O_ab_y
    line CD:  y = tan(theta) x + O_cd_y

                  + D
                 /
                /
               /
              + O_cd
           E /
     A +----+--+--------+ B
           /   O_ab
        C +

    """
    def __init__(self, line_ab, cd_val_tracker, line_cd):
        """
        param[in] line_ab        line AB
        param[in] cd_val_tracker line CD's slope angle value tracker
        param[in] line_cd        line CD

        """
        # self.__m_ab = 0.0
        self.__line_ab = line_ab
        self.__cd_slope_value_tracker = cd_val_tracker
        self.__line_cd = line_cd


    def __call__(self, follower_obj):
        """The method add_updater() receives a function. This object behaves a
        function with this method.  (Note: A closure will work, too.)
        See Effective python: Item 15, Item 23.

        param[in] follower_obj follower object which location is the intersection
                               point of line_ab and line_cd

        """
        # theta = self.__cd_slope_value_tracker[0].get_value()
        theta = self.__cd_slope_value_tracker.get_value()
        # print(theta)
        e_pos_x = 0.0
        e_pos_y = self.__line_ab.get_center()[1]
        if (math.fabs(theta - (math.pi/2.0)) > 0.001):
            e_pos_x = (self.__line_ab.get_center()[1] - self.__line_cd.get_center()[1]) / math.tan(theta)

        e_pos = np.array((e_pos_x, e_pos_y, 0.0))
        follower_obj.move_to(e_pos)



class Intersection_point_e_updater_by_line_ab_2_rotation(object):
    """
    Intersection point e position updater.
    The point e is an intersection point on line A'B' and line CD.

    This follows the a'b's rotation change.

    Where
      * the line AB: y = m_ab x + o_ab
      * the line CD: y = m_cd x + o_cd

    line AB
      * m_ab: slope of line AB
      * O_ab: origin, the center point, of the line segment AB (O_ab_x, O_ab_y, 0.0)

    line CD
      * m_cd: slope of line CD
      * O_cd: origin, the center point, of the line segment CD (O_cd_x, O_cd_y, 0.0)

    O_ab, O_cd: y intersepts
    E_x = (O_ab - O_cd)/(m_cd - m_ab)
    E_y = (m_cd O_ab - m_ab O_cd)/(m_cd - m_ab)
    Where m_cd != m_ab
    m_cd = tan(theta_cd)
    m_ab = tan(theta_ab)


                   + D
            O_ab  /
     A +-----+---+---+ B
                /E
               /
              + O_cd
             /
            /
         C +

    """
    def __init__(self, line_ab, ab_val_tracker, line_cd, cd_val_tracker):
        """
        param[in] line_ab        line AB
        param[in] ab_val_tracker line AB's slope angle value tracker
        param[in] line_cd        line CD
        param[in] cd_val_tracker line CD's slope angle value tracker

        """
        # self.__m_ab = 0.0
        self.__line_ab = line_ab
        self.__ab_slope_value_tracker = ab_val_tracker
        self.__line_cd = line_cd
        self.__cd_slope_value_tracker = cd_val_tracker


    def __call__(self, follower_obj):
        """The method add_updater() receives a function. This object behaves a
        function with this method.  (Note: A closure will work, too.)
        See Effective python: Item 15, Item 23.

        param[in] follower_obj follower object which location is the intersection
                               point of line_ab and line_cd

        """
        theta_ab = self.__ab_slope_value_tracker.get_value()
        theta_cd = self.__cd_slope_value_tracker.get_value()
        # print(theta_ab)

        O_ab = self.__line_ab.get_center()[1]
        O_cd = self.__line_cd.get_center()[1]

        # No check for thera_ab, theta_cd: not +-pi/2 && thera_ab != theta_cd
        m_ab = math.tan(theta_ab)
        m_cd = math.tan(theta_cd)

        e_x = (O_ab - O_cd)/(m_cd - m_ab)
        e_y = (m_cd * O_ab - m_ab * O_cd)/(m_cd - m_ab)

        e_pos = np.array((e_x, e_y, 0.0))
        follower_obj.move_to(e_pos)




class Intersection_arc_updater_all_calc(object):
    """
    Unused for now.

    Intersection arc updater. The arc center is the same to the point E of
    Intersection_arc_updater_by_slope.

    Currently, assume m_ab is constant and = 0 (horizontal line)
    (TODO: m_ab is constant but can be non-zero)

    Where
      * the line AB: y = m_ab x + o_ab
      * the line CD: y = m_cd x + o_cd

    line AB
      * m_ab: slope of line AB
      * O_ab: origin, the center point, of the line segment AB (O_ab_x, O_ab_y, 0.0)

    line CD
      * m_cd: slope of line CD
      * O_cd: origin, the center point, of the line segment CD (O_cd_x, O_cd_y, 0.0)


    line AB1: y = O_ab_y
    line CD:  y = tan(theta) x + O_cd_y

                  + D
                 /
                /
               /
              + O_cd
           E /\ <-- arc
     A +----+--+--------+ B
           /   O_ab
        C +

    """
    def __init__(self, O_ab, cd_val_tracker, O_cd, dot_e):
        """
        param[in] O_ab           line AB
        param[in] cd_val_tracker line CD's slope angle value tracker
        param[in] O_cd           line CD

        """
        # self.__m_ab = 0.0
        self.__O_ab = O_ab

        self.__cd_slope_value_tracker = cd_val_tracker
        self.__O_cd = O_cd
        self.__dot_e = dot_e


    def __call__(self, arc_obj):
        """The method add_updater() receives a function. This object behaves a
        function with this method.  (Note: A closure will work, too.)
        See Effective python: Item 15, Item 23.

        param[in] arc_obj arc object which location is the intersection
                          point of line_ab and line_cd

        """
        # theta = self.__cd_slope_value_tracker[0].get_value()
        theta = self.__cd_slope_value_tracker.get_value()
        # print(theta)
        e_pos_x = 0.0
        e_pos_y = self.__O_ab[1]
        if (math.fabs(theta - (math.pi/2.0)) > 0.001):
            e_pos_x = (self.__O_ab[1] - self.__O_cd[1]) / math.tan(theta)

        e_pos = np.array((e_pos_x, e_pos_y, 0.0))
        # print("dot_e: {0}, e_pos: {1}".format(self.__dot_e.get_center(), e_pos))
        arc_obj.become(
            Arc(
                start_angle = 0.0,
                angle       = theta,
                radius      = 0.7,
                color       = WHITE,
                arc_center  = self.__dot_e.get_center()
            )
        )
        # follower_obj.move_to(e_pos)


class Intersection_arc_updater_follow_dot(object):
    """
    Intersection arc updater. The arc center is the same to the point E of
    Intersection_arc_updater_by_slope.
             _
           E  \ <-- arc
           +  +

    """
    def __init__(self, cd_val_tracker, dot_e, start_angle=0.0, radius=0.7, color=WHITE):
        """
        param[in] cd_val_tracker angle value tracker
        param[in] dot_e          dot_e to follow

        """
        # self.__m_ab = 0.0
        self.__cd_slope_value_tracker = cd_val_tracker
        self.__dot_e                  = dot_e
        self.__start_angle            = start_angle
        self.__radius                 = radius
        self.__color                  = color
        # print("init: dot_e: {0}".format(dot_e.get_arc_center()))

    def __call__(self, arc_obj):
        """The method add_updater() receives a function. This object behaves a
        function with this method.  (Note: A closure will work, too.)
        See Effective python: Item 15, Item 23.

        param[in] arc_obj arc object which location is the intersection
                          point of line_ab and line_cd

        """
        # theta = self.__cd_slope_value_tracker[0].get_value()
        theta = self.__cd_slope_value_tracker.get_value()
        # print("dot_e: {0}".format(self.__dot_e.get_center())) # get_arc_center() has a problem. warning
        arc_obj.become(
            Arc(
                start_angle = self.__start_angle,
                angle       = theta,
                radius      = self.__radius,
                color       = self.__color,
                arc_center  = self.__dot_e.get_center()
            )
        )



class Intersection_arc_updater_follow_dot_angle(object):
    """
    Intersection arc updater. The arc center is the same to the point E and
    also follows two lines slopes
             _
           E  \ <-- arc
           +  +

    """
    def __init__(self, ab_val_tracker, cd_val_tracker, dot_e, radius=0.7, color=WHITE):
        """
        param[in] ab_val_tracker line ab angle value tracker
        param[in] cd_val_tracker line cd angle value tracker
        param[in] dot_e          dot_e to follow

        """
        # self.__m_ab = 0.0
        self.__ab_slope_value_tracker = ab_val_tracker
        self.__cd_slope_value_tracker = cd_val_tracker
        self.__dot_e                  = dot_e
        self.__radius                 = radius
        self.__color                  = color
        # print("init: dot_e: {0}".format(dot_e.get_arc_center()))

    def __call__(self, arc_obj):
        """The method add_updater() receives a function. This object behaves a
        function with this method.  (Note: A closure will work, too.)
        See Effective python: Item 15, Item 23.

        param[in] arc_obj arc object which location is the intersection
                          point of line_ab and line_cd

        """
        # theta = self.__cd_slope_value_tracker[0].get_value()
        slope_ab = self.__ab_slope_value_tracker.get_value()
        slope_cd = self.__cd_slope_value_tracker.get_value()
        # print("dot_e: {0}".format(self.__dot_e.get_center())) # get_arc_center() has a problem. warning
        # print("slope_ab: {0}, slope_cd: {1}".format(slope_ab, slope_cd))
        arc_obj.become(
            Arc(
                start_angle =  slope_ab,
                angle       = -slope_ab + slope_cd,
                radius      = self.__radius,
                color       = self.__color,
                arc_center  = self.__dot_e.get_center()
            )
        )



def play_create_and_fade_in(self_obj, mobj_dict):
    """
    Create MObject with ShowCreation and TexMobject/TextObject with FadeIn (FadeInFromDown is also an candidate)
    """

    play_list = []
    for mobj in mobj_dict.values():
        if   (isinstance(mobj, TexMobject)):
            play_list.append(FadeIn(mobj))
        elif (isinstance(mobj, TextMobject)):
            play_list.append(FadeIn(mobj))
        else:
            play_list.append(ShowCreation(mobj))

    assert (len(play_list) > 0)
    self_obj.play(*play_list)


class CorrespondingAngles01(Scene):
    """03. What is corresponding angles
    """
    CONFIG={
        "wait_time":               1,
        "line_ab_1_color":         YELLOW,
        "line_ab_2_color":         YELLOW,
        "line_cd_color":           BLUE,
        "parallel_line_length":    8,
        "transversal_line_length": 6.5,
        "theta":                   0,        # theta of cd
        "theta_ab_2":              0,        # theta of a'b'
        "increment_theta":         PI/2,
        "final_theta":             PI,
        "radius":                  0.7,
        "radius_color_1":          WHITE,
        "radius_color_2":          WHITE,
        "arc_center_1":            ORIGIN + DOWN,
    }

    def construct(self):

        all_play  = True

        # language: 0 ... English, 1 ... Deutsch, 2 ... 日本語
        CUR_LANG = 0

        #-- 1. create all elements

        # line ab 1
        line_ab_1_tex_up_offset = 0.3 * DOWN
        line_ab_1_start  = ORIGIN
        line_ab_1_end    = RIGHT * self.parallel_line_length
        line_ab_1_origin = ORIGIN + 1.5 * DOWN
        line_ab_1        = Line(line_ab_1_start, line_ab_1_end, color=self.line_ab_1_color).move_to(line_ab_1_origin)
        dot_a_1          = Dot(ORIGIN, color=YELLOW).next_to(line_ab_1, LEFT,  buff=0)
        dot_b_1          = Dot(ORIGIN, color=YELLOW).next_to(line_ab_1, RIGHT, buff=0)
        tex_a_1          = TexMobject(r"A", color=YELLOW).next_to(dot_a_1, LEFT  + line_ab_1_tex_up_offset, buff=0)
        tex_b_1          = TexMobject(r"B", color=YELLOW).next_to(dot_b_1, RIGHT + line_ab_1_tex_up_offset, buff=0)

        group_line_ab_1 = {
            "line_ab_1": line_ab_1,
            "dot_a_1":   dot_a_1,
            "dot_b_1":   dot_b_1,
            "tex_a_1":   tex_a_1,
            "tex_b_1":   tex_b_1,
        }

        # line_cd
        line_cd_start  = ORIGIN
        line_cd_end    = RIGHT * self.transversal_line_length
        line_cd_origin = ORIGIN + 0.5 * DOWN
        line_cd        = Line(line_cd_start, line_cd_end, color=self.line_cd_color).move_to(line_cd_origin)
        dot_c          = Dot(ORIGIN, color=BLUE).  next_to(line_cd, LEFT,  buff=0)
        dot_d          = Dot(ORIGIN, color=BLUE).  next_to(line_cd, RIGHT, buff=0)
        tex_c          = TexMobject(r"C", color=BLUE).  next_to(dot_c, LEFT,  buff=MED_SMALL_BUFF)
        tex_d          = TexMobject(r"D", color=BLUE).  next_to(dot_d, RIGHT, buff=MED_SMALL_BUFF)

        # -- line cd value tracker
        self.theta = PI/4

        theta = ValueTracker(self.theta)
        # theta_list = [ValueTracker(self.theta)]

        # Use rotate the line instead of set_angle. (due to no about_point)
        def update_line_cd_angle(line_obj):
            delta = theta.get_value() - line_obj.get_angle()
            line_obj.rotate(delta)

        line_cd.add_updater(update_line_cd_angle)

        dot_c.add_updater(Glue_line_point_edge_rotate_updater(line_cd, position=ORIGIN, where=0)) # where=0 is left  of the line_cd
        dot_d.add_updater(Glue_line_point_edge_rotate_updater(line_cd, position=ORIGIN, where=1)) # where=1 is right of the line_cd
        tex_c.add_updater(Glue_obj_side_updater(dot_c, position=LEFT,  buff=MED_SMALL_BUFF))
        tex_d.add_updater(Glue_obj_side_updater(dot_d, position=RIGHT, buff=MED_SMALL_BUFF))

        #   add all togather to show
        # self.add(*[line_cd, dot_c, tex_c, dot_d, tex_d])

        group_line_cd = {
            "line_cd": line_cd,
            "dot_c":   dot_c,
            "dot_d":   dot_d,
            "tex_c":   tex_c,
            "tex_d":   tex_d,
            }

        # angle alpha 1 at E
        dot_e_1       = Dot(point=ORIGIN + DOWN, color=GREEN)
        tex_e_1       = TexMobject(r"E",      color=GREEN).next_to(dot_e_1, DOWN, buff=MED_SMALL_BUFF)
        tex_alpha_1   = TexMobject(r"\alpha", color=WHITE).next_to(dot_e_1, LEFT, buff=MED_SMALL_BUFF)
        arc_alpha_1 = Arc(
            start_angle = line_ab_1.get_angle(),
            angle       = PI,
            radius      = self.radius,
            color       = self.radius_color_1,
            arc_center  = self.arc_center_1
        )

        # point e updater setup
        dot_e_1.add_updater(Intersection_point_e_updater_by_line_position(line_ab_1, theta, line_cd))
        tex_e_1.add_updater(Glue_obj_side_updater(dot_e_1, position=RIGHT + DOWN, buff=MED_SMALL_BUFF))
        tex_alpha_1.add_updater(Glue_obj_side_updater(dot_e_1, position=3.0 * RIGHT + 2.0 * UP, buff=MED_SMALL_BUFF))
        arc_alpha_1.add_updater(Intersection_arc_updater_follow_dot(theta, dot_e_1, start_angle=0.0, radius=self.radius, color=self.radius_color_1))

        group_angle_alpha_1 = {
            "dot_e_1":     dot_e_1,
            "tex_e_1":     tex_e_1,
            "tex_alpha_1": tex_alpha_1,
            "arc_alpha_1": arc_alpha_1,
            }

        play_create_and_fade_in(self, group_line_ab_1)
        play_create_and_fade_in(self, group_line_cd)
        play_create_and_fade_in(self, group_angle_alpha_1)
        self.wait(self.wait_time)

        # -- create line A'B'
        # line ab 2 (ab', parallel to ab)
        line_ab_2_tex_up_offset = 0.3 * UP
        line_ab_2_start  = line_ab_1_start
        line_ab_2_end    = line_ab_1_end
        line_ab_2_origin = line_ab_1_origin
        line_ab_2        = Line(line_ab_2_start, line_ab_2_end, color=self.line_ab_2_color).move_to(line_ab_2_origin)
        dot_a_2          = Dot(ORIGIN, color=YELLOW).next_to(line_ab_2, LEFT,  buff=0)
        dot_b_2          = Dot(ORIGIN, color=YELLOW).next_to(line_ab_2, RIGHT, buff=0)
        tex_a_2          = TexMobject(r"A'", color=YELLOW).next_to(dot_a_2, LEFT  + line_ab_2_tex_up_offset, buff=0)
        tex_b_2          = TexMobject(r"B'", color=YELLOW).next_to(dot_b_2, RIGHT + line_ab_2_tex_up_offset, buff=0)

        dot_a_2.add_updater(Glue_obj_side_updater(line_ab_2, position=LEFT,  buff=0))
        dot_b_2.add_updater(Glue_obj_side_updater(line_ab_2, position=RIGHT, buff=0))
        tex_a_2.add_updater(Glue_obj_side_updater(dot_a_2, position=LEFT  + line_ab_2_tex_up_offset, buff=0))
        tex_b_2.add_updater(Glue_obj_side_updater(dot_b_2, position=RIGHT + line_ab_2_tex_up_offset, buff=0))

        group_line_ab_2 = {
            "line_ab_2": line_ab_2,
            "dot_a_2":   dot_a_2,
            "dot_b_2":   dot_b_2,
            "tex_a_2":   tex_a_2,
            "tex_b_2":   tex_b_2,
            }

        #-- angle alpha 2 with the point E'
        dot_e_2       = Dot(point=ORIGIN + DOWN, color=GREEN)
        tex_e_2       = TexMobject(r"E'",      color=GREEN).next_to(dot_e_2, DOWN, buff=MED_SMALL_BUFF)
        tex_alpha_2   = TexMobject(r"\alpha'", color=WHITE).next_to(dot_e_2, LEFT, buff=MED_SMALL_BUFF)
        arc_alpha_2 = Arc(
            start_angle = line_ab_2.get_angle(),
            angle       = PI,
            radius      = self.radius,
            color       = self.radius_color_1, # same to alpha 1
            arc_center  = self.arc_center_1    # same to alpha 1
        )

        dot_e_2.add_updater(Intersection_point_e_updater_by_line_position(line_ab_2, theta, line_cd))
        tex_e_2.add_updater(Glue_obj_side_updater(dot_e_2, position=RIGHT + DOWN, buff=MED_SMALL_BUFF))
        tex_alpha_2.add_updater(Glue_obj_side_updater(dot_e_2, position=3.0 * RIGHT + 2.0 * UP, buff=MED_SMALL_BUFF))
        arc_alpha_2.add_updater(Intersection_arc_updater_follow_dot(theta, dot_e_2, start_angle=0.0, radius=self.radius, color=self.radius_color_2))

        group_angle_alpha_2 = {
            "dot_e_2":     dot_e_2,
            "tex_e_2":     tex_e_2,
            "tex_alpha_2": tex_alpha_2,
            "arc_alpha_2": arc_alpha_2,
            }

        play_create_and_fade_in(self, group_line_ab_2)
        play_create_and_fade_in(self, group_angle_alpha_2)
        self.wait(self.wait_time)

        # move up
        self.play(line_ab_2.shift, 2.2 * UP)
        self.wait(self.wait_time)

        # Do not deep copy alpha_1, alpha_2 due to updaters.
        # Though, we could do tex_alpha_2_copy.clear_updaters(), I want to keep them.
        tex_alpha_eq_alpha_d  = TexMobject(r"\alpha", r"=",    r"\alpha'").move_to(3.2 * UP + 3 * RIGHT).set_color(WHITE)
        tex_alpha_pos = [tex_alpha_eq_alpha_d[0].get_center(),
                         tex_alpha_eq_alpha_d[1].get_center(),
                         tex_alpha_eq_alpha_d[2].get_center()]

        tex_alpha_eq_alpha_d[0].move_to(tex_alpha_1.get_center())
        tex_alpha_eq_alpha_d[2].move_to(tex_alpha_2.get_center())

        alpha_scale = 1.6       # \alpha char scale
        self.play(FadeIn(tex_alpha_eq_alpha_d))
        self.play(tex_alpha_eq_alpha_d[0].move_to, tex_alpha_pos[0],
                  tex_alpha_eq_alpha_d[2].move_to, tex_alpha_pos[2])
        self.play(tex_alpha_eq_alpha_d.scale, alpha_scale)
        self.wait(self.wait_time)

        text_corresponding_angles = [
            TextMobject(r"Corresponding", r"angles"),
            TextMobject(r"Stufenwinkel"),
            TextMobject(r"同位角"),
        ]
        pos_corresponding_angles = [
            3.2 * UP - 2.5 * RIGHT,
            3.2 * UP - 2.5 * RIGHT,
            3.2 * UP - 2.5 * RIGHT
        ]
        text_corresponding_angles[CUR_LANG].scale(1.6).move_to(pos_corresponding_angles[CUR_LANG])
        # self.play(FadeIn(text_corresponding_angles[CUR_LANG]))
        # self.play(FadeIn(text_corresponding_angles[CUR_LANG]))
        self.play(FadeInFromDown(text_corresponding_angles[CUR_LANG]))
        self.wait(self.wait_time)

        # rotate line cd
        self.play(theta.increment_value,   PI/4)
        self.wait(self.wait_time)
        self.play(theta.increment_value,  -PI/4)
        self.wait(self.wait_time)

        # Create '>' with two lines
        parallel_sign_1 = VGroup()
        l1 = Line(ORIGIN + 0.8 * UP - RIGHT, ORIGIN)
        l2 = Line(ORIGIN - 0.8 * UP - RIGHT, ORIGIN)
        parallel_sign_1.add(l1, l2).set_color(YELLOW).scale(0.3)

        parallel_sign_2 = copy.deepcopy(parallel_sign_1)
        parallel_sign_1.move_to(-1.5 * UP + 3.0 * RIGHT)
        parallel_sign_2.move_to( 0.7 * UP + 3.0 * RIGHT)

        ab_adbd_parallel_tex  = TexMobject(r"AB", r"\parallel",  r"A'B'", color=YELLOW).move_to( 2.0 * UP + 5.0 * RIGHT)
        ab_adbd_nparallel_tex = TexMobject(r"AB", r"\nparallel", r"A'B'", color=YELLOW).move_to( 2.0 * UP + 5.0 * RIGHT)
        # For Transform working buffer
        work_ab_adbd_parallel_tex = copy.deepcopy(ab_adbd_parallel_tex)

        self.play(ShowCreation(parallel_sign_1), ShowCreation(parallel_sign_2), FadeIn(work_ab_adbd_parallel_tex))
        self.wait(self.wait_time)

        # Transversal
        text_transversal = [
            TextMobject(r"Transversal"),
            TextMobject(r"Transversal"),
            TextMobject(r"横断線"),
        ]
        pos_text_transversal = [
            -2.8 * UP + 1.4 * RIGHT,
            -2.8 * UP + 1.4 * RIGHT,
            -2.8 * UP + 0.8 * RIGHT, # -2.8 * UP + 2.2 * RIGHT,
        ]
        text_transversal[CUR_LANG].set_color(BLUE).scale(1.0).move_to(pos_text_transversal[CUR_LANG])

        # buff=0 makes the start and end exact position
        trans_arrow_start  = -2.8 * UP + -0.2 * RIGHT
        trans_arrow_end    = -2.0 * UP + -1.5 * RIGHT
        trans_arrow        = Arrow(trans_arrow_start, trans_arrow_end, stroke_width = 16, color=BLUE, buff=0)
        self.play(ShowCreation(trans_arrow), FadeIn(text_transversal[CUR_LANG]))
        self.wait(self.wait_time)

        #-----
        # Non parallel case. Show alpha != alpha' when AB \nparallel A'B'

        # -- line a'b' value tracker
        self.theta_ab_2 = 0
        tracker_theta_ab_2 = ValueTracker(self.theta_ab_2)

        # Use rotate the line instead of set_angle. (due to no about_point)
        def update_line_ab_2_angle(line_obj):
            delta = tracker_theta_ab_2.get_value() - line_obj.get_angle()
            line_obj.rotate(delta)

        # clear all updaters related with line_ab and arc E'
        for mobj in [line_ab_2, dot_a_2, dot_b_2, tex_a_2, tex_b_2,
                     dot_e_2, tex_e_2, tex_alpha_2, arc_alpha_2]:
            mobj.clear_updaters()

        line_ab_2.add_updater(update_line_ab_2_angle)
        dot_a_2.add_updater(Glue_line_point_edge_rotate_updater(line_ab_2, position=ORIGIN, where=0)) # where=0 is left  of the line_ab_2
        dot_b_2.add_updater(Glue_line_point_edge_rotate_updater(line_ab_2, position=ORIGIN, where=1)) # where=1 is right of the line_ab_2
        tex_a_2.add_updater(Glue_obj_side_updater(dot_a_2, position=LEFT,  buff=MED_SMALL_BUFF))
        tex_b_2.add_updater(Glue_obj_side_updater(dot_b_2, position=RIGHT, buff=MED_SMALL_BUFF))

        dot_e_2.add_updater(Intersection_point_e_updater_by_line_ab_2_rotation(line_ab_2, tracker_theta_ab_2, line_cd, theta))
        tex_e_2.add_updater(Glue_obj_side_updater(dot_e_2, position=RIGHT + DOWN, buff=MED_SMALL_BUFF))
        tex_alpha_2.add_updater(Glue_obj_side_updater(dot_e_2, position=3.0 * RIGHT + 2.0 * UP, buff=MED_SMALL_BUFF))
        arc_alpha_2.add_updater(Intersection_arc_updater_follow_dot_angle(tracker_theta_ab_2, theta, dot_e_2, radius=self.radius, color=self.radius_color_2))

        # remove transversal, parallel
        self.play(FadeOut(trans_arrow), FadeOut(text_transversal[CUR_LANG]),
                  FadeOut(parallel_sign_1), FadeOut(parallel_sign_2))

        # AB \parallel A'B' -> AB \nparallel A'B' -> AB \parallel A'B'
        # alpha = alpha'    -> alpha \neq alpha'  -> alpha = alpha'
        tex_alpha_neq_alpha_d     = TexMobject(r"\alpha", r"\neq", r"\alpha'").move_to(3.2 * UP + 3 * RIGHT).set_color(WHITE).scale(alpha_scale)
        copy_tex_alpha_eq_alpha_d = copy.deepcopy(tex_alpha_eq_alpha_d) # for Transform back

        self.play(tracker_theta_ab_2.increment_value,  -PI/8,
                  Transform(work_ab_adbd_parallel_tex[1], ab_adbd_nparallel_tex[1]),
                  Transform(tex_alpha_eq_alpha_d[1],      tex_alpha_neq_alpha_d[1]))
        self.wait(self.wait_time)
        self.play(tracker_theta_ab_2.increment_value,   PI/8,
                  Transform(work_ab_adbd_parallel_tex[1], ab_adbd_parallel_tex[1]),
                  Transform(tex_alpha_eq_alpha_d[1],      copy_tex_alpha_eq_alpha_d[1]),
                  FadeIn(parallel_sign_1), FadeIn(parallel_sign_2))
        self.wait(self.wait_time)

        self.wait(5)
