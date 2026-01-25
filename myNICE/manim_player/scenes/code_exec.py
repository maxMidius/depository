#-------------------------------
# vi: sw=4 ts=4 expandtab
#-------------------------------
"""
Code execution visualization scenes - function calls, stack, heap
"""

from manim import *


class FunctionCallStackVisualization(Scene):
    """Visualize function call stack with recursive calls"""

    def construct(self):
        # Title
        title = Text("Function Call Stack", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Show code
        code = Code(
            code="""def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)

result = factorial(4)""",
            language="python",
            font_size=20,
            background="window",
            style="monokai"
        ).to_edge(LEFT).shift(UP * 0.5)

        self.play(Create(code))
        self.wait(1)

        # Stack visualization area
        stack_label = Text("Call Stack", font_size=24).to_edge(RIGHT).shift(UP * 3)
        self.play(Write(stack_label))

        # Simulate function calls
        stack_frames = []
        calls = [
            ("factorial(4)", BLUE),
            ("factorial(3)", GREEN),
            ("factorial(2)", YELLOW),
            ("factorial(1)", ORANGE),
        ]

        y_offset = 2
        for call_name, color in calls:
            frame = Rectangle(
                width=2.5,
                height=0.8,
                fill_opacity=0.8,
                fill_color=color,
                stroke_color=WHITE
            )
            frame.move_to(RIGHT * 4.5 + UP * y_offset)

            label = Text(call_name, font_size=18, color=WHITE)
            label.move_to(frame.get_center())

            self.play(
                Create(frame),
                Write(label),
                run_time=0.6
            )
            stack_frames.append((frame, label))
            y_offset -= 1
            self.wait(0.3)

        self.wait(1)

        # Return values (pop stack)
        return_text = Text("Returning values...", font_size=24, color=GREEN).to_edge(DOWN)
        self.play(Write(return_text))
        self.wait(0.5)

        returns = ["1", "2", "6", "24"]
        for i in range(len(stack_frames) - 1, -1, -1):
            frame, label = stack_frames[i]

            # Show return value
            ret_val = Text(f"→ {returns[len(stack_frames) - 1 - i]}", font_size=20, color=YELLOW)
            ret_val.next_to(frame, RIGHT)

            self.play(Write(ret_val))
            self.wait(0.4)

            # Pop from stack
            self.play(
                FadeOut(frame),
                FadeOut(label),
                FadeOut(ret_val),
                run_time=0.5
            )
            self.wait(0.2)

        self.play(FadeOut(return_text))
        result_text = Text("Result: 24", font_size=36, color=GREEN).to_edge(DOWN)
        self.play(Write(result_text))
        self.wait(2)


class VariableScopeVisualization(Scene):
    """Visualize variable scopes and memory"""

    def construct(self):
        # Title
        title = Text("Variable Scope & Memory", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Code
        code = Code(
            code="""x = 10          # Global
def func():
    y = 20      # Local
    x = 30      # Local
    return x + y

result = func()
print(x)        # 10""",
            language="python",
            font_size=18,
            background="window",
            style="monokai"
        ).to_edge(LEFT)

        self.play(Create(code))
        self.wait(1)

        # Memory visualization
        global_box = Rectangle(width=3, height=2, fill_opacity=0.3, fill_color=BLUE, stroke_color=WHITE)
        global_box.shift(RIGHT * 4 + UP * 1.5)
        global_label = Text("Global Scope", font_size=20).next_to(global_box, UP, buff=0.2)

        self.play(Create(global_box), Write(global_label))

        # Global variable x
        global_x = Text("x = 10", font_size=20, color=YELLOW).move_to(global_box.get_center())
        self.play(Write(global_x))
        self.wait(0.5)

        # Function call - create local scope
        local_box = Rectangle(width=3, height=2, fill_opacity=0.3, fill_color=GREEN, stroke_color=WHITE)
        local_box.shift(RIGHT * 4 + DOWN * 1.5)
        local_label = Text("Local Scope (func)", font_size=18).next_to(local_box, UP, buff=0.2)

        self.play(Create(local_box), Write(local_label))
        self.wait(0.3)

        # Local variables
        local_y = Text("y = 20", font_size=20, color=YELLOW).move_to(local_box.get_center() + UP * 0.4)
        self.play(Write(local_y))
        self.wait(0.3)

        local_x = Text("x = 30", font_size=20, color=ORANGE).move_to(local_box.get_center() + DOWN * 0.4)
        self.play(Write(local_x))
        self.wait(0.5)

        # Highlight that local x shadows global x
        shadow_note = Text("Local x shadows global x", font_size=18, color=RED).to_edge(DOWN)
        self.play(Write(shadow_note))
        self.wait(1)

        # Return from function
        self.play(FadeOut(shadow_note))
        return_note = Text("Function returns 50", font_size=18, color=GREEN).to_edge(DOWN)
        self.play(Write(return_note))
        self.wait(0.5)

        # Remove local scope
        self.play(
            FadeOut(local_box),
            FadeOut(local_label),
            FadeOut(local_y),
            FadeOut(local_x),
            FadeOut(return_note)
        )

        # Global x unchanged
        final_note = Text("Global x is still 10", font_size=22, color=GREEN).to_edge(DOWN)
        self.play(Write(final_note))
        self.play(global_x.animate.set_color(GREEN))
        self.wait(2)


class ArrayMemoryVisualization(Scene):
    """Visualize array memory allocation and access"""

    def construct(self):
        # Title
        title = Text("Array Memory Layout", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Show array creation
        code_text = Text("arr = [10, 20, 30, 40, 50]", font_size=24, font="monospace").to_edge(LEFT).shift(UP * 2)
        self.play(Write(code_text))
        self.wait(0.5)

        # Memory cells
        values = [10, 20, 30, 40, 50]
        addresses = ["0x1000", "0x1004", "0x1008", "0x100C", "0x1010"]

        cells = VGroup()
        value_labels = VGroup()
        addr_labels = VGroup()
        index_labels = VGroup()

        for i, (val, addr) in enumerate(zip(values, addresses)):
            # Memory cell
            cell = Rectangle(width=1.2, height=1, fill_opacity=0.5, fill_color=BLUE, stroke_color=WHITE)

            # Value
            value_label = Text(str(val), font_size=24, color=YELLOW)
            value_label.move_to(cell.get_center())

            # Address
            addr_label = Text(addr, font_size=14, color=GREY, font="monospace")
            addr_label.next_to(cell, DOWN, buff=0.1)

            # Index
            index_label = Text(f"[{i}]", font_size=18, color=GREEN)
            index_label.next_to(cell, UP, buff=0.1)

            cells.add(cell)
            value_labels.add(value_label)
            addr_labels.add(addr_label)
            index_labels.add(index_label)

        cells.arrange(RIGHT, buff=0.1)
        cells.move_to(ORIGIN)

        for cell, value, addr, idx in zip(cells, value_labels, addr_labels, index_labels):
            value.move_to(cell.get_center())
            addr.next_to(cell, DOWN, buff=0.1)
            idx.next_to(cell, UP, buff=0.1)

        # Animate creation
        self.play(Create(cells))
        self.play(Write(value_labels))
        self.play(Write(addr_labels), Write(index_labels))
        self.wait(1)

        # Show array access
        access_text = Text("Accessing arr[2]", font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(Write(access_text))

        # Highlight accessed cell
        self.play(
            cells[2].animate.set_fill(GREEN, opacity=0.8),
            run_time=0.5
        )
        self.wait(0.5)

        # Show pointer
        pointer = Arrow(
            start=cells[2].get_top() + UP * 1.5,
            end=cells[2].get_top() + UP * 0.2,
            buff=0,
            color=RED,
            stroke_width=6
        )
        pointer_label = Text("Current", font_size=18, color=RED).next_to(pointer, UP, buff=0.1)

        self.play(Create(pointer), Write(pointer_label))
        self.wait(0.5)

        # Show value
        self.play(FadeOut(access_text))
        result_text = Text("Value: 30", font_size=28, color=GREEN).to_edge(DOWN)
        self.play(Write(result_text))
        self.wait(2)
