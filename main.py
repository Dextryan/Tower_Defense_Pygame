import re
import pygame as pg
import colors
from objects.bloon import Bloon

GRASS_GREEN = colors.forestgreen
YELLOW = colors.yellow
BLACK = colors.black
WHITE = colors.white
GREEN = colors.green
PINK = colors.pink
BLUE = colors.blue
GRAY  = colors.gray
RED = colors.red

SIZE = (800, 600)
TILE = {'x': 50, 'y': 50}

def split_str(str):
    """
    Separes the numbers of the letters of a string
    Converts num to float and makes letters lowercase
    Returns a tuple (num, letter)
    Ex. '20n' -> (20, 'n')
    """
    _, num, ltt = re.split('(\d+(?:.\d+)?)', str)
    num = (float)(num)
    ltt = ltt.lower()
    return (num, ltt)

def rect_val(current_x, current_y, len, direction):
    """
    Defines how the rectangle that compose each path segment will be drawed
    """
    if direction == 'n':
        w = TILE['x']
        h = TILE['y']*len
        x = current_x
        y = current_y+TILE['y']-h    
    elif direction == 's':
        w = TILE['x']
        h = TILE['y']*len
        x = current_x
        y = current_y
        return(x, y, w, h)
    elif direction == 'e':
        w = TILE['x']*len
        h = TILE['y']
        x = current_x
        y = current_y 
    elif direction == 'w':
        w = TILE['x']*len
        h = TILE['y']
        x = current_x+TILE['x']-w
        y = current_y 
    return(x, y, w, h)

def refresh_x_y(start_x, start_y, length, direction):
    """
    Refresh the X and Y positions after the last path rectangle was drawed
    See draw_path() for more info
    """
    if direction == 'n':
        start_y -= length*TILE['y']
    elif direction == 's':
        start_y += length*TILE['y']
    elif direction == 'e':
        start_x += length*TILE['x']
    elif direction == 'w':
        start_x -= length*TILE['y']
    return(start_x, start_y)

def create_path(path_list, path_start):
    """
    Creates the coordinates of path that the bloons will follow
    """
    x, y = path_start
    path = []
    for path_segment in path_list:
        lenght, direction = split_str(path_segment)
        match direction:
            case 'n':
                y -= lenght*TILE['y']
                path.append([(x, y), direction])
            case 's':
                y += lenght*TILE['y']
                path.append([(x, y), direction])
            case 'w':
                x -= lenght*TILE['x']
                path.append([(x, y), direction])
            case 'e':
                x += lenght*TILE['x']
                path.append([(x, y), direction])
    return path

def get_path_end(path_list, path_start):
    """
    Returns the end of the path
    """
    x, y = path_start
    for path_segment in path_list:
        lenght, direction = split_str(path_segment)
        match direction:
            case 'n':
                y -= lenght*TILE['y']
            case 's':
                y += lenght*TILE['y']
            case 'w':
                x -= lenght*TILE['x']
            case 'e':
                x += lenght*TILE['x']
    return (x, y)
          
def main():
    # Pygame logic
    pg.init()
    screen = pg.display.set_mode(SIZE)
    pg.display.set_caption("Bloons Tower Defense")
    clock = pg.time.Clock()

    def draw_path(path_list, start_pos):
        """
        Draws the path of the game
        Path list should be a list of strings in the format "LENGHT+DIRECTION"
        """
        x, y = start_pos
        for path_segment in path_list:
            length, direction = split_str(path_segment)
            pg.draw.rect(screen, GRAY, rect_val(x, y, length, direction)) # Draws the rectangles of each path segment
            x, y = refresh_x_y(x, y, length, direction)

    # < WEST || > EAST || ^ NORTH || v SOUTH
    pathing = ['2.5E', '3N', '4E', '6S', '5W', '2S', '12E', '3N', '4W', '3N', '4E', '3N', '4W', '4N']
    start_pos = (0, 240)
    end_pos = get_path_end(pathing, start_pos)
    path = create_path(pathing, start_pos)


    # Initializing the sprite group and grouping all sprites
    all_bloons = pg.sprite.Group()

    # Game loop
    game_running = True
    while game_running:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE): 
                game_running = False
            elif event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_1: #Spawn red bloons when 1 is pressed
                            red_bloon = Bloon(RED, 50, 50, 1, path)
                            red_bloon.set_pos(*start_pos)
                            all_bloons.add(red_bloon)
                    case pg.K_2: #Spawn blue bloons when 2 is pressed
                            blue_bloon = Bloon(BLUE, 50, 50, 2, path)
                            blue_bloon.set_pos(*start_pos)
                            all_bloons.add(blue_bloon)
                    case pg.K_3: #Spawn green bloons when 3 is pressed
                            green_bloon = Bloon(GREEN, 50, 50, 3, path)
                            green_bloon.set_pos(*start_pos)
                            all_bloons.add(green_bloon)
                    case pg.K_4: #Spawn pink bloons when 4 is pressed
                            pink_bloon = Bloon(PINK, 50, 50, 4, path)
                            pink_bloon.set_pos(*start_pos)
                            all_bloons.add(pink_bloon)


        
        # Drawing screen
        screen.fill(GRASS_GREEN)
        draw_path(pathing, start_pos=start_pos)

        # Drawing all bloons
        all_bloons.update()
        all_bloons.draw(screen)

        # Bloons controller
        for bloon in all_bloons:
            bloon.move_bloon()
            if bloon.pos == end_pos:
                all_bloons.remove(bloon)
        
        #Refresh screen and max framerate
        pg.display.flip()
        clock.tick(60)
    
    pg.quit()

if __name__ == "__main__":
    main()