# -*- coding: utf-8; -*-
#
# Graph 2D example 02
# Copyright (C) 2020 Hitoshi Yamauchi
#
# License: BSD 3-Clause License
#
# References:
#  * 3Blue1Brown (https://github.com/3b1b/manim)
#  * Todd Zimmerman (Talking Physics https://talkingphysics.wordpress.com/)
#  * Theorem of Beethoven (https://www.youtube.com/channel/UCxiWCEdx7aY88bSEUgLOC6A)
#
# Preview resolution rendering
#   python3 -m manim example_graph2d_02.py Example_Graph2d_02_01 --resolution 360,640 -pl
# Full resolution rendering
#   python3 -m manim example_graph2d_02.py Example_Graph2d_02_02 --resolution 720,1280 -p --high_quality
#

from manimlib.imports import *
import os, copy
import pyclbr


class Example_Graph2d_02_02(GraphScene):
    """Example Graph2d_02 02
    Create a graph of f(x) = 0
    Then, trasform to g(x) = cos(x)

    Follow a Dot from one point on f(k) to g(k)
    Follow a normal vector arrow at point on f(k) to g(k)

    This does not look up the function point f(x) in the animation.
    Thus, we rely on:
    * all the path function are util.straight_path
    * the same interpolation function applies to {each point
      of ParametricFunction, Dot, Arrow}

    This works well, but if you really need to follow any path, any
    interpolation function, you need to write an Animation class,
    which gets interpolation alpha while play().

    """
    CONFIG = {
        # original: y = 0
        "function_orginal" : lambda x : 0,
        "function_orginal_color" : GREEN,

        # target: y = cos(x)
        "function_target" : lambda x : np.cos(x),
        "function_target_color" :  GREEN,

        "axes_color":     GRAY,
        "x_axis_label":   "$x$",
        "y_axis_label":   "$y$",
        "x_labeled_nums": range(-2,3,1),
        "y_labeled_nums": range(-1,2,1),
        "center_point":     0,
        "x_min" :          -2,
        "x_max" :           2,
        "y_min" :        -1.5,
        "y_max" :         1.5,
        "graph_origin" : ORIGIN,
    }

    # Get given graph point
    #
    # @param[in] pgraph  a parametric graph
    # @param[in] val_x   x value of the graph
    # @return point on the graph at x
    def get_graph_point(self, pgraph, val_x):
        val_y = pgraph.underlying_function(val_x)
        return np.array((val_x, val_y, 0.0))


    def construct(self):
        # Axis but no animation
        self.setup_axes(animate=False)

        # Create a manim drawable graph (a ParametricFunction)
        # using GraphScene.get_graph()
        # This is the Transform source graph.
        original_drawable_parametric_graph = self.get_graph(
            self.function_orginal,
            self.function_orginal_color,
        )

        # create working copy to keep the original
        work_graph = copy.deepcopy(original_drawable_parametric_graph)

        # Create a manim drawable graph (a ParametricFunction)
        # using GraphScene.get_graph()
        # This is the Transform target graph.
        target_drawable_parametric_graph = self.get_graph(
            self.function_target,
            self.function_target_color,
        )

        # Show the original function y = 0
        self.play(ShowCreation(work_graph))
        self.wait(1)

        # x coordinate of the point
        x_1 = 1.0

        # Graph coordinate
        gcoord_src = self.get_graph_point(original_drawable_parametric_graph, x_1)
        gcoord_dst = self.get_graph_point(target_drawable_parametric_graph,   x_1)
        # Screen position
        spos_src = self.coords_to_point(gcoord_src[0], gcoord_src[1])
        spos_dst = self.coords_to_point(gcoord_dst[0], gcoord_dst[1])
        # Dot
        dot_src = Dot(spos_src, color=YELLOW)
        dot_dst = Dot(spos_dst, color=YELLOW)
        self.add(dot_src)

        # Note: we need the aspect (approximately) ratio = 1 graph,
        # otherwise direction will distort by this calculation.
        # E.g., try x_min = -20, x_max = 20
        normal_src = UP
        m_sin_x_1  = -np.sin(x_1)
        normal_dst = np.array((-m_sin_x_1, x_1, 0.0)) / math.sqrt(m_sin_x_1**2 + x_1**2)

        normal_arrow_src = Arrow(spos_src, spos_src + normal_src, stroke_width = 16, color=WHITE, buff=0)
        normal_arrow_dst = Arrow(spos_dst, spos_dst + normal_dst, stroke_width = 16, color=WHITE, buff=0)
        self.add(normal_arrow_src)

        self.play(Transform(work_graph, target_drawable_parametric_graph),
                  Transform(dot_src, dot_dst),
                  Transform(normal_arrow_src, normal_arrow_dst))
        self.wait(5)
