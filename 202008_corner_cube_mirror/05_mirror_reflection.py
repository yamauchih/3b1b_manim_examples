# -*- coding: utf-8; -*-
#
# Section 5: Mirror reflection
#
#    (C) 2020 Hitoshi Yamauchi
#
# References: 3Blue1Brown, Theorem of Beethoven (manim tutorial)
#
#  cd data/gitdata/manim
#  source manim-venv/bin/activate
#
# Full resolution
#   python3 -m manim 05_mirror_reflection.py MirrorReflection01 --resolution 720,1280 -p --high_quality
# Preview resolution
#   python3 -m manim 05_mirror_reflection.py MirrorReflection01 --resolution 360,640 -pl
#   python3 -m manim 05_mirror_reflection.py MirrorReflection01 --resolution 360,640 -i --high_quality
# -i as gif


from manimlib.imports import *
import os, copy
import pyclbr


class MirrorReflection01(Scene):
    """05. mirror reflection 01
    Show a mirror surface as a line
    Show what is normal
    """
    CONFIG={
        # shared variables
        "wait_time": 1,

        # mirror
        "mirror_width":  7,
        "mirror_origin": ORIGIN + 2 * LEFT + 2 * DOWN,
        "mirror_color":  WHITE,
        "mirror_line":   None,

        # mirror normal
        "text_normal_fig":   None,
        "text_mirror_fig":   None,
        "normal_length": 4,
        "normal_color":  WHITE,
        "normal_line":   None,
        "normal_arrow":  None,
        "mirror_reflect_tex_scale": 1.4,


        # right angle (90 degree) sign between mirror and normal
        "right_right_angle_len": 0.4,
        "left_right_angle_len":  0.4,
        "right_right_angle":    None,
        "left_right_angle":     None,


        # incident/reflected angle (incident angle == reflected angle)
        "incident_angle":  PI/6,
        "reflected_angle":  PI/6,

        # incident ray
        "arrow_incident_color":    YELLOW,
        "arc_incident_radius":     1.0,
        "arc_incident_tan_radius": 0.8,
        "arc_incident_color":      YELLOW,
        "arrow_incident":          None,
        "arc_incident":            None,
        "text_incident_fig":       None,
        "tex_theta_in":            None,
        "tex_theta_in_color":      YELLOW,

        # reflected ray
        "arrow_reflected_color":    BLUE,
        "arc_reflected_radius":     1.0,
        "arc_reflected_tan_radius": 0.8,
        "arc_reflected_color":      BLUE,
        "arrow_reflected":          None,
        "arc_reflected":            None,
        "tex_theta_ref":            None,
        "tex_theta_ref_color":      BLUE,

        # incident tangent
        "arc_incident_tan":      None,
        "tex_theta_in_tan":      None,

        # reflected tangent
        "arc_reflected_tan":     None,
        "tex_theta_ref_tan":     None,

        # mirror and tangent equation
        "text_mirror":               None,
        "tex_derive_ti_tr":          None,
        "tex_derive_tan_tin_tan_tr": None,

        # equality: theta_i = theta_r = theta_0
        "theta_0": None,
        # equality: 90 - theta_i = 90 - theta_r = theta_0'
        "theta_0_d": None,
    }


    def create_mirror_normal(self):
        """create a mirror as a line and a normal as a line
        """
        # mirror
        self.mirror_line = Line(ORIGIN, ORIGIN + self.mirror_width * RIGHT, color=self.mirror_color).move_to(self.mirror_origin)

        # normal
        normal_center = self.mirror_origin + 0.5 * self.normal_length * UP
        self.normal_line  = Line (ORIGIN, ORIGIN + self.normal_length * UP, color=self.normal_color).move_to(normal_center)
        self.normal_arrow = Arrow(ORIGIN, ORIGIN + self.normal_length * UP, color=self.normal_color,
                                  stroke_width = 4, buff=0).move_to(normal_center)

        # text normal
        self.text_normal_fig = TextMobject(r"Normal").scale(1.4).move_to(-0.2 * RIGHT +  0.0 * UP)
        self.text_mirror_fig = TextMobject(r"Mirror").scale(1.4).move_to( 3.0 * RIGHT + -2.0 * UP)

        # right side 90 degree angle (right side right angle)
        self.right_right_angle = Elbow(width = self.right_right_angle_len,
                                       angle = 0, color = YELLOW, about_point = ORIGIN)
        self.right_right_angle.move_to(self.mirror_origin +
                                       0.5 * self.right_right_angle_len * RIGHT + 0.5 * self.right_right_angle_len * UP)

        # left side 90 degree angle (left side right angle)
        self.left_right_angle = Elbow(width = self.left_right_angle_len,
                                       angle = PI/2, color = YELLOW, about_point = ORIGIN)
        self.left_right_angle.move_to(self.mirror_origin +
                                      -0.5 * self.left_right_angle_len * RIGHT + 0.5 * self.left_right_angle_len * UP)


    def animate_mirror_normal(self):
        """Show normal
        """
        normal_line_work  = copy.deepcopy(self.normal_line)
        normal_arrow_work = copy.deepcopy(self.normal_arrow) # .shift(0.2 * RIGHT)

        self.play(ShowCreation(self.mirror_line), FadeIn(self.text_mirror_fig))

        self.play(ShowCreation(normal_line_work),
                  ShowCreation(self.left_right_angle),
                  ShowCreation(self.right_right_angle),
                  FadeIn(self.text_normal_fig))
        self.wait(self.wait_time)

        self.play(FadeOut(normal_line_work),
                  FadeOut(self.left_right_angle),
                  FadeOut(self.right_right_angle),
                  FadeOut(self.text_normal_fig),
                  FadeOut(self.text_mirror_fig))


    def animate_normal_on_curve(self):
        """When the mirror is curved, normal are useful.

        @param mirror_line current displayed mirror line
        """

        mirror_line_work = copy.deepcopy(self.mirror_line)

        # create a curved mirror by an arc
        arc_1 = Arc(
            start_angle =  PI,
            angle       = -PI,
            radius      = self.mirror_width / 2,
            color       = WHITE,
            arc_center  = self.mirror_origin
        )

        # self.play(ShowCreation(arc_1))

        # create source normals (on the mirror)
        normal_color        = WHITE
        normal_stroke_width = 4
        normal_arrow_src    = []
        for x in range(-3, 4, 1):
            arrow_s = Arrow(self.mirror_origin + x * RIGHT,
                            self.mirror_origin + UP + x * RIGHT,
                            stroke_width = normal_stroke_width, color = normal_color, buff=0)
            normal_arrow_src.append(arrow_s)

        normal_arrow_src_work = copy.deepcopy(normal_arrow_src)
        normal_arrow_src_org  = copy.deepcopy(normal_arrow_src)

        # destination normals (on the arc)
        radius = self.mirror_width / 2
        normal_arrow_dst = []
        for dst_x in range(-3, 4, 1):
            dst_y       = math.sqrt(radius**2 - dst_x**2)
            dst_o       = dst_x * RIGHT + dst_y * UP + self.mirror_origin # destination normal vector origin (start)
            dst_normal  = (dst_o - self.mirror_origin)
            norm        = np.linalg.norm(dst_normal)                      # just radius, though
            dst_normal /= norm
            arrow_d     = Arrow(dst_o, dst_o + dst_normal, stroke_width = normal_stroke_width, color=normal_color, buff=0)
            normal_arrow_dst.append(arrow_d)

        normal_src_creation = [ShowCreation(mobj) for mobj in normal_arrow_src_work]
        self.add(mirror_line_work)
        self.play(FadeOut(self.mirror_line), *normal_src_creation)

        text_normal_1 = TextMobject(r"Normal is different everywhere on a curve.").move_to(0.0 * RIGHT + 3.0 * UP)
        text_normal_2 = TextMobject(r"But the same on a plane.").move_to(0.0 * RIGHT + 3.0 * UP)
        self.play(FadeIn(text_normal_1))

        normal_transform = [ReplacementTransform(m1, m2) for (m1, m2) in zip(normal_arrow_src_work, normal_arrow_dst)]
        self.play(ReplacementTransform(mirror_line_work, arc_1), *normal_transform)
        self.wait(self.wait_time)

        mirror_line_dst = copy.deepcopy(self.mirror_line)
        normal_transform_reverse = [ReplacementTransform(m1, m2) for (m1, m2) in zip(normal_arrow_dst, normal_arrow_src_org)]
        self.play(FadeOut(text_normal_1), FadeIn(text_normal_2))
        self.play(ReplacementTransform(arc_1, mirror_line_dst), *normal_transform_reverse)
        self.wait(self.wait_time)

        fadeout_normals = [FadeOut(mobj) for mobj in normal_arrow_src_org]
        self.add(self.mirror_line)
        self.play(FadeOut(mirror_line_dst), *fadeout_normals)
        self.play(FadeOut(text_normal_2))


    def create_incident_reflected(self):
        """Show specular reflection
        1. add the normal
        2. show an  incident  ray
        3. show the incident  angle
        4. show an  reflected ray
        5. show the reflected angle

        """
        # 1. add the normal
        # MObject already constructed

        # 2. show an  incident ray
        #
        # |<-dx->|
        #
        # +      |
        #  \     |
        #   \    |
        #    \   |
        #     \ i|    i: incident angle
        #      \ |
        #       \|
        # -------*-------
        #
        delta_x = self.normal_length * math.tan(self.incident_angle)
        self.arrow_incident = Arrow(ORIGIN + -delta_x * RIGHT + self.normal_length * UP,
                                    ORIGIN,
                                    color=self.arrow_incident_color,
                                    stroke_width = 4, buff=0).shift(self.mirror_origin)


        # 3. show the incident angle
        self.arc_incident = Arc(
            start_angle = PI/2,
            angle       = self.incident_angle,
            radius      = self.arc_incident_radius,
            color       = self.arc_incident_color,
            arc_center  = self.mirror_origin
        )

        self.text_incident_fig = TextMobject(r"Incident ray").set_color(self.tex_theta_in_color).\
                                 scale(1.2).move_to(-5.0 * RIGHT + -1.0 * UP)
        theta_in_pos_offset = -0.5 * RIGHT + 1.9 * UP
        self.tex_theta_in = TexMobject(r"\theta_{i}", color=self.arc_incident_color).move_to(self.mirror_origin + theta_in_pos_offset)


        # 4. show an  reflected ray
        #
        # |<-dx->|
        #
        # +      |      +
        #  \     |     /
        #   \    |    /
        #    \   |   /
        #     \ i|r /  i: incident angle
        #      \ | /   r: reflected angle
        #       \|/
        # -------*-------
        #
        delta_x = self.normal_length * math.tan(self.reflected_angle)
        self.arrow_reflected = Arrow(ORIGIN,
                                    ORIGIN +  delta_x * RIGHT + self.normal_length * UP,
                                    color=self.arrow_reflected_color,
                                    stroke_width = 4, buff=0).shift(self.mirror_origin)

        # 5. show the reflected angle
        self.arc_reflected = Arc(
            start_angle = PI/2 - self.reflected_angle,
            angle       = self.reflected_angle,
            radius      = self.arc_reflected_radius,
            color       = self.arc_reflected_color,
            arc_center  = self.mirror_origin
        )
        self.text_reflected_fig = TextMobject(r"Reflected ray").set_color(self.tex_theta_ref_color).\
                                  scale(1.2).move_to(1.0 * RIGHT + -1.0 * UP)

        theta_out_pos_offset =  0.5 * RIGHT + 1.9 * UP
        self.tex_theta_ref = TexMobject(r"\theta_{r}", color=self.arc_reflected_color).move_to(self.mirror_origin + theta_out_pos_offset)

        self.tex_mirror_reflect = TexMobject(r"\text{Specular reflection: }",
                                             r"\theta_{i}",
                                             r"=",
                                             r"\theta_{r}")
        self.tex_mirror_reflect.scale(self.mirror_reflect_tex_scale).move_to(-1.0 * RIGHT + 3.0 * UP)
        self.tex_mirror_reflect[1].set_color(self.arc_incident_color)
        self.tex_mirror_reflect[3].set_color(self.arc_reflected_color)



    def animate_incident_reflected(self):
        """Animate incident/reflected ray
        """

        # animate normal
        self.play(ShowCreation(self.normal_line))
        self.wait(self.wait_time)

        # animate incident ray
        self.play(ShowCreation(self.arrow_incident), FadeIn(self.text_incident_fig))
        self.play(ShowCreation(self.arc_incident),   FadeIn(self.tex_theta_in))
        self.wait(self.wait_time)

        # animate reflected ray
        self.play(ShowCreation(self.arrow_reflected), FadeOut(self.text_incident_fig), FadeIn(self.text_reflected_fig))
        self.play(ShowCreation(self.arc_reflected), FadeIn(self.tex_theta_ref))
        self.wait(self.wait_time)

        # show title
        theta_in_work  = copy.deepcopy(self.tex_theta_in)
        theta_out_work = copy.deepcopy(self.tex_theta_ref)

        self.add(theta_in_work, theta_out_work)
        self.play(FadeOut(self.text_reflected_fig),
                  FadeIn(self.tex_mirror_reflect[0]), FadeIn(self.tex_mirror_reflect[2]))
        self.wait(self.wait_time)

        # Note override self.tex_mirror_reflect
        self.play(ReplacementTransform(theta_in_work,   self.tex_mirror_reflect[1]),
                  ReplacementTransform(theta_out_work,  self.tex_mirror_reflect[3]))
        self.wait(self.wait_time)

        self.play(FadeOut(self.tex_mirror_reflect))
        self.play(FadeOut(self.arrow_incident),  FadeOut(self.arc_incident),
                  FadeOut(self.tex_theta_in),
                  FadeOut(self.arrow_reflected), FadeOut(self.arc_reflected),
                  FadeOut(self.tex_theta_ref))
        self.play(FadeOut(self.normal_line))

        self.wait(self.wait_time)



    def animate_tangent_on_curve(self):
        """When the mirror is curved, tangents are also useful.

        @param mirror_line current displayed mirror line
        """

        mirror_line_work = copy.deepcopy(self.mirror_line)

        # create a curved mirror by an arc
        arc_1 = Arc(
            start_angle =  PI,
            angle       = -PI,
            radius      = self.mirror_width / 2,
            color       = WHITE,
            arc_center  = self.mirror_origin
        )

        # create source tangent (on the mirror)
        tangent_color        = GREEN
        tangent_stroke_width = 10
        tangent_length_coeff = 0.9

        # Add one tangent vector with text "Tangent"
        text_tangent_0 = TextMobject(r"Tangent").scale(1.4).move_to(-2.0 * RIGHT + -1.0 * UP)
        arrow_one_tan  = Arrow(self.mirror_origin,
                               self.mirror_origin + 2.0 * RIGHT,
                               stroke_width = tangent_stroke_width * 8, color = tangent_color, buff=0)
        self.play(FadeIn(text_tangent_0),
                  ShowCreation(arrow_one_tan))
        self.wait(self.wait_time)
        self.play(FadeOut(text_tangent_0),
                  FadeOut(arrow_one_tan))
        self.wait(self.wait_time)

        # Many tangent vectors
        tangent_arrow_src    = []
        for x in range(-3, 4, 1):
            arrow_s = Arrow(self.mirror_origin + x * RIGHT,
                            self.mirror_origin + x * RIGHT + tangent_length_coeff * RIGHT, # length adjustment to a bit shorter
                            stroke_width = tangent_stroke_width, color = tangent_color, buff=0)
            tangent_arrow_src.append(arrow_s)

        tangent_arrow_src_work = copy.deepcopy(tangent_arrow_src)
        tangent_arrow_src_org  = copy.deepcopy(tangent_arrow_src)

        # destination tangents (on the arc)
        radius = self.mirror_width / 2
        tangent_arrow_dst = []
        for dst_x in range(-3, 4, 1):
            dst_y       = math.sqrt(radius**2 - dst_x**2)
            dst_o       = dst_x * RIGHT + dst_y * UP + self.mirror_origin # destination normal vector origin (start)
            dst_normal  = (dst_o - self.mirror_origin)
            norm        = np.linalg.norm(dst_normal)                      # just radius, though
            dst_normal /= norm
            tan_arrow_dst_v = np.array([dst_normal[1], -dst_normal[0], dst_normal[2]]) # rotate pi/2
            tan_arrow_dst_v = tangent_length_coeff * tan_arrow_dst_v                   # length adjustment to a bit shorter
            arrow_d     = Arrow(dst_o, dst_o + tan_arrow_dst_v, stroke_width = tangent_stroke_width, color=tangent_color, buff=0)
            tangent_arrow_dst.append(arrow_d)

        tangent_src_creation = [ShowCreation(mobj) for mobj in tangent_arrow_src_work]
        self.add(mirror_line_work)
        self.play(FadeOut(self.mirror_line), *tangent_src_creation)

        text_tangent_1 = TextMobject(r"Tangent is also different everywhere on a curve.").move_to(0.0 * RIGHT + 3.0 * UP)
        text_tangent_2 = TextMobject(r"But the same on a plane.").move_to(0.0 * RIGHT + 3.0 * UP)
        self.play(FadeIn(text_tangent_1))

        tangent_transform = [ReplacementTransform(m1, m2) for (m1, m2) in zip(tangent_arrow_src_work, tangent_arrow_dst)]
        self.play(ReplacementTransform(mirror_line_work, arc_1), *tangent_transform)
        self.wait(self.wait_time)

        mirror_line_dst = copy.deepcopy(self.mirror_line)
        tangent_transform_reverse = [ReplacementTransform(m1, m2) for (m1, m2) in zip(tangent_arrow_dst, tangent_arrow_src_org)]
        self.play(FadeOut(text_tangent_1), FadeIn(text_tangent_2))
        self.play(ReplacementTransform(arc_1, mirror_line_dst), *tangent_transform_reverse)
        self.wait(self.wait_time)

        fadeout_normals = [FadeOut(mobj) for mobj in tangent_arrow_src_org]
        self.add(self.mirror_line)
        self.play(FadeOut(mirror_line_dst), *fadeout_normals)
        self.play(FadeOut(text_tangent_2))
        self.wait(self.wait_time)


    def animate_incident_reflected_tangent(self):
        """
        1. Show mirror_line, incident ray, reflected ray
        2. Emphasize mirror_line as a tangent
        3. Show tangent and incident/reflected angles
        """

        # 1. Show mirror_line, incident ray, reflected ray: The mirror_line has been shown
        self.play(ShowCreation(self.arrow_incident), ShowCreation(self.arrow_reflected))

        # temporal text: Angles between the rays and the tangent
        text_tangent_fig_1 = TextMobject(r"Angles between the rays").scale(1.2).move_to(3.0 * RIGHT +   0.0 * UP)
        text_tangent_fig_2 = TextMobject(r"and the ", r"tangent").   scale(1.2).move_to(3.0 * RIGHT +  -1.0 * UP)
        self.play(FadeIn(text_tangent_fig_1), FadeIn(text_tangent_fig_2))
        self.wait(self.wait_time)

        # 2. Emphasize mirror_line as a tangent
        mirror_line_work = copy.deepcopy(self.mirror_line)

        mirror_line_dst  = copy.deepcopy(self.mirror_line)
        mirror_line_dst.set_stroke(GREEN, 10).scale(1.2)

        # Use work (push mirror_line)
        self.add(mirror_line_work)
        self.play(FadeOut(self.mirror_line))

        self.play(Transform(mirror_line_work, mirror_line_dst),
                  # text color: "tangent"
                  ApplyMethod(text_tangent_fig_2[1].set_color, GREEN))
        self.wait(self.wait_time)

        self.play(Transform(mirror_line_work, self.mirror_line),
                  # text color: "tangent"
                  ApplyMethod(text_tangent_fig_2[1].set_color, WHITE))
        self.wait(self.wait_time)

        # restore mirror_line
        self.add(self.mirror_line)
        self.play(FadeOut(mirror_line_work))
        self.wait(self.wait_time)

        # fade out incident/reflected
        self.play(FadeOut(self.arrow_incident),
                  FadeOut(self.arrow_reflected),
                  FadeOut(text_tangent_fig_1),
                  FadeOut(text_tangent_fig_2))


    def create_left_right_tangent(self):
        """Show normal and right angle
        Show incident angle theta_i and 90 - theta_i

        """
        self.arc_incident_tan = Arc(
            start_angle = PI/2 + self.incident_angle,
            angle       = PI/2 - self.incident_angle,
            radius      = self.arc_incident_tan_radius,
            color       = self.arc_incident_color,
            arc_center  = self.mirror_origin
        )

        theta_in_tan_pos_offset = -2.0 * RIGHT + 0.8 * UP
        self.tex_theta_in_tan = TexMobject(r"90^{\circ}",
                                           r"-",
                                           r"\theta_{i}",
                                           color=self.tex_theta_in_color).\
                                           move_to(self.mirror_origin + theta_in_tan_pos_offset)

        self.arc_reflected_tan = Arc(
            start_angle = 0,
            angle       = PI/2 - self.reflected_angle,
            radius      = self.arc_reflected_tan_radius,
            color       = self.arc_reflected_color,
            arc_center  = self.mirror_origin
        )

        theta_out_tan_pos_offset = 2.0 * RIGHT + 0.8 * UP
        self.tex_theta_ref_tan = TexMobject(r"90^{\circ}",
                                            r"-",
                                            r"\theta_{r}",
                                            color=self.tex_theta_ref_color).\
                                            move_to(self.mirror_origin + theta_out_tan_pos_offset)



    def animate_left_right_tangent(self):
        """
        Show the angle between incident  and tangent
        Show the angle between reflected and tangent
        """

        # normal + left right angle
        self.play(ShowCreation(self.normal_line),
                  ShowCreation(self.left_right_angle))
        self.wait(self.wait_time)

        # incident ray, \theta_i, arc
        self.play(ShowCreation(self.arrow_incident),
                  ShowCreation(self.arc_incident),
                  FadeIn(self.tex_theta_in))
        self.wait(self.wait_time)

        # incident tangent angle
        self.play(ShowCreation(self.arc_incident_tan),
                  FadeIn(self.tex_theta_in_tan))
        self.wait(self.wait_time)

        # reflected ray, \theta_r, arc
        self.play(ShowCreation(self.arrow_reflected),
                  ShowCreation(self.arc_reflected),
                  FadeIn(self.tex_theta_ref))
        self.wait(self.wait_time)

        # reflected tangent angle
        self.play(ShowCreation(self.arc_reflected_tan),
                  FadeIn(self.tex_theta_ref_tan))
        self.wait(self.wait_time)


    def create_tangent_angles_equal(self):
        """
        Derive 90 - \theta_i = 90 - \theta_r = \theta'
        object creation
        """

        self.text_mirror = TextMobject(r"Specular reflection")
        self.text_mirror.move_to(4.0 * RIGHT + 2.0 * UP)

        self.tex_derive_ti_tr = TexMobject(r"\theta_{i}", r"=", r"\theta_{r}", r"=", r"\theta_{0}")
        self.tex_derive_ti_tr[0].set_color(self.tex_theta_in_color)
        self.tex_derive_ti_tr[2].set_color(self.tex_theta_ref_color)
        self.tex_derive_ti_tr[4].set_color(RED)
        self.tex_derive_ti_tr.move_to(4.0 * RIGHT + 1.0 * UP)

        self.tex_derive_tan_tin_tan_tr = TexMobject(r"90^{\circ}", r"-", r"\theta_{i}",
                                                    r"=",
                                                    r"90^{\circ}", r"-", r"\theta_{r}",
                                                    r"=", r"\theta_{0}'")
        for i in range(0,3):
            self.tex_derive_tan_tin_tan_tr[  i].set_color(self.tex_theta_in_color)
            self.tex_derive_tan_tin_tan_tr[4+i].set_color(self.tex_theta_ref_color)
        self.tex_derive_tan_tin_tan_tr[8].set_color(RED)
        self.tex_derive_tan_tin_tan_tr.move_to(4.0 * RIGHT + 0.0 * UP)

        self.theta_0   = TexMobject(r"\theta_{0}"). set_color(RED)
        self.theta_0_d = TexMobject(r"\theta_{0}'").set_color(RED)


    def animate_tangent_angles_equal(self):
        """
        Derive 90 - \theta_i = 90 - \theta_r = \theta'
        animation
        """

        # \theta_i and \theta_r
        self.play(FadeIn(self.tex_derive_ti_tr[0]), FadeIn(self.tex_derive_ti_tr[2]))
        self.wait(self.wait_time)

        # mirror reflection
        self.play(FadeIn(self.text_mirror), FadeIn(self.tex_derive_ti_tr[1]))
        self.wait(self.wait_time)

        self.play(FadeIn(self.tex_derive_ti_tr[3]), FadeIn(self.tex_derive_ti_tr[4]))
        self.wait(self.wait_time)

        # tangent
        tex_derive_tan_tin_tan_tr_work = copy.deepcopy(self.tex_derive_tan_tin_tan_tr)
        theta_work_1 = copy.deepcopy(self.theta_0)
        theta_work_1.move_to(self.tex_derive_tan_tin_tan_tr[2].get_center())
        theta_work_2 = copy.deepcopy(self.theta_0)
        theta_work_2.move_to(self.tex_derive_tan_tin_tan_tr[6].get_center())
        theta_i_org  = copy.deepcopy(tex_derive_tan_tin_tan_tr_work[2])
        theta_r_org  = copy.deepcopy(tex_derive_tan_tin_tan_tr_work[6])

        # Show 90 - theta_i , 90 - theta_r
        self.play(FadeIn(tex_derive_tan_tin_tan_tr_work[0:2]),
                  FadeIn(tex_derive_tan_tin_tan_tr_work[4:6]),
                  # Make final memory destination of ReplacementTransform
                  # tex_derive_tan_tin_tan_tr_work, thus here we start with
                  # the copies (theta_i_org and theta_r_org).
                  FadeIn(theta_i_org),
                  FadeIn(theta_r_org))
        self.wait(self.wait_time)

        # transform to theta_i, theta_r = theta
        self.play(ReplacementTransform(theta_i_org, theta_work_1),
                  ReplacementTransform(theta_r_org, theta_work_2))
        self.wait(self.wait_time)

        # transform back to theta_i, theta_r
        self.play(ReplacementTransform(theta_work_1, tex_derive_tan_tin_tan_tr_work[2]),
                  ReplacementTransform(theta_work_2, tex_derive_tan_tin_tan_tr_work[6]))
        self.wait(self.wait_time)

        # show = thera'
        self.play(FadeIn(tex_derive_tan_tin_tan_tr_work[3]),
                  FadeIn(tex_derive_tan_tin_tan_tr_work[7:9]))
        self.wait(self.wait_time)

        # Show equal anges: theta_0
        theta_i_equal = copy.deepcopy(self.tex_derive_ti_tr[4])
        theta_r_equal = copy.deepcopy(self.tex_derive_ti_tr[4])
        self.add(theta_i_equal, theta_r_equal)
        self.play(ApplyMethod(theta_i_equal.move_to, self.tex_theta_in.get_center()),
                  FadeOut(self.tex_theta_in),
                  ApplyMethod(theta_r_equal.move_to, self.tex_theta_ref.get_center()),
                  FadeOut(self.tex_theta_ref))
        self.wait(self.wait_time)

        # Show equal anges: theta_0'
        theta_i_tan_equal = copy.deepcopy(self.tex_derive_tan_tin_tan_tr[8])
        theta_r_tan_equal = copy.deepcopy(self.tex_derive_tan_tin_tan_tr[8])
        self.add(theta_i_tan_equal, theta_r_tan_equal)
        self.play(ApplyMethod(theta_i_tan_equal.move_to, self.tex_theta_in_tan. get_center()),
                  FadeOut(self.tex_theta_in_tan),
                  ApplyMethod(theta_r_tan_equal.move_to, self.tex_theta_ref_tan.get_center()),
                  FadeOut(self.tex_theta_ref_tan))
        self.wait(self.wait_time)

        self.play(FadeOut(self.text_mirror),
                  FadeOut(self.tex_derive_ti_tr),
                  FadeOut(tex_derive_tan_tin_tan_tr_work))
        self.wait(self.wait_time)


    def construct(self):
        """Animation main
        """

        # Create and animate a mirror line and a normal
        self.create_mirror_normal()
        self.animate_mirror_normal()

        # Animate normals on arc
        self.animate_normal_on_curve()

        # Incident and reflected
        self.create_incident_reflected()
        self.animate_incident_reflected()

        # Tangent
        self.animate_tangent_on_curve()

        # incident/reflected, tangent (mirror surface), between angles
        self.animate_incident_reflected_tangent()

        # left side tangent angle
        self.create_left_right_tangent()
        self.animate_left_right_tangent()

        # derive 90 - \theta_i = 90 - \theta_r = \theta'
        self.create_tangent_angles_equal()
        self.animate_tangent_angles_equal()

        self.wait(5)
