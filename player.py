from tkinter import *
from tkinter import filedialog
import pygame

root = Tk()

root.title("MP3 Player")
root.geometry("500x400")

#Initialize pygame mixer
pygame.mixer.init()


def play_time():
	current_time=pygame.mixer.music.get_pos()/1000
	my_label.config(text=int(current_time))

	my_label.after(1000,play_time)


#Function To Add One Song
def add_song():
	song=filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetypes=(( "mp3 Files", "*.mp3" ), ) )
	#Strip Out Absolute Path And mp3 Extension
	song=song.replace("/home/luna/mp3/audio/", "")
	song=song.replace(".mp3", "")
	#Add To End
	playlist_box.insert(END, song)

#Function To Add Many Songs
def add_many_songs():
	songs=filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song", filetypes=(( "mp3 Files", "*.mp3" ), ) )
	#Loop Through List Of Songs
	for song in songs:
		#Strip Out Absolute Path And mp3 Extension
		song=song.replace("/home/luna/mp3/audio/", "")
		song=song.replace(".mp3", "")
		#Add To End
		playlist_box.insert(END, song)


def delete_song():
	playlist_box.delete(ANCHOR)#ANCHOR Is The Selected Option In Playlist


def delete_all_songs():
	playlist_box.delete(0, END)


#Create Play Function
def play():
	#Reconstruct Song Name
	song = playlist_box.get(ACTIVE)
	song = f'/home/luna/mp3/audio/{song}.mp3'
	

	#Load And Play Song With Pygame Mixer
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(0)

	#Get Play Time
	play_time()


def stop():
	#Stop The Song
	pygame.mixer.music.stop()

	#Clear Playlist Bar
	playlist_box.selection_clear(ACTIVE)

global paused
paused = False

#Pause Function
def pause(is_paused):
	global paused
	paused = is_paused

	if paused:
		#Unpause The Song
		pygame.mixer.music.unpause()
		paused = False
	else:
		#pause The Song
		pygame.mixer.music.pause()
		paused = True


def next_song():
	#Get Current Song Number
	next_one=playlist_box.curselection()

	next_one=next_one[0]+1

	#Grab The Song Title From Playlist
	song = playlist_box.get(next_one)

	song = f'/home/luna/mp3/audio/{song}.mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(0)

	#Clear ActiveBar In Playlist
	playlist_box.selection_clear(0, END)

	#Move Active Bar
	playlist_box.activate(next_one)

	#Set The Avtive Bar To Next Song
	playlist_box.selection_set(next_one, last=None)


def prev_song():
	#Get Current Song Number
	prev_one=playlist_box.curselection()

	prev_one=prev_one[0]-1

	#Grab The Song Title From Playlist
	song = playlist_box.get(prev_one)

	song = f'/home/luna/mp3/audio/{song}.mp3'
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(0)

	#Clear ActiveBar In Playlist
	playlist_box.selection_clear(0, END)

	#Move Active Bar
	playlist_box.activate(prev_one)

	#Set The Avtive Bar To Prev Song
	playlist_box.selection_set(prev_one, last=None)







	

#Create Playlist Box
playlist_box=Listbox(root, bg="white", fg="green", width=60, selectbackground="black", selectforeground="white")
playlist_box.pack(pady=20)

#Define Button Images For Controls
back_btn_img = PhotoImage(file='images/prev-button.png')
forward_btn_img = PhotoImage(file='images/next-button.png')
play_btn_img = PhotoImage(file='images/play.png')
pause_btn_img = PhotoImage(file='images/pause.png')
stop_btn_img = PhotoImage(file='images/stop.png')

#Create Button Frames
control_frame=Frame(root)
control_frame.pack(pady=20)

#Create Buttons
back_button=Button(control_frame, image=back_btn_img, borderwidth=0, command=prev_song)
forward_button=Button(control_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button=Button(control_frame, image=play_btn_img, borderwidth=0,command=play)
pause_button=Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button=Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=5)
forward_button.grid(row=0, column=1, padx=5)
play_button.grid(row=0, column=2, padx=5)
pause_button.grid(row=0,column=3, padx=5)
stop_button.grid(row=0,column=4, padx=5)


#Create Menu

my_menu=Menu(root)
root.config(menu=my_menu)

#Create Add Song Menu Dropdowns
add_song_menu=Menu(my_menu, tearoff=0)#Removes Dotted Line tearoff
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
#Add One Song
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)
#Add Many Songs
add_song_menu.add_command(label="Add Many Songs To Playlist", command=add_many_songs)


#Delete Song Menu
remove_song_menu=Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Remove A Song", command=delete_song)
remove_song_menu.add_command(label="Remove All Songs", command=delete_all_songs)

#Create Stautus Bar
status_bar=Label(root,text='Nothing', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)


#Temporary Label
my_label=Label(root, text='')
my_label.pack(pady=20)


root.mainloop()