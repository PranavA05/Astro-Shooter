import pygame
from random import randint, uniform
from os.path import join
'''player_dir.x=int(keys[pygame.K_d]-keys[pygame.K_a]) # this works as this gives boolean values 1 and 0 as true and false
    player_dir.y=int(keys[pygame.K_s]-keys[pygame.K_w])
    player_dir=player_dir.normalize() if player_dir else player_dir # this is done so that when we move diagonally the speed doesn't increase then intended 
    player_rect.center+=player_dir*player_speed*dt'''
class Player(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.image=pygame.image.load('images/player.png').convert_alpha()
        self.rect=self.image.get_frect(center=(w/2, h/2))
        self.dir=pygame.Vector2()
        self.speed=300 
    # cooldown  
        self.can_shoot=True
        self.laser_shoot_time=0
        self.cooldown_duration=400
        self.spawn_met=True
        self.spawn_dur=2000
    # mask
        self.mask=pygame.mask.from_surface(self.image) # masks allow pixel perfect collisions

    def laser_timer(self):
        if not self.can_shoot:
            curr_time=pygame.time.get_ticks()
            if curr_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot=True
    

    def update(self,dt):
        keys=pygame.key.get_pressed()
        self.dir.x=int(keys[pygame.K_d]-keys[pygame.K_a])
        self.dir.y=int(keys[pygame.K_s]-keys[pygame.K_w])
        self.dir+=self.dir.normalize() if self.dir else self.dir
        self.rect.center+=self.dir*self.speed*dt
        rec_keys=pygame.key.get_just_pressed()
        if rec_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf,self.rect.midtop,(all_sprites,laser_sprites))
            self.can_shoot=False
            self.laser_shoot_time=pygame.time.get_ticks()
            laser_sound.play()
    
        self.laser_timer()
class Star(pygame.sprite.Sprite):
    def __init__(self,groups,surf):
        super().__init__(groups)
        self.image=surf  # This is done so that the stars don't change in every frame
        self.rect=self.image.get_frect(center=(randint(0,w),randint(0,h)))
class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)  
    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()
class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.orig=surf
        self.image = self.orig
        self.rect = self.image.get_frect(center=pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.dire = pygame.Vector2(uniform(-0.5,0.5), 1)  # Slightly adjusted range for more variety in direction
        self.speed = randint(400, 500)
        self.rotation=0
    def update(self, dt):
        self.rect.center += self.dire * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.rotation+=50*dt
        self.image=pygame.transform.rotozoom(self.orig,self.rotation,1)
        self.rect=self.image.get_frect(center=self.rect.center)
class Explosion(pygame.sprite.Sprite):
    def __init__(self,frames,pos,groups):
        global counter
        super().__init__(groups)
        self.frames=frames
        self.frame_index=0
        self.image=self.frames[self.frame_index]
        self.rect=self.image.get_frect(center=pos)
        exp_sound.play()                            # can also be placed in the collisions func
    def update(self,dt):
        self.frame_index +=30*dt
        if self.frame_index < len(self.frames):
            self.image=self.frames[int(self.frame_index)]
        else:
            self.kill()

def collisions():
    global running, asteroids_destroyed
    collision_sprites = pygame.sprite.spritecollide(player, met_sprites, True, pygame.sprite.collide_mask)
    if collision_sprites:
        running = False
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, met_sprites, True)
        if collided_sprites:
            laser.kill()
            Explosion(exp_frames, laser.rect.midtop, all_sprites)
            asteroids_destroyed += 1  # Increment the number of asteroids destroyed

def disp_score():
    text_surf = font.render(str(asteroids_destroyed), True, 'white')
    text_rect = text_surf.get_frect(midbottom=(w / 2, h - 50))
    display_surface.blit(text_surf, text_rect)
    #pygame.draw.rect(display_surface, 'white', text_rect.inflate(20, 16).move(0, -5), 5, 10)


# general setup
pygame.init()
w, h = 1280, 720
display_surface = pygame.display.set_mode((w, h))
pygame.display.set_caption('ASTRO SHOOTER') 
running = True
clock=pygame.time.Clock()
# import 
star_surf=pygame.image.load('images/star.png').convert_alpha()
meteor = pygame.image.load('images/meteor.png')
laser_surf = pygame.image.load('images/laser.png')
font =pygame.font.Font(join('images','Oxanium-Bold.ttf'),60)
exp_frames=[pygame.image.load(join('images','explosion',f'{i}.png')).convert_alpha() for i in range(21)]
laser_sound=pygame.mixer.Sound(join('audio','laser.wav'))
game_sound=pygame.mixer.Sound(join('audio','game_music.wav'))
exp_sound=pygame.mixer.Sound(join('audio','explosion.wav'))
game_sound.play()
# Sprites
all_sprites=pygame.sprite.Group()
met_sprites=pygame.sprite.Group()
laser_sprites=pygame.sprite.Group()

for i in range(20):
    Star(all_sprites,star_surf)
player=Player(all_sprites)

# meteor event -- > custom event
met_event=pygame.event.custom_type()
pygame.time.set_timer(met_event,500)
test_rect=pygame.FRect(0,0,300,600)
asteroids_destroyed=0

while running:
                                                                    #event loop | diff bw getting input via event loop and get.keys is that event loop just checks if the button is press ( so if if i hold 1 it only registers it as 1 and doesn't store any thing else, whereas get.keys checks if i released or not thus storing multiple 1s)
    dt=clock.tick()/1000                                            # delta time allows the same execution regardless of the computer's capability, also coz it's in ms s we divide by 1000 to get it in s
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == met_event:
            x,y=randint(0,w),randint(-200,-100)
            Meteor(meteor,(x,y),(all_sprites,met_sprites))
    #update
    all_sprites.update(dt)
    collisions()
    # draw the game
    display_surface.fill('#3a2e3f')
    all_sprites.draw(display_surface) 
    # TEST COLLISIONS
    #print(player.rect.colliderect(test_rect))
    disp_score()

    # draw test
    #pygame.draw.rect(display_surface,'white',(text_surf.rect,10,10))
    pygame.display.update()
pygame.quit()   
