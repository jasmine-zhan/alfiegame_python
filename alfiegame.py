import pygame, sys, random
#sys gives access to system modules

def draw_floor(): #draws the base and positions it
   screen.blit(floor_surface, (floor_x_pos, 720))
   screen.blit(floor_surface, (floor_x_pos + 700, 720))

def create_ice():
   random_ice_pos = random.choice(ice_height) #picks random height from list
   # adds rectangle and places on screen and creates top and bottom icicles
   bottom_ice = ice_surface.get_rect(midtop=(800, random_ice_pos))
   top_ice = ice_surface.get_rect(midbottom=(800, random_ice_pos - 375))
   return bottom_ice, top_ice

#moves icicles every second to create moving animation (takes all the icicle rectangles and moves left)
def move_ices(ices):
   for ice in ices:
       ice.centerx -= 5
   visible_ices = [ice for ice in ices if ice.right > -50]
   return visible_ices #returns new list

#draws all the icicles
def draw_ices(ices):
   for ice in ices:
       if ice.bottom >= 900: #icicle is on bottom
           screen.blit(ice_surface, ice)
       else: #so when its on the top, we flip it so the images look better
           flip_ice = pygame.transform.flip(ice_surface, False, True) #only flips in y direction(x is false)
           screen.blit(flip_ice, ice)

#function checking for collisions between alfie and the icicles
def check_collision(ices):
   global can_score
   for ice in ices: #all icicles
       if alf_rect.colliderect(ice): #if alphie's rectangle collides with the icicles rectangle:
           death_sound.play()
           can_score = True
           return False #game over if triggered
   #checking if alphie is out of bounds
   if alf_rect.top <= -75 or alf_rect.bottom >= 750:
       can_score = True
       return False #game over if triggered

   return True #or else game still active

#rotating to create flying animation
#rotozoom is pygames rotate function, it can scale and rotate surface, only used rotate
def rotate_alf(alf):
   new_alf = pygame.transform.rotozoom(alf, -alf_movement * 3, 1) #rotates to an angle relative to opposite of alfie movement so when he down down there is a positive rotation, scale is third argument so its just 1
   return new_alf #updates position

def alf_animation(): #switches between frames to create animation and helps make it look like theres lights flashing on the ship
   new_alf = alf_frames[alf_index]
   new_alf_rect = new_alf.get_rect(center=(100, alf_rect.centery)) #positions new frame
   return new_alf, new_alf_rect

#function to show score depending on game's state
def score_display(game_state):
   if game_state == 'main_game':
       score_surface = game_font.render(str(int(score)), True, (255, 255, 255)) #renders text and displays score as integer, colours
       score_rect = score_surface.get_rect(center=(350, 70)) #positions score on the screen
       screen.blit(score_surface, score_rect) #draws the score to put it on the screen

   #draws current score and highsore when game is over
   if game_state == 'game_over':
       #displays score
       score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255)) #f string combines string and other variables in bracket
       score_rect = score_surface.get_rect(center=(350, 60)) #position
       screen.blit(score_surface, score_rect)
       #displays highscore
       high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
       high_score_rect = high_score_surface.get_rect(center=(350, 110)) #position
       screen.blit(high_score_surface, high_score_rect)

#updates highscore
def update_score(score, high_score):
   if score > high_score:
       high_score = score
   return high_score

def ice_score_check():
   global score, can_score

   if ice_list:
       for ice in ice_list: #when the icicle is in this position, it means that alfie has past it and the score can go up
           if 95 < ice.centerx < 105 and can_score:
               score += 1
               score_sound.play()
               can_score = False
           if ice.centerx < 0:
               can_score = True

#initializing game
pygame.init()
screen = pygame.display.set_mode((700, 750)) #size
#determines speed at which the game run/framerate
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19__.TTF', 50) #imports the font style that will be used and the size of it

# Game Variables
gravity = 0.25 #makes alfie fall down
alf_movement = 0 #used to move alfie
#these are the defaults
game_active = True
score = 0
high_score = 0
can_score = True
#importing background surface/.convert helps it run at more consistent speeds for when the game is running
bg_surface = pygame.image.load('background.png').convert()
# scaling the background image: it overrides the previous size
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('base.png').convert_alpha()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

#importing images for flying animation
#.convert alpha gets rid of the black square that was around alfie
alf_down = pygame.transform.scale2x(pygame.image.load('alfiedown.png').convert_alpha())
alf_mid = pygame.transform.scale2x(pygame.image.load('alfieinspaceship.png').convert_alpha())
alf_up = pygame.transform.scale2x(pygame.image.load('alfieup.png').convert_alpha())
#compiles images into list
alf_frames = [alf_down, alf_mid, alf_up]
alf_index = 0 #used to pick image from list
# turns alfie's surface into rectangle around it
alf_surface = alf_frames[alf_index] #picks item from list
alf_rect = alf_surface.get_rect(center=(100, 512)) #center of alfie is at that point

ALF = pygame.USEREVENT + 1 #new event
pygame.time.set_timer(ALF, 200) #changes index every 200 miliseconds

# alf_surface = pygame.image.load('alfieinspaceship.png').convert_alpha()
# alf_surface = pygame.transform.scale2x(alf_surface)
# alf_rect = alf_surface.get_rect(center = (100,512))

#making icicles
ice_surface = pygame.image.load('icicle.png') #import image
ice_surface = pygame.transform.scale2x(ice_surface) #scaling image
ice_list = [] # makes list
SPAWNICE = pygame.USEREVENT #variable to create obstacle
pygame.time.set_timer(SPAWNICE, 1200) #creates icicle every 1200 miliseconds
ice_height = [200, 400, 500, 600, 700, 800] #possible heights of icicles that will be used

game_over_surface = pygame.transform.scale2x(pygame.image.load('message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(350, 350))

#sounds
fly_sound = pygame.mixer.Sound('Rising_putter.ogg')
death_sound = pygame.mixer.Sound('Falling_putter.ogg')
score_sound = pygame.mixer.Sound('Bag-of-Coins-A-www.fesliyanstudios.com.mp3')
pygame.mixer.music.load("Elevator Music - Vanoss Gaming Background Music (HD).mp3")
pygame.mixer.music.play(loops=-1)
score_sound_countdown = 100
SCOREEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SCOREEVENT, 100)


#game loop
while True:
   for event in pygame.event.get():
       # uninitializing game
       if event.type == pygame.QUIT: #checks if user closes game
           pygame.quit()
           #shuts down game completely
           sys.exit()
       if event.type == pygame.KEYDOWN: #checks for keyboard input
           if event.key == pygame.K_SPACE and game_active: #checks for specific key when game is running
               alf_movement = 0 #disables effects of gravity before alfie flies up
               alf_movement -= 7 #moves alfie up when space pressed
               fly_sound.play()

           #restarting the game
           if event.key == pygame.K_SPACE and game_active == False: #if the space key is pressed and the game is not active
               game_active = True #then the game becomes running
               #when the game is over the his and ice are still in same position, following resets this
               ice_list.clear() #clears the ice list
               alf_rect.center = (100, 512) #repositions alphie
               alf_movement = 0 #resets his movement
               score = 0 #score erases to zero

       # when event is triggered, a new icicle is created and added to the list
       if event.type == SPAWNICE:
           ice_list.extend(create_ice()) #extend is used because the list is returning 2 VARIABLES, TOP AND BOTTOM ICICLE

       if event.type == ALF:
           # sets list back to 0 when its about to get greater than 2
           if alf_index < 2:
               alf_index += 1
           else:
               alf_index = 0

           alf_surface, alf_rect = alf_animation()

   #adds to display surface so user can see it(image, position)- origin is on top left
   screen.blit(bg_surface, (0, 0))

   #following will only run when game is still running
   if game_active:
       # alfie
       alf_movement += gravity
       rotated_alf = rotate_alf(alf_surface) #2surfaces to improve quality alphie's flying motion
       alf_rect.centery += alf_movement #only moves alfie up and down (only changing y coordinate)
       screen.blit(rotated_alf, alf_rect)
       game_active = check_collision(ice_list) #stores in game active variable

       #icicles
       ice_list = move_ices(ice_list) #takes all icicles, moves them and then makes new list
       draw_ices(ice_list) #draws

       # Score
       #only shows current score when game is active
       ice_score_check()
       score_display('main_game')
   else:
       #scores
       screen.blit(game_over_surface, game_over_rect)
       high_score = update_score(score, high_score)
       score_display('game_over')

   # moving the floor: moves right by one each time surface is re-drawn
   floor_x_pos -= 1
   draw_floor()
   # moves floor back to were it started when it goes too far left
   if floor_x_pos <= -700:
       floor_x_pos = 0

   pygame.display.update()
   #cant go past 120 frames per second
   clock.tick(120)

#stops when game is closed
pygame.mixer.music.stop()
pygame.mixer.quit()
