import pygame
from mutagen.mp3 import MP3
import tkinter as tkr
from tkinter.filedialog import askdirectory
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import os
import time
music_player = tkr.Tk()
music_player.title("Music Player")
music_player.geometry("1000x350")
songsframe = tkr.LabelFrame(music_player, text="Playlist", font=("times new roman", 15, "bold"), bg="grey", fg="white", bd=5,relief=tkr.GROOVE)
songsframe.place(x=600, y=0, width=400, height=350)
scrol_y = tkr.Scrollbar(songsframe,orient=tkr.VERTICAL)
directory = askdirectory()
os.chdir(directory)
song_list = os.listdir()
play_list = tkr.Listbox(songsframe, font="Helvetica 12 bold", bg='#b9b9b9',fg="black", selectmode=tkr.SINGLE)
for item in song_list:
    pos = 0
    play_list.insert(pos, item)
    pos += 1
pygame.init()
pygame.mixer.init()

global autoplay
autoplay=False
def playprev():
    cur_one = play_list.curselection()
    if cur_one[0]!=0:
        next_one = cur_one[0] - 1
        song=play_list.get(next_one)
        myslider.config(value=0)
        songtime.config(text=time.strftime('%M:%S', time.gmtime(0)))
        pygame.mixer.music.load(song)
        var.set(song)
        pygame.mixer.music.play()
        direc = directory + "/" + song
        duration(direc)
        play_list.selection_clear(cur_one[0])
        play_list.activate(next_one)
        play_list.selection_set(next_one, last=None)
def playnext():
    cur_one = play_list.curselection()
    if cur_one[0]<len(song_list)-1:
        next_one = cur_one[0] + 1
        myslider.config(value=0)
        song = play_list.get(next_one)
        songtime.config(text=time.strftime('%M:%S', time.gmtime(0)))
        pygame.mixer.music.load(song)
        var.set(song)
        pygame.mixer.music.play()
        direc = directory + "/" + song
        duration(direc)
        play_list.selection_clear(cur_one[0])
        play_list.activate(next_one)
        play_list.selection_set(next_one, last=None)
def playtime():
    if stopped:
        return
    global curtime
    ctime=pygame.mixer.music.get_pos()/1000
    curtime=time.strftime('%M:%S',time.gmtime(ctime))
    ctime += 1
    if int(myslider.get()) == int(length):
        if autoplay==True:
            playnext()
    elif paused:
        pass
    elif int(myslider.get()) == int(ctime):
        # Update Slider To position
        slider_position = int(length)
        myslider.config(to=slider_position, value=int(ctime))
    else:
        # Update Slider To position
        slider_position = int(length)
        myslider.config(to=slider_position, value=int(myslider.get()))
        next_time = int(myslider.get()) +1
        myslider.config(value=next_time)
        converted_current_time = time.strftime('%M:%S', time.gmtime(next_time))
        songtime.config(text=converted_current_time)
    songtime.after(1000,playtime)
def slider(x):
    pygame.mixer.music.load(play_list.get(tkr.ACTIVE))
    pygame.mixer.music.play(start=int(myslider.get()))
def volumeslider(y):
    volume1=float('0.'+str(int(volume.get())))
    pygame.mixer.music.set_volume(volume1)
def duration(dir):
    audio = MP3(dir)
    audio_info = audio.info
    global length
    length=int(audio_info.length)
    global secs
    secs =time.strftime('%M:%S',time.gmtime(audio_info.length))
    songtotaltime.config(text=secs)
global stopped
stopped= False
global playing
playing=False
def play():
    global playing
    if playing == False :
        stop()
        pygame.mixer.music.load(play_list.get(tkr.ACTIVE))
        var.set(play_list.get(tkr.ACTIVE))
        pygame.mixer.music.play()
        global stopped
        stopped = False
        playing = True
        direc = directory + "/" + play_list.get(tkr.ACTIVE)
        duration(direc)
        playtime()
    else:
        stop()
def stop():
    pygame.mixer.music.stop()
    global stopped
    stopped = True
    global paused
    paused = False
    global playing
    playing = False
    myslider.config(value=0)
    songtime.config(text=time.strftime('%M:%S', time.gmtime(0)))
global  paused
paused = False
def pause():
    pygame.mixer.music.pause()
    global paused
    paused = True
def unpause():
    pygame.mixer.music.unpause()
    global paused
    paused = False
def toggle1():
    global autoplay
    if autoplay==False:
        autoplay = True
    else:
        autoplay = False
midframe = tkr.LabelFrame(music_player,font=("times new roman",15,"bold"),bg="black",fg="white")
midframe.place(x=0,y=60,width=550,height=130)
image = Image.open(r"C:\Users\SRIDHAR\Music\image.png")
photo = ImageTk.PhotoImage(image)
varun_label = tkr.Label(midframe,image=photo)
varun_label.pack()
volframe = tkr.LabelFrame(music_player,font=("times new roman",15,"bold"),bg="black",fg="white")
volframe.place(x=550,y=60,width=50,height=130)
vol = tkr.Label(volframe,font="Helvetica 8 bold", text="Volume",bg="black",fg='white').grid(row=0,column=0,pady=0,padx=0,)
volume=ttk.Scale(volframe,from_=9,to=0,orient=tkr.VERTICAL,value=9,command=volumeslider,length=100)
volume.grid(row=1,column=0,pady=0,padx=0,)
sliderframe = tkr.LabelFrame(music_player,font=("times new roman",15,"bold"),bg="black",fg="white")
sliderframe.place(x=0,y=190,width=600,height=60)
songtime = tkr.Label(sliderframe, font="Helvetica 13 bold", text='00:00',bg="black",fg='white')
songtime.grid(row=1,column=0)
myslider=ttk.Scale(sliderframe,from_=0,to=100,orient=tkr.HORIZONTAL,value=0,command=slider,length=450)
myslider.grid(row=1,column=2,pady=10,padx=20)
songtotaltime = tkr.Label(sliderframe, font="Helvetica 13 bold", text='00:00',bg="black",fg='white')
songtotaltime.grid(row=1,column=4)
buttonframe = tkr.LabelFrame(music_player,font=("times new roman",15,"bold"),bg="#b9b9b9",fg="white",bd=5,relief=tkr.GROOVE)
buttonframe.place(x=0,y=250,width=600,height=100)
playb = tkr.Button(buttonframe,text="Play",command=play,width=8,height=1,font=("times new roman",15,"bold"),fg="white",bg="#304a9c").grid(row=0,column=0,padx=10,pady=3)
pauseb = tkr.Button(buttonframe,text="Pause",command=pause,width=8,height=1,font=("times new roman",15,"bold"),fg="white",bg="#304a9c").grid(row=0,column=1,padx=10,pady=3)
unpasueb = tkr.Button(buttonframe,text="Resume",command=unpause,width=8,height=1,font=("times new roman",15,"bold"),fg="white",bg="#304a9c").grid(row=0,column=2,padx=10,pady=3)
stopb = tkr.Button(buttonframe,text="Stop",command=stop,width=8,height=1,font=("times new roman",15,"bold"),fg="white",bg="#304a9c").grid(row=0,column=3,padx=10,pady=3)
playnxt = tkr.Button(buttonframe,text="Play Next",command=playnext,width=8,height=1,font=("times new roman",12),fg="white",bg="#304a9c").grid(row=1,column=2,padx=10,pady=3)
playprev = tkr.Button(buttonframe,text="Play Prev",command=playprev,width=8,height=1,font=("times new roman",12),fg="white",bg="#304a9c").grid(row=1,column=1,padx=10,pady=3)
CB1 = tkr.Checkbutton(buttonframe, text = "Auto Play",onvalue = 1,offvalue = 0,height = 1,width = 7,bg='#b9b9b9',command=toggle1)
CB1.grid(row=0,column=4)
Songframe = tkr.LabelFrame(music_player,font=("times new roman",15,"bold"),bg="#b9b9b9",fg="white",bd=5,relief=tkr.GROOVE)
Songframe.place(x=0,y=0,width=600,height=60)
text = tkr.Label(Songframe,font="Helvetica 10 bold", text="Currently playing",bg="#b9b9b9",fg='black').grid(row=0,column=1)
var = tkr.StringVar()
song_title = tkr.Label(Songframe, font="Helvetica 13 bold", textvariable=var,bg="#b9b9b9").grid(row=1,column=2)
play_list.pack(fill="both", expand="yes")
music_player.mainloop()
