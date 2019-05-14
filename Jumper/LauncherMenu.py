#initialisation
from tkinter import *
import subprocess as sp

w=1366
h=766

#fonction lancer le jeu
def launchGame():
	sp.Popen(("python","projet.py"))
	ScreenMenu.destroy()

#fonction quitter
def exit(a): #a est un paramÃ¨tre du bind qui est forcÃ©ment envoyÃ©..
	ScreenMenu.destroy()

#lecture du meilleur score
file = open("Files/Score.txt","r")
score = file.read()
file.close()

#creation de la fenetre tk
ScreenMenu = Tk()
ScreenMenu.title('Jumper')
#ScreenMenu.attributes("-fullscreen",1)

image = PhotoImage(file='MenuBackground.png', master=ScreenMenu)#image de fond
Background = Canvas(ScreenMenu, width=w, height=h)
Background.pack()
Background.create_image((w/2, h/2), image=image)

ScreenMenu.bind('<Escape>', exit) #on associe echap Ã  quitter

Background.create_text(840,290,text="Dernier Score : "+score, fill="#fff") #texte de score
ButtonPicture= PhotoImage(file='titre.png') #bouton jouer
Bouton = Button(image=ButtonPicture, command = launchGame,cursor="hand2")
Bouton.place(bordermode=OUTSIDE, height=76, width=512,x=400,y=148)


ScreenMenu.mainloop()
