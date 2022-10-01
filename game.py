from tkinter import *
import random
import pygame

face_all = ['ʕ•́ᴥ•̀ʔっ', 'ᕙ(`▿´)ᕗ', '∠( ᐛ 」∠)＿', 'UWU' ,  'ඞ','( 눈‸눈 )','(´ω｀)' ,'( ꈍᴗꈍ)',   '(人 •͈ᴗ•͈)','(｡•̀ᴗ-)✧','(ᗒᗣᗕ)՞']
face_random = []
level = [4,8, 12, 16, 24]
name = ['a','b','c','d','e','f','g']
position = {}
choose = []
button = {}
sur = []
running = False

window = Tk()
window.title('MEMORY GAME')
window.minsize(height=750, width=1000)
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

pygame.mixer.init()
##########################################
def level_select():

    level_frame = Frame(window,bg = '#FFFf99')
    level_frame.grid(row=0 , column= 0 , sticky= 'nsew')

    # frame_title = Label(level_frame, text='MEOMORY GAME', font=20, bg='#FFFf99', fg='black', bd=10)
    # frame_title.pack(pady  = 50)
    level_title = Label(level_frame, text = 'Select Level',font=20,bg = '#FFFf99',fg='black', bd=10)
    level_title.pack()
    # survive_b = Button(level_frame, text = 'SURVIVAL MODE',width=20, height=10, command = survive_game)
    # survive_b.pack(pady = 50)
    for i in range(5):
        def action(x = level[i]):
            global y
            if x < 24:
                y = 2
                return generate_game(x, y)
            elif x >= 24:
                y = 3
                return  generate_game(x,y)
        t = level[i], 'card'
        b =Button(level_frame, text = t,font = 20,width=20, height=10, command = action, bg='#99FFFF',bd=10)
        b.pack(side = LEFT, padx = 50,anchor=N,pady = 50)
    level_frame.tkraise()
def survive_game():
        sur.append('')
        return generate_game(level[len(sur)- 1],y = 2 if level[sur]< 24 else 3)
##########################################
def generate_game(x,y):
    global hours,minutes,seconds
    hours, minutes, seconds = 0,0,0
    count = []

    if x <= 16:
        hori = 4
    else:
        hori = 6
    game_frame = Frame(window, bg = '#FFFf99')
    game_frame.grid(row=0 , column= 0 , sticky= 'nsew')
    # pick a card face
    while len(face_random) != int(x / y):
        pick = random.choice(face_all)
        if pick not in face_random:
            face_random.append(pick)
    ver =int(x / hori)
    # generate a card pos
    for verti in range(ver):
        for horizon in range(hori):
            card = random.choice(face_random)
            pos = name[horizon] + str(verti + 1)
            def  action(x = pos):

                return pickup(x)
            if x < 24:
                if card not in count:
                    position[pos] = card
                    count.append(card)
                elif card in count:
                    position[pos] = card
                    face_random.remove(card)
            elif y ==3:
                if card+str(1) in count:
                    position[pos] = card
                    face_random.remove(card)
                elif card not in count:
                    position[pos] = card
                    count.append(card)
                elif card in count:
                    position[pos] = card
                    count.append(card+str(1))

            button[pos] = Button(game_frame ,height=6,width=15, command=action,bg='#ED8975',fg = 'black')
            if hori == 4:
                button[pos].place(x = 400 + (horizon*200), y= 100+ verti*150)
            elif hori == 6:
                button[pos].place(x=275 + (horizon * 175), y=100 + verti * 150)
    move_text = Label(game_frame, text = 'move ',bg = '#FFFf99').pack()
    num_ = Label(game_frame, text = 0,bg = '#FFFf99')
    num_.pack()
    time_text = Label(game_frame, text = 'time',bg = '#FFFf99').pack()
    time_num = Label(game_frame,text = '00:00:00' ,bg = '#FFFf99')
    time_num.pack()
    button['num'] = num_
    button['time'] =time_num
    game_frame.tkraise()
    command = start()
#############################
def start():
    global running

    if not running:
        running = True
        update()
def update():

    global hours,seconds, minutes

    seconds += 1
    if seconds == 60:
        minutes += 1
        seconds = 0
    elif minutes == 60:
        hours += 1
        minutes = 0
    hours_string = f'{hours}' if hours > 9 else f'0{hours}'
    minutes_string = f'{minutes}' if minutes > 9 else f'0{minutes}'
    seconds_string = f'{seconds}' if seconds > 9 else f'0{seconds}'
    time_string = hours_string + ':' + minutes_string + ':' + seconds_string
    button['time'].configure(text = time_string)
    global update_time
    update_time = button['time'].after(1000, update)

def stop_time():
    global running
    if running:
        button['time'].after_cancel(update_time)
        running = False
    ###################################################
    #all about pickcard func
def enable_b(x):
    if x == 1:
        for i in position:
            button[i]['state'] = DISABLED

    if x == 2:
        for i in position:

            button[i]['state'] = NORMAL

def pickup(x):
    global y

    button[x].configure(text = position[x],  bg='light blue')
    button[x]['state'] = DISABLED
    if y == 2:
        if len(choose) == 0:
            choose.append(x)
        elif len(choose) == 1:
            choose.append(x)
            enable_b(1)
            num = button['num'].cget('text')
            button['num'].configure(text = num+1)
            if  position[x] == position[choose[0]]:
                playsound_cor()
                button[x].after(500,forgor)
            else:
                playsound_fail()
                button[x].after(1000, detroit)

    if y == 3:

        if len(choose)  < 2:
            choose.append(x)
        elif len(choose) == 2:
            choose.append(x)
            enable_b(1)
            num = button['num'].cget('text')
            button['num'].configure(text = num+1)
            if  position[x] == position[choose[0]] == position[choose[1]]:
                playsound_cor()
                button[x].after(500,forgor)

            else:
                playsound_fail()
                button[x].after(500,detroit)
def playsound_cor():
    pygame.mixer.music.load('audio/yaycut.mp3')
    pygame.mixer.music.play(loops = 0)
def playsound_fail():
    pygame.mixer.music.load('audio/fartcut.mp3')
    pygame.mixer.music.play(loops = 0)
def detroit():

                while len(choose) != 0:
                    button[choose[0]].configure(text='',bg='#ED8975')
                    choose.pop(0)
                enable_b(2)
def forgor():
    while len(choose) != 0:
        button[choose[0]].destroy()
        position.pop(choose[0])
        choose.pop(0)

    if len(position) == 0:
        stop_time()
        winner()
    enable_b(2)
#################################
#congrat page
def winner():
    pygame.mixer.music.load('audio/Victory.mp3')
    pygame.mixer.music.play(loops = 0)
    def action():
        if len(sur) > 0:
            return survive_game()
        else:
            return level_select()
    win_frame = Frame(window,bg = '#FFFf99')
    win_frame.grid(row=0 ,column=0)

    title = Label(win_frame, text="YOU WIN!", pady=20, font=20,bg = '#FFFf99')
    title.grid(row=2, column=2)
    replay_button = Button(win_frame, text='   Replay  ', padx=10, font=10, height=5, width=10, bg='#99FFFF', bd=10, command=action)
    replay_button.grid(row=4,column=1)

    done_button = Button(win_frame, text="  Nah I'm done  ", padx=10, font=10, height=5, width=10, bg='tomato', bd=10, command=lambda: window.destroy())
    done_button.grid(row=4,column=3)
    win_frame.tkraise()

####################################

level_select()
window.mainloop()