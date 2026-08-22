from kivy.config import Config

# Window settings (must be before importing other Kivy modules)
Config.set("graphics", "width", "390")
Config.set("graphics", "height", "844")
Config.set("graphics", "resizable", "0")

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

from ai_logic import chat_with_ai


# Light mode
Window.clearcolor = (1, 1, 1, 1)

class ChatApp(App):

    def build(self):

        self.current_answer = ""
        self.current_index = 0

        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        # ---------------- Chat Area ----------------

        self.scroll = ScrollView(
            size_hint=(1, 0.85)
        )

        self.chat = Label(
            text="[size=22][b]AI Chatbot[/b][/size]",
            markup=True,
            color=(0, 0, 0, 1),
            halign="left",
            valign="top",
            size_hint_y=None
        )

        self.chat.bind(
            texture_size=self.chat.setter("size")
        )

        self.chat.bind(
            width=lambda *args: setattr(
                self.chat,
                "text_size",
                (self.chat.width, None)
            )
        )

        self.scroll.add_widget(self.chat)

        # ---------------- Input Area ----------------

        input_layout = BoxLayout(
            size_hint_y=0.15,
            spacing=10
        )

        self.input_box = TextInput(
            multiline=False,
            hint_text="Type your message..."
        )

        # Press Enter to send
        self.input_box.bind(
            on_text_validate=self.send_message
        )

        #Exit Button
        exit_button = Button(
            text="Exit",
            size_hint_x=0.25
        )

        exit_button.bind(
            on_press=self.exit_app
        )

        # Send Button
        send_button = Button(
            text="Send",
            size_hint_x=0.25
        )

        send_button.bind(
            on_press=self.send_message
        )

        input_layout.add_widget(self.input_box)
        input_layout.add_widget(send_button)
        input_layout.add_widget(exit_button)

        layout.add_widget(self.scroll)
        layout.add_widget(input_layout)

        return layout

    def send_message(self, instance):
        user_message = self.input_box.text.strip()

        if not user_message:
            return

        self.input_box.text = ""

        # Display the user's message immediately
        self.chat.text += (
            f"\n\n"
            f"[b][color=0066FF]You:[/color][/b] {user_message}\n"
            f"[b][color=00AA00]Bot:[/color][/b] "
        )

        # Scroll once when the bot starts responding
        self.update_chat(scroll=True)

        # Get the AI response
        answer = chat_with_ai(user_message)

        self.current_answer = answer
        self.current_index = 0

        Clock.schedule_interval(self.type_response, 0.02)

    def type_response(self, dt):
        if self.current_index >= len(self.current_answer):

            # Scroll one last time after the message finishes
            self.update_chat(scroll=True)

            return False

        self.chat.text += self.current_answer[self.current_index]
        self.current_index += 1

        # Resize the label only.
        # Don't force scrolling every frame.
        self.update_chat(scroll=False)

    def update_chat(self, scroll=False):
        # Resize the label to fit its contents
        self.chat.texture_update()
        self.chat.height = self.chat.texture_size[1]

        # Only scroll when requested
        if scroll:
            Clock.schedule_once(
                lambda dt: setattr(self.scroll, "scroll_y", 0),
                0
            )

    def exit_app(self, instance):
        App.get_running_app().stop()


if __name__ == "__main__":
    ChatApp().run()