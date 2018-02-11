'''
pokeServer.py
code originally taken from the Sockets optional lecture, but heavily edited (full credit given in comment below)

Purpose: 
  to run the server and create the game board for all clients
'''

#############################
# Sockets Server Demo
# by Rohan Varma
# adapted by Kyle Chin
#############################

import socket
import threading
import random
from queue import Queue
import pygame
from Obstacle import Obstacle
from Pokemon import Pokemon
from Pokeball import Pokeball
from Enemy import Enemy

HOST = "" # put your IP address here if playing on multiple computers
PORT = 8090
BACKLOG = 2

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)
print("looking for connection")

def handleClient(client, serverChannel, cID, clientele):
  client.setblocking(1)
  msg = ""
  while True:
    try:
      msg += client.recv(10).decode("UTF-8")
      command = msg.split("\n")
      while (len(command) > 1):
        readyMsg = command[0]
        msg = "\n".join(command[1:])
        serverChannel.put(str(cID) + " " + readyMsg)
        command = msg.split("\n")
    except:
      # we failed
      return

def serverThread(clientele, serverChannel):
  while True:
    msg = serverChannel.get(True, None)
    print("msg recv: ", msg)
    msgList = msg.split(" ")
    senderID = msgList[0]
    instruction = msgList[1]
    details = " ".join(msgList[2:])
    if (details != ""):
      for cID in clientele:
        if cID != senderID:
          sendMsg = instruction + " " + senderID + " " + details + "\n"
          clientele[cID].send(sendMsg.encode())
          print("> sent to %s:" % cID, sendMsg[:-1])
    print()
    serverChannel.task_done()





'''below initializes all randomness of game board for each game instance, but keeps them same for both players'''
obstacles=pygame.sprite.Group()
def makeObstacles():
  obstacleList=[]
  pygame.display.set_mode((1200, 800))
  Obstacle.init()
  for j in range(40):
      x1=random.randint(0,1200)
      y1=random.randint(0,800-150) #don't spawn under score rect
      if x1 in range(1200//2-50,1200//2+50): #don't want to spawn any obstacles in starting range of user
          continue
      if y1 in range(800//2-50,800//2+50): #don't want to spawn any obstacles in starting range of user
          continue
      j=Obstacle(x1,y1)
      obstacles.add(j)
  for obstacle in obstacles: #don't let obstacle overlap
      obstacles.remove(obstacle)
      if len(pygame.sprite.spritecollide(obstacle,obstacles,False))>0:
          obstacles.remove(obstacle)
      else: 
        obstacles.add(obstacle)
        obstacleList.append(str(obstacle.x)+'-'+str(obstacle.y)+'-'+str(obstacle.imageKey))
  return obstacleList
obstacleList=makeObstacles()


def makePokemon(obstacles):
  pokemon=pygame.sprite.Group()
  pokemonList=[]
  keyList=[]
  Pokemon.init()
  while len(pokemon)<8:
    x3=random.randint(0,1200)
    y3=random.randint(0,800-150) #don't spawn under score rect
    pokemon.add(Pokemon(x3,y3))
    if len(pygame.sprite.spritecollide(Pokemon(x3,y3),obstacles,False))>0:
      pokemon.remove(Pokemon(x3,y3))
  for i in pokemon:
    pokemonList.append(str(i.x)+'='+str(i.y)+'='+str(i.key)+'='+str(i.vX)+'='+str(i.vY)+'='+str(i.angleSpeed))
  return pokemonList
pokemonList=makePokemon(obstacles)


def makeEnemies():
  enemies=pygame.sprite.Group()
  enemyList=[]
  count=0
  Enemy.init()
  for l in range(10):
    x2=random.randint(0,1200)
    y2=random.randint(0,800-150) #don't spawn under score rect
    enemies.add(Enemy(x2,y2))
  for enemy in enemies:
    count+=1
    enemyList.append(str(enemy.x)+'='+str(enemy.y)+'='+str(enemy.vX)+'='+str(enemy.vY)+'='+str(enemy.angleSpeed))
  return enemyList
enemyList=makeEnemies()


def makePokeballs():
  pokeballs=pygame.sprite.Group()
  pokeballList=[]
  Pokeball.init()
  for i in range(10):
    x=random.randint(0,1200)
    y=random.randint(0,800-150) #don't spawn under score rect
    pokeballs.add(Pokeball(x,y))
    for pokeball in pokeballs: #don't let obstacle overlap
      pokeballs.remove(pokeball)
      if len(pygame.sprite.spritecollide(pokeball,obstacles,False))>0:
          pokeballs.remove(pokeball)
      else: 
        pokeballs.add(pokeball)
        pokeballList.append(str(pokeball.x)+'-'+str(pokeball.y)+'-'+str(pokeball.timeDuration))
  return pokeballList
pokeballList=makePokeballs()






'''below initializes/ handles all server messages and relevant data'''
clientele = dict()
playerNum = 0

serverChannel = Queue(100)
threading.Thread(target = serverThread, args = (clientele, serverChannel)).start()

names = ["PlayerOne", "PlayerTwo"]

while True:
  client, address = server.accept()
  # myID is the key to the client in the clientele dictionary
  myID = names[playerNum]
  print(myID, playerNum)
  for cID in clientele:
    print (repr(cID), repr(playerNum))
    clientele[cID].send(("newPlayer %s\n" % myID).encode())
    client.send(("newPlayer %s\n" % cID).encode())
  clientele[myID] = client
  client.send(("myIDis %s \n" % myID).encode())
  for obstacle in obstacleList:
    obstacle=obstacle.split('-')
    client.send(("obstacles %s %s %s\n" % (obstacle[0],obstacle[1],obstacle[2])).encode())
  for pokemon in pokemonList:
    pokemon=pokemon.split('=')
    client.send(("pokemon %s %s %s %s %s %s\n" % (pokemon[0],pokemon[1],pokemon[2],pokemon[3],pokemon[4],pokemon[5])).encode())
  for enemy in enemyList:
    enemy=enemy.split('=')
    client.send(("enemy %s %s %s %s %s\n" %(enemy[0],enemy[1],enemy[2],enemy[3],enemy[4])).encode())
  for pokeball in pokeballList:
    pokeball=pokeball.split('-')
    client.send(("pokeballs %s %s %s\n" % (pokeball[0],pokeball[1],pokeball[2])).encode())
  print("connection recieved from %s" % myID)
  threading.Thread(target = handleClient, args = 
                        (client ,serverChannel, myID, clientele)).start()
  playerNum += 1
