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


class ThemeSample(rio.Component):
    theme: rio.Theme

    async def _apply_theme_worker(self) -> None:
        # Wait for a bit to ensure the client has time to update the HTML
        await asyncio.sleep(0.2)

        # Get all variables to apply
        light_or_dark = "light" if self.theme.is_light_theme else "dark"
        theme_vars = self.session._calculate_theme_css_values(self.theme)

        # Apply the theme
        await self.session._evaluate_javascript(
            f"""
let themeVars = {json.dumps(theme_vars)};

let elem = globalThis.componentsById[{self._id}].element;

for (let key in themeVars) {{
    elem.style.setProperty(
        key,
        themeVars[key],
    );
}}

// Set the theme variant
document.documentElement.setAttribute(
    "data-theme",
    {json.dumps(light_or_dark)}
);

            """
        )

    def build(self) -> rio.Component:
        # Apply the theme
        asyncio.create_task(
            self._apply_theme_worker(),
        )

        # Build the content
        content = rio.Row(
            # Main Content
            rio.Column(
                rio.Text(
                    "Lorem Ipsum",
                    style="heading1",
                ),
                rio.Markdown(
                    """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam nec
ultricies elit. Nullam nec ultricies elit. Nullam nec ultricies elit.
                    """,
                ),
                rio.Image(
                    rio.URL("https://picsum.photos/300/200"),
                    min_width=26,
                    min_height=14,
                    corner_radius=self.theme.corner_radius_medium,
                ),
                rio.Markdown(
                    """
Lorem markdownum auctor fiant aversa, scopulos bos ima ruptosque turbam, fertur
flexile amictu temptaretque *superum temptarunt* volatu ad veros. Fatebor
Aesacos.

```js
rom_root(record);
direct = subdirectory(symbolic_restore_t, url);
```

Coniuge et tamen et omnibus ille concordant mitissima accedere fratrem
auditurum, spes petunt ore insigne mille. Te explorant ardor, dies inde eloquio
rostrum vestemque et frustra purum. Cynthia quoniam dextra aequoris, emissi [in
                    """,
                ),
                grow_x=True,
            ),
            # (Fake) Drawer
            rio.ThemeContextSwitcher(
                content=rio.Rectangle(
                    content=rio.Grid(
                        rio.Text(
                            "Drawer Heading",
                            style="heading2",
                        ),
                        rio.TextInput(
                            text="Foobar",
                            style="rounded",
                        ),
                        rio.TextInput(
                            text="Foobar",
                            style="rounded",
                            is_sensitive=False,
                        ),
                        [
                            rio.Text("Switch"),
                            rio.Switch(),
                        ],
                        [
                            rio.Button("Major", style="major"),
                            rio.Button("Minor", style="minor"),
                        ],
                        [
                            rio.Button("Colored Text", style="colored-text"),
                            rio.Button("Plain Text", style="plain-text"),
                        ],
                        rio.Switch(is_on=True),
                        rio.Switch(is_on=False),
                        rio.Switch(is_on=True, is_sensitive=False),
                        rio.Switch(is_on=False, is_sensitive=False),
                        rio.Button("Enabled"),
                        rio.Button("Disabled", is_sensitive=False),
                        rio.Spacer(),
                        rio.Separator(),
                        rio.Row(
                            rio.Icon("material/castle"),
                            rio.Text(
                                "Castles are Cool",
                                grow_x=True,
                            ),
                            spacing=0.5,
                        ),
                        row_spacing=1,
                        column_spacing=1,
                        margin=2,
                    ),
                    fill=self.theme.neutral_color,
                    corner_radius=(
                        self.theme.corner_radius_large,
                        0,
                        0,
                        self.theme.corner_radius_large,
                    ),
                    shadow_color=self.theme.shadow_color,
                    shadow_radius=1.3,
                ),
                color="neutral",
            ),
            spacing=1,
        )

        # Wrap up the content
        #
        # A rectangle acts as a fake background
        return rio.Rectangle(
            # A Theme context switcher ensures that the theme variables are
            # locally exposed.
            content=rio.ThemeContextSwitcher(
                content=content,
                color="background",
            ),
            fill=self.theme.background_color,
        )


class ThemeViewer(rio.Component):
    def build(self) -> rio.Component:
        # Decide on the colors to use
        theme_colors: list[rio.Color] = [
            self.session.theme.primary_color,
            rio.Color.RED,
            rio.Color.GREEN,
            rio.Color.YELLOW,
        ]

        # Create the themes
        light_viewers: list[ThemeSample] = []
        dark_viewers: list[ThemeSample] = []

        for col in theme_colors:
            light_theme = rio.Theme.from_colors(
                primary_color=col,
                mode="light",
            )

            dark_theme = rio.Theme.from_colors(
                primary_color=col,
                mode="dark",
            )

            light_viewers.append(ThemeSample(theme=light_theme))
            dark_viewers.append(ThemeSample(theme=dark_theme))

        # Populate
        return rio.Grid(
            light_viewers,
            dark_viewers,
            row_spacing=0.4,
            column_spacing=0.4,
        )


app = rio.App(
    build=ThemeViewer,
    theme=(
        rio.Theme.from_colors(mode="light"),
        rio.Theme.from_colors(mode="dark"),
    ),
    default_attachments=[],
)
