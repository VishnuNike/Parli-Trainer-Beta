from kivy.clock import Clock
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.dropdown import DropDown
import requests
import random
from bs4 import BeautifulSoup

Builder.load_string(''' 
#:import datetime datetime

<MainWidget>:
    drop_content: drop_content.__self__
    BoxLayout: 

        orientation: 'vertical'
        Label:
            id: mainl
            text: (str(datetime.timedelta(seconds=root.number)))[3:7]
            font_size: 160
            markup: True
            halign: 'center' 
            valign: 'middle'

        BoxLayout:
            orientation: 'horizontal'
            padding: [20, 20, 20, 10]
            spacing: 20
            height: 160
            size_hint: (1, None)

            TextInput:
                id: input
                font_size: 12
                hint_text: 'Resolution: '

        BoxLayout:
            orientation: 'horizontal'
            padding: [20, 10, 20, 20]
            spacing: 20
            height: 90
            size_hint: (1, None)       
            Button:
                id: starpper
                text: 'Start'
                font_size: 25
                background_normal: 'green_normal.png'
                background_down: 'green_down.png'
                on_press: root.start_stop()
                border: (2,2,2,2)

            Button:
                text: 'Reset'
                font_size: 25
                background_normal: 'blue_normal.png'
                background_down: 'blue_down.png'
                on_press: root.reset()
                border: (2,2,2,2)


            Button:
                id: btn
                background_normal: 'yellow_down.png'
                background_down: 'yellow_normal.png'
                text: "Speeches"
                font_size: 25
                border: (2,2,2,2)
                on_parent: drop_content.dismiss()
                on_release: drop_content.open(self)

            Button:
                id: toss
                text: 'Toss'
                font_size: 25
                background_normal: 'grey_normal.png'
                background_down: 'grey_down.png'
                border: (2,2,2,2)
                on_press: root.toss()

            Button:
                text: 'Random'
                font_size: 25
                background_normal: 'purple_normal.png'
                background_down: 'purple_down.png'
                border: (2,2,2,2)
                on_press: root.random_res()

        DropDown:
            id: drop_content
            on_select: btn.text = '{}'.format(args[1])

            Button:
                id: btn1
                text: 'PMC'
                on_release: drop_content.select('PMC')
                on_press: root.set(420)
                size_hint_y: None
                height: 35
                border: (2,2,2,2)
                background_normal: 'black_normal.png'
                background_down: 'black_down.png'

            Button:
                id: btn2
                text: 'LOC'
                color: 0,0,0,1
                size_hint_y: None
                height: 35
                on_release: drop_content.select('LOC')
                on_press: root.set(480)
                background_normal: 'white_normal.png'
                background_down: 'white_down.png'

            Button:
                id: btn3
                text: 'MOG'
                size_hint_y: None
                height: 35
                on_release: drop_content.select('MOG')
                on_press: root.set(480)
                border: (2,2,2,2)
                background_normal: 'black_normal.png'
                background_down: 'black_down.png'

            Button:
                id: btn4
                text: 'MOO'
                color: 0,0,0,1
                size_hint_y: None
                height: 35
                on_release: drop_content.select('MOO')
                on_press: root.set(480)
                background_normal: 'white_normal.png'
                background_down: 'white_down.png'

            Button:
                id: btn5
                text: 'LOR'
                color: 0,0,0,1
                size_hint_y: None
                height: 35
                on_release: drop_content.select('LOR')
                on_press: root.set(240)
                background_normal: 'white_normal.png'
                background_down: 'white_down.png'

            Button:
                id: btn6
                text: 'PMR'
                size_hint_y: None
                height: 35
                on_release: drop_content.select('PMR')
                on_press: root.set(300)
                border: (2,2,2,2)
                background_normal: 'black_normal.png'
                background_down: 'black_down.png'
''')


class drop_content(DropDown):
    pass


class MainWidget(BoxLayout):
    number = NumericProperty(420)

    original_number = NumericProperty(420)

    page = requests.get("https://sites.google.com/view/kick-some-aff-break-a-neg/motions?authuser=0")
    soup = BeautifulSoup(page.content, 'html.parser')
    page.close()
    results = soup.find_all('p', class_="CDt4Ke zfr3Q")
    resolutions = []
    for result in results:
        if result.text[0:5] == "Info ":
            resolutions[len(resolutions) - 1] = resolutions[len(resolutions) - 1] + " " + result.text
        elif result.text == '' or ' ' == result.text:
            continue
        else:
            resolutions.append(result.text)

    side = ['Heads', 'Tails']

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.run = False
        self.grace = False
        self.overtime = False

    def increment_time(self, interval):
        self.run = True
        if self.grace is False and self.number != 0:
            self.number -= 1
        else:
            if self.number > 28:
                self.number += 1
                self.ids.mainl.color = [1, 0, 0, 1]
                Clock.unschedule(self.grace_period_red)
                Clock.unschedule(self.grace_period_black)
            else:
                self.number += 1
                Clock.schedule_interval(self.grace_period_red, 1)
                Clock.schedule_once(self.grace_period_trigger, 0.5)
            self.grace = True

    def start_stop(self):
        if self.run is False:
            Clock.unschedule(self.increment_time)
            Clock.schedule_interval(self.increment_time, 1)
            self.ids.starpper.text = "Stop"
            self.ids.starpper.background_normal = 'red_normal.png'
            self.ids.starpper.background_down = 'red_down.png'
        else:
            Clock.unschedule(self.increment_time)
            self.run = False
            self.ids.starpper.text = "Start"
            self.ids.starpper.background_normal = 'green_normal.png'
            self.ids.starpper.background_down = 'green_down.png'

    def reset(self):
        self.grace = False
        self.ids.mainl.color = [1, 1, 1, 1]
        Clock.unschedule(self.grace_period_black)
        Clock.unschedule(self.grace_period_red)
        self.number = self.original_number

    def set(self, seconds):
        self.number = seconds
        self.original_number = seconds

    def grace_period_red(self, interval):
        self.ids.mainl.color = [1, 0, 0, 1]

    def grace_period_trigger(self, interval):
        Clock.schedule_interval(self.grace_period_black, 1)

    def grace_period_black(self, interval):
        self.ids.mainl.color = [0, 0, 0, 1]

    def random_res(self):
        self.ids.input.text = str(random.choice(self.resolutions[1:]))

    def toss(self):
        self.ids.toss.text = str(random.choice(self.side))


class MyApp(App):
    def build(self):
        return MainWidget()


if __name__ == '__main__':
    from kivy.core.window import Window
    from kivy.utils import get_color_from_hex
    Window.clearcolor = get_color_from_hex('#4b5162')
    MyApp().run()
