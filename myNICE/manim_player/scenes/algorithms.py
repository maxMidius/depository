#-------------------------------
# vi: sw=4 ts=4 expandtab
#-------------------------------
"""
Algorithm visualization scenes for sorting, searching, trees, and graphs
"""

from manim import *


class BubbleSortVisualization(Scene):
    """Visualize the bubble sort algorithm with array bars"""

    def construct(self):
        # Initial array
        numbers = [64, 34, 25, 12, 22, 11, 90]
        max_num = max(numbers)

        # Create title
        title = Text("Bubble Sort Algorithm", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create bars
        bars = VGroup()
        labels = VGroup()

        for i, num in enumerate(numbers):
            bar_height = (num / max_num) * 3
            bar = Rectangle(
                width=0.8,
                height=bar_height,
                fill_opacity=0.8,
                fill_color=BLUE,
                stroke_color=WHITE,
                stroke_width=2
            )
            label = Text(str(num), font_size=20).next_to(bar, DOWN, buff=0.1)

            bars.add(bar)
            labels.add(label)

        # Arrange bars
        bars.arrange(RIGHT, buff=0.2)
        for bar, label in zip(bars, labels):
            label.move_to(bar.get_bottom() + DOWN * 0.3)

        bars.move_to(ORIGIN)
        labels.move_to(bars.get_bottom() + DOWN * 0.3)

        self.play(Create(bars), Write(labels))
        self.wait(1)

        # Bubble sort algorithm
        n = len(numbers)
        for i in range(n):
            for j in range(n - 1 - i):
                # Highlight comparison
                self.play(
                    bars[j].animate.set_fill(RED),
                    bars[j + 1].animate.set_fill(RED),
                    run_time=0.3
                )

                if numbers[j] > numbers[j + 1]:
                    # Swap animation
                    numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]

                    # Animate swap
                    self.play(
                        bars[j].animate.shift(RIGHT * 1.0),
                        bars[j + 1].animate.shift(LEFT * 1.0),
                        labels[j].animate.shift(RIGHT * 1.0),
                        labels[j + 1].animate.shift(LEFT * 1.0),
                        run_time=0.5
                    )

                    # Swap in VGroup
                    bars.submobjects[j], bars.submobjects[j + 1] = bars.submobjects[j + 1], bars.submobjects[j]
                    labels.submobjects[j], labels.submobjects[j + 1] = labels.submobjects[j + 1], labels.submobjects[j]

                # Restore color
                self.play(
                    bars[j].animate.set_fill(BLUE),
                    bars[j + 1].animate.set_fill(BLUE),
                    run_time=0.2
                )

            # Mark sorted element as green
            self.play(bars[n - 1 - i].animate.set_fill(GREEN), run_time=0.3)

        # All sorted
        completion_text = Text("Sorted!", font_size=48, color=GREEN).to_edge(DOWN)
        self.play(Write(completion_text))
        self.wait(2)


class BinarySearchVisualization(Scene):
    """Visualize binary search algorithm"""

    def construct(self):
        # Title
        title = Text("Binary Search Algorithm", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Sorted array
        numbers = [2, 5, 8, 12, 16, 23, 38, 45, 56, 67, 78]
        target = 23

        # Create array visualization
        cells = VGroup()
        values = VGroup()

        for num in numbers:
            cell = Square(side_length=0.7, fill_opacity=0.3, fill_color=BLUE, stroke_color=WHITE)
            value = Text(str(num), font_size=20)
            value.move_to(cell.get_center())

            cells.add(cell)
            values.add(value)

        cells.arrange(RIGHT, buff=0.1)
        cells.move_to(ORIGIN)

        for cell, value in zip(cells, values):
            value.move_to(cell.get_center())

        self.play(Create(cells), Write(values))
        self.wait(0.5)

        # Target indicator
        target_text = Text(f"Target: {target}", font_size=28, color=YELLOW).to_edge(DOWN)
        self.play(Write(target_text))
        self.wait(0.5)

        # Binary search algorithm
        left, right = 0, len(numbers) - 1
        step = 1

        while left <= right:
            mid = (left + right) // 2

            # Highlight search range
            for i in range(left, right + 1):
                self.play(cells[i].animate.set_fill(YELLOW, opacity=0.3), run_time=0.1)

            # Highlight middle element
            self.play(cells[mid].animate.set_fill(RED, opacity=0.7), run_time=0.3)

            step_text = Text(f"Step {step}: Check middle = {numbers[mid]}", font_size=24).next_to(target_text, UP)
            self.play(Write(step_text))
            self.wait(0.8)

            if numbers[mid] == target:
                # Found!
                self.play(cells[mid].animate.set_fill(GREEN, opacity=0.9), run_time=0.5)
                found_text = Text(f"Found {target} at index {mid}!", font_size=32, color=GREEN)
                found_text.next_to(cells, DOWN, buff=1)
                self.play(Write(found_text))
                self.wait(2)
                break
            elif numbers[mid] < target:
                # Search right half
                for i in range(left, mid + 1):
                    self.play(cells[i].animate.set_fill(GREY, opacity=0.2), run_time=0.1)
                left = mid + 1
            else:
                # Search left half
                for i in range(mid, right + 1):
                    self.play(cells[i].animate.set_fill(GREY, opacity=0.2), run_time=0.1)
                right = mid - 1

            self.play(FadeOut(step_text))
            step += 1

        self.wait(1)


class DijkstraVisualization(Scene):
    """Visualize Dijkstra's shortest path algorithm"""

    def construct(self):
        # Title
        title = Text("Dijkstra's Shortest Path", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create graph vertices
        vertices = {
            "A": [-3, 2, 0],
            "B": [0, 2, 0],
            "C": [3, 2, 0],
            "D": [-3, -1, 0],
            "E": [0, -1, 0],
            "F": [3, -1, 0]
        }

        edges = [
            ("A", "B", 4),
            ("A", "D", 1),
            ("B", "C", 3),
            ("B", "E", 2),
            ("C", "F", 2),
            ("D", "E", 5),
            ("E", "F", 1)
        ]

        # Create vertex objects
        vertex_objects = {}
        vertex_labels = {}

        for name, pos in vertices.items():
            circle = Circle(radius=0.4, fill_opacity=0.8, fill_color=BLUE, stroke_color=WHITE)
            circle.move_to(pos)
            label = Text(name, font_size=28, color=WHITE)
            label.move_to(circle.get_center())

            vertex_objects[name] = circle
            vertex_labels[name] = label

        # Create edge objects
        edge_objects = []
        edge_weights = []

        for source, target, weight in edges:
            start = vertex_objects[source].get_center()
            end = vertex_objects[target].get_center()
            line = Line(start, end, stroke_color=GREY, stroke_width=2)

            # Weight label at midpoint
            mid = (start + end) / 2
            weight_label = Text(str(weight), font_size=20, color=YELLOW)
            weight_label.move_to(mid + UP * 0.3)

            edge_objects.append(line)
            edge_weights.append(weight_label)

        # Draw graph
        self.play(*[Create(line) for line in edge_objects])
        self.play(*[Write(weight) for weight in edge_weights])
        self.play(*[Create(vertex_objects[name]) for name in vertices.keys()])
        self.play(*[Write(vertex_labels[name]) for name in vertices.keys()])
        self.wait(1)

        # Start from A
        start_text = Text("Starting from A", font_size=24).to_edge(DOWN)
        self.play(Write(start_text))
        self.play(vertex_objects["A"].animate.set_fill(GREEN, opacity=0.9))
        self.wait(1)

        # Simulate visiting nodes (simplified visualization)
        visit_order = ["A", "D", "B", "E", "F", "C"]

        for i in range(1, len(visit_order)):
            node = visit_order[i]
            self.play(vertex_objects[node].animate.set_fill(GREEN, opacity=0.9), run_time=0.8)
            self.wait(0.5)

        self.play(FadeOut(start_text))
        complete_text = Text("Shortest paths found!", font_size=32, color=GREEN).to_edge(DOWN)
        self.play(Write(complete_text))
        self.wait(2)
