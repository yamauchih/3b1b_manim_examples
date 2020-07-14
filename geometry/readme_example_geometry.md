# Geometry examples
1. Example 1. [A simple line start position move](https://github.com/yamauchih/3b1b_manim_examples/blob/master/geometry/readme_example_geometry.md#a-simple-line-start-position-move)
2. Example 2. [A comparison between line transform and line rotation](https://github.com/yamauchih/3b1b_manim_examples/blob/master/geometry/readme_example_geometry.md#a-comparison-between-transform-a-line-and-rotatin-a-line)


| Ex. 1 | Ex. 2 |
| --- | --- |
|<img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/geometry/gifs/ExampleGeometry_01_01.gif" width=300/>|
|<img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/geometry/gifs/ExampleGeometry_02_01.gif" width=300/>|


## A simple line start position move

```python3
class ExampleGeometry_01_01(Scene):
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
```

<p align="center"><img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/geometry/gifs/ExampleGeometry_01_01.gif" width=800/></p>

## A comparison between transform a line and rotatin a line

```python3
class ExampleGeometry_02_01(Scene):
    """
    Example Geometry_02 01

    Comparison between transforming a line and rotating a line
    """
    CONFIG={
    }

    def construct(self):

        x_0 = -1.5
        x_1 =  1.5
        start_0 = ORIGIN + x_0 * RIGHT
        end_0   = ORIGIN + x_1 * RIGHT
        line_1 = Line(start_0, end_0)
        line_2 = Line(start_0, end_0)
        self.play(ShowCreation(line_1))

        # rotate line animation by set angle (default: linear interpolation)
        self.play(ApplyMethod(line_1.set_angle, 1.5 * PI/2))
        self.wait(1)

        # rotate line animation by Rotate
        self.play(FadeOut(line_1), FadeIn(line_2))
        self.play(Rotate(line_2, angle=1.5 * PI/2, about_point=line_2.get_start()))
        self.wait(5)
```

<p align="center"><img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/geometry/gifs/ExampleGeometry_02_01.gif" width=800/></p>

