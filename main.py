import tcod
from tcod import libtcodpy
import random
from Classes import Tile, Room
import GenerateDungeon
import Globals
import textwrap

player_x = Globals.ROOT_CON_WIDTH // 2
player_y = Globals.ROOT_CON_HEIGHT // 2

# Initialize libtcod
tcod.console_set_custom_font('terminal16x16.png', tcod.FONT_LAYOUT_TCOD)
tcod.console_init_root(Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT, 'tcod Dungeon Generation', False)

# Render the dungeon
def render_dungeon(con, dungeon):
    for x in range(Globals.ROOT_CON_WIDTH):
        for y in range(Globals.ROOT_CON_HEIGHT):

            if dungeon[x][y].isWall:
                dungeon[x][y].blocked = True
                dungeon[x][y].block_sight = True
                dungeon[x][y].name = "wall"
                tcod.console_put_char(con, x, y, ' ', tcod.BKGND_SET)
                tcod.console_set_char_background(con, x, y, tcod.Color(0,0,100), tcod.BKGND_SET)
            
            elif dungeon[x][y].isNPC:
                dungeon[x][y].blocked = True
                tcod.console_put_char(con, x, y, 'N', tcod.BKGND_SET)
                tcod.console_set_char_foreground(con, x, y, tcod.red)

            elif dungeon[x][y].isInner:
                dungeon[x][y].blocked = False
                dungeon[x][y].block_sight = False
                tcod.console_put_char(con, x, y, ' ', tcod.BKGND_SET)
                tcod.console_set_char_background(con, x, y, tcod.Color(50,50,150), tcod.BKGND_SET)

            else:
                dungeon[x][y].blocked = True
                dungeon[x][y].block_sight = True
                tcod.console_put_char(con, x, y, ' ', tcod.BKGND_SET)
                # tcod.console_set_char_background(con, x, y, tcod.Color(200, 200, 200), tcod.BKGND_SET)

def handle_mouse_hover(info_con, dungeon, hover_x, hover_y):
    # Clear the info console before rendering
    info_con.clear()

    # Check if the cursor is hovering over a tile and display the tile name in the info console
    if 0 <= hover_x < Globals.ROOT_CON_WIDTH and 0 <= hover_y < Globals.ROOT_CON_HEIGHT:
        tile_name = dungeon[hover_x][hover_y].name
        tcod.console_print(info_con, 1, 2, f"Tile: {tile_name}")

    tcod.console_print(info_con, 1, 2, f"Tile:")


def handle_mouse_click(rooms, mouse_x, mouse_y):
    for room in rooms:
        if (
            room.x1 <= mouse_x < room.x1 + room.w and
            room.y1 <= mouse_y < room.y1 + room.h
        ):
            return room
    return None


# Main function
def main():
    player_x = Globals.SCREEN_WIDTH // 2
    player_y = Globals.SCREEN_HEIGHT // 2

    desc_con_content = None

    desc_con = tcod.console.Console(Globals.DESC_CON_WIDTH, Globals.DESC_CON_HEIGHT) 
    
    info_con = tcod.console.Console(Globals.INFO_CON_WIDTH, Globals.INFO_CON_HEIGHT)

    con = tcod.console.Console(Globals.ROOT_CON_WIDTH, Globals.ROOT_CON_HEIGHT)
    
    dungeonGenerator = GenerateDungeon.dungeonGenerator()

    player_x, player_y, dungeon, rooms = dungeonGenerator.generate_dungeon(con)
    
    render_dungeon(con, dungeon)

    while not tcod.console_is_window_closed():
        
        render_dungeon(con, dungeon)
        tcod.console_put_char(con, player_x, player_y, '@', tcod.BKGND_SET)  # Place the player
        tcod.console_set_char_foreground(con, player_x, player_y, tcod.yellow)


        tcod.console_blit(con, 0, 0, Globals.ROOT_CON_WIDTH, Globals.ROOT_CON_HEIGHT, 0, 0, 0)
        tcod.console_blit(desc_con, 0, 0, Globals.DESC_CON_WIDTH, Globals.DESC_CON_HEIGHT, 0, Globals.SCREEN_WIDTH - Globals.DESC_CON_WIDTH, 0)
        desc_con.draw_frame(0, 0, Globals.DESC_CON_WIDTH, Globals.DESC_CON_HEIGHT, title="DESC")
        
        tcod.console_blit(info_con, 
                          0, 0, 
                          Globals.INFO_CON_WIDTH, Globals.INFO_CON_HEIGHT, 
                          0, 0, 
                          Globals.SCREEN_HEIGHT - Globals.INFO_CON_HEIGHT )
        info_con.draw_frame(0, 0, Globals.INFO_CON_WIDTH, Globals.INFO_CON_HEIGHT, title="INFO")
        # tcod.console_print(desc_con, 0, 0, "New Window Content")

        # Get mouse position
        mouse = tcod.mouse_get_status()
        hover_x = mouse.cx
        hover_y = mouse.cy
        handle_mouse_hover(info_con, dungeon, hover_x, hover_y)
        if mouse.lbutton_pressed:
            clicked_room = handle_mouse_click(rooms, hover_x, hover_y)
            if clicked_room:
                desc_con.clear()
                wrapped_lore = textwrap.fill(clicked_room.lore, Globals.DESC_CON_WIDTH - 4)
                desc_con_content = clicked_room.name+"\n\n"+wrapped_lore
        desc_con.print(1, 2, f"{desc_con_content}")
        
        
        key = tcod.console_check_for_keypress()
        if key.vk == tcod.KEY_ESCAPE:
            return True  # Exit the game
        

        new_x = player_x
        new_y = player_y
        # Move the player
        if key.vk == tcod.KEY_UP:
            new_y -= 1
        elif key.vk == tcod.KEY_DOWN:
            new_y += 1
        elif key.vk == tcod.KEY_LEFT:
            new_x -= 1
        elif key.vk == tcod.KEY_RIGHT:
            new_x += 1
        
        if not dungeon[new_x][new_y].blocked:
            player_x = new_x
            player_y = new_y
        elif dungeon[new_x][new_y].isNPC:
            tcod.console_print(desc_con, 0, 0, "Bumped")

        # Ensure the player stays within the bounds of the screen
        player_x = max(0, min(player_x, Globals.SCREEN_WIDTH - 1))
        player_y = max(0, min(player_y, Globals.SCREEN_HEIGHT - 1))

        # Blit the info console at the bottom of the screen

        libtcodpy.console_flush()


if __name__ == '__main__':
    main()
