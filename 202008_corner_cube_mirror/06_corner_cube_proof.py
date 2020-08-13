# -*- coding: utf-8; -*-
#
# Section 6: Corner cube reflection proof
#
#    (C) 2020 Hitoshi Yamauchi
#
# References: 3Blue1Brown, Theorem of Beethoven (manim tutorial)
#
#  cd data/gitdata/manim
#  source manim-venv/bin/activate
#
# Full resolution
#   python3 -m manim 06_corner_cube_proof.py CornerReflection01 --resolution 720,1280 -p --high_quality
# Preview resolution
#   python3 -m manim 06_corner_cube_proof.py CornerReflection01 --resolution 360,640 -pl
#   python3 -m manim 06_corner_cube_proof.py CornerReflection01 --resolution 360,640 -i --high_quality
# -i as gif


from manimlib.imports import *
import os, copy
import pyclbr

class CornerReflection01(Scene):
    """06. corner cube reflection 01
    """
    CONFIG={
        #-- shared variables
        #   show all the MObject construction when True (for debug)
        "is_show_construct": False,
        "wait_time":         1,
        #   Each animation skip to the end state of the part of animation
        "is_skip_to_end":    False,

        #-- shared MObjects

        # mirror, its normal, elbow (right angle sign)
        "mirror_corner_pos":   -4.5 * RIGHT + 2.0 * UP,
        "mirror_1_length":      5.0,
        "mirror_2_length":      5.0,
        "mirror_stroke_width":  4.0,
        "mirror_color":        WHITE,
        "elbow_length":         0.4,
        "elbow_color":         YELLOW,
        "line_mirror_up_l1"  : None,
        "line_mirror_left_n1": None,
        "line_normal_left_l2": None,
        "line_normal_up_n2":   None,
        "elbow_l1_n1":         None,
        "elbow_l2_n1":         None,
        "elbow_l1_n2":         None,
        "elbow_edge_len":      0.6,
        "parallel_sign_l1":    None,
        "parallel_sign_l2":    None,

        # rays: laser light
        #   line: extended line of the laser ray
        "line_ray_1":   None,
        "line_ray_2":   None,
        "line_ray_3":   None,
        "line_o1":      None,
        "line_m":       None,
        "line_o2":      None,
        "elbow_o1":     None,
        "elbow_o2":     None,
        "ray_1_spos":          -1.0 * RIGHT + -3.0 * UP,
        # This is heuristic value. I found [1/6, 1/5] looks nice.
        "ray_1_theta":           (21/100) * PI,
        "ray_1_color":           YELLOW,
        "ray_1_stroke_width":    4,
        "ray_2_color":           BLUE,
        "ray_2_stroke_width":    4,
        "ray_3_color":           RED,
        "ray_3_stroke_width":    4,
        "ray_3_length":          4,
        "line_o1_color":         WHITE,
        "line_o1_factor":        1.6,
        "line_o1_stroke_width":  4,
        "line_m_color":          WHITE,
        "line_m_factor":         1.7,
        "line_m_stroke_width":   4,
        "line_o2_color":         WHITE,
        "line_o2_factor":        1.7,
        "line_o2_stroke_width":  4,

        # arcs, angles
        #   arc_theta[5]
        #   tex_theta[5]
        #   arc_2_theta[2]
        #   tex_2_theta[2]
        "arc_theta":                 None,
        "arc_theta_pos_offset":      None,
        "arc_theta_radius":          1.0,
        "arc_theta_color":           YELLOW,
        "tex_theta":                 None,
        #   offset from the arc center
        "tex_theta_position_offset": [ 1.5 * RIGHT + -0.5 * UP,
                                       1.5 * RIGHT +  0.5 * UP,
                                      -1.5 * RIGHT + -0.5 * UP,
                                       1.5 * RIGHT + -0.5 * UP,
                                      -1.5 * RIGHT +  0.5 * UP],
        "tex_theta_color":           WHITE,
        "tex_angle_x":               None,
        "tex_angle_y":               None,
        "arc_2_theta":               None,
        "arc_2_theta_pos_offset":    None,
        "arc_2_theta_radius":        1.0,
        "arc_2_theta_color":         WHITE,
        "tex_2_theta":               None,
        "tex_2_theta_color":         WHITE,
        "tex_2_theta_position_offset": [ 1.6 * RIGHT +  0.0 * UP,
                                         -1.6 * RIGHT +  0.0 * UP],
        # line annotation texs
        "tex_line_l1":               None,
        "tex_line_l1_pos":           0.0 * RIGHT +  0.0 * UP,
        "tex_line_l2":               None,
        "tex_line_l2_pos":           0.0 * RIGHT +  0.0 * UP,
        "tex_line_n1":               None,
        "tex_line_n1_pos":           0.0 * RIGHT +  0.0 * UP,
        "tex_line_n2":               None,
        "tex_line_n2_pos":           0.0 * RIGHT +  0.0 * UP,
        "tex_line_o1":               None,
        "tex_line_o1_pos":           0.0 * RIGHT +  0.0 * UP,
        "tex_line_o2":               None,
        "tex_line_o2_pos":           0.0 * RIGHT +  0.0 * UP,
        "tex_line_m":                None,
        "tex_line_m_pos":            0.0 * RIGHT +  0.0 * UP,
    }


    def get_r1(self):
        """Get r1 (reflection 1 position) via
        self. ray_1_spos and ray_1_theta.
        """
        assert(self.ray_1_theta > 0.0)
        cx = self.mirror_corner_pos[0]
        px = self.ray_1_spos[0]
        py = self.ray_1_spos[1]

        r1_x = cx
        r1_y = py + abs(px - cx) * math.tan(self.ray_1_theta)

        return np.array((r1_x, r1_y, 0.0))


    def get_r2(self):
        """Get r2 (reflection 2 position)
        """
        assert(self.ray_1_theta > 0.0)

        cx = self.mirror_corner_pos[0]
        cy = self.mirror_corner_pos[1]

        r1 = self.get_r1()

        t2 = abs(r1[1] - cy)
        t3 = t2 / math.tan(self.ray_1_theta)
        r2_x = cx + t3
        r2_y = cy

        return np.array((r2_x, r2_y, 0.0))


    def get_vdir(self):
        """Get final reflection ray direction
        """
        norm = math.sqrt(1 + math.tan(self.ray_1_theta) ** 2)

        vdir = np.array((1.0, -math.tan(self.ray_1_theta), 0.0))
        vdir /= norm

        return vdir


    def get_line_from_ray(self, ray_start, ray_end, length_factor):
        """
        From ray_start, ray_end, length, get the extended/shrinked line
        extended when length_factor > 1.
        """

        line_center_pos = 0.5 * (ray_start + ray_end)
        line_vec        = ray_end - ray_start
        line_norm       = np.linalg.norm(line_vec)
        line_vec       /= line_norm
        line_start      = line_center_pos + -0.5 * line_norm * length_factor * line_vec
        line_end        = line_center_pos + +0.5 * line_norm * length_factor * line_vec

        return (line_start, line_end)


    def get_arc_theta_1(self, theta):
        """
        = lambda theta: return (0, -theta), but I wanted documents like this, thus have these methods
            /
        r1 +---------
            \ t1 = [0, -thata]
             \
        """
        arc_start = 0
        arc_angle = -theta
        return (arc_start, arc_angle)


    def get_arc_theta_2(self, theta):
        """
        = lambda theta: return (0, theta)
             /
            / t2 = [0, theta]
        r1 +---------
            \
        """
        arc_start = 0
        arc_angle = theta
        return (arc_start, arc_angle)


    def get_arc_theta_3(self, theta):
        """
        = lambda theta: return (PI, theta)
               r2
           ----+---
           t3 / \      = [PI, theta]
             /   \
        """
        arc_start = PI
        arc_angle = theta
        return (arc_start, arc_angle)


    def get_arc_theta_4(self, theta):
        """
        = lambda theta: return (0, -theta)
               r2
           ----+---
              / \ t4 = [0, -theta]
             /   \
        """
        arc_start = 0
        arc_angle = -theta
        return (arc_start, arc_angle)


    def get_arc_theta_5(self, theta):
        """
        = lambda theta: return (0, -theta)
             \r2 /
           t5 \ / = [PI-theta, theta]
           ----+---
              / \

        """
        arc_start = PI - theta
        arc_angle = theta
        return (arc_start, arc_angle)


    def get_arc_theta_n(self, n, theta):
        """
        get n-th theta, start and angle
        """
        assert ((0 <= n) and (n < 5))
        theta_f = [self.get_arc_theta_1, self.get_arc_theta_2, self.get_arc_theta_3, self.get_arc_theta_4, self.get_arc_theta_5]
        return theta_f[n](theta)


    def get_arc_2_theta_n(self, n, theta):
        """
        get n-th 2 * theta, start and angle
        This is a bit simpler than get_arc_theta_n, use lambdas.
        """
        assert ((0 <= n) and (n < 2))
        theta_f = [lambda theta: (-theta,   2 * theta),
                   lambda theta: (PI-theta, 2 * theta)]
        return theta_f[n](theta)


    def create_mirror_normal(self):
        """

           mirror_corner_pos   r_2
           +--------------------+------------ line_mirror_up_l1 (l1: mirror up)
           |  |                 |  |
           |--+                 |--+
           |elbow_l1_n1         |elbow_l1_n2 (right angle symbol for (l1) and normal (n2))
           |                    |
           |                    |
           |                    |
           |                    |
        r_1+--------------------+------------ line_normal_left_l2 (l2: normal for the left mirror)
           |  |                 |
           |--+                 |
           |elbow_l2_n1         |
           |                    |
           |                    |
           |                    |
           |                    |
                                line_normal_up_n2 (n2: normal for the up mirror)
           line_mirror_left_n1 (n1: mirro left)

        """
        self.line_mirror_up_l1   = Line(self.mirror_corner_pos, self.mirror_corner_pos + self.mirror_1_length * RIGHT,
                                        color=self.mirror_color,
                                        # color=RED,
                                        stroke_width=self.mirror_stroke_width)

        intersect_l1_n2_pos = self.get_r1()
        self.line_normal_left_l2 = Line(intersect_l1_n2_pos, intersect_l1_n2_pos + self.mirror_1_length * RIGHT,
                                        color=self.mirror_color,
                                        # color=PURPLE,
                                        stroke_width=self.mirror_stroke_width)

        self.line_mirror_left_n1 = Line(self.mirror_corner_pos, self.mirror_corner_pos + self.mirror_2_length * DOWN,
                                        color=self.mirror_color,
                                        # color=GREEN,
                                        stroke_width=self.mirror_stroke_width)

        intersect_l1_n2_pos = self.get_r2()
        self.line_normal_up_n2   = Line(intersect_l1_n2_pos, intersect_l1_n2_pos + self.mirror_1_length * DOWN,
                                        color=self.mirror_color,
                                        # color=YELLOW,
                                        stroke_width=self.mirror_stroke_width)

        self.elbow_l1_n1 = Elbow(width = self.elbow_length, angle=-PI/2, color=self.elbow_color, about_point = ORIGIN)
        self.elbow_l2_n1 = copy.deepcopy(self.elbow_l1_n1)
        self.elbow_l1_n2 = copy.deepcopy(self.elbow_l1_n1)

        self.elbow_l1_n1.move_to(self.mirror_corner_pos + 0.5 * self.elbow_length * (RIGHT + DOWN))
        self.elbow_l2_n1.move_to(self.get_r1() + 0.5 * self.elbow_length * (RIGHT + DOWN))
        self.elbow_l1_n2.move_to(self.get_r2() + 0.5 * self.elbow_length * (RIGHT + DOWN))


        self.parallel_sign_l1  = VGroup()
        l1 = Line(ORIGIN + 0.8 * UP - RIGHT, ORIGIN)
        l2 = Line(ORIGIN - 0.8 * UP - RIGHT, ORIGIN)
        self.parallel_sign_l1.add(l1, l2).set_color(YELLOW).scale(0.3)
        self.parallel_sign_l2  = copy.deepcopy(self.parallel_sign_l1)
        paralle_line_l_offset = 4.5 * RIGHT
        self.parallel_sign_l1.move_to(self.mirror_corner_pos + paralle_line_l_offset)
        self.parallel_sign_l2.move_to(self.get_r1()          + paralle_line_l_offset)

        if (self.is_show_construct):
            self.play(ShowCreation(self.line_mirror_up_l1),   ShowCreation(self.line_mirror_left_n1),
                      ShowCreation(self.line_normal_left_l2), ShowCreation(self.line_normal_up_n2),
                      ShowCreation(self.elbow_l1_n1), ShowCreation(self.elbow_l2_n1), ShowCreation(self.elbow_l1_n2),
                      ShowCreation(self.parallel_sign_l1), ShowCreation(self.parallel_sign_l2))


    def create_rays_lines(self):
        """
        Create (laser) rays
                      r_2
                     +
                    / \
                   /   \
                  /     \line_ray_3
                 /line_  \
                /   ray_2 \
            r_1+           \
                \
                 \
                  \line_ray_1
                   \
        ray_1_theta \
                 ----+
                     ray_1_spos


                   \   / line_m
                    \ /
                     + r_2
                    / \
                   /   \
            \     /     \
             \   /       \
              \ /         \ V: elbow_o2 (parallel sign of o2)
               + r_1       \ line_o2
              / \
             /   \
            /     \
                   \
                    \
          ray_1_spos +
                      \ V: elbow_o1 (parallel sign of o1)
                       \ line_o1

        """

        ray_1_s = self.ray_1_spos
        ray_1_e = self.get_r1()
        self.line_ray_1 = Arrow(ray_1_s, ray_1_e,
                                color=self.ray_1_color, stroke_width = self.ray_1_stroke_width, buff=0)
        ray_2_s = self.get_r1()
        ray_2_e = self.get_r2()
        self.line_ray_2 = Arrow(ray_2_s, ray_2_e,
                                color=self.ray_2_color, stroke_width = self.ray_2_stroke_width, buff=0)
        ray_3_s = self.get_r2()
        ray_3_e = self.get_r2() + self.get_vdir() * self.ray_3_length
        self.line_ray_3 = Arrow(ray_3_s, ray_3_e,
                                color=self.ray_3_color, stroke_width = self.ray_3_stroke_width, buff=0)

        (line_o1_s, line_o1_e) = self.get_line_from_ray(ray_1_s, ray_1_e, self.line_o1_factor)
        (line_m_s,  line_m_e)  = self.get_line_from_ray(ray_2_s, ray_2_e, self.line_m_factor)
        (line_o2_s, line_o2_e) = self.get_line_from_ray(ray_3_s, ray_3_e, self.line_o2_factor)

        self.line_o1  = Line(line_o1_s, line_o1_e, color=self.line_o1_color, stroke_width = self.line_o1_stroke_width)
        self.line_m   = Line(line_m_s,  line_m_e,  color=self.line_m_color,  stroke_width = self.line_m_stroke_width)
        self.line_o2  = Line(line_o2_s, line_o2_e, color=self.line_o2_color, stroke_width = self.line_o2_stroke_width)
        self.elbow_o1 = Elbow(width = self.elbow_length, angle=-PI/2, color=self.elbow_color, about_point = ORIGIN)
        self.elbow_o2 = Elbow(width = self.elbow_length, angle=-PI/2, color=self.elbow_color, about_point = ORIGIN)
        self.elbow_o1.move_to(self.line_o1.get_start() +  1.0 * self.line_o1.get_unit_vector())
        self.elbow_o2.move_to(self.line_o2.get_end()   + -1.0 * self.line_o2.get_unit_vector())


        if (self.is_show_construct):
            self.play(ShowCreation(self.line_ray_1), ShowCreation(self.line_ray_2), ShowCreation(self.line_ray_3),
                      ShowCreation(self.line_o1),    ShowCreation(self.line_m),     ShowCreation(self.line_o2),
                      ShowCreation(self.elbow_o1),   ShowCreation(self.elbow_o2))


    def create_arcs_angles(self):
        """
        Arcs and angles
        Create (laser) rays
                          \
                           \
               tex_theta[4] \ r_2
                         ----+----
              tex_theta[2],x/ \tex_theta[3],y
                           /   \
                          /     \
                         /       \
                        /ray_2    \ray_3
                       /           \
                      /tex_theta[1] \
                  r_1+------         \
                      \tex_theta[0]
                       \
                        \ray_1
                         \
                          \


                           \   / line_m
                            \ /
              tex_2_theta[0] + r_2
                            / \
                           /   \
                    \     /     \
                     \   /       \
                      \ /         \
        tex_2_theta[1] + r_1       \ line_o2
                      / \
                     /   \
                    /     \
                           \
                            \
                             \
                              \ line_o1

        """
        #----- theta-s
        theta = self.ray_1_theta
        self.arc_theta            = []
        self.arc_theta_pos_offset = []
        self.tex_theta            = []
        # reflection points array
        arc_origin_ary = [self.get_r1, self.get_r1, self.get_r2, self.get_r2, self.get_r2]
        for i in range(0,5):
            # arc
            (arc_start, arc_angle) = self.get_arc_theta_n(i, theta)
            self.arc_theta.append(
                Arc(
                    start_angle = arc_start,
                    angle       = arc_angle,
                    radius      = self.arc_theta_radius,
                    color       = self.arc_theta_color,
                    arc_center  = ORIGIN # initial center of the arc is at ORIGIN
                ))
            # Initialize self.arc_theta_pos_offset
            #
            # Arc's center is the arc object center, not the arc (circle)'s center
            # Now the arc_center of all arcs are at the ORIGIN, thus,
            # get_center() gives an offset from the center.
            #          ___
            #             \_
            #               \
            #                | arc
            #  ORIGIN *   +   \
            #             arc.get_center()
            #         |<->|
            #           offset
            #
            self.arc_theta_pos_offset.append(self.arc_theta[i].get_center())
            arc_center = arc_origin_ary[i]() + self.arc_theta_pos_offset[i]
            self.arc_theta[i].move_to(arc_center)

            # tex (\theta), when visualize which one, use the next line
            #     tex_str = r"\theta_{0}".format(i)
            tex_str = r"\theta"
            self.tex_theta.append(TexMobject(tex_str, color=self.tex_theta_color))
            self.tex_theta[i].move_to(arc_origin_ary[i]() + self.tex_theta_position_offset[i])

        # x, y share the the position theta[2] and theta[3]
        self.tex_angle_x = TexMobject(r"x", color=self.tex_theta_color).move_to(self.tex_theta[2])
        self.tex_angle_y = TexMobject(r"y", color=self.tex_theta_color).move_to(self.tex_theta[3])

        if (self.is_show_construct):
            self.play(*[ShowCreation(obj) for obj in self.arc_theta])
            self.play(FadeIn(self.tex_angle_x),  FadeIn(self.tex_angle_y))
            self.play(FadeOut(self.tex_angle_x), FadeOut(self.tex_angle_y))
            self.play(*[FadeIn(obj)       for obj in self.tex_theta])

        #----- 2 theta-s
        self.arc_2_theta            = []
        self.arc_2_theta_pos_offset = []
        self.tex_2_theta            = []
        arc_2_theta_origin_ary = [self.get_r1, self.get_r2]
        for i in range(0,2):
            # arc
            (arc_start, arc_angle) = self.get_arc_2_theta_n(i, theta)
            self.arc_2_theta.append(
                Arc(
                    start_angle = arc_start,
                    angle       = arc_angle,
                    radius      = self.arc_2_theta_radius,
                    color       = self.arc_2_theta_color,
                    arc_center  = ORIGIN
                ))
            # Arc's center is the arc object center, not the arc (circle)'s center
            self.arc_2_theta_pos_offset.append(self.arc_2_theta[i].get_center())
            arc_2_theta_center = arc_2_theta_origin_ary[i]() + self.arc_2_theta_pos_offset[i]
            self.arc_2_theta[i].move_to(arc_2_theta_center)

            # tex (\theta), when visualize which one, use the next line
            # tex_str = r"2\theta_{0}".format(i)
            tex_str = r"2\theta"
            self.tex_2_theta.append(TexMobject(tex_str, color=self.tex_2_theta_color))
            self.tex_2_theta[i].move_to(arc_2_theta_origin_ary[i]() + self.tex_2_theta_position_offset[i])

        if (self.is_show_construct):
            self.play(*[ShowCreation(obj) for obj in self.arc_2_theta])
            self.play(*[FadeIn(obj)       for obj in self.tex_2_theta])



    def create_line_annotation_tex(self):
        """
                    r_2
           +---------+------------ l_1
           |         |
           |         |
           |         |
        r_1+---------+------------ l_2
           |         |
           |         |
           |         |
          n_1       n_2


               \   / m: transversal
                \ /
                 + r_2
                / \
               /   \
        \     /     \
         \   /       \
          \ /         \
           + r_1       \ o_2
          / \
         /   \
        /     \
               \
                \
                 \
                  \ o_1
        """
        line_l1_offset = 0.4 * RIGHT
        self.tex_line_l1_pos = self.line_mirror_up_l1.get_end() + line_l1_offset
        line_l2_offset = 0.4 * RIGHT
        self.tex_line_l2_pos = self.line_normal_left_l2.get_end() + line_l2_offset

        line_n1_offset = 0.4 * DOWN
        self.tex_line_n1_pos = self.line_mirror_left_n1.get_end() + line_n1_offset
        line_n2_offset = 0.4 * DOWN
        self.tex_line_n2_pos = self.line_normal_up_n2.get_end() + line_n2_offset

        line_o1_offset = 0.4 * UP
        self.tex_line_o1_pos = self.line_o1.get_start() + line_o1_offset
        line_o2_offset = 0.4 * UP
        self.tex_line_o2_pos = self.line_o2.get_end()   + line_o2_offset

        line_m_offset = 1.4 * RIGHT + 0.35 * UP
        self.tex_line_m_pos  = self.line_m.get_end()  + line_m_offset

        self.tex_line_l1 = TexMobject(r"l_{1}", color=WHITE).move_to(self.tex_line_l1_pos)
        self.tex_line_l2 = TexMobject(r"l_{2}", color=WHITE).move_to(self.tex_line_l2_pos)
        self.tex_line_n1 = TexMobject(r"n_{1}", color=WHITE).move_to(self.tex_line_n1_pos)
        self.tex_line_n2 = TexMobject(r"n_{2}", color=WHITE).move_to(self.tex_line_n2_pos)
        self.tex_line_o1 = TexMobject(r"o_{1}", color=WHITE).move_to(self.tex_line_o1_pos)
        self.tex_line_o2 = TexMobject(r"o_{2}", color=WHITE).move_to(self.tex_line_o2_pos)
        self.tex_line_m  = TexMobject(r"m", r"\text{: transversal}", color=WHITE).move_to(self.tex_line_m_pos)

        tex_line_list = [self.tex_line_l1, self.tex_line_l2,
                         self.tex_line_n1, self.tex_line_n2,
                         self.tex_line_o1, self.tex_line_o2,
                         self.tex_line_m]
        if (self.is_show_construct):
            self.play(*[ShowCreation(obj) for obj in tex_line_list])



    def animate_setup(self):
        """Start the setup: the corner reflector: T1
        """

        if (self.is_skip_to_end):
            # Add mirror (l1, n1) only
            self.play(*[FadeIn(mobj) for mobj in
                        [self.line_mirror_up_l1, self.line_mirror_left_n1]])
            return

        self.play(ShowCreation(self.line_mirror_up_l1),   ShowCreation(self.line_mirror_left_n1))
        self.wait(self.wait_time)

        self.play(ShowCreation(self.elbow_l1_n1))
        self.wait(self.wait_time)

        self.play(FadeOut(self.elbow_l1_n1))
        self.wait(self.wait_time)


    def animate_incident_ray(self):
        """
        Incident ray: T2
        Normal, show angles: T3, T4, T5
        Same corresponding angles, l1||l2: T6
        """
        # T6 Mobjects
        text_corresponding_pos = 3.2 * RIGHT + 1.0 * UP
        text_corresponding = TextMobject(r"Corresponding angles", color=WHITE).move_to(text_corresponding_pos)

        # get left position of the text
        arrow_start    = text_corresponding.get_critical_point(LEFT) + -0.2 * RIGHT
        arrow_corres_1 = Arrow(arrow_start, self.mirror_corner_pos + 0.6 * RIGHT + -0.2 * UP,
                               color=BLUE, stroke_width = 4, buff=0)
        arrow_corres_2 = Arrow(arrow_start, self.get_r1()          + 0.6 * RIGHT + -0.2 * UP,
                               color=BLUE, stroke_width = 4, buff=0)

        if (self.is_skip_to_end):
            # l1, l2, parallel only
            self.play(*[FadeIn(mobj) for mobj in
                        [self.line_normal_left_l2,
                         self.tex_line_l1,      self.tex_line_l2,
                         self.parallel_sign_l1, self.parallel_sign_l2]])
            return

        # T2: incident ray
        self.play(ShowCreation(self.line_ray_1))
        self.wait(self.wait_time)

        # T3: draw the normal
        self.play(ShowCreation(self.line_normal_left_l2))
        self.wait(self.wait_time)

        # T4, T5: show two lines (l1, l2) are perpendicular to n1
        self.play(FadeOut(self.line_ray_1), ShowCreation(self.elbow_l2_n1))
        self.wait(self.wait_time)
        self.play(ShowCreation(self.elbow_l1_n1))
        self.wait(self.wait_time)

        # T6: corresponding angles, show parallel
        self.play(FadeIn(self.tex_line_l1), FadeIn(self.tex_line_l2))
        self.play(FadeIn(text_corresponding), ShowCreation(arrow_corres_1), ShowCreation(arrow_corres_2))
        self.wait(self.wait_time)
        self.play(ShowCreation(self.parallel_sign_l1), ShowCreation(self.parallel_sign_l2))
        self.wait(self.wait_time)

        # Remove corresponding angles and right angles
        self.play(FadeOut(text_corresponding), FadeOut(arrow_corres_1), FadeOut(arrow_corres_2),
                  FadeOut(self.elbow_l2_n1), FadeOut(self.elbow_l1_n1))
        self.wait(self.wait_time)



    def animate_reflection_1_ray(self):
        """
        Incident ray 1: T7
        Show angles:    T8
        """

        if (self.is_skip_to_end):
            self.play(*[FadeIn(mobj) for mobj in
                        [self.line_ray_1,   self.line_ray_2,
                         self.arc_theta[0], self.tex_theta[0],
                         self.arc_theta[1], self.tex_theta[1]]])
            return


        # T7: Show incident ray 1, normal
        self.play(ShowCreation(self.line_ray_1))
        self.wait(self.wait_time)

        # T8: reflection ray 2, angle theta[0]
        self.play(ShowCreation(self.line_ray_2))
        self.wait(self.wait_time)
        self.play(ShowCreation(self.arc_theta[0]), FadeIn(self.tex_theta[0]))
        self.wait(self.wait_time)
        self.play(ShowCreation(self.arc_theta[1]), FadeIn(self.tex_theta[1]))
        self.wait(self.wait_time)


    def animate_reflection_2_ray(self):
        """
        Reflection ray 1, ray 2, Show the angle x and l1||l2 again: T9
        Show transversal: T10
        Show only prallel and transversal, x == theta: T11
        Put back the mirrors: T12
        """

        # tex l1, tex l2, parallel signs are shown, but removed at the end
        fadeout_at_end_list = [
            self.tex_line_l1, self.parallel_sign_l1,
            self.tex_line_l2, self.parallel_sign_l2]

        if (self.is_skip_to_end):
            self.play(*[FadeIn(mobj) for mobj in
                        [self.line_normal_up_n2,
                         self.line_ray_3,
                         self.arc_theta[2], self.tex_theta[2]]],
                      *[FadeOut(mobj) for mobj in fadeout_at_end_list])
            return


        # T9: reflection ray 3, normal n2, angle theta[2], angle theta[3]
        self.play(ShowCreation(self.line_normal_up_n2), ShowCreation(self.elbow_l1_n2))
        self.wait(self.wait_time)
        self.play(FadeOut(self.elbow_l1_n2))
        self.wait(self.wait_time)
        self.play(ShowCreation(self.line_ray_3))
        self.wait(self.wait_time)
        self.play(ShowCreation(self.arc_theta[2]), FadeIn(self.tex_angle_x))
        self.wait(self.wait_time)

        # T10: fadeout n1, n2, ray1, ray3, arc[0], theta[0], arc[1], theta[0], fadein l_m
        non_parallel_creation_push = [self.line_mirror_left_n1,
                                      self.line_normal_up_n2,
                                      self.line_ray_1,
                                      self.line_ray_3,
                                      self.arc_theta[0]]
        non_parallel_fade_push     = [self.tex_theta[0]]

        self.play(*[FadeOut(mobj) for mobj in non_parallel_creation_push],
                  *[FadeOut(mobj) for mobj in non_parallel_fade_push])
        self.wait(self.wait_time)
        self.play(ShowCreation(self.line_m))
        self.wait(self.wait_time)
        self.play(FadeIn(self.tex_line_m))
        self.wait(self.wait_time)

        # T10 tmp Mobjects
        text_alt_pos = 3.2 * RIGHT + 1.0 * UP
        text_alt     = TextMobject(r"Alternate angles", color=WHITE).move_to(text_alt_pos)
        tex_x_eq_t   = TexMobject( r"x = \theta", color=WHITE).move_to(text_alt_pos + DOWN)

        # get left position of the text
        arrow_start = text_alt.get_critical_point(LEFT) + -0.4 * RIGHT
        arrow_alt_1 = Arrow(arrow_start, self.get_r2() + -0.1 * RIGHT + -0.4 * UP,
                            color=BLUE, stroke_width = 4, buff=0)
        arrow_alt_2 = Arrow(arrow_start, self.get_r1() +  1.8 * RIGHT +  0.6 * UP,
                            color=BLUE, stroke_width = 4, buff=0)

        # T10: m: transversal
        self.play(FadeIn(text_alt),
                  ShowCreation(arrow_alt_1),
                  ShowCreation(arrow_alt_2))
        self.wait(self.wait_time)

        # T11: x = theta
        self.play(FadeIn(tex_x_eq_t))
        self.wait(self.wait_time)
        self.play(FadeOut(self.tex_angle_x), FadeIn(self.tex_theta[2]))
        self.wait(self.wait_time)

        # T12: restore the mirrors and rays. hide l1, l2, parallel signs
        fadeout_list = [text_alt, tex_x_eq_t, arrow_alt_1, arrow_alt_2,
                        self.line_m,      self.tex_line_m]
        fadeout_list.extend(fadeout_at_end_list)

        self.play(*[FadeOut(mobj) for mobj in fadeout_list])
        self.play(*[ShowCreation(mobj) for mobj in non_parallel_creation_push],
                  *[FadeIn(mobj)       for mobj in non_parallel_fade_push])
        self.wait(self.wait_time)


    def animate_2nd_reflection_y_theta(self):
        """
        T15-1: show angle y
        T15-2: mirror reflection y = theta
        """

        if (self.is_skip_to_end):
            self.add(self.arc_theta[3], self.tex_theta[3])
            return

        y_work = copy.deepcopy(self.tex_angle_y)
        self.play(ShowCreation(self.arc_theta[3]), FadeIn(y_work))
        self.wait(self.wait_time)

        self.play(FadeOut(y_work))
        self.play(FadeIn(self.tex_theta[3]))
        self.wait(self.wait_time)


    def animate_show_upper_2_theta(self):
        """
        Show upper (2*theta)
        T16-1: extend line o1
        T16-2: push non-vertical angle objects
        T16-3: show vertical angles text
        T16-4: pop  non-vertical angle objects
        T17-1: (theta, theta) -> (theta + theta) -> 2 theta
        T17-2: remove the upper mirror and adjust 2 theta
        """

        # push and pop list
        push_tex_list_1 = [self.tex_theta[2]]
        push_mob_list_1 = [self.arc_theta[2], self.line_ray_2]

        # push list
        push_tex_list_2 = [self.tex_theta[0], self.tex_theta[1]]
        push_mob_list_2 = [self.arc_theta[0], self.arc_theta[1],
                          # mirror left, normal at r2
                          self.line_mirror_left_n1, self.line_normal_up_n2,
                          # normal at r1
                          self.line_normal_left_l2,
                          # ray_1, ray_2
                          self.line_ray_1, self.line_ray_3]

        if (self.is_skip_to_end):
            self.remove(*[t for t in push_tex_list_2])
            self.remove(*[m for m in push_mob_list_2])
            self.remove(self.line_mirror_up_l1, self.tex_theta[3], self.arc_theta[3])
            self.remove(self.tex_theta[2])
            self.add(self.line_o2)
            self.add(self.arc_theta[4])
            self.add(self.tex_2_theta[1])
            return


        # T16-1: extend line o1
        self.play(ShowCreation(self.line_o2))
        self.wait(self.wait_time)

        # T16-2: push non-vertical angle objects
        self.play(*[FadeOut(tex) for tex in push_tex_list_1],
                  *[FadeOut(tex) for tex in push_tex_list_2],
                  *[FadeOut(mob) for mob in push_mob_list_1],
                  *[FadeOut(mob) for mob in push_mob_list_2])
        self.wait(self.wait_time)

        # T16-3: show vertical angles text
        self.play(ShowCreation(self.arc_theta[4]))
        self.wait(self.wait_time)

        # temporal text
        text_vertical_pos = -2.0 * RIGHT + -1.0 * UP
        text_vertical     = TextMobject(r"Vertical angles", color=WHITE).move_to(text_vertical_pos)

        arrow_start  = text_vertical.get_critical_point(UP) + 0.2 * UP
        arrow_vert_1 = Arrow(arrow_start, self.get_r2() + -0.8 * RIGHT + -0.2 * UP,
                             color=BLUE, stroke_width = 4, buff=0)
        arrow_vert_2 = Arrow(arrow_start, self.get_r2() + +0.5 * RIGHT + -0.5 * UP,
                             color=BLUE, stroke_width = 4, buff=0)
        self.play(ShowCreation(arrow_vert_1), ShowCreation(arrow_vert_2), FadeIn(text_vertical))
        self.wait(self.wait_time)

        # Show vertical angle theta
        self.play(FadeIn(self.tex_theta[4]))
        self.wait(self.wait_time)

        # fadeout vertical angle annotation (text and arrows)
        self.play(FadeOut(arrow_vert_1), FadeOut(arrow_vert_2), FadeOut(text_vertical))
        self.wait(self.wait_time)


        # T16-4: pop back ray 2 and theta
        self.play(*[FadeIn(tex)       for tex in push_tex_list_1],
                  *[ShowCreation(mob) for mob in push_mob_list_1])
        self.wait(self.wait_time)

        # T17-1: (theta, theta) -> (theta + theta) -> 2 theta

        #  replace with copied works
        theta_work_2 = copy.deepcopy(self.tex_theta[2])
        theta_work_4 = copy.deepcopy(self.tex_theta[4])
        self.remove(self.tex_theta[2], self.tex_theta[4])
        self.add(theta_work_2, theta_work_4)

        tex_theta_p_theta_pos = theta_work_4.get_center() + - 0.2 * RIGHT
        tex_theta_p_theta     = TexMobject( r"\theta + \theta", color=WHITE).move_to(tex_theta_p_theta_pos)
        self.play(Transform(theta_work_2, tex_theta_p_theta), FadeOut(theta_work_4))
        self.wait(self.wait_time)

        # T17-2: remove the upper mirror and adjust 2 theta
        self.play(FadeOut(self.line_mirror_up_l1), FadeOut(self.tex_theta[3]), FadeOut(self.arc_theta[3]))
        self.wait(self.wait_time)

        self.play(Transform(theta_work_2, self.tex_2_theta[1]))

        # replace the work with the invariants
        self.remove(theta_work_2)
        self.add(self.tex_2_theta[1])

        self.wait(self.wait_time)


    def animate_show_lower_2_theta(self):
        """
        Show lower (2*theta)
        T18, T19: show theta + theta = 2 theta, remove normal at r1
        T20: remove left mirror, extend o2
        T21: coin the line name text o1, text o2, text m
        T22-1: show alternate angles, parallel o1||o2
        T22-2: show parallel ray1 || ray3
        T22-3: restore the mirrors and rays
        """

        ray_list        = [self.line_ray_1, self.line_ray_2, self.line_ray_3] # rays
        mirror_list     = [self.line_mirror_up_l1, self.line_mirror_left_n1]  # mirrors

        if (self.is_skip_to_end):
            self.remove(self.line_ray_2, self.line_o2, self.tex_2_theta[1], self.arc_theta[2], self.arc_theta[4])
            self.add(*ray_list, *mirror_list)
            return


        # put back to the left mirror, ray 1, angles
        restore_list = [self.line_mirror_left_n1, self.line_normal_left_l2,
                        self.line_ray_1,
                        self.arc_theta[0], self.tex_theta[0],
                        self.arc_theta[1], self.tex_theta[1]]
        self.play(*[FadeIn(mobj) for mobj in restore_list])

        # T19: (theta, theta) -> (theta + theta) -> 2 theta

        #  replace with copied works
        theta_work_0 = copy.deepcopy(self.tex_theta[0])
        theta_work_1 = copy.deepcopy(self.tex_theta[1])
        self.remove(self.tex_theta[0], self.tex_theta[1])
        self.add(theta_work_0, theta_work_1)

        tex_theta_p_theta_pos = theta_work_1.get_center() + +0.4 * RIGHT
        tex_theta_p_theta     = TexMobject( r"\theta + \theta", color=WHITE).move_to(tex_theta_p_theta_pos)
        self.play(Transform(theta_work_0, tex_theta_p_theta), FadeOut(theta_work_1))
        self.wait(self.wait_time)

        # remove left mirror normal
        self.play(FadeOut(self.line_normal_left_l2))

        # theta + theta -> 2 theta
        self.play(Transform(theta_work_0, self.tex_2_theta[0]))

        # replace the work with the invariants
        self.remove(theta_work_0)
        self.add(self.tex_2_theta[0])
        self.wait(self.wait_time)

        # T20: remove left mirror, extend o2
        self.play(FadeOut(self.line_mirror_left_n1),
                  ShowCreation(self.line_o1), FadeOut(self.line_ray_1),
                  ShowCreation(self.line_m),  FadeOut(self.line_ray_2))
        self.wait(self.wait_time)
        # T21: coin the line name text o1, text o2, text m
        self.play(FadeIn(self.tex_line_o1))
        self.wait(self.wait_time)
        self.play(FadeIn(self.tex_line_o2))
        self.wait(self.wait_time)
        self.play(FadeIn(self.tex_line_m[0]))
        self.wait(self.wait_time)

        # T22-1: show alternate angles, parallel o1||o2

        text_alt_pos = 3.0 * RIGHT + 2.0 * UP
        text_alt     = TextMobject(r"Alternate angles", color=WHITE).move_to(text_alt_pos)

        # get left position of the text
        arrow_start = text_alt.get_critical_point(LEFT) + -0.4 * RIGHT
        arrow_alt_1 = Arrow(arrow_start, self.get_r2() +  0.4 * RIGHT +  0.0 * UP,
                            color=BLUE, stroke_width = 4, buff=0)
        arrow_alt_2 = Arrow(arrow_start, self.get_r1() +  1.5 * RIGHT +  0.3 * UP,
                            color=BLUE, stroke_width = 4, buff=0)
        self.play(FadeIn(text_alt),
                  ShowCreation(arrow_alt_1), ShowCreation(arrow_alt_2))
        self.wait(self.wait_time)

        # add transversal
        self.play(FadeIn(self.tex_line_m[1]))
        self.wait(self.wait_time)

        # T22-2: show parallel ray1 || ray3
        tex_2_theta_eq_2_theta = TexMobject(r"2\theta", r"=", r"2\theta", color=WHITE).\
                                                            move_to(text_alt_pos + -1.0 * UP)
        work_2_thetas = [copy.deepcopy(self.tex_2_theta[0]), copy.deepcopy(self.tex_2_theta[1])]
        self.play(FadeIn(tex_2_theta_eq_2_theta[1]))
        self.wait(self.wait_time)

        self.play(ApplyMethod(work_2_thetas[0].move_to, tex_2_theta_eq_2_theta[0].get_center()),
                  ApplyMethod(work_2_thetas[1].move_to, tex_2_theta_eq_2_theta[2].get_center()))
        self.remove(work_2_thetas[0], work_2_thetas[1])
        self.add(tex_2_theta_eq_2_theta[0], tex_2_theta_eq_2_theta[2]) # replace the work with tex_2_theta_eq_2_theta
        self.wait(self.wait_time)

        # this means o1||o2
        tex_o1_parallel_o2     = TexMobject(r"o_1 \parallel o_2", color=WHITE).move_to(text_alt_pos + -1.0 * UP)
        self.play(Transform(tex_2_theta_eq_2_theta, tex_o1_parallel_o2))
        self.wait(self.wait_time)

        # Remove the alternate angles and annotations
        self.play(FadeOut(text_alt),
                  FadeOut(arrow_alt_1), FadeOut(arrow_alt_2),
                  FadeOut(self.tex_line_m),
                  FadeOut(tex_2_theta_eq_2_theta))
        self.wait(self.wait_time)

        # T22-3: restore the mirrors and rays
        annotation_list = [self.tex_2_theta[0], self.tex_2_theta[1],          # 2 theta
                           self.line_o1,  self.line_o2, self.line_m,          # lines
                           self.tex_line_o1, self.tex_line_o2,                # text o1, o2
                           self.elbow_o1,  self.elbow_o2,                     # parallel signs
                           self.arc_theta[0], self.arc_theta[1],              # arcs
                           self.arc_theta[2], self.arc_theta[4]]

        self.play(*[FadeOut(mobj) for mobj in annotation_list],
                  *[FadeIn(mobj)  for mobj in ray_list])
        self.wait(self.wait_time)
        self.play(*[FadeIn(mobj)  for mobj in mirror_list])

        self.wait(self.wait_time)


    def construct(self):
        """Corner cube animation main
        """

        # Create mobjects
        self.is_show_construct = False
        self.create_mirror_normal()
        self.create_rays_lines()
        self.create_arcs_angles()
        self.create_line_annotation_tex()

        # animation
        # self.is_skip_to_end = True
        self.animate_setup()
        self.animate_incident_ray()
        self.animate_reflection_1_ray()
        self.animate_reflection_2_ray()
        self.animate_2nd_reflection_y_theta()
        self.animate_show_upper_2_theta()
        self.animate_show_lower_2_theta()

        self.wait(5)
