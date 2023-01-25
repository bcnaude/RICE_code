# implementation of Spaceship - RiceRocks
# Copy and paste this code into the CodeSkulptor editor at https://py2.codeskulptor.org/ to run.

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False
flag = 1

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim


# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_brown.png")
debris2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_brown.png")
nebula2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")
missile2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_brown.png")
asteroid2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
meteor_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blend.png")
# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def change_environment():
    global nebula_image, debris_image, asteroid_image, missile_image, flag
    flag = flag * -1
    if flag == 1:
        nebula_image = nebula1
        debris_image = debris1
        asteroid_image = asteroid1
        missile_image = missile1
    else:
        nebula_image = nebula2
        debris_image = debris2
        asteroid_image = asteroid2
        missile_image = missile2
        
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
   
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        if self.animated:
            explosion_index = [self.age % self.image_size[0], (self.age // self.image_size[0]) % self.image_size[1]]
            canvas.draw_image(self.image,
                              [self.image_center[0] + explosion_index[0] * self.image_size[0],
                               self.image_center[1] + explosion_index[1] * self.image_size[1]],
                               self.image_size, self.pos, self.image_size, self.angle)
              
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                              self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
 
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        self.age += 1
        if self.age > self.lifespan:
            return True
        else:
            return False
        
  
    def collide(self, other_object):
        if dist(self.pos, other_object.pos) < (self.radius + other_object.radius):
            print "Collision detected!"
            return True  
        else:
            return False
           
        
# key handlers to control ship   
def keydown(key):
    if started:
        if key == simplegui.KEY_MAP['left']:
            my_ship.decrement_angle_vel()
        elif key == simplegui.KEY_MAP['right']:
            my_ship.increment_angle_vel()
        elif key == simplegui.KEY_MAP['up']:
            my_ship.set_thrust(True)
        elif key == simplegui.KEY_MAP['space']:
            missile_spawner()
        
def keyup(key):
    if started:
        if key == simplegui.KEY_MAP['left']:
            my_ship.increment_angle_vel()
        elif key == simplegui.KEY_MAP['right']:
            my_ship.decrement_angle_vel()
        elif key == simplegui.KEY_MAP['up']:
            my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        soundtrack_player()
        lives = 3
        score = 0
        change_environment()           

def draw(canvas):
    global time, started, rock_group, missile_group, explosion_group, meteor_group, lives, score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")

    # draw and update ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    
    if started:
                
        process_sprite_group(rock_group, canvas)
        process_sprite_group(missile_group, canvas)
        process_sprite_group(explosion_group, canvas)
        process_sprite_group(meteor_group, canvas)
        
       
        # check for collision
        if group_collide(rock_group, my_ship) or group_collide(meteor_group, my_ship):
            lives -= 1
            
        if lives == 0:
            # reset game
            started = False
            rock_group = set([])
            missile_group = set([])
            explosion_group = set([])
            meteor_group = set([])
            my_ship.set_thrust(False)
            my_ship.angle_vel = 0
                    
        if group_group_collide(rock_group, missile_group) or group_group_collide(meteor_group, missile_group):
            score += 1
        
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

# helper functions        
def process_sprite_group(sprite_group, canvas):
    for sprite in list(sprite_group):
        sprite.draw(canvas)
        sprite.update()
        if sprite.update():
           sprite_group.discard(sprite)
        
def group_collide(group1, group2):  
    for item in list(group1):
        if item.collide(group2):
            an_explosion = Sprite(item.pos, (0, 0), 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(an_explosion)
            group1.remove(item)
            
            return True
            
def group_group_collide(group1, group2):
    for item in list(group1):
        if group_collide(group2, item):
            group1.discard(item)
            return True
        
        
change_environment()
    
# spawner functions   
def rock_spawner():
    if started:
        global rock_group
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
        rock_avel = random.random() * .2 - .1
        if len(rock_group) < 12:
            a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info)
            if a_rock.collide(my_ship):
                print "Rock spawn collision detected! Discarding rock."
                pass
            else:
                rock_group.add(a_rock)
        
def missile_spawner():
    global missile_group
    a_missile = Sprite([my_ship.pos[0] + (angle_to_vector(my_ship.angle)[0] * my_ship.radius), my_ship.pos[1] + (angle_to_vector(my_ship.angle)[1] * my_ship.radius) ],
                        [my_ship.vel[0] + angle_to_vector(my_ship.angle)[0] * 5, my_ship.vel[1] + angle_to_vector(my_ship.angle)[1] * 5], 
                        0, 0, missile_image, missile_info, missile_sound) 
    missile_group.add(a_missile)

def meteor_spawner():
    if started:
        global meteor_group
        meteor_pos = [random.randrange(0, WIDTH), 0]
        meteor_vel = [2,2]
        meteor_avel = random.random() * .2 - .1
        a_meteor = Sprite(meteor_pos, meteor_vel, 0, meteor_avel, meteor_image, asteroid_info)
        meteor_group.add(a_meteor)        
               
    
def soundtrack_player():
    soundtrack.rewind()
    soundtrack.play()

        
# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])
meteor_group = set ([])

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1300.0, rock_spawner)
soundtrack_timer = simplegui.create_timer(185000.0, soundtrack_player)
meteor_timer = simplegui.create_timer(20000.0, meteor_spawner)
# get things rolling
timer.start()
soundtrack_timer.start()
meteor_timer.start()
frame.start()
