import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

GROQ_KEY = "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"
H = [{"role":"system","content":"You are XAVIER, elite AI social media and money expert. Be sharp and brief. Call user sir."}]

def ask(msg):
    H.append({"role":"user","content":msg})
    r = requests.post("https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization":"Bearer "+GROQ_KEY,"Content-Type":"application/json"},
        json={"model":"llama-3.3-70b-versatile","messages":H,"max_tokens":300})
    j = r.json()
    rep = j["choices"][0]["message"]["content"]
    H.append({"role":"assistant","content":rep})
    return rep

class XavierApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=15, spacing=10)
        self.output = Label(text="XAVIER READY SIR", size_hint=(1,0.75), text_size=(350,None))
        self.input = TextInput(hint_text="Command Xavier...", size_hint=(1,0.15), multiline=False)
        btn = Button(text="SEND", size_hint=(1,0.1))
        btn.bind(on_press=self.send)
        layout.add_widget(self.output)
        layout.add_widget(self.input)
        layout.add_widget(btn)
        return layout

    def send(self, instance):
        msg = self.input.text.strip()
        if not msg: return
        self.output.text = "Processing..."
        self.input.text = ""
        try:
            rep = ask(msg)
            self.output.text = "XAVIER: " + rep
        except Exception as e:
            self.output.text = "Error: " + str(e)

XavierApp().run()
