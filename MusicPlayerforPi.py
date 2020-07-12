# If on Windows to avoid fullscreen, use the following two lines of code
from kivy.config import Config

Config.set('graphics', 'fullscreen', '0')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from os import listdir, path

Builder.load_string('''
#: kivy 1.10.0
#: import datetime datetime
<MusicPlayer>:

    canvas.before:
        Color:
            rgba: 0, 0, .1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        id: date
        text: datetime.datetime.now().strftime("%A %d %B %Y")
        size: 200,35
        background_color: 0,.5,1,1
        pos: root.width-200, root.top-35

    ScrollView:
        size_hint: None, None
        size: root.width, root.height-135
        pos: 0, 100
        GridLayout:
            id: scroll
            cols: 1
            spacing: 10
            size_hint_y: None
            row_force_default: True
            row_default_height: 40

    GridLayout:
        rows: 1
        pos: 0, 50
        size: root.width, 50
        Button:
            id: pause
            text: '||'
            background_color: 0,.5,1,1
            on_press: root.pauseSong()
        Button:
            id: play
            text: 'Play'
            background_color: 0,.5,1,1
            on_press: root.playSong(root.spot)
    Button:
        id: nowplay
        text: 'Now Playing'
        pos: 0,0
        size: root.width, 50
        background_color: 0,.5,1,1

    Label:
        id: status
        text: ''
        center: root.center


''')


class MusicPlayer(Widget):
    directory = "/home/pi/Desktop/RPi Music"  # location of songs folder
    nowPlaying = ''  # Song that is currently playing

    spot = None
    songs = []

    def getpath(self):
        f = open("sav.dat", "r")
        f.close()
        self.getSongs()

    def savepath(self, path):
        f = open("sav.dat", "w")
        f.write(path)
        f.close()

    def select(self, path):
        self.directory = path
        self.ids.direct.text = self.directory
        self.savepath(self.directory)
        self.getSongs()

    def pauseSong(self):
        if self.nowPlaying.state == 'play':
            spot = self.nowPlaying.get_pos()
            self.nowPlaying.stop()
            self.spot = spot

    def playSong(self, p):
        if self.nowPlaying.state == 'stop':
            self.nowPlaying.play()
            self.nowPlaying.seek(p)


    def getSongs(self):

        songs = []  # List to hold songs from music directory
        self.directory = "/home/pi/Desktop/RPi Music"

        if self.directory == '':
            self.fileSelect()

        # To make sure that the directory ends with a '/'
        if not self.directory.endswith('/'):
            self.directory += '/'

        # Check if directory exists
        if not path.exists(self.directory):
            self.ids.status.text = 'Folder Not Found'
            self.ids.status.color = (1, 0, 0, 1)

        else:

            self.ids.status.text = ''

            self.ids.scroll.bind(minimum_height=self.ids.scroll.setter('height'))

            # get mp3 files from directory
            for fil in listdir(self.directory):
                if fil.endswith('.mp3'):
                    songs.append(fil)

            # If there are no mp3 files in the chosen directory
            if songs == [] and self.directory != '':
                self.ids.status.text = 'No Music Found'
                self.ids.status.color = (1, 0, 0, 1)

            songs.sort()

            for song in songs:

                def playSong(bt):
                    try:
                        self.nowPlaying.stop()
                    except:
                        pass
                    finally:
                        self.nowPlaying = SoundLoader.load(self.directory + bt.text + '.mp3')
                        self.nowPlaying.play()
                        self.ids.nowplay.text = bt.text

                btn = Button(text=song[:-4], on_press=playSong)

                # Color Buttons Alternatively
                if songs.index(song) % 2 == 0:
                    btn.background_color = (0, 0, 1, 1)
                else:
                    btn.background_color = (0, 0, 2, 1)

                self.ids.scroll.add_widget(btn)  # Add btn to layout

        self.songs = songs



class MusicApp(App):

    def build(self):
        music = MusicPlayer()
        music.getpath()
        return music



if __name__ == "__main__":
    MusicApp().run()
