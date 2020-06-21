import pygame

config = [{'frequency':44100, 'size':-16, 'channels':2, 'buffer':512}]

#player, stopping
players =  [
    [object, False ],
    [object, False ],
    [object, False ],
    [object, False ],
    [object, False ],
    [object, False ],
    [object, False ],
    [object, False ],
    [object, False ],
    [object, False ],
    [object, False ],
    [object, False ],
    [object, False ],
    [object, False ],
    [object, False ]
    ]

def IsStopping(index):

def Play(index, audiofile):
    players[index,0]=pygame.mixer
    players[index,0].init(frequency=44100, size=-16, channels=2, buffer=512)
    pygame.mixer.music.load(audiofile)
    pygame.mixer.music.play()
    
def Stop(index):
    players[index,1] = True;
    if players[index,0].get_busy():
        players[index,0].fadeout(500)
        players[index,0].set_endevent(EndEvent)
    
def EndEvent(index):
    players[index,0].quit
    players[index,1] = False;

print (players)