# When loading images via resources, pyglet does not like importing
# the level interactively, but importing in another script works fine
# use this script to check to see if you have any errors in your design.

# Prevent the creation of pyc files
import sys
sys.dont_write_bytecode = True

# Allow for importing a library by provideing the library name as a string
import imp

# load the level (Provide as an argument on the command line)
# example: python load-level.py level1
levelname = sys.argv[-1]
level = imp.load_source('happy',levelname+'.py')

# Provide some debugging, just to see:
print(str(['rows=',level.rows,'cols=',level.cols]))

# Other useful variables availabe to you from the level library:
#  level.rows <- number of rows in the world
#  level.cols <- number of columns in the world
#  level.level <- the terrain of the world
#  level.goals <- all of the goals in the world
#     Both stored as {row:col:image}
#  level.enemies <- the Location of all enemies on the board
#     Stored as {row:col:enemy_type}

#  level.playerStartRow <- row where the player *hero* will start
#  level.playerStartCol <- col where the player *hero* will start

#  level.background <- background image to use

#  level.music <- music file to play for the level

#  level.heroSoundFire <- sound to play when the hero fires their weapon
#  level.heroSoundAttack <- sound to play when the hero attacks
#  level.heroSoundWin <- sound to play when the hero wins the level
#  level.heroSoundJump <- sound to play when the hero jumps
#  level.heroSoundDeath <- sound to play when the hero dies
#  level.enemySoundDeath <- sound to play when an enemy dies

#  level.tilepath <- location of the tile images
#  level.goalpath <- location of the goal images
