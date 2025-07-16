"""Checkbox Demo with JSON Editor - A Reflex App"""

import reflex as rx
import json
from typing import Dict, Any



class CheckboxState(rx.State):
    """State for the checkbox demo app."""
    # Feature toggles
    dark_mode: bool = False
    notifications: bool = True
    auto_save: bool = False
    debug_mode: bool = False
    advanced_features: bool = True
    # User preferences
    show_tooltips: bool = True
    compact_view: bool = False
    animate_transitions: bool = True
    enable_sound: bool = False
    # JSON string for the editor
    json_text: str = ""

    def set_json_text(self, value: str):
        self.json_text = value

    def update_from_json(self, _):
        """Update state from JSON editor."""
        try:
            new_config = json.loads(self.json_text)
            # Feature toggles
            ft = new_config.get("feature_toggles", {})
            self.dark_mode = bool(ft.get("dark_mode", False))
            self.notifications = bool(ft.get("notifications", False))
            self.auto_save = bool(ft.get("auto_save", False))
            self.debug_mode = bool(ft.get("debug_mode", False))
            self.advanced_features = bool(ft.get("advanced_features", False))
            # User preferences
            up = new_config.get("user_preferences", {})
            self.show_tooltips = bool(up.get("show_tooltips", False))
            self.compact_view = bool(up.get("compact_view", False))
            self.animate_transitions = bool(up.get("animate_transitions", False))
            self.enable_sound = bool(up.get("enable_sound", False))
            # Update JSON text to reflect normalized state
            self.json_text = self._get_json()
        except Exception:
            # If JSON is invalid, revert to current state
            self.json_text = self._get_json()

    def _get_json(self):
        return json.dumps({
            "feature_toggles": {
                "dark_mode": self.dark_mode,
                "notifications": self.notifications,
                "auto_save": self.auto_save,
                "debug_mode": self.debug_mode,
                "advanced_features": self.advanced_features
            },
            "user_preferences": {
                "show_tooltips": self.show_tooltips,
                "compact_view": self.compact_view,
                "animate_transitions": self.animate_transitions,
                "enable_sound": self.enable_sound
            }
        }, indent=2)

    def toggle_checkbox(self, name: str):
        # Toggle the named boolean and update JSON
        setattr(self, name, not getattr(self, name))
        self.json_text = self._get_json()

    def reset_to_defaults(self):
        self.dark_mode = False
        self.notifications = True
        self.auto_save = False
        self.debug_mode = False
        self.advanced_features = True
        self.show_tooltips = True
        self.compact_view = False
        self.animate_transitions = True
        self.enable_sound = False
        self.json_text = self._get_json()


def checkbox_panel() -> rx.Component:
    """Left panel with checkboxes."""
    return rx.vstack(
        rx.heading("Checkbox Controls", size="6", margin_bottom="20px"),
        # Feature Toggles Section
        rx.vstack(
            rx.heading("Feature Toggles", size="5", margin_bottom="10px", color="blue.600"),
            rx.hstack(
                rx.checkbox(
                    checked=CheckboxState.dark_mode,
                    on_change=lambda _: CheckboxState.toggle_checkbox("dark_mode"),
                    color_scheme="blue",
                ),
                rx.text("Dark Mode", margin_left="8px"),
                align="center", margin_bottom="8px"
            ),
            rx.hstack(
                rx.checkbox(
                    checked=CheckboxState.notifications,
                    on_change=lambda _: CheckboxState.toggle_checkbox("notifications"),
                    color_scheme="blue",
                ),
                rx.text("Notifications", margin_left="8px"),
                align="center", margin_bottom="8px"
            ),
            rx.hstack(
                rx.checkbox(
                    checked=CheckboxState.auto_save,
                    on_change=lambda _: CheckboxState.toggle_checkbox("auto_save"),
                    color_scheme="blue",
                ),
                rx.text("Auto Save", margin_left="8px"),
                align="center", margin_bottom="8px"
            ),
            rx.hstack(
                rx.checkbox(
                    checked=CheckboxState.debug_mode,
                    on_change=lambda _: CheckboxState.toggle_checkbox("debug_mode"),
                    color_scheme="blue",
                ),
                rx.text("Debug Mode", margin_left="8px"),
                align="center", margin_bottom="8px"
            ),
            rx.hstack(
                rx.checkbox(
                    checked=CheckboxState.advanced_features,
                    on_change=lambda _: CheckboxState.toggle_checkbox("advanced_features"),
                    color_scheme="blue",
                ),
                rx.text("Advanced Features", margin_left="8px"),
                align="center", margin_bottom="8px"
            ),
            align="start", margin_bottom="20px", padding="15px",
            border="1px solid #e2e8f0", border_radius="8px", background="gray.50"
        ),
        # User Preferences Section
        rx.vstack(
            rx.heading("User Preferences", size="5", margin_bottom="10px", color="blue.600"),
            rx.hstack(
                rx.checkbox(
                    checked=CheckboxState.show_tooltips,
                    on_change=lambda _: CheckboxState.toggle_checkbox("show_tooltips"),
                    color_scheme="blue",
                ),
                rx.text("Show Tooltips", margin_left="8px"),
                align="center", margin_bottom="8px"
            ),
            rx.hstack(
                rx.checkbox(
                    checked=CheckboxState.compact_view,
                    on_change=lambda _: CheckboxState.toggle_checkbox("compact_view"),
                    color_scheme="blue",
                ),
                rx.text("Compact View", margin_left="8px"),
                align="center", margin_bottom="8px"
            ),
            rx.hstack(
                rx.checkbox(
                    checked=CheckboxState.animate_transitions,
                    on_change=lambda _: CheckboxState.toggle_checkbox("animate_transitions"),
                    color_scheme="blue",
                ),
                rx.text("Animate Transitions", margin_left="8px"),
                align="center", margin_bottom="8px"
            ),
            rx.hstack(
                rx.checkbox(
                    checked=CheckboxState.enable_sound,
                    on_change=lambda _: CheckboxState.toggle_checkbox("enable_sound"),
                    color_scheme="blue",
                ),
                rx.text("Enable Sound", margin_left="8px"),
                align="center", margin_bottom="8px"
            ),
            align="start", margin_bottom="20px", padding="15px",
            border="1px solid #e2e8f0", border_radius="8px", background="gray.50"
        ),
        spacing="4", align="start", width="100%"
    )


def json_panel() -> rx.Component:
    """Right panel with JSON editor."""
    return rx.vstack(
        rx.heading("JSON Configuration", size="6", margin_bottom="20px"),
        rx.text(
            "Edit the JSON below to update checkboxes:",
            margin_bottom="10px",
            color="gray.600"
        ),
        rx.text_area(
            value=CheckboxState.json_text,
            on_change=CheckboxState.set_json_text,
            on_blur=CheckboxState.update_from_json,
            placeholder="JSON configuration...",
            font_family="monospace",
            font_size="14px",
            width="100%",
            height="400px",
            resize="vertical",
            border="1px solid #cbd5e0",
            border_radius="8px",
            padding="10px"
        ),
        rx.button(
            "Reset to Defaults",
            on_click=CheckboxState.reset_to_defaults,
            color_scheme="red",
            variant="outline",
            margin_top="10px"
        ),
        width="100%",
        align="start"
    )


def index() -> rx.Component:
    """Main page with two-panel layout."""
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            # Header
            rx.heading(
                "Checkbox ↔ JSON Demo",
                size="9",
                text_align="center",
                margin_bottom="10px"
            ),
            rx.text(
                "Edit checkboxes on the left or JSON on the right - they stay in sync!",
                size="4",
                text_align="center",
                color="gray.600",
                margin_bottom="30px"
            ),
            
            # Two-panel layout
            rx.hstack(
                # Left panel - Checkboxes
                rx.box(
                    checkbox_panel(),
                    width="45%",
                    padding="20px",
                    border="1px solid #e2e8f0",
                    border_radius="12px",
                    background="white",
                    box_shadow="0 2px 4px rgba(0,0,0,0.1)"
                ),
                
                # Right panel - JSON Editor
                rx.box(
                    json_panel(),
                    width="45%",
                    padding="20px",
                    border="1px solid #e2e8f0",
                    border_radius="12px",
                    background="white",
                    box_shadow="0 2px 4px rgba(0,0,0,0.1)"
                ),
                
                spacing="4",
                justify="center",
                width="100%"
            ),
            
            # Footer
            rx.text(
                "💡 Tip: Try adding new boolean fields in the JSON editor!",
                size="3",
                color="gray.500",
                text_align="center",
                margin_top="20px"
            ),
            
            spacing="5",
            min_height="100vh",
            padding="20px"
        ),
        max_width="1200px",
        margin="0 auto"
    )


# Create the app
app = rx.App(
    style={
        "font_family": "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"
    }
)
app.add_page(index)