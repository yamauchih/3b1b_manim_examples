# Transform examples
1. Example 1. [Demonstrate how Transform() changes the memory contents](https://github.com/yamauchih/3b1b_manim_examples/blob/master/transform/readme_example_transform.md#demonstrate-how-transform-changes-the-memory-contents-minimal)
1. Example 2. [Demonstrate how to keep the invariant with Transform()](https://github.com/yamauchih/3b1b_manim_examples/blob/master/transform/readme_example_transform.md#demonstrate-how-to-keep-the-invariant-with-transform-minimal)

| Example  | With explanation  |
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

## Demonstrate how Transform() changes the memory contents (with an explanation)
```python3
class Example_Transform_01_02(Scene):
    """Example Transform_01 02 with explanation.

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
        wait_time = 1
        text_0 = TextMobject("Demo: Transform(x, y) overwrites x.",
                             color=WHITE).move_to(-2.0 * RIGHT + 3.0 * UP)
        text_1 = TextMobject("The contents of x is gone.",
                             color=WHITE).move_to(-2.0 * RIGHT + 2.0 * UP)

        tex_xy = TexMobject(r"x", r"y", color=WHITE)
        tex_xy[0].move_to(-2.0 * RIGHT + 1.0 * UP)
        tex_xy[1].move_to(-2.0 * RIGHT + 0.0 * UP)

        self.play(FadeIn(text_0), FadeIn(text_1), FadeIn(tex_xy[0]), FadeIn(tex_xy[1]))
        self.wait(wait_time)

        str_ary = [r"Transform(x,y)",
                   r"x.shift, RIGHT",
                   r"y.shift, LEFT",
                   r"FadeOut(x)",
                   r"FadeOut(y)",
        ]
        text_ary = []
        for s in str_ary:
            text = TextMobject(s, color=WHITE).move_to( 2.0 * RIGHT + 0.0 * UP)
            text_ary.append(text)

        cur_text = 0
        self.play(Transform(tex_xy[0], tex_xy[1]), FadeIn(text_ary[cur_text]))
        self.wait(wait_time)

        # x.shift
        self.play(ApplyMethod(tex_xy[0].shift, RIGHT), FadeOut(text_ary[cur_text]), FadeIn(text_ary[cur_text + 1]))
        self.wait(wait_time)
        cur_text += 1

        # y.shift
        self.play(ApplyMethod(tex_xy[1].shift, LEFT),  FadeOut(text_ary[cur_text]), FadeIn(text_ary[cur_text + 1]))
        self.wait(wait_time)
        cur_text += 1

        # FadeOut(x)
        self.play(FadeOut(tex_xy[0]), FadeOut(text_ary[cur_text]), FadeIn(text_ary[cur_text + 1]))
        self.wait(wait_time)
        cur_text += 1

        # FadeOut(y)
        self.play(FadeOut(tex_xy[1]), FadeOut(text_ary[cur_text]), FadeIn(text_ary[cur_text + 1]))
        self.wait(wait_time)
        cur_text += 1

        self.wait(1)
```

<p align="center"><img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/transform/gifs/Example_Transform_01_02.gif" width=800/></p>

## Demonstrate how to keep the invariant with Transform() (minimal)
```python3
class Example_Transform_02_01(Scene):
    """Example Transform_01 02. minimal demo. keep x, y invariant.

    Even after a Transform(), sometimes we want to keep the
    same memory contents to when we started.

    But Transform() does
      Transform(x,y): x = deepcopy(y)
    Thus, x is overwritten and the contents will be gone.

    To avoid x is overwritten, first make a working copy.
    Note: TexMobject does not support item assignment,
    so we use a variable 'work' here.

      tex_xy = ['x', 'y']
      work   = deepcopy(tex_xy[0])
      Transform(work, y)           # work = deepcopy(y)
      remove(work)

    In this way, tex_xy doesn't change.

    I found this useful when the animation is long, we can still
    keep some mobjects invariant.
    """
    CONFIG={
    }

    def construct(self):
        # tex_xy = ["x", "y"]
        tex_xy = TexMobject(r"x", r"y", color=WHITE)
        tex_xy[0].move_to(-2.0 * RIGHT + 1.0 * UP)
        tex_xy[1].move_to(-2.0 * RIGHT + 0.0 * UP)

        # tex_xy = ["x", "y"], work = "x"
        work = copy.deepcopy(tex_xy[0])

        self.play(FadeIn(work), FadeIn(tex_xy[1]))
        self.wait(1)

        self.play(Transform(work, tex_xy[1]))
        self.wait(1)

        # FadeIn(x)
        self.play(FadeIn(tex_xy[0]))
        self.wait(1)

        # x.shift RIGHT, y.shift LEFT, work.shift DOWN
        self.play(ApplyMethod(tex_xy[0].shift, RIGHT), ApplyMethod(tex_xy[1].shift, LEFT), ApplyMethod(work.shift, DOWN))
        self.wait(1)
```

<p align="center"><img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/transform/gifs/Example_Transform_02_01.gif" width=800/></p>

## Demonstrate how to keep the invariant with Transform() (with an explanation)
```python3
class Example_Transform_02_02(Scene):
    """Example Transform_02 02 with explanation.

    Even after a Transform(), sometimes we want to keep the
    same memory contents to when we started.

    But Transform() does
      Transform(x,y): x = deepcopy(y)
    Thus, x is overwritten and the contents will be gone.

    To avoid x is overwritten, first make a working copy.
    Note: TexMobject does not support item assignment,
    so we use a variable 'work' here.

      tex_xy = ['x', 'y']
      work   = deepcopy(tex_xy[0])
      Transform(work, y)           # work = deepcopy(y)
      remove(work)

    In this way, tex_xy doesn't change.

    I found this useful when the animation is long, we can still
    keep some mobjects invariant.
    """
    CONFIG={
    }

    def construct(self):
        wait_time = 1
        text_0 = TextMobject("Demo: Transform(work, y)",
                             color=WHITE).move_to(-2.0 * RIGHT + 3.0 * UP)
        text_1 = TextMobject("Using a work memory. No change x,y.",
                             color=WHITE).move_to(-2.0 * RIGHT + 2.0 * UP)

        # tex_xy = ["x", "y"]
        tex_xy = TexMobject(r"x", r"y", color=WHITE)
        tex_xy[0].move_to(-2.0 * RIGHT + 1.0 * UP)
        tex_xy[1].move_to(-2.0 * RIGHT + 0.0 * UP)

        # tex_xy = ["x", "y"], work = "x"
        work = copy.deepcopy(tex_xy[0])

        self.play(FadeIn(text_0), FadeIn(text_1))
        # Note: FadeIn work, not tex_xy[0]
        self.play(FadeIn(work), FadeIn(tex_xy[1]))
        self.wait(wait_time)

        str_ary = [r"Transform(work,y)",
                   r"FadeIn(x)",
                   r"work.shift, DOWN",
                   r"FadeOut(work)",
                   r"x.shift, RIGHT",
                   r"y.shift, LEFT",
                   r"FadeOut(x)",
                   r"FadeOut(y)",
        ]
        text_ary = []
        for s in str_ary:
            text = TextMobject(s, color=WHITE).move_to( 2.0 * RIGHT + 0.0 * UP)
            text_ary.append(text)

        cur_text = 0
        # Transforrm(work, y): tex_xy = ['x', 'y'], work = 'y'
        self.play(Transform(work, tex_xy[1]), FadeIn(text_ary[cur_text]))
        self.wait(wait_time)

        # FadeIn(x)
        self.play(FadeIn(tex_xy[0]), FadeOut(text_ary[cur_text]), FadeIn(text_ary[cur_text + 1]))
        self.wait(wait_time)
        cur_text += 1

        # work.shift
        self.play(ApplyMethod(work.shift, DOWN), FadeOut(text_ary[cur_text]), FadeIn(text_ary[cur_text + 1]))
        self.wait(wait_time)
        cur_text += 1

        # FadeOut(work)
        self.play(FadeOut(work), FadeOut(text_ary[cur_text]), FadeIn(text_ary[cur_text + 1]))
        self.wait(wait_time)
        cur_text += 1

        # x.shift
        self.play(ApplyMethod(tex_xy[0].shift, RIGHT), FadeOut(text_ary[cur_text]), FadeIn(text_ary[cur_text + 1]))
        self.wait(wait_time)
        cur_text += 1

        # y.shift
        self.play(ApplyMethod(tex_xy[1].shift, LEFT),  FadeOut(text_ary[cur_text]), FadeIn(text_ary[cur_text + 1]))
        self.wait(wait_time)
        cur_text += 1

        # FadeOut(x)
        self.play(FadeOut(tex_xy[0]), FadeOut(text_ary[cur_text]), FadeIn(text_ary[cur_text + 1]))
        self.wait(wait_time)
        cur_text += 1

        # FadeOut(y)
        self.play(FadeOut(tex_xy[1]), FadeOut(text_ary[cur_text]), FadeIn(text_ary[cur_text + 1]))
        self.wait(wait_time)
        cur_text += 1

        self.wait(1)
```

<p align="center"><img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/transform/gifs/Example_Transform_02_02.gif" width=800/></p>
