# Transform examples
1. Example 1. [Demonstrate how Transform() changes the memory contents](https://github.com/yamauchih/3b1b_manim_examples/blob/master/geometry/readme_example_transform.md)
1. Example 2. [Demonstrate how to keep the invariant with Transform()](https://github.com/yamauchih/3b1b_manim_examples/blob/master/geometry/readme_example_transform.md)

| Example  | With explain  |
| --- | --- |
|<img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/transform/gifs/Example_Transform_01_01.gif" width=300/>|<img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/transform/gifs/Example_Transform_01_02.gif" width=300/>|
|<img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/transform/gifs/Example_Transform_02_01.gif" width=300/>|<img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/transform/gifs/Example_Transform_02_02.gif" width=300/>|

## Demonstrate how Transform() changes the memory contents (minimal)
```python3
class Example_Transform_01_01(Scene):
    """Example Transform_01 01. minimal demo. x is overwitten.

    Demonstrate how the Transform(x, y) changes the memory image.
    x is transformed to y:
       tex_xy = ['x', 'y']
    are transformed
       tex_xy = ['y', 'y']

    From the variable point of view (memory image), Transform() does
       tex_xy[0] = deepcopy(tex_xy[1]) # &tex_xy[0] != &tex_xy[1]
    """
    CONFIG={
    }

    def construct(self):
        tex_xy = TexMobject(r"x", r"y", color=WHITE)
        tex_xy[0].move_to(-2.0 * RIGHT + 1.0 * UP)
        tex_xy[1].move_to(-2.0 * RIGHT + 0.0 * UP)

        self.play(FadeIn(tex_xy[0]), FadeIn(tex_xy[1]))
        self.wait(1)

        self.play(Transform(tex_xy[0], tex_xy[1]))
        self.wait(1)

        # x.shift, y.shift
        self.play(ApplyMethod(tex_xy[0].shift, RIGHT), ApplyMethod(tex_xy[1].shift, LEFT))
        self.wait(1)
```

<p align="center"><img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/transform/gifs/Example_Transform_01_01.gif" width=800/></p>
