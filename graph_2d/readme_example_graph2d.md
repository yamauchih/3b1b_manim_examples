# Graph 2d examples
1. Example 1. [A simple y = cos(x) graph](https://github.com/yamauchih/3b1b_manim_examples/blob/master/graph_2d/readme_example_graph2d.md#a-simple-y--cosx-graph)
2. Example 2. [Transform y = 0 to y = cos(x)](https://github.com/yamauchih/3b1b_manim_examples/blob/master/graph_2d/readme_example_graph2d.md#transform-y--0-to-y--cosx)
3. Example 3. [Transform y = 0 to y = cos(x), but keep the y = 0](https://github.com/yamauchih/3b1b_manim_examples/blob/master/graph_2d/readme_example_graph2d.md#transform-y--0-to-y--cosx-1)
4. Example 4. [Transform y = 0 to y = cos(x), tracking normal at x = 1]()


| Example 1 | Example 2 | Example 3 |
| --- | --- | --- | 
|<img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/graph_2d/gifs/Example_Graph2d_01_01.gif" width=300/>|<img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/graph_2d/gifs/Example_Graph2d_01_02.gif" width=300/>|<img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/graph_2d/gifs/Example_Graph2d_01_03.gif" width=300/>|
| Example 4 |  |  |
|<img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/graph_2d/gifs/Example_Graph2d_02_02.gif" width=300/>|||



## A simple y = cos(x) graph

```python3
class Example_Graph2d_01_01(GraphScene):
    """
    Example Graph2d_01 01
    Create a y = cos(x) graph
    """
    CONFIG = {
        "axes_color":     GRAY,
        "x_axis_label":   "$x$",
        "y_axis_label":   "$y$",
        "x_labeled_nums": range(-10,12,2),
        "y_labeled_nums": range(-1,2,1),
        "center_point":     0,
        "x_min" :         -10,
        "x_max" :          10,
        "y_min" :        -1.5,
        "y_max" :         1.5,
        "graph_origin" : ORIGIN,
    }A simple y = cos(x) graph

    def construct(self):
        # Axis creation with animation
        self.setup_axes(animate=True)

        # Create a manim drawable graph (a ParametricFunction)
        # using GraphScene.get_graph()
        drawable_parametric_graph = self.get_graph(
            lambda x : np.cos(x),
            BLUE,
        )

        # Show the function y = cos(x)
        self.play(ShowCreation(drawable_parametric_graph))
        self.wait(5)
```

<p align="center"><img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/graph_2d/gifs/Example_Graph2d_01_01.gif" width=800/></p>

## Transform y = 0 to y = cos(x)

```python3
class Example_Graph2d_01_02(GraphScene):
    """
    Example Graph2d_01 02
    Create a graph of y = 0
    Then, trasform to y = cos(x)
    """
    CONFIG = {
        # original: y = 0
        "function_orginal" : lambda x : 0,
        "function_orginal_color" : BLUE,

        # target: y = cos(x)
        "function_target" : lambda x : np.cos(x),
        "function_target_color" : GREEN,

        "axes_color":     GRAY,
        "x_axis_label":   "$x$",
        "y_axis_label":   "$y$",
        "x_labeled_nums": range(-10,12,2),
        "y_labeled_nums": range(-1,2,1),
        "center_point":     0,
        "x_min" :         -10,
        "x_max" :          10,
        "y_min" :        -1.5,
        "y_max" :         1.5,
        "graph_origin" : ORIGIN,
    }

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
        self.wait()

        # run_time is used in composition. Animation has this parameter. How fast it transform.
        # Transform(a, b) write b to memory a. The work_graph memory is overwritten.
        # Thus, we keep the original_drawable_parametric_graph.
        # run_time controls how much time for the animation, a larger number makes slower.
        self.play(Transform(work_graph, target_drawable_parametric_graph, run_time = 2))
        self.wait(1)
        self.play(Transform(work_graph, original_drawable_parametric_graph, run_time = 2))
        self.wait(1)
        self.play(Transform(work_graph, target_drawable_parametric_graph, run_time = 1))
        self.wait(1)
        self.play(Transform(work_graph, original_drawable_parametric_graph, run_time = 1))

        self.wait(5)
```
<p align="center"><img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/graph_2d/gifs/Example_Graph2d_01_02.gif" width=800/></p>

## Transform y = 0 to y = cos(x), but keep the y = 0

```python3
class Example_Graph2d_01_03(GraphScene):
    """
    Example Graph2d_01 02
    Create a graph of y = 0
    Keep the y = 0, but trasform to y = cos(x)
    """
    CONFIG = {
        # original: y = 0
        "function_orginal" : lambda x : 0,
        "function_orginal_color" : BLUE,

        # target: y = cos(x)
        "function_target" : lambda x : np.cos(x),
        "function_target_color" : GREEN,

        "axes_color":     GRAY,
        "x_axis_label":   "$x$",
        "y_axis_label":   "$y$",
        "x_labeled_nums": range(-10,12,2),
        "y_labeled_nums": range(-1,2,1),
        "center_point":     0,
        "x_min" :         -10,
        "x_max" :          10,
        "y_min" :        -1.5,
        "y_max" :         1.5,
        "graph_origin" : ORIGIN,
    }

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

        # Create a manim drawable graph (a ParametricFunction)
        # using GraphScene.get_graph()
        # This is the Transform target graph.
        target_drawable_parametric_graph = self.get_graph(
            self.function_target,
            self.function_target_color,
        )

        # Show the original function y = 0
        self.play(ShowCreation(original_drawable_parametric_graph))
        self.wait()

        # This is a placeholder, invisible at first. and used by Transform.
        work_graph = copy.deepcopy(original_drawable_parametric_graph)

        # run_time parameter is used in composition.
        # Animation has this parameter. How fast it transform.

        # Transform(a, b) is the memory a is written by b, and pointing at a
        # ReplacementTransform(a, b) is the memory a is written by b, and pointing at b.
        # See 16 manim tutorial 4.1 Transformations by Theorem of Beethoven
        self.play(Transform(work_graph, target_drawable_parametric_graph, run_time = 2))
        self.wait(1)
        self.play(Transform(work_graph, original_drawable_parametric_graph, run_time = 2))
        self.wait(5)
```
<p align="center"><img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/graph_2d/gifs/Example_Graph2d_01_03.gif" width=800/></p>

## Transform y = 0 to y = cos(x), tracking normal at x = 1

```python3
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
```
<p align="center"><img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/graph_2d/gifs/Example_Graph2d_02_02.gif" width=800/></p>

