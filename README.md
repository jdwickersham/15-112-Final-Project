# 15-112-Final-Project
View the demo-video.txt file for a visual demonstration submitted for the Term Project.


Welcome to PokeRescue!

PokeRescue is a pygame based single or 2 player game that operates using sockets. It intuits which ‘mode’ you are playing based on how many people join the server (1 or 2). It utilizes a web scraping and caching algorithm to store images and retain information for gameplay, so be sure not to delete any image folders, unless told to directly below. Each player starts with the same randomized game board, but is playing the game in parallel. While you will see the other user moving across your screen, this is simply to allow you to “spy” on them. They won’t interfere with your game play. Each user is essentially playing their own game, meaning one’s loss won’t affect another’s status (if player one loses in stage two, the other player can still continue to stage three). Final results are compared. You will also be able to see how many Pokemon the other person has caught/ is catching on the doc, along with relevant values for your own game and the countdown timer. At the end of the game, if you win, you will be able to enter your AndrewID and view the 10 most recent scores added.



Controls:

The arrow keys are used to move the player and mouse presses are used to throw poke balls towards that point on the screen. Press the space bar to move past the instruction page when launching the game. The instructions are essentially the same as the ones under Game Play and Controls.



Game Play:

“Professor Oak is on his infamous quest to study all Pokémon, but he has run into a serious problem. Team Rocket has managed to steal the Pokémon he had with him, leaving him defenseless against their leader. Prof. Oak needs you to deliver (3) Pokémon to him so he can continue his work!”

Your goal as a user is to complete all three game stages and finish with 3 Pokemon.

First, you must navigate around obstacles and collect poke balls by colliding with them. Each poke ball has a timer, so be sure to get to it before its timer runs outs. Poke balls will spawn both at the beginning and throughout the round. There is 20 seconds in this round.

Second, you must catch Pokemon by throwing poke balls at them. To do so, click the screen where you want the poke ball to go. The stage ends when all poke balls have been thrown. Some Pokemon will move across the screen and others will be panicked near obstacles, for varied level of difficulty. Pokemon also move at different speeds based on rarity.

Third, you must avoid the same Team Rocket enemies that stole from professor oak! Team Rocket has special tools to scale over obstacles, so you cannot rely on hiding behind them. They also have the potential to change speeds. If they collide with you, they will steal a random Pokemon from you, which you will see reflected in your doc and you will see a poke ball in the arm of the enemy. Note: each enemy can only take one Pokemon from you. There is 20 seconds in this round.



Winning/Losing:

You lose if you have less than three Pokemon at any point during stage three, do not have enough pokemon to enter stage three, or do not have any poke balls with which to enter stage two.
You win if you finish with more than three Pokemon, and in multiplayer you can beat the other player by having more Pokemon than them. In the case that both players win their own games, once both have done so, the final winner’s ID will be displayed.



Get Started/ Special Notes:

The user must have Chrome on their OS device as well as the following programs/ libraries in order to run the game/web scraper/caching systems:
pygame, standard python libraries, PokeRescue game files, json, bs4, selenium, PIL, base 64, os.path
The font that is included in the Images folder must be downloaded onto the computer’s font library.

The computer that will act as the server must retrieve their public IP address and put in the marked HOST spots at the top of both the PokeServer.py file and the PokeRescue.py file (across all computers). Only one computer needs to initialize the server by running the file.

If only one person is playing the game, then they should keep the HOST string empty. The provided port should work, but another value can be used if kept consistent across all users.

In the Images folder, there is a subfolder called Pokemon. This folder will store all cached photos from the web scraper. This folder can be emptied to save space on your computer, but the folder itself cannot be deleted.
