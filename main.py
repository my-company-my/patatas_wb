# Show loading text
cidk = textsprite.create("Cargando")
pause(1)
music.play(music.create_song(assets.song("""title""")),music.PlaybackMode.LOOPING_IN_BACKGROUND)

# Ask level
if controller.A.is_pressed():
    nivel = -1
else:
    nivel = game.ask_for_number("¿Cual nivel?", 1)
# Example: Detect left/right wall collision for "player" sprite

def itws(sprite: Sprite, k: number) -> bool:
    # Get sprite position in tile coordinates
    col = sprite.x // 16
    row = sprite.y // 16

    # Check left tile
    left_tile = tiles.get_tile_location(col - 1, row)
    if (k==0 and tiles.tile_at_location_equals(left_tile, assets.tile("ce"))) or (k==1 and tiles.tile_at_location_equals(left_tile, assets.tile("st"))):
        return True

    # Check right tile
    right_tile = tiles.get_tile_location(col + 1, row)
    if (k==0 and tiles.tile_at_location_equals(right_tile, assets.tile("ce"))) or (k==1 and tiles.tile_at_location_equals(right_tile, assets.tile("st"))):        return True

    return False

music.stop_all_sounds()

# Load tilemap
if nivel == 1:
    tiles.set_current_tilemap(tilemap("""
        nivel1
    """))
    ls = 13  # coins/lives
    rc = 24  # timer
    psm = [30]
    music.play(music.create_song(assets.song("""back1""")),music.PlaybackMode.LOOPING_IN_BACKGROUND)
elif nivel == 2:
    tiles.set_current_tilemap(tilemap("""
        nivel2
    """))
    ls = 13  # coins/lives
    rc = 25  # timer
    psm = [30]
    music.play(music.create_song(assets.song("""back2""")),music.PlaybackMode.LOOPING_IN_BACKGROUND)

elif nivel == 3:
    tiles.set_current_tilemap(tilemap("""
        nivel0
    """))
    ls = 6  # coins/lives
    rc = 24  # timer
    music.play(music.create_song(assets.song("""back3""")),music.PlaybackMode.LOOPING_IN_BACKGROUND)


elif nivel == 4:
    tiles.set_current_tilemap(tilemap("""
        nivel10
    """)) # 6
    ls = 4  # coins/lives 2
    rc = 40  # timer 15
    psm = [-50,-50,-50,-50,-50,-50,-50,-50]
    music.play(music.create_song(assets.song("""back4""")),music.PlaybackMode.LOOPING_IN_BACKGROUND)

elif nivel == 5:
    tiles.set_current_tilemap(tilemap("""nivel8"""))
    ls = 3
    psm = [-30, 50, 70, 90, 110, 30, 150, 170,100,300,500]
    rc = 40
elif nivel == 9:
    tiles.set_current_tilemap(tilemap("""
        test
    """))
    ls = 3  # coins/lives
    rc = 9999  # timer
    psm = [30, 40, 50, 60]
    #psm = [300,300,300,1000]
else:
    game.splash("Nivel no válido")
    game.reset()

pause(1)

# UI
timercount = textsprite.create(str(rc))
patatacount = textsprite.create(str(ls))
timercount.set_outline(1, 6)
patatacount.set_outline(1, 6)

# Game state
rscoins_ins: List[Sprite] = []
enmyss_ins: List[Sprite] = []
enmyssg1_ins: List[Sprite] = []

    



        
isj = False  # is jumping

def load1():
    ins_tile = assets.tile("""
        ins
    """)
    if nivel == -1 or nivel == 1 or nivel == 3 or nivel == 5:
        sb_tile = assets.tile("sb")
    else:
        sb_tile = assets.tile("sb0")

    floor_tile1 = assets.tile("""
        ce
    """)
    floor_tile2 = assets.tile("""
        flbasic
    """)
    enmy_tile1 = assets.tile("""e1""")
    enmy_tile2 = assets.tile("""e2""")

    # Place coins
    ins_locations = tiles.get_tiles_by_type(ins_tile)
    enmy1_locations = tiles.get_tiles_by_type(enmy_tile1)
    enmy2_locations = tiles.get_tiles_by_type(enmy_tile2)
    for loc1 in ins_locations:
        tiles.set_tile_at(loc1, sb_tile)
        coin = sprites.create(assets.image("rscoin"), SpriteKind.food)
        rscoins_ins.append(coin)
        tiles.place_on_tile(coin, loc1)
        pause(1)

    for loc2 in enmy1_locations:
        tiles.set_tile_at(loc2, sb_tile)
        enmyns = sprites.create(assets.image("se1"), SpriteKind.enemy)
        enmyns.ay = 30
        enmyss_ins.append(enmyns)
        tiles.place_on_tile(enmyns, loc2)
        pause(1)

    for loc3 in enmy2_locations:
        tiles.set_tile_at(loc3, sb_tile)
        enmyns = sprites.create(assets.image("proy0"), SpriteKind.projectile)
        enmyssg1_ins.append(enmyns)
        tiles.place_on_tile(enmyns, loc3)
        pause(1)


load1()

# Create player
playersprite = sprites.create(assets.image("player"), SpriteKind.player)
playersprite.set_velocity(0, 0)
playersprite.ay = 300  # gravity
scene.camera_follow_sprite(playersprite)
sprites.destroy(cidk)

# Update UI with camera
def update_ui():
    while True:
        timercount.set_position(scene.camera_property(CameraProperty.X) - 68,
                                scene.camera_property(CameraProperty.Y) - 50)
        patatacount.set_position(scene.camera_property(CameraProperty.X) + 68,
                                 scene.camera_property(CameraProperty.Y) - 50)
        pause(50)
timer.background(update_ui)

# Movement and win logic
def controller_loop():
    global ls
    while True:
        if ls == 0:
            music.stop_all_sounds()
            music.play(music.create_song(assets.song("""win""")),music.PlaybackMode.IN_BACKGROUND)

            game.splash("Has ganao")
            game.reset()
        playersprite.vx = controller.dx(3750 if controller.B.is_pressed() else 2200)
        pause(10)
timer.background(controller_loop)

# Countdown timer
def countdown():
    global rc
    while True:
        pause(1000)
        rc -= 1
        timercount.set_text(str(rc))
        if rc < 0 and ls > 0:
            music.stop_all_sounds()
                        
            music.play(music.create_song(assets.song("""lose""")),music.PlaybackMode.IN_BACKGROUND)
            game.splash("Has perdido")
            

            game.reset()
timer.background(countdown)

def enmydel():
    ps = psm
    if ps == None:
        return
    xs = [0]
    while True:
        ce = 0
        pause(2000)
        for ei in enmyss_ins:
            ei.vx = ps[ce]
            if xs[ce] == ei.x:
                ei.vy = -30
            xs[ce] = ei.vy
            
            if itws(ei, 0):
                ps[ce] = -ps[ce]
                ei.vy = -30
            if Math.percent_chance(25) and ei.is_hitting_tile(CollisionDirection.BOTTOM):
                ei.vy = -30
def enmydel2():
    prs: List[Sprite] = []
    while True:
        pause(1000)
        sc = int(str(int(game.runtime())/1000))
        cgn = 0
        for gn in enmyssg1_ins:
            print(gn.x)
            if (sc % 2 == 0) == (int(str((gn.x-5)/16)) % 2 == 0):
                sprites.destroy(prs[cgn])
                prs[cgn] = sprites.create(assets.image("""proy"""), SpriteKind.enemy)
                prs[cgn].ay = 100
                prs[cgn].x = gn.x
                prs[cgn].y = gn.y
            cgn += 1

timer.background(enmydel)
timer.background(enmydel2)

# Collect coins
def collect_coins():
    global ls
    while True:
        for c in rscoins_ins:
            if playersprite.overlaps_with(c):
                sprites.destroy(c)
                rscoins_ins.remove_at(rscoins_ins.index_of(c))
                ls -= 1
                patatacount.set_text(str(ls))
                music.play(music.create_sound_effect(WaveShape.NOISE,
                                                     1038, 1286, 255, 0, 500,
                                                     SoundExpressionEffect.VIBRATO,
                                                     InterpolationCurve.LOGARITHMIC),
                           music.PlaybackMode.IN_BACKGROUND)
        pause(20)
timer.background(collect_coins)
def on_overlap(sprite, otherSprite):
    
    music.stop_all_sounds()
    music.play(music.create_song(assets.song("""lose""")),music.PlaybackMode.IN_BACKGROUND)
    game.splash("Has perdido")
    game.reset()
sprites.on_overlap(SpriteKind.player, SpriteKind.enemy, on_overlap)
# Check if on ground using tile collision
def check_ground():
    global isj
    while True:
        isj = playersprite.is_hitting_tile(CollisionDirection.BOTTOM) or itws(playersprite, 1)
        pause(10)
        if isj == False:
            p = playersprite.x
            while playersprite.x == p and not playersprite.is_hitting_tile(CollisionDirection.BOTTOM):
                pause(1)
                
            isj = True

timer.background(check_ground)

# Jump logic using gravity
def jump_loop():
    global isj
    while True:
        if controller.A.is_pressed() and isj:
            isj = False
            music.play(music.create_sound_effect(WaveShape.SINE,
                                                 500, 600, 255, 0, 500,
                                                 SoundExpressionEffect.NONE,
                                                 InterpolationCurve.LINEAR),
                       music.PlaybackMode.IN_BACKGROUND)
            playersprite.vy = -175 if controller.B.is_pressed() else -150
        pause(1)
timer.background(jump_loop)
