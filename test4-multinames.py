source2="C:/Users/bing/Documents/trusti/ABP-655.jpg",  # Path to the image
from kivymd.app import MDApp
from kivymd.uix.imagelist import MDSmartTile
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.button import MDIconButton

class MainApp(MDApp):
    def build(self):
        tile = MDSmartTile(
            radius=24,
            box_radius=[0, 0, 24, 24],
            box_color=(0, 0, 0, .8),  # Dark color with a bit of transparency
            box_position="header",  # Place the box as a header
            overlap=False,  # Don't let the box overlap the image
            lines=2,  # Allow two lines of text in the box
            source="C:/Users/bing/Documents/trusti/ABP-655.jpg",  # Path to the image
        )

        # Add a heart icon button to the tile
        icon_button = MDIconButton(
            icon="heart-outline",
            theme_icon_color="Custom",
            icon_color=(1, 1, 1, 1),  # White color for the icon
            pos_hint={"center_y": .5},
        )
        icon_button.bind(on_release=lambda x: setattr(icon_button, 'icon', "heart" if icon_button.icon == "heart-outline" else "heart-outline"))
        tile.add_widget(icon_button)

        # Add a two-line text item to the tile
        text_item = TwoLineListItem(
            text="[color=#ffffff][b]My cats[/b][/color]",  # White bold text
            secondary_text="[color=#808080][b]Julia and Julie[/b][/color]",  # Gray bold secondary text
            pos_hint={"center_y": .5},
            _no_ripple_effect=True,
        )
        tile.add_widget(text_item)

        return tile

MainApp().run()
