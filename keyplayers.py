import pygame

config = [{'frequency':44100, 'size':-16, 'channels':2, 'buffer':512}]

player = pygame.mixer


def IsPlaying(index):
    isBusy = player.Channel(index).get_busy()
    print("Player of channel {} is busy? {}".format(index,isBusy))
    return isBusy

def Play(index, audiofile):
    player.Channel(index).play(pygame.mixer.Sound(audiofile))
    
def Stop(index):
    player.Channel(index).fadeout(500)
    
def Init():
    player.init(frequency=44100, size=-16, channels=2)
    player.set_num_channels(15)
    print("Number of channels {}".format(player.get_num_channels()))
    print("Init {}".format(player.get_init()))

#print ("players: {}".format( players))