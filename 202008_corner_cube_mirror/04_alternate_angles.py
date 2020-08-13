# -*- coding: utf-8; -*-
#
# Section 4: Alternate angles
#
#    (C) 2020 Hitoshi Yamauchi
#
# References: 3Blue1Brown, Theorem of Beethoven (manim tutorial)
#
#  cd data/gitdata/manim
#  source manim-venv/bin/activate
#
# Full resolution
#   python3 -m manim 04_alternate_angles.py AlternateAngles01 --resolution 720,1280 -p --high_quality
# Preview resolution
#   python3 -m manim 04_alternate_angles.py AlternateAngles01 --resolution 360,640 -pl
#   python3 -m manim 04_alternate_angles.py AlternateAngles01 --resolution 360,640 -i --high_quality
# -i as gif


from manimlib.imports import *
import os, copy
import pyclbr


def get_fadeout_mobject_list(group_mobj, fadeout_key_list, is_print=False):
    """FadeOut mobjects list
    """
    fadeout_list = []
    for key in fadeout_key_list:
        if (is_print):
            print("FadeOut: {0}".format(key))
        fadeout_list.append(FadeOut(group_mobj[key]))

    return fadeout_list



class NoLineIntersection(Exception):
    """No line intersection case exception"""

    def __init__(self, reason):
        """No intersection reason: expecting {"parallel", "co-linear"}
        """
        self.reason = reason

    def __str__(self):
        return repr(self.reason)


def intersect_point_of_lines(line_1, line_2):
    """Get line intersection point of line_1 and line_2

    The line's angle is normalized in [-PI/2, PI/2]
    @param[in] line_1 a Line MObject 1
    @param[in] line_2 a Line MObject 2
    @return The intersection point of line_1 and line_2. None when no intersection point
    """
    eps = 0.001

    def is_perpendicular(theta):
        assert((-math.pi <= theta) and (theta <= math.pi))
        if (math.fabs(theta - (math.pi / 2.0)) < eps):
            print('1: theta: {0}'.format(theta))
            return True
        if (math.fabs(theta + (math.pi / 2.0)) < eps):
            print('2: theta: {0}'.format(theta))
            return True
        return False

    theta_1 = line_1.get_angle()
    theta_2 = line_2.get_angle()

    # check parallel (no unique intersection point when co-linear, treat it as parallel)
    if (math.fabs(theta_1 - theta_2) < eps):
        return None

    # check vertical line: assume 0 <= thera <= 2pi
    if (is_perpendicular(theta_1)):
        # print("line_1: perpendicular")
        x_1 = line_1.get_center()[0]
        y_2 = line_2.get_center()[1]
        return np.array((x_1, y_2, 0.0))

    if (is_perpendicular(theta_2)):
        # print("line_2: perpendicular")
        x_2 = line_2.get_center()[0]
        y_1 = line_1.get_center()[1]
        return np.array((x_2, y_1, 0.0))

    # Now, lines are not parallel, none of the slopes is vertical

    # slopes and y-intercepts
    m_1 = math.tan(theta_1)
    m_2 = math.tan(theta_2)

    b_1 = line_1.get_center()[1] - m_1 * line_1.get_center()[0]
    b_2 = line_2.get_center()[1] - m_2 * line_2.get_center()[0]

    # intersection point
    x_int = -(b_1 - b_2)/(m_1 - m_2)
    y_int = (m_1 * b_2 - m_2 * b_1)/(m_1 - m_2)

    p_int = np.array((x_int, y_int, 0.0))
    return p_int


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


class AlternateAngles01(Scene):
    """04. AlternateAngles
    """
    CONFIG={
        #---- Shared members
        "all_play": True,
        "wait_time": 1,
        # current language: 0 ... English, 1 ... Deutsch, 2 ... 日本語
        "cur_lang": 0,

        #---- Corresponding angles
        #  corresponding angles setting
        "line_ab_1_color":         YELLOW,
        "line_ab_2_color":         YELLOW,
        "line_cd_color":           BLUE,
        "parallel_line_length":    7,
        "transversal_line_length": 6.5,
        "arc_corr_1_radius":       0.7,
        "arc_coor_1_color":        WHITE,


        #---- Vertical angles
        #  vertical angles setting
        "line_ef_line_length":     3.5,
        "line_ef_color":           YELLOW,
        "line_gh_line_length":     3.0,
        "line_gh_color":           BLUE,
        "arc_vert_1_radius":       0.7,
        "arc_vert_1_color":        WHITE,
    }


    def create_group_corresponding_angles(self):
        """
        Creating corresponding angles

          * parallel line:   AB_1, AB_2
          * Transversal:     CD
          * Arc:             alpha_1, alpha_2
          * Arc text:        alpha_1, alpha_2
          * Parallel sign >: parallel_sign_1, parallel_sign_2

                     CD
                     / alpha'
            --------+-------->- AB_2
                   /
                  / alpha
            -----+----------->- AB_1
                /
        """

        # line_ab_1
        line_ab_1_start  = ORIGIN
        line_ab_1_end    = RIGHT * self.parallel_line_length
        line_ab_1_origin = ORIGIN + -2.0 * UP + -2.5  * RIGHT
        line_ab_1        = Line(line_ab_1_start, line_ab_1_end, color=self.line_ab_1_color).move_to(line_ab_1_origin)

        # line_ab_2
        line_ab_2_start  = ORIGIN
        line_ab_2_end    = RIGHT * self.parallel_line_length
        line_ab_2_origin = ORIGIN +  0.5 * UP + -2.5 * RIGHT
        line_ab_2        = Line(line_ab_2_start, line_ab_2_end, color=self.line_ab_2_color).move_to(line_ab_2_origin)

        # line_cd
        line_cd_start  = ORIGIN
        line_cd_end    = RIGHT * self.parallel_line_length
        line_cd_origin = 0.5 * (line_ab_1_origin + line_ab_2_origin)
        line_cd        = Line(line_cd_start, line_cd_end, color=self.line_cd_color).move_to(line_cd_origin)
        line_cd.rotate(PI/4.0)

        # parallel signs: Create '>' with two lines
        parallel_sign_1  = VGroup()
        parallel_sign_l1 = Line(ORIGIN + 0.8 * UP - RIGHT, ORIGIN)
        parallel_sign_l2 = Line(ORIGIN - 0.8 * UP - RIGHT, ORIGIN)
        parallel_sign_1.add(parallel_sign_l1, parallel_sign_l2).set_color(YELLOW).scale(0.3)

        parallel_sign_2 = copy.deepcopy(parallel_sign_1)
        parallel_sign_1.move_to(line_ab_1_origin + 3.0 * RIGHT)
        parallel_sign_2.move_to(line_ab_2_origin + 3.0 * RIGHT)

        # corresponding angles tex: alpha = alpha' = beta = beta'
        tex_corresponding_angles = TexMobject(r"\alpha",
                                              r"=",
                                              r"\alpha'",
                                              r"=",
                                              r"\beta",
                                              r"=",
                                              r"\beta''",
                                              color=WHITE)

        group_corresponding_angles = {
            "line_ab_1":       line_ab_1,
            "line_ab_2":       line_ab_2,
            "line_cd":         line_cd,
            "parallel_sign_1": parallel_sign_1,
            "parallel_sign_2": parallel_sign_2,
        }

        # intersection points
        alpha_tex_idx = [0, 2]
        line_paires = [[line_ab_1, line_cd], [line_ab_2, line_cd]]
        for i in range(0, len(line_paires)):
            line_1 = line_paires[i][0]
            line_2 = line_paires[i][1]
            # print(line_1.get_center(), line_2.get_center())
            p_int = intersect_point_of_lines(line_1, line_2)
            if (p_int is not None):
                # print(p_int)
                # There is an intersection point
                dot_e = Dot(point=p_int, color=GREEN)
                # arc alpha
                arc_alpha = Arc(
                    start_angle = line_1.get_angle(),
                    angle       = line_2.get_angle(),
                    radius      = self.arc_corr_1_radius,
                    color       = self.arc_coor_1_color,
                    arc_center  = p_int
                )
                # Add to draw
                group_corresponding_angles['dot_e_{0}'.format(i)]     = dot_e
                group_corresponding_angles['arc_alpha_{0}'.format(i)] = arc_alpha
                tex_angle_alpha = copy.deepcopy(tex_corresponding_angles[alpha_tex_idx[i]])
                tex_angle_alpha.next_to(dot_e, RIGHT, buff=0).shift(0.8 * RIGHT + 0.45 * UP)
                group_corresponding_angles['tex_angle_alpha_{0}'.format(i)] = tex_angle_alpha

        #-- Add corresponing angles text
        text_corresponding_angles = [
            TextMobject(r"Corresponding", r"angles"),
            TextMobject(r"Stufenwinkel"),
            TextMobject(r"同位角"),
        ]
        pos_corresponding_angles = [
            3.2 * UP + -3.0 * RIGHT,
            3.2 * UP + -3.0 * RIGHT,
            3.2 * UP + -3.0 * RIGHT
        ]
        text_corresponding_angles[self.cur_lang].scale(1.4).move_to(pos_corresponding_angles[self.cur_lang])
        tex_corresponding_angles.next_to(text_corresponding_angles[self.cur_lang], DOWN)
        group_corresponding_angles['text_corresponding_angles'] = text_corresponding_angles[self.cur_lang]

        play_create_and_fade_in(self, group_corresponding_angles)
        self.wait(self.wait_time)

        #- animation corresponding angles: alpha = alpha' to up
        #  push dest position, set the start positions
        tex_alpha_dest_0 = tex_corresponding_angles[0].get_center()
        tex_alpha_dest_2 = tex_corresponding_angles[2].get_center()
        tex_corresponding_angles[0].move_to(group_corresponding_angles["tex_angle_alpha_0"].get_center())
        tex_corresponding_angles[2].move_to(group_corresponding_angles["tex_angle_alpha_1"].get_center())
        self.play(FadeIn(tex_corresponding_angles[0]),
                  FadeIn(tex_corresponding_angles[1]),
                  FadeIn(tex_corresponding_angles[2]))
        self.play(tex_corresponding_angles[0].move_to, tex_alpha_dest_0,
                  tex_corresponding_angles[2].move_to, tex_alpha_dest_2)

        return (group_corresponding_angles, tex_corresponding_angles)



    def create_group_vertical_angles(self):
        """Create vertical angles

            * Line:            EF, GH
            * Arc:             beta_1, beta_2
            * Arc Text:        beta_1, beta_2

                      H
                      /
                     / beta'
          E --------+--------- F
              beta /
                  /
                 G
        """

        # line_ef
        line_ef_start  = ORIGIN
        line_ef_end    = RIGHT * self.line_ef_line_length
        line_ef_origin = ORIGIN + 1.25 * UP + 3.5  * RIGHT
        line_ef        = Line(line_ef_start, line_ef_end, color=self.line_ef_color).move_to(line_ef_origin)

        # line_gh
        line_gh_start  = ORIGIN
        line_gh_end    = RIGHT * self.line_gh_line_length
        line_gh_origin = ORIGIN + 1.25 * UP + 3.5  * RIGHT
        line_gh        = Line(line_gh_start, line_gh_end, color=self.line_gh_color).move_to(line_gh_origin)
        line_gh.rotate(PI/4.0)

        pos_vert_int    = intersect_point_of_lines(line_ef, line_gh)
        dot_vert_int    = Dot(point=pos_vert_int, color=GREEN)
        arc_vert_beta_1 = Arc(
            start_angle = line_ef.get_angle(),
            angle       = line_gh.get_angle(),
            radius      = self.arc_vert_1_radius,
            color       = self.arc_vert_1_color,
            arc_center  = pos_vert_int
        )
        arc_vert_beta_2 = Arc(
            start_angle = line_ef.get_angle() + PI,
            angle       = line_gh.get_angle(),
            radius      = self.arc_vert_1_radius,
            color       = self.arc_vert_1_color,
            arc_center  = pos_vert_int
        )

        # vertical angles tex: alpha = alpha' = beta = beta'
        tex_vertical_angles = TexMobject(r"\beta",
                                         r"=",
                                         r"\beta'",
                                         color=WHITE)

        tex_vertical_angles_work = copy.deepcopy(tex_vertical_angles)
        tex_vertical_angles_work[0].next_to(dot_vert_int, RIGHT, buff=0).shift( 0.5 * UP +  0.8 * RIGHT)
        tex_vertical_angles_work[2].next_to(dot_vert_int, RIGHT, buff=0).shift(-0.5 * UP + -1.3 * RIGHT)

        group_vertical_angles = {
            "line_ef":         line_ef,
            "line_gh":         line_gh,
            "dot_vert_int":    dot_vert_int,
            "arc_vert_beta_1": arc_vert_beta_1,
            "arc_vert_beta_2": arc_vert_beta_2,
            "tex_vertical_angles_work_0": tex_vertical_angles_work[0],
            "tex_vertical_angles_work_2": tex_vertical_angles_work[2],
        }

        #-- Add Vertical angles text
        text_vertical_angles = [
            TextMobject(r"Vertical", r"angles"),
            TextMobject(r"Scheitelwinkel"),
            TextMobject(r"対頂角"),
        ]
        pos_vertical_angles = [
            3.2 * UP + 3.6 * RIGHT,
            3.2 * UP + 3.6 * RIGHT,
            3.2 * UP + 3.6 * RIGHT
        ]
        text_vertical_angles[self.cur_lang].scale(1.4).move_to(pos_vertical_angles[self.cur_lang])
        tex_vertical_angles.next_to(text_vertical_angles[self.cur_lang], DOWN)
        group_vertical_angles['text_vertical_angles'] = text_vertical_angles[self.cur_lang]

        play_create_and_fade_in(self, group_vertical_angles)
        self.wait(self.wait_time)

        # animation vertical angles: beta = beta'
        group_vertical_angles['tex_vertical_angles'] = tex_vertical_angles
        tex_title_vertical_beta_dest_0 = tex_vertical_angles[0].get_center()
        tex_title_vertical_beta_dest_2 = tex_vertical_angles[2].get_center()
        tex_vertical_angles[0].move_to(group_vertical_angles["tex_vertical_angles_work_0"].get_center())
        tex_vertical_angles[2].move_to(group_vertical_angles["tex_vertical_angles_work_2"].get_center())
        self.play(FadeIn(tex_vertical_angles[0]),
                  FadeIn(tex_vertical_angles[1]),
                  FadeIn(tex_vertical_angles[2]))
        self.play(tex_vertical_angles[0].move_to, tex_title_vertical_beta_dest_0,
                  tex_vertical_angles[2].move_to, tex_title_vertical_beta_dest_2)

        return group_vertical_angles


    def animate_vertical_angle_copy_match(self, group_corresponding_angles, tex_corresponding_angles, group_vertical_angles, target_angle):
        """
        * Copy vertical angles
        * beta -> alpha
        * Move to match corresponding angles alpha, remove the copy lines
        * Set vertical angle beta
        * Copy beta to title

        tex_corresponding_angles: title equality aplha = alpha' = beta = beta'
        target_angle: alpha or alpha_d

        return created beta or beta_d pair (in the title, or in the corresponding angle figure)
        """

        group_vertical_angles_to_alpha =  copy.deepcopy(group_vertical_angles)

        # move to the corresponding angles alpha
        moving_mobj_key = [
            "line_ef",
            "line_gh",
            "dot_vert_int",
            "arc_vert_beta_1",
            "arc_vert_beta_2",
            # "tex_vertical_angles_work_0",
            # "tex_vertical_angles_work_2",
        ]

        # target angle: { alpha, alpha' } -> {dot_e_0, dot_e_1}
        target_dot_dict = {
            "alpha"  : "dot_e_0",
            "alpha_d": "dot_e_1",
        }

        p_target      = group_corresponding_angles[target_dot_dict[target_angle]].get_center()
        p_delta       = p_target - group_vertical_angles_to_alpha["dot_vert_int"].get_center()
        p_move_list   = []

        for key in moving_mobj_key:
            p_move_list.append(group_vertical_angles_to_alpha[key].shift)
            p_move_list.append(p_delta)

        self.play(*p_move_list)
        self.wait(self.wait_time)

        # Fade out vertical angles, except beta arc
        fadeout_mobj_key = [
            "line_ef",
            "line_gh",
            "dot_vert_int",
            "arc_vert_beta_1",
        ]
        fadeout_list = get_fadeout_mobject_list(group_vertical_angles_to_alpha, fadeout_mobj_key, is_print=False)

        self.play(*fadeout_list)
        self.wait(self.wait_time)

        # Let's call the vertical angle of alpha as beta
        pos_beta = group_vertical_angles_to_alpha["tex_vertical_angles_work_2"].get_center() + p_delta

        # alpha -> beta, alpha' -> beta'
        target_beta_dict = {
            "alpha"  : r"\beta",
            "alpha_d": r"\beta'",
        }

        tex_beta        = TexMobject(target_beta_dict[target_angle], color=WHITE).move_to(pos_beta)
        tex_beta_moving = copy.deepcopy(tex_beta)
        self.play(FadeIn(tex_beta), FadeIn(tex_beta_moving))
        self.wait(self.wait_time)

        # alpha -> [3] =, alpha' -> [5] =
        target_eq_idx_dict = {
            "alpha"  : 3,
            "alpha_d": 5,
        }
        # alpha -> [4] beta, alpha' -> [6] beta'
        target_beta_idx_dict = {
            "alpha"  : 4,
            "alpha_d": 6,
        }

        pos_beta_delta = tex_corresponding_angles[target_beta_idx_dict[target_angle]].get_center() - tex_beta_moving.get_center()
        self.play(FadeIn(tex_corresponding_angles[target_eq_idx_dict[target_angle]]), tex_beta_moving.shift, pos_beta_delta)

        # keep created beta||beta' to later use. alpha's vertical angle is beta, alpha_d's vertical angle is beta_d.
        #
        #                   /
        #                  /alpha'(target angle)
        #         --------+---------
        #          beta' /
        #               /
        #              /
        #             /
        #            / alpha (target angle)
        #   --------+---------
        #     beta /
        #         /
        #
        # either beta and beta' is created depends on target_angle
        created_beta_kind = {
            "alpha"  : "beta",
            "alpha_d": "beta_d",
        }

        beta_key = created_beta_kind[target_angle]
        # key is ["beta_1", "beta_2"] or ["beta_d_1", "beta_d_2" }
        created_beta_or_beta_d = {
            "{0}_1".format(beta_key): tex_beta,
            "{0}_2".format(beta_key): tex_beta_moving
        }

        # {beta_1, beta_2}, vertical_angle_moved_copy
        return (created_beta_or_beta_d, group_vertical_angles_to_alpha)



    def animate_alternate_interior_angles(self,
                                          angle_tex,
                                          group_corresponding_angles,
                                          vertical_angle_copy_beta,
                                          vertical_angle_copy_beta_d):
        """
        Alternate interior angles: alpha = beta'
                       /
              --------+---------
               beta' /
                    /
                   /
                  / alpha
         --------+---------
                /
        angle_tex: all title and figure alpha, alpha', beta, beta'
        vertical_angle_copy_beta: vertical angles beta  figure
        vertical_angle_copy_beta: vertical angles beta' figure

        """
        # Scale up/down alpha = beta' in title and corresponding angles
        # [figure alpha, title alpha, figure beta', title beta']
        expand_factor = 1.5
        scale_list    = [angle_tex[i].scale for i in ["figure_alpha", "title_alpha", "figure_beta_d", "title_beta_d"]]
        exp_f_list    = [expand_factor] * 4
        exp_play_list = []
        for i in zip(scale_list, exp_f_list):
            exp_play_list.extend(i)

        recip_exp_f_list = [1/expand_factor] * 4
        recip_play_list = []
        for i in zip(scale_list, recip_exp_f_list):
            recip_play_list.extend(i)

        # Temporary FadeOut the alternate 'exterior' angles
        self.play(FadeOut(angle_tex["figure_alpha_d"]),
                  FadeOut(angle_tex["figure_beta"]),
                  FadeOut(vertical_angle_copy_beta["arc_vert_beta_2"]),
                  FadeOut(group_corresponding_angles["arc_alpha_1"]))

        # emphasis alternate interior angles
        self.play(*exp_play_list)
        self.play(*recip_play_list)
        self.wait(1)

        group_alternate_interior_angles = {}
        text_alternate_interior_angles = VGroup(
            TextMobject(r"Alternate", r"interior"),
            TextMobject(r"angles"),
        )
        text_alternate_interior_angles.arrange_submobjects(
            DOWN,
            aligned_edge = LEFT,
            center = True,
            buff = 0.25,
        )
        text_alternate_interior_angles.scale(1.2).move_to(2.8 * UP + 3.7 * RIGHT)
        group_alternate_interior_angles['text_alternate_interior_angles'] = text_alternate_interior_angles
        self.play(FadeIn(text_alternate_interior_angles))

        # moving alpha and beta' target
        alternate_angle_tex_target = TexMobject(r"\alpha", r"=", r"\beta'").move_to(1.5 * UP + 3.8 * RIGHT)
        self.play(FadeIn(alternate_angle_tex_target[1]))

        # moving alpha and beta' work (figure alpha to [0], figure beta' to [2])
        alternate_angle_tex_work = copy.deepcopy(angle_tex)
        self.play(alternate_angle_tex_work["figure_alpha"].move_to,  alternate_angle_tex_target[0].get_center(),
                  alternate_angle_tex_work["figure_beta_d"].move_to, alternate_angle_tex_target[2].get_center())
        self.play(FadeIn(alternate_angle_tex_target[0]), FadeIn(alternate_angle_tex_target[2]))
        self.play(FadeOut(alternate_angle_tex_work["figure_alpha"]),  FadeOut(alternate_angle_tex_work["figure_beta_d"]))
        self.wait(self.wait_time)

        # Restore FadeOut the alternate 'exterior' angles
        self.play(FadeIn(angle_tex["figure_alpha_d"]),
                  FadeIn(angle_tex["figure_beta"]),
                  FadeIn(vertical_angle_copy_beta["arc_vert_beta_2"]),
                  FadeIn(group_corresponding_angles["arc_alpha_1"]))
        self.wait(self.wait_time)


    def animate_alternate_exterior_angles(self,
                                          angle_tex,
                                          group_corresponding_angles,
                                          vertical_angle_copy_beta,
                                          vertical_angle_copy_beta_d):
        """
        Alternate exterior angles: alpha' = beta
                      /
                     /alpha'
            --------+---------
                   /
                  /
         --------+---------
           beta /
               /
        angle_tex: all title and figure alpha, alpha', beta, beta'
        vertical_angle_copy_beta: vertical angles beta  figure
        vertical_angle_copy_beta: vertical angles beta' figure

        """
        # Scale up/down alpha = beta' in title and corresponding angles
        # [figure alpha, title alpha, figure beta', title beta']

        expand_factor = 1.5
        scale_list    = [angle_tex[i].scale for i in ["figure_alpha_d", "title_alpha_d", "figure_beta", "title_beta"]]
        exp_f_list    = [expand_factor] * 4
        exp_play_list = []
        for i in zip(scale_list, exp_f_list):
            exp_play_list.extend(i)

        recip_exp_f_list = [1/expand_factor] * 4
        recip_play_list = []
        for i in zip(scale_list, recip_exp_f_list):
            recip_play_list.extend(i)

        # Temporary FadeOut the alternate 'interior' angles
        self.play(FadeOut(angle_tex["figure_alpha"]),
                  FadeOut(angle_tex["figure_beta_d"]),
                  FadeOut(vertical_angle_copy_beta_d["arc_vert_beta_2"]),
                  FadeOut(group_corresponding_angles["arc_alpha_0"]))

        # emphasis alternate interior angles
        self.play(*exp_play_list)
        self.play(*recip_play_list)
        self.wait(self.wait_time)

        group_alternate_exterior_angles = {}
        text_alternate_exterior_angles = VGroup(
            TextMobject(r"Alternate", r"exterior"),
            TextMobject(r"angles"),
        )
        text_alternate_exterior_angles.arrange_submobjects(
            DOWN,
            aligned_edge = LEFT,
            center = True,
            buff = 0.25,
        )
        text_alternate_exterior_angles.scale(1.2).move_to(-0.8 * UP + 3.7 * RIGHT)
        group_alternate_exterior_angles['text_alternate_exterior_angles'] = text_alternate_exterior_angles
        self.play(FadeIn(text_alternate_exterior_angles))

        # moving alpha' and beta target
        alternate_angle_tex_target = TexMobject(r"\alpha'", r"=", r"\beta").move_to(-2.0 * UP + 3.8 * RIGHT)
        self.play(FadeIn(alternate_angle_tex_target[1]))

        # moving alpha' and beta work (figure alpha' to [0], figure beta to [1])
        alternate_angle_tex_work = copy.deepcopy(angle_tex)
        self.play(alternate_angle_tex_work["figure_alpha_d"].move_to, alternate_angle_tex_target[0].get_center(),
                  alternate_angle_tex_work["figure_beta"].move_to,    alternate_angle_tex_target[2].get_center())
        self.play(FadeIn(alternate_angle_tex_target[0]), FadeIn(alternate_angle_tex_target[2]))
        self.play(FadeOut(alternate_angle_tex_work["figure_alpha_d"]),  FadeOut(alternate_angle_tex_work["figure_beta"]))
        self.wait(self.wait_time)

        # Restore FadeOut the alternate 'interior' angles
        self.play(FadeIn(angle_tex["figure_alpha"]),
                  FadeIn(angle_tex["figure_beta_d"]),
                  FadeIn(vertical_angle_copy_beta_d["arc_vert_beta_2"]),
                  FadeIn(group_corresponding_angles["arc_alpha_0"]))
        self.wait(self.wait_time)


    def animate_other_alternate_angles(self,
                                       angle_tex,
                                       group_corresponding_angles):
        """
        1. Figure: delta = delta' = gamma = gamma'

                       /
               delta' /(p_2)
             --------+--------- line_ab_2
                    /gamma'
                   /
            delta /(p_1)
         --------+--------- line_ab_1
                /gamma
               /

        2. title: delta = delta' = gamma = gamma'
        3. alternate interior angle: delta  = gamma'
        4. alternate exterior angle: delta' = gamma
        """

        # Show another corresponding angles in the figure
        line_ab_1 = group_corresponding_angles["line_ab_1"]
        line_ab_2 = group_corresponding_angles["line_ab_2"]
        line_cd   = group_corresponding_angles["line_cd"]
        p_1 = intersect_point_of_lines(line_ab_1, line_cd)
        p_2 = intersect_point_of_lines(line_ab_2, line_cd)

        another_angle_color = ORANGE # MAROON_A, PURPLE_A, TEAL_A
        another_arc_radius  = self.arc_corr_1_radius - 0.2
        arc_delta = Arc(
            start_angle = line_cd.get_angle(),
            angle       = math.pi - line_cd.get_angle(),
            radius      = another_arc_radius,
            color       = another_angle_color,
            arc_center  = p_1
        )
        arc_delta_d = Arc(
            start_angle = line_cd.get_angle(),
            angle       = math.pi - line_cd.get_angle(),
            radius      = another_arc_radius,
            color       = another_angle_color,
            arc_center  = p_2
        )

        arc_gamma = Arc(
            start_angle = math.pi + line_cd.get_angle(),
            angle       = math.pi - line_cd.get_angle(),
            radius      = another_arc_radius,
            color       = another_angle_color,
            arc_center  = p_1
        )
        arc_gamma_d = Arc(
            start_angle = math.pi + line_cd.get_angle(),
            angle       = math.pi - line_cd.get_angle(),
            radius      = another_arc_radius,
            color       = another_angle_color,
            arc_center  = p_2
        )

        figure_corresponding_angles = TexMobject(r"\delta", r"\delta'", r"\gamma", r"\gamma'").set_color(another_angle_color)
        up_offset    = 0.5
        right_offset = 0.8
        figure_corresponding_angles[0].move_to(p_1 + up_offset * UP - right_offset * RIGHT)
        figure_corresponding_angles[1].move_to(p_2 + up_offset * UP - right_offset * RIGHT)
        figure_corresponding_angles[2].move_to(p_1 - up_offset * UP + right_offset * RIGHT)
        figure_corresponding_angles[3].move_to(p_2 - up_offset * UP + right_offset * RIGHT)


        # self.play(ShowCreation(arc_delta), ShowCreation(arc_delta_d),
        #           ShowCreation(arc_gamma), ShowCreation(arc_gamma_d))
        self.play(ShowCreation(arc_delta),   FadeIn(figure_corresponding_angles[0]))
        self.play(ShowCreation(arc_delta_d), FadeIn(figure_corresponding_angles[1]))
        self.play(ShowCreation(arc_gamma),   FadeIn(figure_corresponding_angles[2]))
        self.play(ShowCreation(arc_gamma_d), FadeIn(figure_corresponding_angles[3]))
        self.wait(self.wait_time)


        # Show another corresponding angles in the title
        title_corresponding_angles = TexMobject(r"\delta", r"=", r"\delta'", r"=",
                                                r"\gamma", r"=", r"\gamma'").\
                                                set_color(another_angle_color).\
                                                move_to(1.7 * UP + -3.0 * RIGHT)
        self.play(FadeIn(title_corresponding_angles[1]),
                  FadeIn(title_corresponding_angles[3]),
                  FadeIn(title_corresponding_angles[5]))
        self.wait(self.wait_time)

        figure_corresponding_angles_work = copy.deepcopy(figure_corresponding_angles)
        self.play(figure_corresponding_angles_work[0].move_to, title_corresponding_angles[0].get_center(),
                  figure_corresponding_angles_work[1].move_to, title_corresponding_angles[2].get_center(),
                  figure_corresponding_angles_work[2].move_to, title_corresponding_angles[4].get_center(),
                  figure_corresponding_angles_work[3].move_to, title_corresponding_angles[6].get_center())
        # replace the work with original
        self.play(FadeIn(title_corresponding_angles[0]),
                  FadeIn(title_corresponding_angles[2]),
                  FadeIn(title_corresponding_angles[4]),
                  FadeIn(title_corresponding_angles[6]))
        self.play(FadeOut(figure_corresponding_angles_work[0]),
                  FadeOut(figure_corresponding_angles_work[1]),
                  FadeOut(figure_corresponding_angles_work[2]),
                  FadeOut(figure_corresponding_angles_work[3]))
        self.wait(self.wait_time)

        # Show alternate interior angles: down of 1.5 * UP + 3.8 * RIGHT
        #   (work again, last one was FadeOut, thus, they can be garbage collected.)
        figure_corresponding_angles_work = copy.deepcopy(figure_corresponding_angles)

        title_anther_alt_int_angles = TexMobject(r"\delta", r"=", r"\gamma'").\
                                                set_color(another_angle_color).\
                                                move_to(0.7 * UP + 3.8 * RIGHT)
        scale_f = 2.0
        self.play(figure_corresponding_angles[0].scale, scale_f,
                  figure_corresponding_angles[3].scale, scale_f)
        self.play(figure_corresponding_angles[0].scale, 1/scale_f,
                  figure_corresponding_angles[3].scale, 1/scale_f)


        self.play(FadeIn(title_anther_alt_int_angles[1]),
                  FadeIn(figure_corresponding_angles_work[0]), FadeIn(figure_corresponding_angles_work[3]))
        self.play(figure_corresponding_angles_work[0].move_to, title_anther_alt_int_angles[0].get_center(),
                  figure_corresponding_angles_work[3].move_to, title_anther_alt_int_angles[2].get_center())


        # Show alternate exterior angles: down of -2.0 * UP + 3.8 * RIGHT
        title_anther_alt_ext_angles = TexMobject(r"\delta'", r"=", r"\gamma").\
                                                set_color(another_angle_color).\
                                                move_to(-2.8 * UP + 3.8 * RIGHT)

        self.play(figure_corresponding_angles[1].scale, scale_f,
                  figure_corresponding_angles[2].scale, scale_f)
        self.play(figure_corresponding_angles[1].scale, 1/scale_f,
                  figure_corresponding_angles[2].scale, 1/scale_f)

        self.play(FadeIn(title_anther_alt_ext_angles[1]),
                  FadeIn(figure_corresponding_angles_work[1]), FadeIn(figure_corresponding_angles_work[2]))
        self.play(figure_corresponding_angles_work[1].move_to, title_anther_alt_ext_angles[0].get_center(),
                  figure_corresponding_angles_work[2].move_to, title_anther_alt_ext_angles[2].get_center())





    def construct(self):
        """Animation main
        """

        # Create corresponding angles setup animation
        (group_corresponding_angles, tex_corresponding_angles) = self.create_group_corresponding_angles()
        self.wait(self.wait_time)

        # Create vertical angles setup animation
        group_vertical_angles = self.create_group_vertical_angles()
        self.wait(self.wait_time)

        # Vertical angles: copy and beta -> alpha
        (group_tex_beta, vertical_angle_copy_beta) = self.animate_vertical_angle_copy_match(
            group_corresponding_angles, tex_corresponding_angles, group_vertical_angles, "alpha")
        self.wait(self.wait_time)

        # Vertical angles: copy and beta' -> alpha'
        (group_tex_beta_d, vertical_angle_copy_beta_d) = self.animate_vertical_angle_copy_match(
            group_corresponding_angles, tex_corresponding_angles, group_vertical_angles, "alpha_d")
        self.wait(self.wait_time)

        # Delete vertical angles
        fadeout_vertical_angle_key_list = group_vertical_angles.keys()
        fadeout_list = get_fadeout_mobject_list(group_vertical_angles, fadeout_vertical_angle_key_list, is_print=False)
        self.play(*fadeout_list)
        self.wait(self.wait_time)


        # Show alternate interior angles

        # group_corresponding_angles: alpha (in the figure)
        # tex_corresponding_angles:   alpha (in the title)
        # group_tex_beta:             beta' (in the title), beta' (in the figure)
        # [figure alpha, title alpha, figure beta', title beta']
        angle_tex = {
            "title_alpha":    tex_corresponding_angles[0],
            "title_alpha_d":  tex_corresponding_angles[2],
            "title_beta":     group_tex_beta  ["beta_2"],
            "title_beta_d":   group_tex_beta_d["beta_d_2"],
            "figure_alpha":   group_corresponding_angles["tex_angle_alpha_0"],
            "figure_alpha_d": group_corresponding_angles['tex_angle_alpha_1'],
            "figure_beta":    group_tex_beta  ["beta_1"],
            "figure_beta_d":  group_tex_beta_d["beta_d_1"],
        }

        self.animate_alternate_interior_angles(angle_tex,
                                               group_corresponding_angles,
                                               vertical_angle_copy_beta,
                                               vertical_angle_copy_beta_d)

        # Show alternate exterior angles
        self.animate_alternate_exterior_angles(angle_tex,
                                               group_corresponding_angles,
                                               vertical_angle_copy_beta,
                                               vertical_angle_copy_beta_d)

        # Show other vertical angles, other alternate angles
        self.animate_other_alternate_angles(angle_tex,
                                            group_corresponding_angles)

        self.wait(5)
        return
