import imy.inject

import rio.components.fundamental_component


import dataclasses
import io

imy.inject.clear()
import typing as t

from datetime import datetime, timezone
import inspect
import string

import fastapi
import gc
import functools
import random
import asyncio
import numpy as np
from pathlib import Path
import pandas as pd
import fastapi
import rio.docs
import plotly
import json
import rio
import rio.components.class_container
import rio.data_models
import rio.debug
import rio.debug.dev_tools
import rio.debug.dev_tools.dev_tools_connector
import rio.app_server
import rio.debug.dev_tools.icons_page
import rio.debug.dev_tools.layout_display
from datetime import datetime
import rio.debug.layouter


class TableRoot(rio.Component):
    async def _on_refresh(self) -> None:
        self.force_refresh()

    def build(self) -> rio.Component:
        data_df = pd.DataFrame(
            {
                "Text": ["A", "B", "C", "D", "E"],
                "Ones": [1, 2, 3, 4, 5],
                "Tens": [10, 20, 30, 40, 50],
                "Hundreds": [100, 200, 300, 400, 500],
                "Foos": ["Foo", "Bar", "Baz", "Qux", "Quux"],
                "Randoms": [random.randint(1, 6) for ii in range(5)],
            }
        )

        data_np = np.random.rand(5, 3)

        return rio.Column(
            rio.Table(
                data_np,
                show_row_numbers=False,
            ),
            rio.Table(
                data_np,
                show_row_numbers=True,
            ),
            rio.Table(
                data_df,
                show_row_numbers=False,
            )["header", :].style(
                font_weight="normal",
            ),
            rio.Table(
                data_df,
                show_row_numbers=True,
            )[1:3, 2:4].style(
                background_color=rio.Color.GREEN,
                italic=True,
                font_weight="bold",
            ),
            rio.Button(
                "Refresh",
                icon="refresh",
                on_press=self._on_refresh,
            ),
            spacing=1,
            align_x=0.5,
            align_y=0.5,
        )


class MyRoot(rio.Component):
    foo: bool = False

    def _on_toggle(self) -> None:
        self.foo = not self.foo

    async def _on_open_dialog(self) -> None:
        response = await self.session.show_yes_no_dialog(
            "Heyho!",
            title="Foo",
        )

        print(f"Dialog response: {response}")

    async def _on_pick_file(self, event: rio.FilePickEvent) -> None:
        await event.file.read_bytes()

    def build(self) -> rio.Component:
        if self.session.active_page_url.path == "/about-us":
            target = "/"
        else:
            target = "/about-us"

        return rio.Button(
            "Navigate Away",
            on_press=lambda: self.session.navigate_to(target),
            align_x=0.5,
            align_y=0.5,
        )

        return rio.FilePickerArea(
            on_pick_file=self._on_pick_file,
            align_x=0.5,
            align_y=0.5,
        )

        return rio.Markdown(
            f"""
Screen: {self.session.screen_width}x{self.session.screen_height}
Window: {self.session.window_width}x{self.session.window_height}

Pixels/Font Height: {self.session.pixels_per_font_height}
Scroll Bar Size: {self.session.scroll_bar_size}

Primary pointer: {self.session.primary_pointer_type}
            """,
            overflow="nowrap",
            align_x=0.5,
            align_y=0.5,
        )

        # return rio.GraphEditor(
        #     rio.Text(
        #         "foo",
        #     ),
        #     rio.NodeOutput(
        #         "Out 1",
        #         rio.Color.GREEN,
        #         key="out_1",
        #     ),
        #     rio.Column(
        #         rio.NodeInput(
        #             "In 1",
        #             rio.Color.BLUE,
        #             key="in_1",
        #         ),
        #         rio.Button(
        #             "Button",
        #             style="plain-text",
        #         ),
        #         rio.NodeOutput(
        #             "Out 2",
        #             rio.Color.BLUE,
        #             key="out_2",
        #         ),
        #         spacing=0.5,
        #     ),
        #     rio.NodeInput(
        #         "In 2",
        #         rio.Color.YELLOW,
        #         key="in_2",
        #         margin_top=5,
        #     ),
        #     margin_left=5,
        #     margin_top=5,
        # )

        return rio.Column(
            rio.Dropdown(
                label="Short Dropdown",
                options=string.ascii_uppercase[:5],
            ),
            rio.Tooltip(
                anchor=rio.Button("Left"),
                tip="Tooltip content",
                position="left",
            ),
            rio.Tooltip(
                anchor=rio.Button("Top"),
                tip="Tooltip content",
                position="top",
            ),
            rio.Tooltip(
                anchor=rio.Button("Right"),
                tip="Tooltip content",
                position="right",
            ),
            rio.Tooltip(
                anchor=rio.Button("Bottom"),
                tip="Tooltip content",
                position="bottom",
            ),
            rio.Tooltip(
                anchor=rio.Button("Auto"),
                tip="Tooltip content",
                position="auto",
            ),
            rio.Tooltip(
                anchor=rio.Button("Component"),
                tip=rio.Rectangle(
                    content=rio.Text("Tooltip content"),
                    fill=rio.Color.from_gray(0.3),
                ),
                position="auto",
            ),
            rio.Dropdown(
                label="Centered Dropdown",
                options=string.ascii_uppercase,
            ),
            rio.Dropdown(
                label="Superlong Dropdown",
                options=string.ascii_uppercase
                + string.ascii_lowercase
                + string.digits,
            ),
            rio.Popup(
                anchor=rio.Button(
                    "Popup",
                    on_press=self._on_toggle,
                ),
                content=rio.Text(
                    "Popup content",
                    margin=0.5,
                ),
                position="right",
                is_open=self.bind().foo,
                user_closable=True,
                # modal=True,
            ),
            rio.Button(
                "Dialog",
                on_press=self._on_open_dialog,
            ),
            rio.Button(
                "Pick File",
                on_press=self._on_pick_file,
            ),
            rio.Dropdown(
                label="Bottom Dropdown",
                options=string.ascii_uppercase[:15],
            ),
            rio.DateInput(
                datetime.now(),
            ),
            rio.Spacer(min_height=30),
            spacing=2,
            margin=5,
            align_x=0.5,
            align_y=0.5,
        )


class TracingExtension(rio.Extension):
    def __init__(self) -> None:
        # Keeps track of called functions
        self.function_call_log: list[str] = []

    def verify_and_clear_log(self, *expected: str) -> None:
        assert self.function_call_log == list(expected)
        self.function_call_log.clear()

    def _record_function_call(self) -> None:
        # Get the caller's name
        caller_name = inspect.stack()[1].function

        print(f"CALLED {caller_name}")

        # Record it
        self.function_call_log.append(caller_name)

    @rio.extension_event.on_as_fastapi
    def on_as_fastapi(
        self,
        event: rio.ExtensionAsFastapiEvent,
    ) -> None:
        self._record_function_call()

        # Add a test route
        async def route_test() -> fastapi.responses.JSONResponse:
            return fastapi.responses.JSONResponse(
                {
                    "message": "Hello, World!",
                }
            )

        event.fastapi_app.add_api_route(
            "/test",
            route_test,
            methods=["GET"],
        )

    @rio.extension_event.on_app_start
    def on_app_start(
        self,
        event: rio.ExtensionAppStartEvent,
    ) -> None:
        self._record_function_call()

    @rio.extension_event.on_app_close
    def on_app_close(
        self,
        event: rio.ExtensionAppCloseEvent,
    ) -> None:
        self._record_function_call()

    # This function isn't registered at all and should not be called
    def on_session_start(
        self,
        event: rio.ExtensionSessionStartEvent,
    ) -> None:
        self._record_function_call()

    # This function is asynchronous, testing that the extension system awaits
    # functions as needed.
    @rio.extension_event.on_session_start
    def on_session_start_async(
        self,
        event: rio.ExtensionSessionStartEvent,
    ) -> None:
        self._record_function_call()

    @rio.extension_event.on_session_close
    def on_session_close(
        self,
        event: rio.ExtensionSessionCloseEvent,
    ) -> None:
        self._record_function_call()

    @rio.extension_event.on_page_change
    def on_page_change(
        self,
        event: rio.ExtensionPageChangeEvent,
    ) -> None:
        self._record_function_call()

    # This function is registered for multiple events and should be called for
    # each of them
    @rio.extension_event.on_session_start
    @rio.extension_event.on_session_close
    @rio.extension_event.on_page_change
    def on_multiple_events(
        self,
        event: t.Any,
    ) -> None:
        self._record_function_call()


@dataclasses.dataclass
class MyModel:
    name: str
    enabled: bool


class MyRoot(rio.Component):
    def build(self) -> rio.Component:
        form = rio.FormBuilder(
            heading="Hello, World!",
            align_x=0.5,
            align_y=0.5,
        )

        form.add_bool(
            "enabled",
            True,
        )

        return form


class MyRoot(rio.Component):
    is_open: bool = False

    def toggle(self) -> None:
        self.is_open = not self.is_open

    def build(self) -> rio.Component:
        return rio.Popup(
            anchor=rio.Button(
                "Anchor",
                on_press=self.toggle,
                align_x=0.5,
                align_y=0.5,
            ),
            content=rio.Text(
                "Content",
                margin=1,
            ),
            is_open=self.bind().is_open,
            position="top",
        )


class Switching(rio.Component):
    is_open: bool
    content: rio.Component

    def _on_press(self) -> None:
        self.is_open = not self.is_open

    def build(self) -> rio.Component:
        button = rio.Button(
            "Toggle",
            on_press=self._on_press,
            grow_y=False,
        )

        return rio.Column(
            button,
            *([self.content] if self.is_open else []),
        )


class MyRoot(rio.Component):
    value: float = 1.0

    @rio.event.on_populate
    async def foo(self) -> None:
        await asyncio.sleep(1)
        self.value = 2.0

    def build(self) -> rio.Component:
        df = pd.DataFrame(
            {
                "A": ["One", "Two", "Three"],
                "B": [4, 5, 6],
            }
        )

        return rio.Dropdown(
            options=df["A"],
            align_x=0.5,
            align_y=0.5,
            min_width=20,
        )

        table = rio.Table(
            pd.DataFrame(
                {
                    "A": [1, 2, 3],
                    "B": [4, 5, 6],
                }
            ),
            min_width=20,
            align_x=0.5,
            align_y=0.5,
        )

        table["header", :].style(justify="right")

        table[:2, 0].style(
            justify="left",
        )

        return table

        return rio.NumberInput(
            value=self.value,
            min_width=20,
            align_x=0.5,
            align_y=0.5,
        )

        return rio.NumberInput(
            label="Heyho",
            value=-2.0,
            align_x=0.5,
            align_y=0.5,
        )

        return Switching(
            is_open=True,
            content=rio.Text(
                "Content",
            ),
            align_x=0.5,
            align_y=0.5,
        )

        return rio.Rectangle(
            fill=rio.RadialGradientFill(
                rio.Color.RED,
                rio.Color.BLUE,
                center_x=0.2,
                center_y=0.3,
            ),
            min_width=10,
            min_height=10,
            align_x=0.5,
            align_y=0.5,
        )

        return rio.Tooltip(
            anchor=rio.Text("Anchor"),
            tip="Content",
            align_x=0.5,
            align_y=0.5,
        )

        return rio.Dropdown(
            options=["A", "B", "C"],
            style="rounded",
            align_x=0.5,
            align_y=0.5,
        )

        return rio.Button(
            on_press=self._pick_file,
            align_x=0.5,
            align_y=0.5,
        )


app = rio.App(
    icon=Path.home() / "rio.jpsg",
    build=MyRoot,
    default_attachments=[],
)


app._add_extension(TracingExtension())
