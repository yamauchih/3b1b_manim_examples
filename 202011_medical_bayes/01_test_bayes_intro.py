# -*- coding: utf-8; -*-
#
# disease test and Bayes' theorem
#
# 01_test_bayes_intro
#
#    (C) 2020 Hitoshi Yamauchi
#
# New BSD License
#
# Using community manim: 28a733e9
#
# Activate poetry (venv)
#  cd data/gitdata/manim/community/manim
#  poetry shell
#
# Full resolution
#   python3 -m manim 01_test_bayes_intro.py TestBayes01 --resolution 720,1280 -p --high_quality
# Preview resolution
#   python3 -m manim 01_test_bayes_intro.py TestBayes01 --resolution 360,640 -p -ql
#

from manim import *
import myutil


class TestBayes01(Scene):
# class TestBayes01(LinearTransformationScene):
    """Test and Bayes 01: intro

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
        "wait_time":            3,

        # title scaling factor
        "scale_title_f":    0.9,
        # equation scaling factor
        "scale_eq_f":       1.0,
        # text scaling factor
        "scale_txt_f":      0.8,

        #-- shared MObjects
        # time parameter t and its value tracker
        "txt_title_ja":    None,
        "txt_title_en":    None,
        "txt_ref_video":   None,
        "txt_footnote_en": None,
    }

    def create_title(self):
        """
        """
        scale_f = 0.7
        self.txt_title_ja  = Text(r"病気の検査とベイズの定理")            .scale(self.scale_title_f)
        self.txt_title_en  = Text(r"Medical Diagnosis and Bayes' Theorem").scale(self.scale_txt_f)
        self.txt_ref_video = [Text(r"参考ビデオ(英語)")                   .scale(self.scale_txt_f),
                          Text(r"* 3Blue1Brown: Bayes theorem")       .scale(self.scale_txt_f),
                          Text(r"* Numberphile: Are you REALLY sick?").scale(self.scale_txt_f),
                          Text(r"* Veritasium:  The Bayesian Trap")   .scale(self.scale_txt_f)]
        self.txt_footnote_en = Text(r"The video narration is in Japanese with English subtitles.").scale(self.scale_txt_f * 0.85)

        myutil.critical_point_move_to(self.txt_title_ja,     LEFT + DOWN, ORIGIN + -6   * RIGHT +  2.8 * UP)
        myutil.critical_point_move_to(self.txt_title_en,     LEFT + DOWN, ORIGIN + -6   * RIGHT +  1.8 * UP)
        myutil.critical_point_move_to(self.txt_ref_video[0], LEFT + DOWN, ORIGIN + -6   * RIGHT +  0.5 * UP)
        myutil.critical_point_move_to(self.txt_ref_video[1], LEFT + DOWN, ORIGIN + -5.5 * RIGHT + -0.5 * UP)
        myutil.critical_point_move_to(self.txt_ref_video[2], LEFT + DOWN, ORIGIN + -5.5 * RIGHT + -1.4 * UP)
        myutil.critical_point_move_to(self.txt_ref_video[3], LEFT + DOWN, ORIGIN + -5.5 * RIGHT + -2.3 * UP)
        myutil.critical_point_move_to(self.txt_footnote_en,  LEFT + DOWN, ORIGIN + -6.5 * RIGHT + -3.2 * UP)



    def animate_title(self):
        """
        """
        self.play(FadeIn(self.txt_title_ja),
                  FadeIn(self.txt_title_en),
                  FadeIn(self.txt_footnote_en))
        self.wait(self.wait_time + 3)


        self.play(FadeIn(self.txt_ref_video[0]))
        self.wait(self.wait_time)

        self.play(FadeIn(self.txt_ref_video[1]),
                  FadeIn(self.txt_ref_video[2]),
                  FadeIn(self.txt_ref_video[3]))
        self.wait(self.wait_time)



    def construct(self):
        """Test and Bayes intro
        """
        # Title

        self.create_title()
        self.animate_title()

        self.wait(5)
