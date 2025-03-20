import gc
import random
import asyncio
import json
import rio
from rio.theme import _derive_color, _make_colorful_palette
import rio.components.class_container
import rio.data_models
import rio.debug
import rio.debug.dev_tools
import rio.debug.dev_tools.dev_tools_connector
import rio.debug.dev_tools.icons_page
import rio.debug.dev_tools.layout_display
import rio.debug.layouter
import typing as t


class ColorRect(rio.Component):
    color: rio.Color

    def build(self) -> rio.Component:
        def rect(
            color: rio.Color, child: rio.Component | None
        ) -> rio.Component:
            return rio.Rectangle(
                content=child,
                fill=color,
                corner_radius=1,
                margin=1.5,
            )

        def rectstack(label: str, *colors: rio.Color) -> rio.Component:
            # Terminal case
            if len(colors) == 0:
                return rio.Text(
                    label,
                    justify="center",
                    margin=1.5,
                )

            # Wrap it!
            return rect(
                colors[0],
                rectstack(label, *colors[1:]),
            )

        return rio.Rectangle(
            content=rio.Column(
                # Brighter colors
                rectstack(
                    "Bright",
                    self.color.brighter(0.1),
                    self.color.brighter(0.2),
                    self.color.brighter(0.3),
                    self.color.brighter(0.4),
                    self.color.brighter(0.7),
                    self.color.brighter(1.0),
                ),
                # Darker colors
                rectstack(
                    "Dark",
                    self.color.darker(0.1),
                    self.color.darker(0.2),
                    self.color.darker(0.3),
                    self.color.darker(0.4),
                    self.color.darker(0.7),
                    self.color.darker(1.0),
                ),
                # Derived colors (plain)
                rectstack(
                    "Derived",
                    rio.theme._derive_color(self.color, 0.1),
                    rio.theme._derive_color(self.color, 0.2),
                    rio.theme._derive_color(self.color, 0.3),
                    rio.theme._derive_color(self.color, 0.4),
                    rio.theme._derive_color(self.color, 0.7),
                    rio.theme._derive_color(self.color, 1.0),
                ),
                # Derived colors (colorized)
                rectstack(
                    "Derived",
                    rio.theme._derive_color(
                        self.color,
                        0.1,
                        target_color=self.session.theme.primary_color,
                    ),
                    rio.theme._derive_color(
                        self.color,
                        0.2,
                        target_color=self.session.theme.primary_color,
                    ),
                    rio.theme._derive_color(
                        self.color,
                        0.3,
                        target_color=self.session.theme.primary_color,
                    ),
                    rio.theme._derive_color(
                        self.color,
                        0.4,
                        target_color=self.session.theme.primary_color,
                    ),
                    rio.theme._derive_color(
                        self.color,
                        0.7,
                        target_color=self.session.theme.primary_color,
                    ),
                    rio.theme._derive_color(
                        self.color,
                        1.0,
                        target_color=self.session.theme.primary_color,
                    ),
                ),
                spacing=1.5,
                margin=1.5,
            ),
            fill=self.color,
        )


class ColorRect(rio.Component):
    color: rio.Color

    def build(self) -> rio.Component:
        result = rio.Column()

        for i in range(11):
            color = self.color.brighter(i * 0.1)
            l, a, b = color.oklab
            color_str = f"{l:.2f} {a:.2f} {b:.2f}"

            result.add(
                rio.Rectangle(
                    content=rio.Text(
                        color_str,
                        justify="center",
                        margin=0.5,
                    ),
                    fill=color,
                )
            )

        return result


class ThemeViewer(rio.Component):
    def build(self) -> rio.Component:
        # Decide on the colors to use
        theme_colors: list[rio.Color] = [
            self.session.theme.primary_color,
            rio.Color.RED,
            rio.Color.GREEN,
            rio.Color.YELLOW,
            rio.Color.from_hex("#FFC0CB"),
            rio.Color.from_hex("#32CD32"),
            rio.Color.from_hex("#800080"),
            rio.Color.from_gray(0.1),
        ]

        # Populate
        return rio.Row(
            *[ColorRect(color=col) for col in theme_colors],
            spacing=2,
            align_x=0.5,
            align_y=0.5,
        )


app = rio.App(
    build=ThemeViewer,
    theme=(
        rio.Theme.from_colors(mode="light"),
        rio.Theme.from_colors(mode="dark"),
    ),
    default_attachments=[],
)
