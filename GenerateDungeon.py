import tcod
from Classes import Tile
import random
from Classes import Room
import Globals
from AiModel import GenerateLore

from AiModel import GenerateLore

class dungeonGenerator:

    def __init__(self) -> None:
        # Room properties
        self.ROOM_MAX_SIZE = 15
        self.ROOM_MIN_SIZE = 10
        self.MAX_ROOMS = 10

        # Set up display
        self.SCREEN_WIDTH = Globals.ROOT_CON_WIDTH
        self.SCREEN_HEIGHT = Globals.ROOT_CON_HEIGHT


        self.loreGenerator = GenerateLore.loreGenerator()


    # Generate rooms
    def create_rooms(self):
        rooms = []
        for _ in range(self.MAX_ROOMS):
            w = tcod.random_get_int(0, self.ROOM_MIN_SIZE, self.ROOM_MAX_SIZE)
            h = tcod.random_get_int(0, self.ROOM_MIN_SIZE, self.ROOM_MAX_SIZE)
            x = tcod.random_get_int(0, 0, self.SCREEN_WIDTH - w - 1)
            y = tcod.random_get_int(0, 0, self.SCREEN_HEIGHT - h - 1)
            new_room = Room.Room(x, y, w, h)

            if not any(new_room.intersect(other) for other in rooms):
                rooms.append(new_room)
                
        return rooms

    # Carve the dungeon
    def carve_dungeon(self, rooms, con):
        
        dungeon = [[Tile.Tile(True) for y in range(self.SCREEN_HEIGHT)] for x in range(self.SCREEN_WIDTH)]
        for room in rooms:
            for x in range(room.x1, room.x2 + 1):
                for y in range(room.y1, room.y2 + 1):
                    if (
                        x == room.x1 or x == room.x2 or
                        y == room.y1 or y == room.y2
                    ):
                        
                        dungeon[x][y].isWall = True
                        tcod.console_put_char(con, x, y, '#', tcod.BKGND_NONE) 
                    else:
                        dungeon[x][y].isInner = True
                        tcod.console_put_char(con, x, y, ' ', tcod.BKGND_NONE)  # Set empty space to '.'


            #for carving the insides of the room
            inner_x = room.x1 + 1
            inner_y = room.y1 + 1
            inner_width = room.w - 1
            inner_height = room.h - 1

            for y in range(inner_y, inner_y + inner_height):
                for x in range(inner_x, inner_x + inner_width):
                    dungeon[x][y].isInner = True
                    dungeon[x][y].name = room.name


            #place npc
            npc_y = random.randrange(inner_y+1, inner_y + inner_height-1)
            npc_x = random.randrange(inner_x+1, inner_x + inner_width-1)
            dungeon[npc_x][npc_y].isNPC = True
            dungeon[npc_x][npc_y].isInner = False


        #for carving the paths between the rooms
        for idx, room in enumerate(rooms):
            if idx == 0:
                pass
            else:
                for x, y in self.carve_paths(rooms[idx-1].center(), room.center()):
                    dungeon[x][y].isInner = True
                    dungeon[x][y].isWall = False

        
        return dungeon

    # Carve paths between rooms
    def carve_paths(self, start, end):
        x1, y1 = start
        x2, y2 = end

        if random.random() < 0.5:
            corner_x, corner_y = x2, y1
        else:
            corner_x, corner_y = x1, y2

        for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
            yield x, y
        for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
            yield x, y


    def assignLocations(self, rooms, locations):
        for room in rooms:
            room.name = locations.pop()
            room.lore =  self.loreGenerator.generateLore(room.name)

    def generate_dungeon(self, con):
        rooms = self.create_rooms()
        
        #get location names
        locations =  self.loreGenerator.generateNameList(Globals.GENRE)
        self.assignLocations(rooms, locations)

        dungeon = self.carve_dungeon(rooms, con)
        
        start_x, start_y = rooms[0].center()
        return start_x, start_y, dungeon, rooms