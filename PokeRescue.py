'''
pokeRescue.py
framework code originally taken from the PyGame optional lecture, but heavily edited
socket code orginally from Sockets optional lecture, but heavily added to (all messages follow lecture format, but are of my creation)

Purpose: 
	to run the game. This is the main file. This is also therefore the client file.
'''
import pygame
import socket
import threading
from queue import Queue
import random
import time
import math
from User import User
from Pokeball import Pokeball
from Obstacle import Obstacle
from Pokemon import Pokemon
from Enemy import Enemy
from PokeballBullet import PokeballBullet
from pygamegame import PygameGame #the framework

HOST = "" # put your IP address here if playing on multiple computers
PORT = 8090
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((HOST,PORT))
print("connected to server")

def handleServerMsg(server, serverMsg):
    server.setblocking(1)
    msg = ""
    command = ""
    while True:
        msg += server.recv(10).decode("UTF-8")
        command = msg.split("\n")
        while (len(command) > 1):
            readyMsg = command[0]
            msg = "\n".join(command[1:])
            serverMsg.put(readyMsg)
            command = msg.split("\n")

class pokeRescue(PygameGame):
    def init(self):

        #A set of boolean variables are intialized below to organize which game screen is to be drawn in redrawAll
        self.startScreen=True
        self.instructions=False
        self.stageOne=False
        self.stageTwo=False
        self.stageThree=False
        self.won=False
        self.scores=False
        self.enterName=False
        self.lost=False
        self.fail=False #if you don't even collect pokeballs, you just fail



        #Game condition values
        self.pokeballs=0
        self.score=0
        self.pokemonList=[]
        


        #Counters
        self.stageOneCounter=20 #countdown timer for stageOne
        self.stageOneCounterTimer=0
        self.stageThreeCounter=20
        self.stageThreeCounterTimer=0



        #Initializations
        User.init()
        user= User(self.width/2,self.height/2,'Lonely')
        self.userGroup=pygame.sprite.GroupSingle(user)
        self.user=self.userGroup.sprite

        self.otherPlayerGroup=pygame.sprite.Group()

        Obstacle.init()
        self.obstacleGroup= pygame.sprite.Group()

        Pokeball.init()
        self.pokeballGroup= pygame.sprite.Group()
        self.pokeballProb=range(50) #check 2/3 every second currently checking every 1/50 seconds so decrease probability by 50 (multiply value by 50)


        Enemy.init()
        self.enemyGroup= pygame.sprite.Group()

        PokeballBullet.init()
        self.pokeballBullets=pygame.sprite.Group()
        self.otherPokeballBullets=pygame.sprite.Group()

        Pokemon.init()
        self.pokemonGroup= pygame.sprite.Group() 
    
    def saveScore(self): #writes score and name inputted through terminal
        with open('scoreboard.txt','a') as scoreboard:
            scoreboard.write('%s:%d'%(self.user.andrewID,self.user.numPokemon) + '\n')

    def makeScores(self): #return list of name/score pairs read from file
        with open('scoreboard.txt','r') as scoreboard:
            scores=scoreboard.readlines()
            scores=scores[::-1]
        return scores

    def keyPressed(self,keyCode,modifier):
        msg=""
        if keyCode==pygame.K_SPACE and self.startScreen==True: #if on title screen and space bar pressed, move to instructions
            self.startScreen=False
            self.instructions=True
            beep=pygame.mixer.Sound('Music/beep.wav')
            beep.play()
            msg="openInstruct noDetails\n"
        elif keyCode==pygame.K_SPACE and self.instructions==True: #if on instructions and space bar pressed, move to stageOne
            self.instructions=False
            self.stageOne=True
            self.stageOneCounterTimer=time.time()
            beep=pygame.mixer.Sound('Music/beep.wav')
            beep.play()
            msg="startGame noDetails\n"
        
        elif keyCode==pygame.K_SPACE and self.won==True:
            beep=pygame.mixer.Sound('Music/beep.wav')
            beep.play()
            self.won=False
            self.enterName=True

        elif self.enterName==True: #enter andrewID
            if keyCode==pygame.K_RETURN:
                self.enterName=False
                self.scores=True
                self.saveScore() #read the final andrewID to file
                beep=pygame.mixer.Sound('Music/beep.wav')
                beep.play()
                self.user.scoreInputted=True
            if keyCode==pygame.K_BACKSPACE:
                if len(self.user.andrewID)>0:
                    self.user.andrewID=self.user.andrewID[:-1]
            else:
                self.user.andrewID+=pygame.key.name(keyCode)

        
        #keyboard shortcuts for testing (uncomment to use these features/cheats)
        elif keyCode==pygame.K_SPACE and self.stageOne==True: #skip to stage two from stage one
            self.stageOne=False
            self.stageTwo=True
        elif keyCode==pygame.K_SPACE and self.stageTwo==True: #skip to stage three from stage two
            self.stageTwo=False
            self.stageThree=True
            self.stageThreeCounterTimer=time.time()
        elif keyCode==pygame.K_BACKSPACE and self.stageTwo==True: #skip from stage two to win screen
            self.stageTwo=False
            self.won=True
        elif keyCode==pygame.K_0 and self.user.scoreInputted==False: #skip to inputting score (passes over requirement of game being won)
            self.startScreen=False
            self.instructions=False
            self.stageOne=False
            self.stageTwo=False
            self.stageThree=False
            self.won=False
            self.lost=False
            self.fail=False
            self.scores=False
            self.enterName=True
            self.user.scoreInputted=True
        





        # if (msg != ""):
        #     print ("sending: ", msg,)
        self.server.send(msg.encode())


    def mousePressed(self, x, y):
        msg=""
        if self.stageTwo==True and self.pokeballs>0:
            user=self.userGroup.sprites()[0]
            self.pokeballBullets.add(PokeballBullet(user.x,user.y,x,y))
            msg="bulletFired %d %d\n"%(x,y)
            self.pokeballs-=1

        # if (msg != ""):
        #     print ("sending: ", msg,)
        self.server.send(msg.encode())

    
    def timerFired(self,dt):
        while (self.serverMsg.qsize()>0):
            msg=self.serverMsg.get(False)
            try:
            #print('received: ',msg,'\n')
                msg=msg.split()
                command=msg[0]

                if command == 'myIDis':
                    myPID=msg[1]
                    self.user.changePID(myPID)

                elif command == 'newPlayer':
                    newPID=msg[1]
                    otherPlayer= User(self.width//2,self.height//2,newPID)
                    self.otherPlayerGroup= pygame.sprite.GroupSingle(otherPlayer)
                    self.otherPlayer= self.otherPlayerGroup.sprite
                    self.otherPlayer.baseImage= pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Images/otherPlayerLeft.png').convert_alpha(),(30, 50)),0)
                    self.otherPlayer.image= pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Images/otherPlayerLeft.png').convert_alpha(),(30, 50)),0)
                    for pokeball in self.pokeballGroup:
                        pokeball.startTime=time.time()
                        pokeball.timeLeft=pokeball.timeDuration-(time.time()-pokeball.startTime)
                
                elif command == 'obstacles':
                    obstacleX=int(msg[1])
                    obstacleY=int(msg[2])
                    imageKey=int(msg[3])
                    obstacle= Obstacle(obstacleX,obstacleY)
                    obstacle.image=Obstacle.image_list[imageKey]
                    self.obstacleGroup.add(obstacle)

                elif command == 'pokemon':
                    pokemonX=int(msg[1])
                    pokemonY=int(msg[2])
                    key=int(msg[3])
                    vX=float(msg[4])
                    vY=float(msg[5])
                    angleSpeed=int(msg[6])
                    poke=Pokemon(pokemonX,pokemonY)
                    poke.key=key
                    poke.image_loc=Pokemon.checkImageCache(poke.key)
                    poke.image=pygame.transform.scale(pygame.image.load(poke.image_loc).convert_alpha(),(60,60))
                    poke.name=Pokemon.pokemon_dict[poke.key]['name']
                    poke.speed=(Pokemon.pokemon_dict[poke.key]['avg_stats'])//8.
                    poke.vX=vX
                    poke.vY=vY
                    poke.angleSpeed=angleSpeed
                    poke.velocity=poke.vX,poke.vY
                    if poke.vX>0: poke.image= pygame.transform.flip(poke.image,True,False)
                    poke.updateRect()
                    self.pokemonGroup.add(poke)
                
                elif command == 'enemy':
                    enemyX= int(msg[1])
                    enemyY= int(msg[2])
                    vX= float(msg[3])
                    vY= float(msg[4])
                    angleSpeed= int(msg[5])
                    enemy=Enemy(enemyX,enemyY)
                    enemy.vX=vX
                    enemy.vY=vY
                    enemy.angleSpeed=angleSpeed
                    enemy.velocity=vX,vY
                    enemy.canSteal=True
                    if enemy.vX>0: 
                        enemy.image=enemy.rightImage
                    self.enemyGroup.add(enemy)

                elif command == 'pokeballs':
                    pokeballX=int(msg[1])
                    pokeballY=int(msg[2])
                    timeDuration=int(msg[3])
                    ball=Pokeball(pokeballX,pokeballY)
                    ball.timeDuration=timeDuration
                    self.pokeballGroup.add(ball)


                elif command == 'bulletFired':
                    x= int(msg[2])
                    y= int(msg[3])
                    player=self.otherPlayerGroup.sprites()[0]
                    self.otherPokeballBullets.add(PokeballBullet(player.x,player.y,x,y))

                elif command == 'playerUpdate':
                    x= int(msg[2])
                    y= int(msg[3])
                    ogX=self.otherPlayer.x
                    ogY=self.otherPlayer.y
                    if x<ogX:
                        self.otherPlayer.baseImage=pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Images/otherPlayerLeft.png').convert_alpha(),(30, 50)),0)
                    if x>ogX:
                        self.otherPlayer.baseImage=pygame.transform.rotate(pygame.transform.scale(pygame.image.load('Images/otherPlayerRight.png').convert_alpha(),(30, 50)),0)
                    self.otherPlayer.movePos(x,y)
                    self.otherPlayerGroup.update(self.isKeyPressed, self.width, self.height)

                elif command == 'userCaught':
                    self.otherPlayer.numPokemon+=1

                elif command == 'userStolenFrom':
                    self.otherPlayer.numPokemon-=1
                    
                elif command == 'bulletUpdate':
                    self.otherPokeballBullets.update(self.width, self.height)

                elif command == 'openInstruct':
                    self.startScreen=False
                    self.instructions=True

                elif command == 'startGame':
                    self.instructions=False
                    self.stageOne=True
                    self.stageOneCounterTimer=time.time()

            except:
                #print('failed')
                serverMsg.task_done()
        

        msg=""
        self.userGroup.update(self.isKeyPressed, self.width, self.height)
        msg="playerUpdate %d %d\n"%(self.user.x,self.user.y)
        # if (msg != ""):
        #     print ("sending: ", msg,)
        self.server.send(msg.encode())
        
        self.enemyGroup.update(self.width,self.height)
        self.pokemonGroup.update(self.width,self.height)
        
        msg=""
        self.pokeballBullets.update(self.width,self.height)
        msg="bulletUpdate noDetails\n"
        # if (msg != ""):
        #     print ("sending: ", msg,)
        self.server.send(msg.encode())
        
        #STAGE ONE
        if self.stageOne==True:
            self.pokeballGroup.update() #timer on pokeball decreased
            for ball in self.pokeballGroup: #once their time runs out, get rid of them
                if ball.timeLeft<=0:
                    self.pokeballGroup.remove(ball)
            
            # msg=""
            prob=random.choice(self.pokeballProb)
            if(prob==1): #will randomly add pokeballs during the stageOne
                x=random.randint(0,self.width)
                y=random.randint(0,self.height-150) #don't spawn under score rect
                self.pokeballGroup.add(Pokeball(x,y))
                for pokeball in self.pokeballGroup: #don't let obstacle overlap
                    self.pokeballGroup.remove(pokeball)
                    if len(pygame.sprite.spritecollide(pokeball,self.obstacleGroup,False))>0:
                        self.pokeballGroup.remove(pokeball)
                    else: 
                        self.pokeballGroup.add(pokeball)

            if (self.stageOneCounter-int(time.time()-self.stageOneCounterTimer))==0: #when timer runs out, move on to next stage
                self.stageOne=False
                self.stageTwo=True
            
            if pygame.sprite.groupcollide(self.userGroup, self.pokeballGroup, False, True):
                pokeballSound=pygame.mixer.Sound('Music/pokeball.wav')
                pokeballSound.play()
                self.pokeballs+=1
        
        #STAGE TWO
        if self.stageTwo==True:
            for pokemon in self.pokemonGroup:
                if len(pygame.sprite.spritecollide(pokemon, self.obstacleGroup, False))>0:
                    vX,vY=pokemon.velocity
                    vX*=-1
                    vY*=-1
                    pokemon.velocity=vX,vY
            msg=""
            collisions=pygame.sprite.groupcollide(self.pokemonGroup, self.pokeballBullets, True, True)
            for pokemon in collisions:
                 if len(collisions[pokemon])>0:
                     if pokemon.added==False:
                         self.pokemonList.append(pokemon.name)
                         self.user.numPokemon+=1
                         pokemonSound=pygame.mixer.Sound('Music/pokemon.wav')
                         pokemonSound.play()
                         msg="userCaught noDetails\n"
            # if (msg != ""):
            #     print ("sending: ", msg,)
            self.server.send(msg.encode())

            if self.pokeballs<1 and len(self.pokeballBullets)<1 or len(self.pokemonList)==6:
                if len(self.pokemonList)==0:
                    self.stageTwo=False
                    self.fail=True
                    lostSound=pygame.mixer.Sound('Music/lost.wav')
                    lostSound.play()
                else:
                    self.stageTwo=False
                    self.stageThree=True
                    self.stageThreeCounterTimer=time.time()

        #STAGE THREE
        if self.stageThree==True:
            self.enemyGroup.update(self.width,self.height)
            for enemy in self.enemyGroup:
                if len(pygame.sprite.spritecollide(enemy, self.obstacleGroup, False))>0:
                    vX,vY=enemy.velocity
                    enemy.vX*=-1
                    enemy.vY*=-1
                    enemy.velocity=enemy.vX,enemy.vY
            if len(self.pokemonList)<3:
                self.stageThree=False
                self.lost=True
                lostSound=pygame.mixer.Sound('Music/lost.wav')
                lostSound.play()
            msg=""
            for collision in pygame.sprite.spritecollide(self.user, self.enemyGroup, False):
                if collision.canSteal==True:
                    self.score+=1
                    self.pokemonList.pop(random.randint(0,len(self.pokemonList)-1)) #randomly remove
                    self.user.numPokemon-=1
                    collision.canSteal=False #can only take one pokemon from you
                    stolenSound=pygame.mixer.Sound('Music/stolen.wav')
                    stolenSound.play()
                    msg="userStolenFrom noDetails\n"
            # if (msg != ""):
            #     print ("sending: ", msg,)
            self.server.send(msg.encode())
            
            

            if (self.stageThreeCounter-int(time.time()-self.stageThreeCounterTimer))==0: #when timer runs out, move on to next stage
                self.stageThree=False
                self.won=True

        #COLLISION
        ogX=self.user.x
        ogY=self.user.y
        self.user.move(self.isKeyPressed)
        if self.user.dx==-1:
            if pygame.sprite.groupcollide(self.userGroup, self.obstacleGroup,False,False): #stop user from moving, carries through all stages
                self.user.x=ogX+20
                self.user.dx=1
        elif self.user.dx==1:
            if pygame.sprite.groupcollide(self.userGroup, self.obstacleGroup,False,False): #stop user from moving, carries through all stages
                self.user.x=ogX-20
                self.user.dx=-1
        if self.user.dy==1:
            if pygame.sprite.groupcollide(self.userGroup, self.obstacleGroup,False,False): #stop user from moving, carries through all stages
                self.user.y=ogY+20
                self.user.dy=-1
        elif self.user.dy==-1:
            if pygame.sprite.groupcollide(self.userGroup, self.obstacleGroup,False,False): #stop user from moving, carries through all stages
                self.user.y=ogY+20
                self.user.dy=1
            

    
    def redrawAll(self,screen):
        self.storyFont=pygame.font.Font('Images/pokemonfont2.ttf', 14) #font found on internet and downloaded into game folder
        self.cenFont=pygame.font.Font('Images/pokemonfont2.ttf', 24)
        self.timeFont=pygame.font.Font('Images/pokemonfont2.ttf', 18)

        #START SCREEN AND INSTRUCTION
        if self.startScreen==True:
            screen.blit(pygame.transform.scale(pygame.image.load('Images/tittle.png').convert_alpha(),(1200,800)),(0,0))
        
        elif self.instructions==True:
            screen.blit(pygame.transform.scale(pygame.image.load('Images/instructions.png').convert_alpha(),(1200,800)),(0,0))
        
        #STAGE ONE
        elif self.stageOne==True:

            self.pokeballGroup.draw(screen) #pokeballs
            self.obstacleGroup.draw(screen) #obstacles
            self.otherPlayerGroup.draw(screen)
            self.userGroup.draw(screen) #user

            for pokeball in self.pokeballGroup: #draws timer above pokeballs
                pokeballTime=self.storyFont.render(str(int(pokeball.timeLeft)),1,(0,0,255))
                screen.blit(pokeballTime,(pokeball.rect.center[0]-5,pokeball.rect.y-12))

            self.menu = pygame.transform.scale(pygame.image.load('Images/menu.png').convert_alpha(),(1200,100))
            screen.blit(self.menu, (0,self.height-100))
            pokeballDisplay=self.storyFont.render('Pokeballs: %d'%(self.pokeballs),1,(0,0,255))
            pokeballDisplayCen=pokeballDisplay.get_rect(center=(self.width-(self.width//10),self.height-(self.height//12)))
            screen.blit(pokeballDisplay,pokeballDisplayCen)

            timer=self.timeFont.render('Time Left: '+ str(self.stageOneCounter-int(time.time()-self.stageOneCounterTimer)),1,(0,0,255))
            timerCen=timer.get_rect(center=(self.width//2,self.height-(self.height//12)))
            screen.blit(timer,timerCen)

            name=self.cenFont.render(self.user.PID,1,(0,0,0))
            nameCen=name.get_rect(center=(120,self.height//24))
            screen.blit(name,nameCen)

        #STAGE TWO
        elif self.stageTwo==True:
            self.obstacleGroup.draw(screen) #obstacles
            self.userGroup.draw(screen) #user
            self.otherPlayerGroup.draw(screen)
            self.pokeballBullets.draw(screen)
            self.pokemonGroup.draw(screen)

            self.menu = pygame.transform.scale(pygame.image.load('Images/menu.png').convert_alpha(),(1200,100))
            screen.blit(self.menu, (0,self.height-100))
            pokeballDisplay=self.storyFont.render('Pokeballs: %d'%(self.pokeballs),1,(0,0,255))
            pokeballDisplayCen=pokeballDisplay.get_rect(center=(self.width-(self.width//10),self.height-(self.height//12)))
            if len(self.otherPlayerGroup)>0:
                otherPokeDisplay=self.storyFont.render('%s PokeCount: %d'%(self.otherPlayer.PID,self.otherPlayer.numPokemon),1,(0,0,255))
                otherPokeDisplayCen=otherPokeDisplay.get_rect(center=(self.width-(self.width//6),self.height-(self.height//24)))
                screen.blit(otherPokeDisplay,otherPokeDisplayCen)
            
            screen.blit(pokeballDisplay,pokeballDisplayCen)

            pokemonDisplay=self.storyFont.render('Pokemon:',1,(0,0,255))
            pokemonDisplayCen=pokemonDisplay.get_rect(center=(0+(self.width//11),self.height-(self.height//12)))
            screen.blit(pokemonDisplay,pokemonDisplayCen)
            strOne=''
            for elem in self.pokemonList:
                strOne+='%s, '%(elem)
            strOne=strOne[0:-2]
            pokemonListDisplay=self.storyFont.render(strOne,1,(0,0,255))
            screen.blit(pokemonListDisplay,(150, self.height-(self.height//14)))

            name=self.cenFont.render(self.user.PID,1,(0,0,0))
            nameCen=name.get_rect(center=(120,self.height//24))
            screen.blit(name,nameCen)

        #STAGE THREE
        elif self.stageThree==True:
            self.obstacleGroup.draw(screen) #obstacles
            self.userGroup.draw(screen) #user
            self.otherPlayerGroup.draw(screen)
            self.enemyGroup.draw(screen) #enemies
            
            self.menu = pygame.transform.scale(pygame.image.load('Images/menu.png').convert_alpha(),(1200,100))
            screen.blit(self.menu, (0,self.height-100))
            scoreDisplay=self.storyFont.render('Stolen: %d'%(self.score),1,(0,0,255))
            scoreDisplayCen=scoreDisplay.get_rect(center=(self.width-(self.width//10),self.height-(self.height//12)))
            screen.blit(scoreDisplay,scoreDisplayCen)
            if len(self.otherPlayerGroup)>0:
                otherPokeDisplay=self.storyFont.render('%s PokeCount: %d'%(self.otherPlayer.PID,self.otherPlayer.numPokemon),1,(0,0,255))
                otherPokeDisplayCen=otherPokeDisplay.get_rect(center=(self.width-(self.width//6),self.height-(self.height//24)))
                screen.blit(otherPokeDisplay,otherPokeDisplayCen)

            timer=self.timeFont.render('Time Left: '+ str(self.stageThreeCounter-int(time.time()-self.stageThreeCounterTimer)),1,(0,0,255))
            timerCen=timer.get_rect(center=(self.width//2,self.height-(self.height//12)))
            screen.blit(timer,timerCen)

            pokemonDisplay=self.storyFont.render('Pokemon:',1,(0,0,255))
            pokemonDisplayCen=pokemonDisplay.get_rect(center=(0+(self.width//11),self.height-(self.height//12)))
            screen.blit(pokemonDisplay,pokemonDisplayCen)
            strTwo=''
            for elem in self.pokemonList:
                strTwo+='%s, '%(elem)
            strTwo=strTwo[0:-2]
            pokemonListDisplay=self.storyFont.render(strTwo,1,(0,0,255))
            screen.blit(pokemonListDisplay,(150, self.height-(self.height//14)))

            name=self.cenFont.render(self.user.PID,1,(0,0,0))
            nameCen=name.get_rect(center=(120,self.height//24))
            screen.blit(name,nameCen)

        #WINNING AND LOSING SCREEN
        elif self.won==True:
            if len(self.otherPlayerGroup)>0:
                if self.user.numPokemon>self.otherPlayer.numPokemon:
                    self.whoWon=self.user.PID
                    screen.blit(pygame.transform.scale(pygame.image.load('Images/whoWon.png').convert_alpha(),(1200,800)),(0,0))
                    whoWonDisplay=self.cenFont.render('%s (You!)'%(self.whoWon),1,(0,0,255))
                    whoWonDisplayCen=whoWonDisplay.get_rect(center=(self.width//2,125))
                    screen.blit(whoWonDisplay,whoWonDisplayCen)
                    
                    yourScore=self.cenFont.render('Your PokeCount: %d'%self.user.numPokemon,1,(0,0,255))
                    yourScoreCen=yourScore.get_rect(center=(self.width//3,2*self.height//3-20))
                    screen.blit(yourScore, yourScoreCen)
                    
                    theirScore=self.cenFont.render('Opponent PokeCount: %d'%self.otherPlayer.numPokemon,1,(0,0,255))
                    theirScoreCen=theirScore.get_rect(center=(self.width//3,2*self.height//3+20))
                    screen.blit(theirScore, theirScoreCen)

                    scoreboard=self.storyFont.render('Press -space- to enter your andrewID and view recent scores!',1,(0,0,255))
                    scoreboardCen=scoreboard.get_rect(center=(self.width//2,self.height-40))
                    screen.blit(scoreboard, scoreboardCen)
                
                if self.user.numPokemon<self.otherPlayer.numPokemon:
                    self.whoWon=self.otherPlayer.PID
                    screen.blit(pygame.transform.scale(pygame.image.load('Images/whoWon.png').convert_alpha(),(1200,800)),(0,0))
                    whoWonDisplay=self.cenFont.render('%s (Opponent)'%(self.whoWon),1,(0,0,255))
                    whoWonDisplayCen=whoWonDisplay.get_rect(center=(self.width//2,125))
                    screen.blit(whoWonDisplay,whoWonDisplayCen)
                    
                    yourScore=self.cenFont.render('Your PokeCount: %d'%self.user.numPokemon,1,(0,0,255))
                    yourScoreCen=yourScore.get_rect(center=(self.width//3,2*self.height//3-20))
                    screen.blit(yourScore, yourScoreCen)
                    
                    theirScore=self.cenFont.render('Opponent PokeCount: %d'%self.otherPlayer.numPokemon,1,(0,0,255))
                    theirScoreCen=theirScore.get_rect(center=(self.width//3,2*self.height//3+20))
                    screen.blit(theirScore, theirScoreCen)

                    scoreboard=self.storyFont.render('Press -space- to enter your andrewID and view recent scores!',1,(0,0,255))
                    scoreboardCen=scoreboard.get_rect(center=(self.width//2,self.height-40))
                    screen.blit(scoreboard, scoreboardCen)
                
                if self.user.numPokemon==self.otherPlayer.numPokemon:
                    screen.blit(pygame.transform.scale(pygame.image.load('Images/tie.png').convert_alpha(),(1200,800)),(0,0))

                    yourScore=self.cenFont.render('Your PokeCount: %d'%self.user.numPokemon,1,(0,0,255))
                    yourScoreCen=yourScore.get_rect(center=(self.width//3,2*self.height//3-20))
                    screen.blit(yourScore, yourScoreCen)
                    
                    theirScore=self.cenFont.render('Opponent PokeCount: %d'%self.otherPlayer.numPokemon,1,(0,0,255))
                    theirScoreCen=theirScore.get_rect(center=(self.width//3,2*self.height//3+20))
                    screen.blit(theirScore, theirScoreCen)

                    scoreboard=self.storyFont.render('Press -space- to enter your andrewID and view recent scores!',1,(0,0,255))
                    scoreboardCen=scoreboard.get_rect(center=(self.width//2,self.height-40))
                    screen.blit(scoreboard, scoreboardCen)
            else:
                screen.blit(pygame.transform.scale(pygame.image.load('Images/won.png').convert_alpha(),(1200,800)),(0,0))
                
                scoreboard=self.storyFont.render('Press -space- and enter your andrewID to view recent scores!',1,(0,0,255))
                scoreboardCen=scoreboard.get_rect(center=(self.width//2,self.height-40))
                screen.blit(scoreboard, scoreboardCen)

        elif self.lost==True:
            screen.blit(pygame.transform.scale(pygame.image.load('Images/lost.png').convert_alpha(),(1200,800)),(0,0))

        elif self.fail==True:
            screen.blit(pygame.transform.scale(pygame.image.load('Images/fail.png').convert_alpha(),(1200,800)),(0,0))


        elif self.enterName==True:
            screen.blit(pygame.transform.scale(pygame.image.load('Images/pokegrass.png').convert_alpha(),(1200,800)),(0,0))
            screen.blit(pygame.transform.scale(pygame.image.load('Images/menu.png').convert_alpha(),(400,100)),(400,350))
            
            title=self.cenFont.render('Enter Your AndrewID (Lowercase):',1,(0,0,255))
            titleCen=title.get_rect(center=(self.width//2, 50))
            screen.blit(title,titleCen)

            name=self.storyFont.render(self.user.andrewID+'_',1,(0,0,0))
            nameCen=name.get_rect(center=(self.width//2,self.height//2))
            screen.blit(name, nameCen)

            done=self.storyFont.render('press enter when finished',1,(0,0,255))
            doneCen=done.get_rect(center=(self.width//2,self.height-40))
            screen.blit(done, doneCen)
        
        elif self.scores==True:
            screen.blit(pygame.transform.scale(pygame.image.load('Images/pokegrass.png').convert_alpha(),(1200,800)),(0,0))
            scores=self.makeScores() #creates lists of scores
            formatted=[]
            for val in scores: #gets rid of \n characters
                if val=='\n':
                    continue
                else:
                    colonIndex=val.index(':')
                    val=val[0:colonIndex] +'     had a PokeCount of     ' + val[colonIndex+1:]
                    formatted.append(val[:-1])
            scores=formatted

            
            title=self.cenFont.render('Most Recent Scores:',1,(0,0,255))
            titleCen=title.get_rect(center=(self.width//2, 50))
            screen.blit(title,titleCen)
            if len(scores)<10: #if less than 10 scores, show all of them (prevents index out of range for next loop)
                for i in range(len(scores)):
                    score=self.cenFont.render(scores[i],1,(0,0,255))
                    scoreCen=score.get_rect(center=(self.width//2,200+(50*i)))
                    screen.blit(score,scoreCen)
            else:
                for i in range(10): #most recent 10 scores and andrew ID's
                    score=self.cenFont.render(scores[i],1,(0,0,255))
                    scoreCen=score.get_rect(center=(self.width//2,200+(50*i)))
                    screen.blit(score,scoreCen)

            quit=self.storyFont.render('close window to finish',1,(0,0,255))
            quitCen=quit.get_rect(center=(self.width//2,self.height-40))
            screen.blit(quit, quitCen)


#creating and running the game
serverMsg= Queue(100)
threading.Thread(target= handleServerMsg, args= (server,serverMsg)).start()
game = pokeRescue()
game.run(serverMsg,server)