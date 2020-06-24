# -*- coding: utf-8; -*-
#
# Geometry example 01
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
#   python3 -m manim example_geometry_01.py Example_Geometry_01_01 --resolution 360,640 -pl
# Full resolution rendering
#   python3 -m manim example_geometry_01.py Example_Geometry_01_01 --resolution 720,1280 -p --high_quality
#

from manimlib.imports import *
import os, copy
import pyclbr

class Example_Geometry_01_01(Scene):
    """
    Example Geometry_01 01
    A line moves between x = x_0, x_1
    This is not a rotation. It changes the start position.
    """
    CONFIG={
    }

    def construct(self):

        x_0 = -2
        x_1 =  2
        start_0 = ORIGIN + x_0 * RIGHT + DOWN
        end_0   = ORIGIN + x_1 * RIGHT + DOWN
        line_1 = Line(start_0, end_0)
        self.play(ShowCreation(line_1))

        start_1 = start_0 + 3.0 * UP
        end_1   = end_0

        # Note: set_start_and_end_attrs doesn't change (no point generation?)
        self.play(ApplyMethod(line_1.put_start_and_end_on, start_1, end_1))
        self.wait(3)
