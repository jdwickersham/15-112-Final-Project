'''
pygamegame.py
framework was originally taken from the PyGame option lecture, created by Lukas Peraza
Multiplayer socket implenation taken from dots_client.py from optional lecture demo

Purpose:
    this is a framework to be imported into the main game file to keep things organized, clean
Notes (from Pereza):
    - you should remove the print calls from any function you aren't using
    - you might want to move the pygame.display.flip() to your redrawAll function,
        in case you don't need to update the entire display every frame (then you
        should use pygame.display.update(Rect) instead)
'''
import pygame


class PygameGame(object):
    
    def init(self):
        pass

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):
        pass

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=1200, height=800, fps=50, title="PokeRescue Term Project"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (0, 153, 76) #background color of screen- dark green
        pygame.init()

    def run(self, serverMsg=None, server=None):
        pygame.mixer.music.load('Music/opening.mp3') #mp3 downloaded from internet
        pygame.mixer.music.play(-1,0.0)
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()
        self.server = server
        self.serverMsg=serverMsg
        # call game-specific initialization
        self.init()
        self.bg = pygame.transform.scale(pygame.image.load('Images/pokegrass.png').convert_alpha(),(1200,800))
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            screen.blit(self.bg,(0,0))
            self.redrawAll(screen)

            pygame.display.flip()

        pygame.quit()


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()