# Graph 2d examples
1. [A simple y = cos(x) graph](https://github.com/yamauchih/3b1b_manim_examples/blob/master/graph_2d/readme_example_graph2d.md#a-simple-y--cosx-graph)
2. [Transform y = 0 to y = cos(x)](https://github.com/yamauchih/3b1b_manim_examples/blob/master/graph_2d/readme_example_graph2d.md#transform-y--0-to-y--cosx)
3. [Transform y = 0 to y = cos(x)](https://github.com/yamauchih/3b1b_manim_examples/blob/master/graph_2d/readme_example_graph2d.md#transform-y--0-to-y--cosx-1)

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

'''python3
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
'''
<p align="center"><img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/graph_2d/gifs/Example_Graph2d_01_02.gif" width=800/></p>

## Transform y = 0 to y = cos(x)

'''python3
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
'''
<p align="center"><img src ="https://github.com/yamauchih/3b1b_manim_examples/blob/master/graph_2d/gifs/Example_Graph2d_01_03.gif" width=800/></p>
