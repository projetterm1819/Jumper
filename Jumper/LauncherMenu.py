from tkinter import * 
import subprocess as sp

def launchGame():
	sp.Popen(("python","projet2.py")) 
	ScreenMenu.destroy()


ScreenMenu = Tk()
ScreenMenu.title('Jumper')
ScreenMenu.geometry("1366x741+0+0")
w=1366
h=741
ScreenMenu.resizable(width=False,height=False)
image = PhotoImage(file='MenuBackground.png', master=ScreenMenu)
Background = Canvas(ScreenMenu, width=w, height=h)
Background.pack()

Background.create_image((w//2, h//2), image=image)

ScreenMenu.bind('<Escape>',exit)

with open("Files/Score.txt","r") as file:
	score = file.read()
Background.create_text(840,290,text="Dernier score : "+score,fill="#fff")
ButtonPicture= PhotoImage(file='titre.png')
Bouton = Button(image=ButtonPicture, command = launchGame)
Bouton.place(bordermode=OUTSIDE, height=76, width=512,x=400,y=148)
ScreenMenu.mainloop()

