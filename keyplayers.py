import pygame

config = [{'frequency':44100, 'size':-16, 'channels':2, 'buffer':512}]

#player, stopping
players =  [
    [None, False ],
    [None, False ],
    [None, False ],
    [None, False ],
    [None, False ],
    [None, False ],
    [None, False ],
    [None, False ],
    [None, False ],
    [None, False ],
    [None, False ],
    [None, False ],
    [None, False ],
    [None, False ],
    [None, False ]
    ]

def IsStopping(index):
    return  players[index][1]

def IsPlaying(index):
    if players[index][0] is None:
        print("Player of key {} is not initialized".format(index))
        return False
    isBusy = players[index][0].music.get_busy()
    print("Player of key {} is busy? {}".format(index,isBusy))
    return isBusy

def Play(index, audiofile):
    players[index][0]=pygame.mixer
    players[index][0].init(frequency=44100, size=-16, channels=2, buffer=512)
    players[index][0].music.load(audiofile)
    players[index][0].music.play()
    players[index][1] = False;
    
def Stop(index):
    if players[index][0].music.get_busy():
        players[index][0].music.fadeout(500)
        players[index][0].music.set_endevent(EndEvent)
        players[index][1] = True;
    
def EndEvent():
    players[index][0].quit
    players[index][1] = False;

#print ("players: {}".format( players))