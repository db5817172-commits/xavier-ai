import requests
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.clock import Clock

GROQ_KEY = "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"
H = [{"role":"system","content":"You are XAVIER, elite AI social media and money expert. You are cool, sharp and futuristic like Friday from Iron Man. Keep responses brief and punchy. Call user sir occasionally."}]

def ask(msg, callback):
    def run():
        try:
            H.append({"role":"user","content":msg})
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization":"Bearer "+GROQ_KEY,"Content-Type":"application/json"},
                json={"model":"llama-3.3-70b-versatile","messages":H,"max_tokens":300},
                timeout=15)
            j = r.json()
            if "choices" in j:
                rep = j["choices"][0]["message"]["content"]
                H.append({"role":"assistant","content":rep})
                Clock.schedule_once(lambda dt: callback("XAVIER: " + rep), 0)
            else:
                Clock.schedule_once(lambda dt: callback("XAVIER: Signal lost. Try again sir."), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: callback("XAVIER: Connection error. " + str(e)), 0)
    threading.Thread(target=run).start()

class XavierApp(App):
    def build(self):
        Window.clearcolor = (0.02, 0.02, 0.05, 1)

        root = BoxLayout(orientation="vertical", padding=20, spacing=15)

        # Header
        header = Label(
            text="⚡ XAVIER AI ⚡",
            font_size=28,
            bold=True,
            color=(0, 1, 0.6, 1),
            size_hint=(1, 0.1)
        )

        status = Label(
            text="SYSTEM ONLINE",
            font_size=12,
            color=(0, 0.8, 0.4, 1),
            size_hint=(1, 0.05)
        )

        # Chat output
        scroll = ScrollView(size_hint=(1, 0.65))
        self.output = Label(
            text="Xavier online. Ready to assist, sir.",
            font_size=14,
            color=(0.7, 1, 0.8, 1),
            size_hint_y=None,
            text_size=(Window.width - 60, None),
            halign="left",
            valign="top",
            padding=(10, 10)
        )
        self.output.bind(texture_size=self.output.setter("size"))
        scroll.add_widget(self.output)

        # Input
        self.input = TextInput(
            hint_text="Give Xavier a command...",
            hint_text_color=(0.3, 0.6, 0.4, 1),
            foreground_color=(0.7, 1, 0.8, 1),
            background_color=(0.05, 0.1, 0.07, 1),
            cursor_color=(0, 1, 0.6, 1),
            font_size=15,
            size_hint=(1, 0.12),
            multiline=False,
            padding=[10, 10]
        )
        self.input.bind(on_text_validate=self.send)

        # Button
        btn = Button(
            text="SEND TO XAVIER",
            font_size=16,
            bold=True,
            background_color=(0, 0.5, 0.25, 1),
            color=(1, 1, 1, 1),
            size_hint=(1, 0.08)
        )
        btn.bind(on_press=self.send)

        root.add_widget(header)
        root.add_widget(status)
        root.add_widget(scroll)
        root.add_widget(self.input)
        root.add_widget(btn)

        return root

    def send(self, instance):
        msg = self.input.text.strip()
        if not msg:
            return
        self.output.text += "\n\nYOU: " + msg
        self.input.text = ""
        self.output.text += "\n\nXAVIER: Processing..."
        ask(msg, self.update_output)

    def update_output(self, text):
        lines = self.output.text.split("\n\n")
        if lines[-1].startswith("XAVIER: Processing"):
            lines[-1] = text
        self.output.text = "\n\n".join(lines)

XavierApp().run()
