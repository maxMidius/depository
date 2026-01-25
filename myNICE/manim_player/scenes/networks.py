#-------------------------------
# vi: sw=4 ts=4 expandtab
#-------------------------------
"""
Network flow and routing visualization scenes
"""

from manim import *


class NetworkFlowVisualization(Scene):
    """Visualize network flow through a graph"""

    def construct(self):
        # Title
        title = Text("Network Flow Visualization", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create network graph
        vertices = {
            "Source": [-4, 0, 0],
            "A": [-2, 2, 0],
            "B": [-2, -2, 0],
            "C": [2, 2, 0],
            "D": [2, -2, 0],
            "Sink": [4, 0, 0]
        }

        edges = [
            ("Source", "A", 10),
            ("Source", "B", 10),
            ("A", "C", 4),
            ("A", "D", 8),
            ("B", "C", 9),
            ("B", "D", 6),
            ("C", "Sink", 10),
            ("D", "Sink", 10)
        ]

        # Create vertices
        vertex_objects = {}
        vertex_labels = {}

        for name, pos in vertices.items():
            if name in ["Source", "Sink"]:
                color = YELLOW
            else:
                color = BLUE

            circle = Circle(radius=0.5, fill_opacity=0.8, fill_color=color, stroke_color=WHITE, stroke_width=3)
            circle.move_to(pos)

            label = Text(name, font_size=20 if len(name) > 2 else 24, color=WHITE)
            label.move_to(circle.get_center())

            vertex_objects[name] = circle
            vertex_labels[name] = label

        # Create edges with capacity labels
        edge_objects = {}
        capacity_labels = {}

        for source, target, capacity in edges:
            start = vertex_objects[source].get_center()
            end = vertex_objects[target].get_center()

            # Create arrow
            arrow = Arrow(
                start=start,
                end=end,
                buff=0.5,
                stroke_color=GREY,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.15
            )

            # Capacity label
            mid = (start + end) / 2
            offset = rotate_vector(normalize(end - start), PI / 2) * 0.4
            capacity_label = Text(f"{capacity}", font_size=18, color=GREEN)
            capacity_label.move_to(mid + offset)

            edge_objects[(source, target)] = arrow
            capacity_labels[(source, target)] = capacity_label

        # Draw network
        self.play(*[Create(arrow) for arrow in edge_objects.values()])
        self.play(*[Write(label) for label in capacity_labels.values()])
        self.play(*[Create(circle) for circle in vertex_objects.values()])
        self.play(*[Write(label) for label in vertex_labels.values()])
        self.wait(1)

        # Animate flow
        info_text = Text("Simulating flow from Source to Sink", font_size=24).to_edge(DOWN)
        self.play(Write(info_text))
        self.wait(0.5)

        # Path 1: Source -> A -> C -> Sink
        path1 = [("Source", "A"), ("A", "C"), ("C", "Sink")]
        for edge in path1:
            self.play(
                edge_objects[edge].animate.set_color(RED).set_stroke(width=6),
                run_time=0.5
            )
        self.wait(0.5)

        # Path 2: Source -> B -> D -> Sink
        path2 = [("Source", "B"), ("B", "D"), ("D", "Sink")]
        for edge in path2:
            self.play(
                edge_objects[edge].animate.set_color(ORANGE).set_stroke(width=6),
                run_time=0.5
            )
        self.wait(1)

        # Show final flow
        self.play(FadeOut(info_text))
        result_text = Text("Maximum Flow Achieved!", font_size=32, color=GREEN).to_edge(DOWN)
        self.play(Write(result_text))
        self.wait(2)


class PacketRoutingVisualization(Scene):
    """Visualize packet routing through network nodes"""

    def construct(self):
        # Title
        title = Text("Packet Routing Visualization", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create network topology (simplified internet)
        routers = {
            "R1": [-5, 2, 0],
            "R2": [-2, 3, 0],
            "R3": [2, 3, 0],
            "R4": [5, 2, 0],
            "R5": [-5, -2, 0],
            "R6": [-2, -3, 0],
            "R7": [2, -3, 0],
            "R8": [5, -2, 0]
        }

        connections = [
            ("R1", "R2"), ("R2", "R3"), ("R3", "R4"),
            ("R1", "R5"), ("R5", "R6"), ("R6", "R7"), ("R7", "R8"),
            ("R2", "R6"), ("R3", "R7"), ("R4", "R8")
        ]

        # Create router objects
        router_objects = {}
        router_labels = {}

        for name, pos in routers.items():
            square = Square(side_length=0.8, fill_opacity=0.8, fill_color=BLUE, stroke_color=WHITE, stroke_width=2)
            square.move_to(pos)

            label = Text(name, font_size=20, color=WHITE)
            label.move_to(square.get_center())

            router_objects[name] = square
            router_labels[name] = label

        # Create connection lines
        connection_lines = []
        for source, target in connections:
            start = router_objects[source].get_center()
            end = router_objects[target].get_center()
            line = Line(start, end, stroke_color=GREY, stroke_width=2)
            connection_lines.append(line)

        # Draw network
        self.play(*[Create(line) for line in connection_lines])
        self.play(*[Create(square) for square in router_objects.values()])
        self.play(*[Write(label) for label in router_labels.values()])
        self.wait(1)

        # Highlight source and destination
        self.play(
            router_objects["R1"].animate.set_fill(GREEN, opacity=0.9),
            router_objects["R8"].animate.set_fill(RED, opacity=0.9)
        )

        route_text = Text("Routing packet from R1 to R8", font_size=24).to_edge(DOWN)
        self.play(Write(route_text))
        self.wait(0.5)

        # Create packet
        packet = Circle(radius=0.15, fill_opacity=1, fill_color=YELLOW, stroke_color=YELLOW)
        packet.move_to(router_objects["R1"].get_center())

        self.play(Create(packet))
        self.wait(0.3)

        # Route: R1 -> R2 -> R3 -> R4 -> R8
        route = ["R1", "R2", "R3", "R4", "R8"]

        for i in range(len(route) - 1):
            current = route[i]
            next_node = route[i + 1]

            # Move packet
            self.play(
                packet.animate.move_to(router_objects[next_node].get_center()),
                router_objects[current].animate.set_fill(BLUE if current not in ["R1", "R8"] else None, opacity=0.8),
                router_objects[next_node].animate.set_fill(ORANGE, opacity=0.9),
                run_time=0.8
            )
            self.wait(0.2)

        # Packet delivered
        self.play(FadeOut(packet), router_objects["R8"].animate.set_fill(GREEN, opacity=0.9))
        self.play(FadeOut(route_text))

        success_text = Text("Packet Delivered Successfully!", font_size=32, color=GREEN).to_edge(DOWN)
        self.play(Write(success_text))
        self.wait(2)


class TCPHandshakeVisualization(Scene):
    """Visualize TCP three-way handshake"""

    def construct(self):
        # Title
        title = Text("TCP Three-Way Handshake", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create client and server
        client = Rectangle(width=2, height=3, fill_opacity=0.8, fill_color=BLUE, stroke_color=WHITE)
        client.shift(LEFT * 4)
        client_label = Text("Client", font_size=28).move_to(client.get_center())

        server = Rectangle(width=2, height=3, fill_opacity=0.8, fill_color=GREEN, stroke_color=WHITE)
        server.shift(RIGHT * 4)
        server_label = Text("Server", font_size=28).move_to(server.get_center())

        self.play(Create(client), Create(server))
        self.play(Write(client_label), Write(server_label))
        self.wait(1)

        # Step 1: SYN
        syn_text = Text("1. SYN", font_size=24, color=YELLOW).next_to(title, DOWN)
        self.play(Write(syn_text))

        syn_arrow = Arrow(
            start=client.get_right(),
            end=server.get_left(),
            buff=0,
            stroke_color=YELLOW,
            stroke_width=4
        )
        syn_label = Text("SYN", font_size=20, color=YELLOW).move_to(syn_arrow.get_center() + UP * 0.4)

        self.play(Create(syn_arrow), Write(syn_label))
        self.wait(1)

        # Step 2: SYN-ACK
        synack_text = Text("2. SYN-ACK", font_size=24, color=ORANGE).next_to(syn_text, DOWN)
        self.play(Write(synack_text))

        synack_arrow = Arrow(
            start=server.get_left(),
            end=client.get_right(),
            buff=0,
            stroke_color=ORANGE,
            stroke_width=4
        )
        synack_arrow.shift(DOWN * 0.8)
        synack_label = Text("SYN-ACK", font_size=20, color=ORANGE).move_to(synack_arrow.get_center() + UP * 0.4)

        self.play(Create(synack_arrow), Write(synack_label))
        self.wait(1)

        # Step 3: ACK
        ack_text = Text("3. ACK", font_size=24, color=GREEN).next_to(synack_text, DOWN)
        self.play(Write(ack_text))

        ack_arrow = Arrow(
            start=client.get_right(),
            end=server.get_left(),
            buff=0,
            stroke_color=GREEN,
            stroke_width=4
        )
        ack_arrow.shift(DOWN * 1.6)
        ack_label = Text("ACK", font_size=20, color=GREEN).move_to(ack_arrow.get_center() + UP * 0.4)

        self.play(Create(ack_arrow), Write(ack_label))
        self.wait(1)

        # Connection established
        complete_text = Text("Connection Established!", font_size=32, color=GREEN).to_edge(DOWN)
        self.play(Write(complete_text))
        self.wait(2)
