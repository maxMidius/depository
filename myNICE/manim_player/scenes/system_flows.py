#-------------------------------
# vi: sw=4 ts=4 expandtab
#-------------------------------
"""
System architecture and data flow visualization scenes
"""

from manim import *


class MicroservicesArchitecture(Scene):
    """Visualize microservices architecture with API gateway"""

    def construct(self):
        # Title
        title = Text("Microservices Architecture", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create components
        # API Gateway
        gateway = Rectangle(width=2.5, height=1.2, fill_opacity=0.8, fill_color=BLUE, stroke_color=WHITE)
        gateway.shift(UP * 2)
        gateway_label = Text("API Gateway", font_size=20, color=WHITE).move_to(gateway.get_center())

        # Microservices
        services = {}
        service_configs = [
            ("Auth Service", GREEN, LEFT * 4 + DOWN * 0.5),
            ("User Service", YELLOW, LEFT * 1.5 + DOWN * 0.5),
            ("Order Service", ORANGE, RIGHT * 1.5 + DOWN * 0.5),
            ("Payment Service", RED, RIGHT * 4 + DOWN * 0.5),
        ]

        for name, color, pos in service_configs:
            service = Rectangle(width=2, height=1, fill_opacity=0.8, fill_color=color, stroke_color=WHITE)
            service.move_to(pos)
            label = Text(name, font_size=16, color=WHITE).move_to(service.get_center())
            services[name] = (service, label)

        # Databases
        databases = {}
        db_configs = [
            ("Auth DB", GREEN, LEFT * 4 + DOWN * 2.5),
            ("User DB", YELLOW, LEFT * 1.5 + DOWN * 2.5),
            ("Order DB", ORANGE, RIGHT * 1.5 + DOWN * 2.5),
            ("Payment DB", RED, RIGHT * 4 + DOWN * 2.5),
        ]

        for name, color, pos in db_configs:
            db = Cylinder(radius=0.4, height=0.6, fill_opacity=0.8, fill_color=color, stroke_color=WHITE)
            db.move_to(pos)
            label = Text(name, font_size=14, color=WHITE).next_to(db, DOWN, buff=0.1)
            databases[name] = (db, label)

        # Draw components
        self.play(Create(gateway), Write(gateway_label))
        self.wait(0.3)

        for service, label in services.values():
            self.play(Create(service), Write(label), run_time=0.4)

        for db, label in databases.values():
            self.play(Create(db), Write(label), run_time=0.3)

        self.wait(0.5)

        # Draw connections
        # Gateway to services
        for name, (service, _) in services.items():
            line = Line(
                gateway.get_bottom(),
                service.get_top(),
                stroke_color=GREY,
                stroke_width=2
            )
            self.play(Create(line), run_time=0.2)

        # Services to databases
        for (srv_name, (srv, _)), (db_name, (db, _)) in zip(services.items(), databases.items()):
            line = Line(
                srv.get_bottom(),
                db.get_top(),
                stroke_color=GREY,
                stroke_width=2
            )
            self.play(Create(line), run_time=0.2)

        self.wait(1)

        # Simulate request flow
        flow_text = Text("Incoming Request", font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(Write(flow_text))

        # Highlight flow
        self.play(gateway.animate.set_fill(opacity=1))
        self.wait(0.3)

        # Route to User Service
        user_service, _ = services["User Service"]
        self.play(user_service.animate.set_fill(opacity=1))
        self.wait(0.3)

        user_db, _ = databases["User DB"]
        self.play(user_db.animate.set_fill(opacity=1))
        self.wait(0.5)

        self.play(FadeOut(flow_text))
        complete_text = Text("Request Processed", font_size=28, color=GREEN).to_edge(DOWN)
        self.play(Write(complete_text))
        self.wait(2)


class DataPipelineFlow(Scene):
    """Visualize data pipeline from source to analytics"""

    def construct(self):
        # Title
        title = Text("Data Pipeline Flow", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Pipeline stages
        stages = [
            ("Data Source", BLUE, LEFT * 5),
            ("Ingestion", GREEN, LEFT * 2.5),
            ("Processing", YELLOW, ORIGIN),
            ("Storage", ORANGE, RIGHT * 2.5),
            ("Analytics", RED, RIGHT * 5),
        ]

        stage_objects = {}

        for name, color, pos in stages:
            box = RoundedRectangle(
                width=1.8,
                height=1.2,
                corner_radius=0.2,
                fill_opacity=0.8,
                fill_color=color,
                stroke_color=WHITE
            )
            box.move_to(pos)
            label = Text(name, font_size=16, color=WHITE).move_to(box.get_center())
            stage_objects[name] = (box, label)

        # Draw stages
        for box, label in stage_objects.values():
            self.play(Create(box), Write(label), run_time=0.4)

        self.wait(0.5)

        # Connect stages with arrows
        for i in range(len(stages) - 1):
            current_name = stages[i][0]
            next_name = stages[i + 1][0]

            current_box, _ = stage_objects[current_name]
            next_box, _ = stage_objects[next_name]

            arrow = Arrow(
                start=current_box.get_right(),
                end=next_box.get_left(),
                buff=0,
                stroke_color=WHITE,
                stroke_width=4
            )
            self.play(Create(arrow), run_time=0.3)

        self.wait(1)

        # Animate data flow
        flow_text = Text("Data Flowing Through Pipeline", font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(Write(flow_text))

        # Create data packet
        data_packet = Circle(radius=0.2, fill_opacity=1, fill_color=YELLOW, stroke_color=YELLOW)
        start_box, _ = stage_objects["Data Source"]
        data_packet.move_to(start_box.get_center())

        self.play(Create(data_packet))
        self.wait(0.3)

        # Move through pipeline
        for name, color, pos in stages[1:]:
            box, _ = stage_objects[name]
            self.play(
                data_packet.animate.move_to(box.get_center()),
                box.animate.set_fill(opacity=1),
                run_time=0.8
            )
            self.wait(0.3)

        self.play(FadeOut(data_packet))
        self.play(FadeOut(flow_text))

        complete_text = Text("Data Processed Successfully!", font_size=28, color=GREEN).to_edge(DOWN)
        self.play(Write(complete_text))
        self.wait(2)


class RequestResponseFlow(Scene):
    """Visualize HTTP request-response cycle"""

    def construct(self):
        # Title
        title = Text("HTTP Request-Response Flow", font_size=36).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Client (Browser)
        client = Rectangle(width=2, height=2.5, fill_opacity=0.8, fill_color=BLUE, stroke_color=WHITE)
        client.shift(LEFT * 4)
        client_label = Text("Client\n(Browser)", font_size=20, color=WHITE).move_to(client.get_center())

        # Server
        server = Rectangle(width=2, height=2.5, fill_opacity=0.8, fill_color=GREEN, stroke_color=WHITE)
        server.shift(RIGHT * 4)
        server_label = Text("Server", font_size=20, color=WHITE).move_to(server.get_center())

        # Database
        database = Cylinder(radius=0.6, height=0.8, fill_opacity=0.8, fill_color=ORANGE, stroke_color=WHITE)
        database.next_to(server, DOWN, buff=1)
        db_label = Text("Database", font_size=18, color=WHITE).next_to(database, DOWN, buff=0.2)

        # Draw components
        self.play(Create(client), Write(client_label))
        self.play(Create(server), Write(server_label))
        self.play(Create(database), Write(db_label))
        self.wait(1)

        # Step 1: HTTP Request
        step1 = Text("1. HTTP Request", font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(Write(step1))

        request = Arrow(
            start=client.get_right(),
            end=server.get_left(),
            buff=0,
            stroke_color=YELLOW,
            stroke_width=4
        )
        request_label = Text("GET /api/users", font_size=16, font="monospace", color=YELLOW)
        request_label.next_to(request, UP, buff=0.2)

        self.play(Create(request), Write(request_label))
        self.wait(0.8)

        # Step 2: Query Database
        self.play(FadeOut(step1))
        step2 = Text("2. Query Database", font_size=24, color=ORANGE).to_edge(DOWN)
        self.play(Write(step2))

        db_query = Arrow(
            start=server.get_bottom(),
            end=database.get_top(),
            buff=0,
            stroke_color=ORANGE,
            stroke_width=4
        )
        query_label = Text("SELECT * FROM users", font_size=14, font="monospace", color=ORANGE)
        query_label.next_to(db_query, LEFT, buff=0.2)

        self.play(Create(db_query), Write(query_label))
        self.wait(0.8)

        # Step 3: Database Response
        self.play(FadeOut(step2))
        step3 = Text("3. Database Returns Data", font_size=24, color=ORANGE).to_edge(DOWN)
        self.play(Write(step3))

        db_response = Arrow(
            start=database.get_top(),
            end=server.get_bottom(),
            buff=0,
            stroke_color=ORANGE,
            stroke_width=4
        )
        db_response.shift(RIGHT * 0.3)

        self.play(Create(db_response))
        self.wait(0.8)

        # Step 4: HTTP Response
        self.play(FadeOut(step3))
        step4 = Text("4. HTTP Response", font_size=24, color=GREEN).to_edge(DOWN)
        self.play(Write(step4))

        response = Arrow(
            start=server.get_left(),
            end=client.get_right(),
            buff=0,
            stroke_color=GREEN,
            stroke_width=4
        )
        response.shift(DOWN * 0.5)
        response_label = Text("200 OK + JSON", font_size=16, font="monospace", color=GREEN)
        response_label.next_to(response, DOWN, buff=0.2)

        self.play(Create(response), Write(response_label))
        self.wait(1)

        # Complete
        self.play(FadeOut(step4))
        complete_text = Text("Request Complete!", font_size=32, color=GREEN).to_edge(DOWN)
        self.play(Write(complete_text))
        self.wait(2)
