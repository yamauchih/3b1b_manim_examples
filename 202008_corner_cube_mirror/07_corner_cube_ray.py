
# -*- coding: utf-8; -*-
#
# Coener Cube rays demo
#
#    (C) 2020 Hitoshi Yamauchi
#
# References: 3Blue1Brown, Theorem of Beethoven (manim tutorial)
#
#  cd data/gitdata/manim
#  source manim-venv/bin/activate
#
# Full resolution
#   python3 -m manim 07_corner_cube_ray.py CornerCubeRay01 --resolution 720,1280 -p --high_quality
# Preview resolution
#   python3 -m manim 07_corner_cube_ray.py CornerCubeRay01 --resolution 360,640 -pl
#   python3 -m manim 07_corner_cube_ray.py CornerCubeRay01 --resolution 360,640 -i --high_quality
# -i as gif


from manimlib.imports import *
import os, copy
import pyclbr

class ElbowRotate(VMobject):
    """manim's this version's Elbow cannot set an angle. This is an extension,
    """
    CONFIG = {
        "width": 0.2,
        "angle": 0,
    }

    def __init__(self, **kwargs):
        VMobject.__init__(self, **kwargs)
        self.set_points_as_corners([UP, UP + RIGHT, RIGHT])
        self.set_width(self.width, about_point=ORIGIN)
        self.rotate(self.angle, about_point=ORIGIN)


    def set_angle(self, angle):
        self.rotate(
            angle - self.get_angle(),
            about_point=ORIGIN,
        )
        self.angle = angle

    def get_angle(self):
        return self.angle



class Ray_1_position_gen(object):
    """
    line_ray_1 (start, end) position genarator object parameterized by time_t.

    """
    def __init__(self, ray_1_ref, mirror_corner_pos, init_start_pos, init_theta):
        """
        param[in] ray_1_ref         ray_1 (Arrow mobj) reference
        param[in] mirror_corner_pos the corner point of the mirror
        param[in] init_start_pos    ray_1 init start position
        param[in] init_thera        ray_1 angle theta from x axis
        """
        self.__ray_1_ref         = ray_1_ref
        self.__mirror_corner_pos = copy.deepcopy(mirror_corner_pos)
        self.__init_start_pos    = init_start_pos
        # end pos: mirror_corner_pos x and fixed y
        self.__init_end_pos      = np.array((self.__mirror_corner_pos[0], 0.0, 0.0))
        self.__init_theta        = init_theta


    def get_ray_1_start_pos(self, time_t):
        """
        get ray_1 start position

        param[in] time_t time parameter [0, 3]
        """
        # animation assumption: t in [0, 3]
        assert((time_t >= 0.0) and (time_t <= 3.0))

        # only x changes: piecewise linear
        coef_1 =  1.5
        coef_2 = -2.0

        pos_start_1 = self.__init_start_pos
        pos_end_1   = self.__init_start_pos

        pos_start_2 = pos_end_1
        pos_end_2   = pos_start_2 + RIGHT

        pos_start_3 = pos_end_2
        pos_end_3   = self.__init_start_pos


        if (time_t < 1.0):
            spos = pos_start_1 + (pos_end_1 - pos_start_1) * (time_t - 0.0)
            return spos
        elif (time_t < 2.0):
            spos = pos_start_2 + (pos_end_2 - pos_start_2) * (time_t - 1.0)
            return spos
        elif (time_t <= 3.0):
            spos = pos_start_3 + (pos_end_3 - pos_start_3) * (time_t - 2.0)
            return spos


    def get_ray_1_thera(self, time_t):
        """thera generator"""

        # animation assumption: t in [0, 3]
        assert((time_t >= 0.0) and (time_t <= 3.0))

        theta_start_1 = self.__init_theta
        theta_end_1   = PI/2 + np.arctan(2.5/5)

        theta_start_2 = theta_end_1
        theta_end_2   = PI/2 + np.arctan(2.5/3)

        theta_start_3 = theta_end_2
        theta_end_3   = self.__init_theta

        if (time_t < 1.0):
            theta = theta_start_1 + (theta_end_1 - theta_start_1) * (time_t - 0.0)
            return theta

        elif (time_t < 2.0):
            theta = theta_start_2 + (theta_end_2 - theta_start_2) * (time_t - 1.0)
            return theta

        elif (time_t <= 3.0):
            theta = theta_start_3 + (theta_end_3 - theta_start_3) * (time_t - 2.0)
            return theta


    def get_ray_1_end_pos(self, time_t):
        """get ray_1 end position

        param[in] time_t time parameter [0, 3]
        return ray 1 end position
        """

        # animation assumption: t in [0, 3]
        assert((time_t >= 0.0) and (time_t <= 3.0))

        spos  = self.get_ray_1_start_pos(time_t)
        theta = self.get_ray_1_thera(time_t)

        # In this scene, the ray direction has a limitation
        assert((PI/2 < theta) and (theta < PI))

        # ray direction vector
        rvec = np.array((np.cos(theta), np.sin(theta), 0.0))

        # compute vector length when the ray hits to the left mirror
        m_x    = self.__mirror_corner_pos[0]
        k_left = (m_x - spos[0]) / rvec[0]

        # compute vector length when the ray hits to the left mirror
        m_y    = self.__mirror_corner_pos[1]
        k_top = (m_y - spos[1]) / rvec[1]

        if (k_left <= k_top):
            # hit to the left
            epos = spos + k_left * rvec
            return epos
        else:
            # hit to the top
            epos = spos + k_top  * rvec
            return epos


def hit_info(mirror_corner_pos, hit_pos):
    """Get hit infomation, which mirror to hit?"""
    is_left = False
    is_top  = False
    if (math.fabs(hit_pos[0] - mirror_corner_pos[0]) < 0.001):
        # left hit
        is_left = True
    if (math.fabs(hit_pos[1] - mirror_corner_pos[1]) < 0.001):
        # top  hit
        is_top  = True

    # should hit one of them
    assert(is_left or is_top)

    return (is_left, is_top)



class Ray_2_position_gen(object):
    """
    line_ray_2 (start, end) position genarator object parameterized by time_t.
    Based on line_ray_1.

    """
    def __init__(self, ray_1_ref, mirror_corner_pos):
        """
        param[in] ray_1_ref         ray_1 (Arrow mobj) reference
        param[in] mirror_corner_pos the corner point of the mirror
        """
        self.__ray_1_ref         = ray_1_ref
        self.__mirror_corner_pos = mirror_corner_pos

    def get_ray_start_pos(self):
        """
        get ray_2 start position
        """
        return self.__ray_1_ref.get_end()


    def get_ray_end_pos(self):
        """
        get ray_2 end position. Depends on the mirror which ray_1 hits



        r2_v = (-r1_v_x, r1_v_y)
        x    = r2_s_x + k r2_v_x  (1)
        m_y  = r2_s_y + k r2_v_y  (2)   m_y: uppper mirror y

        (2)
        k = (m_y - r2s_y) / v_y

        """
        ray_1_end = self.__ray_1_ref.get_end()

        (is_left, is_top) = hit_info(self.__mirror_corner_pos, ray_1_end)

        if (is_left and is_top):
            # just hit the corner, no draw 2nd ray, same as ray_1 end
            print("hit the corner")
            return ray_1_end

        elif (is_left):
            ray2_spos = self.get_ray_start_pos()
            v1        = self.__ray_1_ref.get_unit_vector()
            v2        = np.array((0.0, 0.0, 0.0))
            v2[0]     = -v1[0]
            v2[1]     =  v1[1]
            assert(v2[1] != 0.0)

            k_left = (self.__mirror_corner_pos[1] - ray2_spos[1]) / v2[1]
            r2e_x = ray2_spos[0] + k_left * v2[0]
            ray2_epos = np.array((r2e_x, self.__mirror_corner_pos[1], 0.0))

            return ray2_epos

        else:
            ray2_spos = self.get_ray_start_pos()
            v1        = self.__ray_1_ref.get_unit_vector()
            v2        = np.array((0.0, 0.0, 0.0))
            v2[0]     =  v1[0]
            v2[1]     = -v1[1]
            assert(v2[1] != 0.0)

            k_top = (self.__mirror_corner_pos[0] - ray2_spos[0]) / v2[0]
            r2e_y = ray2_spos[1] + k_top * v2[1]
            ray2_epos = np.array((self.__mirror_corner_pos[0], r2e_y, 0.0))

            return ray2_epos



class Ray_3_position_gen(object):
    """
    line_ray_3 (start, end) position genarator object parameterized by time_t.
    Based on line_ray_1.

    """
    def __init__(self, mirror_corner_pos, ray_1_ref, ray_2_ref, ray_3_len):
        """
        param[in] mirror_corner_pos mirror corner position reference
        param[in] ray_1_ref         ray_1 (Arrow mobj) reference
        param[in] ray_2_ref         ray_2 (Arrow mobj) reference
        param[in] ray_3_len         ray_3 (Arrow mobj) length
        """
        self.__mirror_corner_pos = mirror_corner_pos
        self.__ray_1_ref         = ray_1_ref # need this for a cornet hit case
        self.__ray_2_ref         = ray_2_ref
        self.__ray_3_len         = ray_3_len


    def get_ray_start_pos(self):
        """
        get ray_3 start position

        """
        return self.__ray_2_ref.get_end()


    def get_ray_end_with_limit_y(self, rspos, rlen, rvec, y_min):
        """ray end with limit y value
        end y coordinate is >

        param[in] rspos ray start position
        param[in] rlen  ray length
        param[in] rvec  ray direction vector
        param[in] y_min y minimum limit value
        """
        repos = rspos + rlen * rvec;
        if (repos[1] >= y_min):
            return repos

        # limit y
        limit_rlen = (y_min - rspos[1])/rvec[1]
        repos = rspos + limit_rlen * rvec;
        return repos


    def get_ray_end_pos(self):
        """
        get ray_3 end position

        """
        ray_2_end = self.__ray_2_ref.get_end()

        (is_left, is_top) = hit_info(self.__mirror_corner_pos, ray_2_end)

        if (is_left and is_top):
            # just hit the corner, no draw 2nd ray, same as ray_1 end
            print("2 hit the corner")
            r3_epos = r3_spos + self.__ray_3_len * -self.__ray_1_ref.get_unit_vector()
            return r3_epos
        elif (is_left):
            v2 = self.__ray_2_ref.get_unit_vector()
            v3 = np.array((-v2[0], v2[1], 0.0))
            r3_spos = self.get_ray_start_pos()
            # When (y < -3), limit y = 3
            r3_epos = self.get_ray_end_with_limit_y(r3_spos, self.__ray_3_len, v3, -3)
            return r3_epos
        else:
            v2 = self.__ray_2_ref.get_unit_vector()
            v3 = np.array((v2[0], -v2[1], 0.0))
            r3_spos = self.get_ray_start_pos()
            # r3_epos = r3_spos + self.__ray_3_len * v3
            r3_epos = self.get_ray_end_with_limit_y(r3_spos, self.__ray_3_len, v3, -3)
            return r3_epos



class Ray_1_updater(object):
    """
    line_ray_1 update functor
    """
    def __init__(self, ray_1_pos_gen, vtarcker):
        """
        param[in] ray_1_pos_gen ray_1 position generator
        """
        self.__ray_1_pos_gen = ray_1_pos_gen
        self.__vtarcker      = vtarcker

    def __call__(self, follower):
        """
        update functor.
        Assumed the follower is line_ray_1
        """
        time_t = self.__vtarcker.get_value()
        spos = self.__ray_1_pos_gen.get_ray_1_start_pos(time_t)
        epos = self.__ray_1_pos_gen.get_ray_1_end_pos(  time_t)
        follower.put_start_and_end_on(spos, epos)


class Ray_2_3_updater(object):
    """
    line_ray_2 or line_ray_3 update functor
    """
    def __init__(self, ray_pos_gen):
        """
        param[in] ray_pos_gen ray_{2,3} position generator
        """
        self.__ray_pos_gen = ray_pos_gen

    def __call__(self, follower):
        """
        update functor.
        Assumed the follower is line_ray_2 or line_ray_3
        """
        spos = self.__ray_pos_gen.get_ray_start_pos()
        epos = self.__ray_pos_gen.get_ray_end_pos()
        follower.put_start_and_end_on(spos, epos)


class Elbow_position_angle_gen(object):
    """
    Elbow positions/angle generator
    """
    def __init__(self, mirror_corner_pos, ray_1_ref, elbow_normal_para_offset, ray_3_ref, elbow_ray_para_ratio):
        """
        param[in] mirror_corner_pos mirror corner position reference
        param[in] ray_1_ref                ray_1 (Arrow mobj) reference
        param[in] elbow_normal_para_offset offset for normal lines
        param[in] ray_3_ref                ray_2 (Arrow mobj) reference
        param[in] elbow_ray_para_ratio     length ratio for ray 1 and ray 3
        """
        self.__mirror_corner_pos        = mirror_corner_pos
        self.__ray_1_ref                = ray_1_ref
        self.__elbow_normal_para_offset = elbow_normal_para_offset
        self.__ray_3_ref                = ray_3_ref
        self.__elbow_ray_para_ratio     = elbow_ray_para_ratio


    def get_elbow_position(self, idx):
        """get elbow position
        """
        assert((0 <= idx) and (idx < 4))

        if (idx == 0):          # normal 0 (up) fixed
            return self.__mirror_corner_pos + self.__elbow_normal_para_offset * RIGHT
        elif (idx == 1):        # normal 1 (ray 1 hit position) FIXME: HEREHERE This is hit left only
            return self.__ray_1_ref.get_end()   + self.__elbow_normal_para_offset * RIGHT
        elif (idx == 2):        # ray 1
            return self.__ray_1_ref.get_start() + (1 - self.__elbow_ray_para_ratio) * self.__ray_1_ref.get_vector();
        elif (idx == 3):        # ray 3
            return self.__ray_3_ref.get_start() + self.__elbow_ray_para_ratio * self.__ray_3_ref.get_vector();

        assert(False)           # shold not be here
        return ORIGIN


    def get_elbow_angle(self, idx):
        """get elbow angle
        """
        assert((0 <= idx) and (idx < 4))

        if (idx == 0):          # normal 0 (up) fixed
            return -PI/4
        elif (idx == 1):        # normal 1 (ray 1 hit position) fixed
            return -PI/4
        elif (idx == 2):        # ray 1
            return self.__ray_1_ref.get_angle() - PI/4 - PI
        elif (idx == 3):        # ray 3
            return self.__ray_3_ref.get_angle() - PI/4

        assert(False)           # shold not be here
        return 0


class Elbow_ray_updater(object):
    """
    Elbow line_ray_1 parallel sign (elbow) update functor
    """
    def __init__(self, elbow_position_angle_gen, elbow_idx):
        """
        param[in] elbow_position_angle_gen elbow's position and angle generator
        param[in] elbow_idx                which elbow?
        """
        self.__elbow_position_angle_gen = elbow_position_angle_gen
        self.__elbow_idx                = elbow_idx

    def __call__(self, follower):
        """
        update functor.
        Assumed the follower is an elbow
        """
        follower.set_angle( self.__elbow_position_angle_gen.get_elbow_angle(self.__elbow_idx))
        follower.move_to(self.__elbow_position_angle_gen.get_elbow_position(self.__elbow_idx))



class CornerCubeRay01(Scene):
    """Example value tracker that control a ray
    """
    CONFIG={
        #-- shared variables
        "wait_time":            1,

        #-- shared MObjects
        # time parameter t and its value tracker
        "time_t":               0.0,
        "vtarcker_time_t":      None,

        # mirror, its normal, elbow (right angle sign)
        "mirror_corner_pos":    -4.5 * RIGHT + 2.0 * UP,
        "mirror_1_length":      5.0,
        "mirror_2_length":      5.0,
        "mirror_stroke_width":  4.0,
        "mirror_color":         WHITE,
        "line_mirror_up_l1"  :  None,

        # rays: laser light
        #   line: extended line of the laser ray
        "ray_1_pos_gen":       None,
        "ray_2_pos_gen":       None,
        "ray_3_pos_gen":       None,
        "line_ray_1":          None,
        "line_ray_2":          None,
        "line_ray_3":          None,
        "ray_1_color":         YELLOW,
        "ray_2_color":         RED,
        "ray_3_color":         BLUE,
        "ray_1_stroke_width":  4,
        "ray_2_stroke_width":  4,
        "ray_3_stroke_width":  4,
        "ray_1_spos":          -1.0 * RIGHT + -3.0 * UP,
        "ray_3_length":        5,

        # annotations
        #    line_normal
        #    tex_theta[4]
        #    arc_theta[4]
        #    elbow_parallel[4]
        "is_show_annotation_creation": False,
        "line_normal":                 None,
        "line_normal_color":           WHITE,
        "line_normal_stroke_width":    4,
        "tex_theta":                   None,
        "tex_theta_color":             WHITE,
        "tex_theta_position_offset":   [ 1.0 * RIGHT + -0.4 * UP,
                                         1.0 * RIGHT +  0.4 * UP,
                                        -1.0 * RIGHT + -0.4 * UP,
                                         1.0 * RIGHT + -0.4 * UP],
        "arc_theta":                   None,
        "arc_theta_radius":            0.7,
        "arc_theta_color":             YELLOW,
        "arc_theta_pos_offset":        None,
        "elbow_theta":                 None,
        "elbow_length":                0.4,
        "elbow_color":                 YELLOW,
        "elbow_normal_para_offset":    1.5,
        "elbow_ray_para_ratio":        2/3,
        "elbow_position_angle_gen":    None,
    }


    def create_mirror_ray(self):
        """
           mirror_corner_pos
           +-------+----------- line_mirror_up_l1 (l1: mirror up)
           |      / \
           |     /   \
           |    /     \
           |   /       \
           |  /line_    \
           | /  ray_2    \
        r_1+              \ line_ray_3
           | \             \
           |  \
           |   \
           |    \ line_ray_1
           |
          line_mirror_left_n1 (n1: mirro left)

        """
        # The value tracker
        self.time_t = 0.0
        self.vtarcker_time_t = ValueTracker(self.time_t)

        # mirros
        self.line_mirror_up_l1   = Line(self.mirror_corner_pos, self.mirror_corner_pos + self.mirror_1_length * RIGHT,
                                        color=self.mirror_color,
                                        # color=RED,
                                        stroke_width=self.mirror_stroke_width)

        self.line_mirror_left_n1 = Line(self.mirror_corner_pos, self.mirror_corner_pos + self.mirror_2_length * DOWN,
                                        color=self.mirror_color,
                                        # color=GREEN,
                                        stroke_width=self.mirror_stroke_width)

        self.line_ray_1    = Arrow(ORIGIN, ORIGIN + RIGHT, # this positon is a placeholder. We set after ray_1_pos_gen is available
                                   color=self.ray_1_color, stroke_width = self.ray_1_stroke_width, buff=0)

        init_ray_1_theta = PI - (21/100) * PI
        self.ray_1_pos_gen = Ray_1_position_gen(self.line_ray_1, self.mirror_corner_pos, self.ray_1_spos, init_ray_1_theta)
        init_ray_1_start = self.ray_1_pos_gen.get_ray_1_start_pos(0.0)
        init_ray_1_end   = self.ray_1_pos_gen.get_ray_1_end_pos(0.0)
        self.line_ray_1.put_start_and_end_on(init_ray_1_start, init_ray_1_end)



        self.ray_2_pos_gen = Ray_2_position_gen(self.line_ray_1, self.mirror_corner_pos)
        self.line_ray_2    = Arrow(self.ray_2_pos_gen.get_ray_start_pos(), self.ray_2_pos_gen.get_ray_end_pos(),
                                   color=self.ray_2_color, stroke_width = self.ray_2_stroke_width, buff=0)

        self.ray_3_pos_gen = Ray_3_position_gen(self.mirror_corner_pos, self.line_ray_1, self.line_ray_2, self.ray_3_length)
        self.line_ray_3    = Arrow(self.ray_3_pos_gen.get_ray_start_pos(), self.ray_3_pos_gen.get_ray_end_pos(),
                                   color=self.ray_3_color, stroke_width = self.ray_3_stroke_width, buff=0)

        # Show all
        mobj_list = [self.line_mirror_up_l1, self.line_mirror_left_n1, self.line_ray_1, self.line_ray_2, self.line_ray_3]
        self.play(*[ShowCreation(mobj) for mobj in mobj_list])


    def get_line_normal_pos(self):
        """get line normal position based on the line_ray_1
        """
        normal_line_len = 2
        return (self.line_ray_1.get_end(), self.line_ray_1.get_end() + normal_line_len * RIGHT)

    def get_arc_center(self, idx):
        """get ith arc reference center
        """
        assert((0 <= idx) and (idx < 4))
        if (idx == 0):
            return self.line_ray_1.get_end()
        elif (idx == 1):
            return self.line_ray_1.get_end()
        elif (idx == 2):
            return self.line_ray_2.get_end()
        elif (idx == 3):
            return self.line_ray_2.get_end()

        assert(False)           # shold not be here
        return ORIGIN


    def get_arc_position(self, idx):
        """get arc position
         Assume self.arc_theta_pos_offset has been initialized at the arc creation.
        """
        assert((0 <= idx) and (idx < 4))
        return self.get_arc_center(idx) + self.arc_theta_pos_offset[idx]


    def get_arc_measure(self, idx):
        """get ith arc measure value
        return (start_angle, angle)
        """
        assert((0 <= idx) and (idx < 4))
        theta_mes = (PI - self.line_ray_1.get_angle())
        if (idx == 0):
            return (-theta_mes, theta_mes)
        elif (idx == 1):
            return (0, theta_mes)
        elif (idx == 2):
            return (PI, theta_mes)
        elif (idx == 3):
            return (-theta_mes, theta_mes)

        assert(False)           # shold not be here
        return ORIGIN



    def create_annotation(self):
        """
              e2
           +--->---+-----------
           |t3,a3|/ \| t4,a4
           |     /   \
           |    /     \
           |   /       \
           |  /         \
           | /| t2,a2    \
           +--->- ln,e1   v e4
           | \| t1,a1      \
           |  \
           |   \
           |    v e3
           |     \

        ln     self.line_normal
        t[0:3] self.tex_theta      0...3
        a[0:3] self.arc_theta      0...3
        e[0:3] self.elbow_parallel 0...3 for parallel sign (e0||e1, e2||e3)


            elbow_normal_para_offset
           |<-->|
           +---->--+-----------
           |    |   \
           |    |    \  ratio point: elbow_ray_para_ratio (2/3 ... length 2/3 from the reflection)
           |    |     \
           |    |      v
           |    |       \
           |    |        \
           +---->-        \
           |\
           | \
           |  \
           |   v  ratio point: elbow_ray_para_ratio (2/3 ... length 2/3 from the start)
           |    \


        """
        (n_start, n_end) = self.get_line_normal_pos()
        self.line_normal = Line(n_start, n_end,
                                color=self.line_normal_color,
                                # color=PURPLE,
                                stroke_width=self.line_normal_stroke_width)

        self.tex_theta = []
        tex_str = r"\theta"
        for i in range(0,4):
            self.tex_theta.append(TexMobject(tex_str, color=self.tex_theta_color))
            self.tex_theta[i].move_to(self.get_arc_center(i) + self.tex_theta_position_offset[i])


        self.arc_theta            = []
        self.arc_theta_pos_offset = []
        for i in range(0,4):
            (arc_start, arc_angle) = self.get_arc_measure(i)
            self.arc_theta.append(
                Arc(
                    start_angle = arc_start,
                    angle       = arc_angle,
                    radius      = self.arc_theta_radius,
                    color       = self.arc_theta_color,
                    arc_center  = ORIGIN  # initial center of the arc is at ORIGIN
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
            self.arc_theta[i].move_to(self.get_arc_position(i))


        self.elbow_position_angle_gen = Elbow_position_angle_gen(self.mirror_corner_pos,
                                                                 self.line_ray_1, self.elbow_normal_para_offset,
                                                                 self.line_ray_3, self.elbow_ray_para_ratio)

        self.elbow_parallel = []
        for i in range(0,4):
            self.elbow_parallel.append(ElbowRotate(width = self.elbow_length, angle=-PI/2,
                                                   color = self.elbow_color, about_point = ORIGIN))
            self.elbow_parallel[i].set_angle(self.elbow_position_angle_gen.get_elbow_angle(i))
            self.elbow_parallel[i].move_to(self.elbow_position_angle_gen.get_elbow_position(i))


        if (self.is_show_annotation_creation):
            self.play(ShowCreation(self.line_normal),
                      *[FadeIn(tex)       for tex in self.tex_theta],
                      *[ShowCreation(arc) for arc in self.arc_theta],
                      *[ShowCreation(elb) for elb in self.elbow_parallel],
            )



    def animate_ray_movement_parallel_only(self):
        """
        Depends on the value tracker's parameter t, animate the arrow
        """

        self.line_ray_1.add_updater(Ray_1_updater(self.ray_1_pos_gen, self.vtarcker_time_t))
        self.line_ray_2.add_updater(Ray_2_3_updater(self.ray_2_pos_gen))
        self.line_ray_3.add_updater(Ray_2_3_updater(self.ray_3_pos_gen))

        self.elbow_parallel[2].add_updater(Elbow_ray_updater(self.elbow_position_angle_gen, 2))
        self.elbow_parallel[3].add_updater(Elbow_ray_updater(self.elbow_position_angle_gen, 3))



        self.add(self.line_ray_1, self.line_ray_2, self.line_ray_3,
                 self.elbow_parallel[2], self.elbow_parallel[3])

        self.play(ApplyMethod(self.vtarcker_time_t.increment_value, 1.0))
        self.play(ApplyMethod(self.vtarcker_time_t.increment_value, 1.0))
        self.play(ApplyMethod(self.vtarcker_time_t.increment_value, 1.0), run_time=2)
        self.wait(self.wait_time)


    def construct(self):
        """Incident ray to a mirror animation (part 1)
        """

        # Create mobjects
        self.create_mirror_ray()
        # self.is_show_annotation_creation = True
        self.create_annotation()

        # animation
        self.animate_ray_movement_parallel_only()
        self.wait(5)
