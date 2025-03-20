import rio
from datetime import datetime


def wrap_slide(
    content: rio.Component,
    *,
    add_common: bool = True,
) -> rio.Component:
    if not add_common:
        return content

    return rio.Stack(
        rio.Link(
            rio.Text(
                f'https://rio.dev\n{datetime.now().strftime("%Y-%m-%d")}',
                justify="right",
                style="dim",
            ),
            target_url="https://rio.dev",
            align_x=1,
            align_y=1,
            margin=2,
        ),
        rio.Icon(
            "rio/logo",
            fill="dim",
            min_width=2,
            min_height=3,
            align_x=1,
            align_y=0,
            margin=2,
        ),
        content,
    )


class Slide1_Title(rio.Component):
    def build(self) -> rio.Component:
        return wrap_slide(
            rio.Column(
                rio.Icon(
                    "rio/logo_and_text_horizontal:color",
                    min_width=10,
                    min_height=10,
                ),
                rio.Text(
                    "Build & Share Web-Apps in Pure Python",
                    justify="center",
                    style="heading1",
                ),
                spacing=2,
                align_x=0.5,
                align_y=0.5,
            ),
            add_common=False,
        )


class Slide2_MissionStatement(rio.Component):
    def build(self) -> rio.Component:
        return wrap_slide(
            rio.Markdown(
                """
Rio is a **platform** that empowers **Python developers** to **create modern web applications effortlessly**, without the complexities of managing infrastructure.
                """,
                justify="center",
                min_width=90,
                align_x=0.5,
                align_y=0.5,
            ),
        )


app = rio.App(
    name="Rio Pitch",
    build=Slide2_MissionStatement,
    theme=rio.Theme.from_colors(
        background_color=rio.Color.from_hex("111827"),
    ),
)
