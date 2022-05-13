# code to play Cryptid
# Geoffrey Brent September 2019


# Comment: I've tidied this up in order to share, and haven't had a chance to do much testing
# since then - I'm not aware of any remaining bugs, but that doesn't mean there aren't any!

# Note: for reasons which seemed to make sense at the time but which I cannot now
# recall, this code uses a zero-indexed coordinate system internally (so top-left hex
# is (0,0)) but one-indexed for input and output (so player refers to this as (1,1) ).

print("Let's play Cryptid!")
import math


# Setup - define players. Set up abbreviations for convenience.

abbrevs_to_playernames = {"a":"Alpha","b":"Beta","c":"Gamma","d":"Delta","e":"Epsilon"}
playernames_to_abbrevs=dict()
for k in abbrevs_to_playernames:
    playernames_to_abbrevs[abbrevs_to_playernames[k]] = k


print("Entering players:\n")

def displayplayers():
    # function to show who's playing
    print("Players in this game are:")
    for i in range(num_players):
        print(str(i+1),playerorder[i], ("(AI player)" if ai_player == playerorder[i] else ""))

def collect_player_inputs():    
    accept_player_inputs = False
    global num_players
    global playerorder
    global ai_player
    while not accept_player_inputs:
        players=set()
        possibleplayers = playernames_to_abbrevs
        for p in possibleplayers:
            goodinput = False
            while not goodinput:
                is_included = input("\nIs player " + p + " playing?(y/n)\n")
                if is_included.upper() in {"Y","YES","TRUE"}:
                    goodinput = True
                    players.add(p)
                elif is_included.upper() in {"N","NO","FALSE"}:
                    goodinput = True
                else:
                    print("Input not recognised. Please answer 'y' or 'n'.")

        num_players = len(players)
        playerorder = list()

        print("Entering player order:\n")
        unallocated_players=players.copy()
        for i in range(num_players):
            goodinput = False
            while not goodinput:
                print("\nWho is player #" + str(i+1) + "?\n")
                print("Options are:\n")
                for p in unallocated_players:
                    print((p + " "))
                print("You can also use standard abbreviations: a = Alpha etc.")
                next_player = input()
                if next_player in abbrevs_to_playernames:
                    next_player = abbrevs_to_playernames[next_player]
                if next_player in unallocated_players:
                    playerorder += [next_player]
                    goodinput = True
                    unallocated_players.remove(next_player)
                else:
                    print("Invalid input.\n")

        goodinput = False
        while not goodinput:
            print("\nWhich player is the AI?\n")
            print("Options are:\n")
            for p in players:
                print((p + " "))
            print("You can also use standard abbreviations: a = Alpha etc.")
            ai_player = input()
            if ai_player in abbrevs_to_playernames:
                ai_player = abbrevs_to_playernames[ai_player]
            if ai_player in players:
                goodinput = True
            else:
                print("Invalid input.\n")

        displayplayers()
        accept_player_inputs=input("Enter 'y' to accept these, anything else to re-enter player data.")
        if accept_player_inputs.upper() in {"Y","YES","TRUE"}:    
            accept_player_inputs = True
        else:
            accept_player_inputs = False
            print("Re-enter player data.")


collect_player_inputs()    

def board_input():
    accept_board_input = False
    global is_advanced
    global board_layout
    global board_positions
    while not accept_board_input:   
        goodinput = False
        while not goodinput:
            print("\nAre you playing the advanced game? (y/n)\n")
            is_advanced = input()
            if is_advanced.upper() in {"Y","YES","TRUE"}:
                goodinput = True
                is_advanced = True
            elif is_advanced.upper() in {"N","NO","FALSE"}:
                goodinput = True
                is_advanced = False
            else:
                print("Input not recognised. Please answer 'y' or 'n'.")

        board_positions = [(0,0,"A"),(1,0,"B"),(0,1,"C"),(1,1,"D"),(0,2,"E"),(1,2,"F")]

        board_tiles = {"1","2","3","4","5","6"}
        board_tiles_unplaced = board_tiles.copy()
        print("Time to enter the board layout. Visualise the board as: \nAB\nCD\nEF\n")

        board_layout = dict()

        for pos in board_positions:
            goodinput = False
            while not goodinput:
                print("Which tile number is in position ", pos[2],"? Possible options are:\n")
                for tile in board_tiles_unplaced:
                    print(tile + " ")
                tileno = input()
                if tileno in board_tiles_unplaced:
                    goodinput = True
                    key = (pos[0],pos[1])
                    goodinput2 = False
                    while not goodinput2:
                        print("\nIs the number on this tile in the top left corner? (y/n)\n")
                        orientation = input()
                        if orientation.upper() in {"Y","YES","TRUE"}:
                            goodinput2 = True
                            orientation = 1
                        elif orientation.upper() in {"N","NO","FALSE"}:
                            goodinput2 = True
                            orientation = -1
                        else:
                            print("Input not recognised.\n")
                    board_layout[key]=(tileno,orientation)
                    board_tiles_unplaced.remove(tileno)

        print("Board layout is:\n")
        for j in [0,1,2]:
            for i in [0,1]:
                tilename = board_layout[(i,j)][0]
                orientation = board_layout[(i,j)][1]
                print(tilename + ("^" if (orientation == 1) else "v"), end="")
            print("\n")
        accept_board_input=input("Enter 'y' to accept this, anything else to re-enter board data.")
        if accept_board_input.upper() in {"Y","YES","TRUE"}:    
            accept_board_input = True
        else:
            accept_board_input = False
            print("Re-enter board data.")

board_input()

def hardcode_board_data():
    # Hardcoded data for the six tiles that are used to create a Cryptid board.
    # Within each tile, the hexes are ordered by column (left to right) and then
    # by row (top to bottom) where the tile is oriented "upright" (number in top left).
    # Each hex will contain a tuple: h[0] = M, W, D, S, or F (mountain, water, desert, swamp, forest)
    # and h[1] = B, C, or _ (bear, cougar, blank)
    # Blank values will be replaced with None when creating hex objects.

    global tile_n_rows
    tile_n_rows = 3
    global tile_n_cols
    tile_n_cols = 6
    # number of rows and columns per tile
    global tiles_data
    tiles_data = {"1":\
                  [("W","_"),("S","_"),("S","_"),("W","_"),("S","_"),("S","_"),("W","_"),("W","_"),("D","_"),\
                   ("W","_"),("D","_"),("D","B"),("F","_"),("F","_"),("D","B"),("F","_"),("F","_"),("F","B")],\
                  "2":\
                  [("S","C"),("S","_"),("S","_"),("F","C"),("S","_"),("M","_"),("F","C"),("F","_"),("M","_"),\
                   ("F","_"),("D","_"),("M","_"),("F","_"),("D","_"),("M","_"),("F","_"),("D","_"),("D","_")],\
                  "3":\
                  [("S","_"),("S","C"),("M","C"),("S","_"),("S","C"),("M","_"),("F","_"),("F","_"),("M","_"),\
                   ("F","_"),("M","_"),("M","_"),("F","_"),("W","_"),("W","_"),("W","_"),("W","_"),("W","_")],\
                  "4":\
                  [("D","_"),("D","_"),("D","_"),("D","_"),("D","_"),("D","_"),("M","_"),("M","_"),("D","_"),\
                   ("M","_"),("M","_"),("F","_"),("M","_"),("W","_"),("F","_"),("M","_"),("W","C"),("F","C")],\
                  "5":\
                  [("S","_"),("S","_"),("D","_"),("S","_"),("D","_"),("D","_"),("S","_"),("D","_"),("W","_"),\
                   ("M","_"),("W","_"),("W","_"),("M","_"),("M","_"),("W","B"),("M","_"),("M","B"),("W","B")],\
                  "6":\
                  [("D","B"),("M","B"),("M","_"),("D","_"),("M","_"),("W","_"),("S","_"),("S","_"),("W","_"),\
                   ("S","_"),("S","_"),("W","_"),("S","_"),("F","_"),("W","_"),("F","_"),("F","_"),("F","_")]}

    # Each tile has its internal coords (i,j): i in 0-5 gives column number counting from left,
    # j in 0-2 gives position counting down the column.



    # For things like structure and terrain attributes, we define both a one-
    # character abbreviation (handy for display and tiles_data) and a full name:

    global permitted_terrain
    permitted_terrain = {"F":"forest","S":"swamp","D":"desert","M":"mountain","W":"water"}
    global permitted_animals
    permitted_animals = {"B":"bear","C":"cougar",None:"_"}
    global permitted_structuretypes
    permitted_structuretypes = {"A":"Shack","I":"Stone",None:"_"}
    global permitted_structurecolours
    permitted_structurecolours = {"g":"Green","b":"Blue","w":"White",None:"_"}
    if is_advanced:
        permitted_structurecolours["k"] = "Black"


    global nonnullanimals
    nonnullanimals = set(permitted_animals).difference({None})
    global nonnullstructuretypes
    nonnullstructuretypes= set(permitted_structuretypes).difference({None})
    global nonnullstructurecolours
    nonnullstructurecolours= set(permitted_structurecolours).difference({None})
    global x_size
    x_size= 12
    global y_size
    y_size= 9

hardcode_board_data()

class Hexagon(object):
    def __init__(self,terraintype,animaltype,structuretype,structurecolour,xcoord,ycoord):
        self.Terrain = terraintype
        self.Animal = animaltype
        self.Structuretype = structuretype
        self.Structurecolour = structurecolour
        self.X = xcoord
        self.Y = ycoord
        self.Neighbours = set() # immediately adjacent hexes, to be populated later
        self.Neighbours2 = set() # neighbours within 2, populated later
        self.Neighbours3 = set() # ...within 3
        self.ClueMatches = set() # set of clues consistent with this hex, populated later
    def check(self):
        if self.Terrain not in permitted_terrain:
            raise Exception("Undefined value for hex terrain type: {}".self.Terrain)
        if self.Animal not in permitted_animals:
            raise Exception("Undefined value for hex animal type: {}".self.Animal)
        if self.Structuretype not in permitted_structuretypes:
            raise Exception("Undefined value for hex structure type: {}".self.Structuretype)
        if self.Structurecolour not in permitted_structurecolours:
            raise Exception("Undefined value for hex structure colour: {}".self.permitted_structurecolours)
        if (self.Structurecolour is None and self.Structuretype is not None):
            raise Exception("Hex has structure type but not colour set.")
        if (self.Structurecolour is not None and self.Structuretype is None):
            raise Exception("Hex has structure colour but not type set.")
        if self.X not in range(x_size):
            raise Exception("Hex has x-coord outside permitted range: {}", self.X)
        if self.Y not in range(y_size):
            raise Exception("Hex has y-coord outside permitted range: {}", self.Y)
    def summary(self,individual = False):
        # run with individual = True as a manual query for a single hex, or False
        # to return a brief summary usable for displaying a map.
        if individual:
            print("Tile in column "+ str(self.X+1)+ " from left and row "+ str(self.Y+1)+ " from top:\n")
            print("Terrain type: "+ self.Terrain+ ". Animal type: "+ str(self.Animal)+\
                  ". Structure type: "+ str(self.Structuretype) + " and colour " + str(self.Structurecolour) + ".")
        return(self.Terrain + ("_" if self.Animal is None else self.Animal) +\
               (str(self.Structuretype) if self.Structuretype else "_") + \
               (str(self.Structurecolour) if self.Structurecolour else "_"))

# Create the full board (minus structures): translate tile positions into individual hexes.
def populate_hexes():       
    global coords_to_hexes
    coords_to_hexes = dict()
    # key is (x,y) with x-coord from 0 to 11 and y-coord from 0 to 8, counting across and down from the left-hand
    # corner; will link to the hex object for that space.
    for tile in board_positions:
        tile_x_start = tile[0]*tile_n_cols
        tile_y_start = tile[1]*tile_n_rows
        tile_no = board_layout[(tile[0],tile[1])][0]
        tile_orient = board_layout[(tile[0],tile[1])][1]
        tile_contents = tiles_data.copy()[tile_no][::tile_orient]
        for y_tile in range(tile_n_rows):
            for x_tile in range(tile_n_cols):
                x_coord = tile_x_start + x_tile
                y_coord = tile_y_start + y_tile
                pos_in_tile_list = y_tile + x_tile*tile_n_rows
                tile_data=tile_contents[pos_in_tile_list]
                coords_to_hexes[(x_coord,y_coord)]=Hexagon(terraintype=tile_data[0],\
                                                           animaltype=(None if tile_data[1] == "_" else tile_data[1]),\
                                                           structuretype=None,structurecolour=None,\
                                                           xcoord=x_coord,ycoord=y_coord)
    global AllHexes
    AllHexes = set(coords_to_hexes.values())
    for h in AllHexes:
        h.check()
        
populate_hexes()
global AllClues

def showboard(legend=True,clue=None):
    # if a non-None clue number is provided, it will mark which hexes on the board are consistent with that clues.
    print("\nDisplaying board layout:\n")
    for j in range(y_size):
        for i in range(x_size):
            h = coords_to_hexes[(i,j)]
            bracket1="["
            bracket2="]"
            if clue is not None:
                if clue in h.ClueMatches:
                    bracket1="{"
                    bracket2="}"
            print(bracket1+h.summary()+bracket2,end="")
        print("\n")
    
    # to improve: offset every second column to make hex layout clearer, or just
    # replace it all with a graphic
    if legend:
        print("\nHex format: terrain type, animal type, structure type, structure colour.")
        for t in permitted_terrain:
            print(t,permitted_terrain[t],end="  ")
        print("\n")
        for a in nonnullanimals:
            print(a,permitted_animals[a],end="  ")
        print("\n")
        for st in nonnullstructuretypes:
            print(st,permitted_structuretypes[st],end="  ")
        for st in nonnullstructurecolours:
            print(st,permitted_structurecolours[st],end="  ")
        if clue:
            print("{****} is a hex consistent with specified clue.")
                    
    
def input_structures():
    accept_structure_input = False
    while not accept_structure_input:
        for st in nonnullstructuretypes:
            for sc in nonnullstructurecolours:
                goodinput = False
                while goodinput is False:
                    print("\nPlease enter the location of the "+permitted_structurecolours[sc]+" "+permitted_structuretypes[st]+".\n")
                    xc = int(input("x-coordinate, counting from 1 at left-most column: "))-1
                    yc = int(input("y-coordinate, counting from 1 at top-most row: "))-1
                    if xc not in range(x_size):
                        print("\nError: x-coordinate out of bounds.")
                    elif yc not in range(y_size):
                        print("\nError: y-coordinate out of bounds.")
                    elif coords_to_hexes[(xc,yc)].Structuretype is not None:
                        print("\nError: a structure already exists there.")
                    else:
                        goodinput = True
                        coords_to_hexes[(xc,yc)].Structuretype = st
                        coords_to_hexes[(xc,yc)].Structurecolour = sc
        print("Displaying board layout with structures:")
        showboard()
        accept_structure_input=input("\nEnter 'y' to accept this, anything else to re-enter structure data.")
        if accept_structure_input.upper() in {"Y","YES","TRUE"}:    
            accept_structure_input = True
        else:
            accept_structure_input = False
            for h in AllHexes:
                h.Structuretype = None
                h.Structurecolour = None
            print("Re-enter structure data.")

input_structures()

def populateneighbourinfo():
    for j in range(y_size):
        for i in range(x_size):
            h = coords_to_hexes[i,j]
            h.Neighbours = {h}
            parity = i%2
            # 0 if i is even, 1 if odd
            # if x-coordinate (i) is even, this hex is HIGHER than hexes of the same
            # j-coord in adjacent columns; otherwise, it is LOWER
            poss_neighbour_rel_positions = {(0,0),(0,1),(0,-1),(-1,0+parity),(-1,-1+parity),(1,0+parity),(1,-1+parity)}
            poss_neighbour_positions = {(rp[0]+h.X,rp[1]+h.Y) for rp in poss_neighbour_rel_positions}
            for pos in poss_neighbour_positions:
                if pos in coords_to_hexes:
                    h.Neighbours.add(coords_to_hexes[pos])
    for h in AllHexes:
        for h2 in h.Neighbours:
            h.Neighbours2.update(h2.Neighbours)

    for h in AllHexes:
        for h2 in h.Neighbours2:
            h.Neighbours3.update(h2.Neighbours)

populateneighbourinfo()




num_clues = 0 # counter for how many clues have been created.


class Clue(object):
    def __init__(self,cluename,hexes):
        global num_clues
        self.Cluename = cluename
        self.Cluenumber = num_clues
        num_clues += 1
        self.Hexes = hexes # the set of hexes which match this clue
    def display(self,showmatches=True):
        print(self.Cluenumber,self.Cluename,("Matches "+str(len(self.Hexes))+" hexes" if showmatches else ""))

def populateclues():
    # As well as setting up all the clues available for this game, this also populates
    # the ClueMatches for all hexes
    global AllClues
    AllClues = list()

    pt_list = list(permitted_terrain)
    for i in range(len(pt_list)):
        for j in range(i+1,len(pt_list)):
            t1 = pt_list[i]
            t2 = pt_list[j]
            cluename = "On "+permitted_terrain[t1]+" or "+permitted_terrain[t2]
            permitted_hexes=set()
            for h in AllHexes:
                if (h.Terrain in {t1,t2}):
                    permitted_hexes.add(h)
            AllClues += [Clue(cluename,permitted_hexes.copy())]

    for i in pt_list:
        cluename = "Within one space of "+permitted_terrain[i]
        permitted_hexes = set()
        for h in AllHexes:
            tts_neighbours = {h2.Terrain for h2 in h.Neighbours}
            if i in tts_neighbours:
                permitted_hexes.add(h)
        AllClues += [Clue(cluename,permitted_hexes.copy())]

    cluename = "Within one space of either animal territory"
    permitted_hexes = set()
    for h in AllHexes:
        for h2 in h.Neighbours:
            if h2.Animal in nonnullanimals:
                permitted_hexes.add(h)
                break
    AllClues += [Clue(cluename,permitted_hexes.copy())]

    for i in nonnullstructuretypes:
        cluename = "Within two spaces of "+permitted_structuretypes[i]
        permitted_hexes = set()
        for h in AllHexes:
            for h2 in h.Neighbours2:
                if h2.Structuretype == i:
                    permitted_hexes.add(h)
                    break
        AllClues += [Clue(cluename,permitted_hexes.copy())]

    for i in nonnullanimals:
        cluename = "Within two spaces of "+permitted_animals[i]+" territory"
        permitted_hexes = set()
        for h in AllHexes:
            for h2 in h.Neighbours2:
                if h2.Animal == i:
                    permitted_hexes.add(h)
                    break
        AllClues += [Clue(cluename,permitted_hexes.copy())]

    for i in nonnullstructurecolours:
        cluename = "Within three spaces of "+permitted_structurecolours[i]
        permitted_hexes = set()
        for h in AllHexes:
            for h2 in h.Neighbours3:
                if h2.Structurecolour == i:
                    permitted_hexes.add(h)
                    break
        AllClues += [Clue(cluename,permitted_hexes.copy())]
    # if in advanced mode, add NOT clues for all of the above
    if is_advanced:
        for cl in AllClues.copy():
            cluename = "NOT " + cl.Cluename
            permitted_hexes = AllHexes.difference(cl.Hexes)
            AllClues += [Clue(cluename,permitted_hexes.copy())]
    # update hexes to show what clues they match
    for cl in AllClues:
        for h in cl.Hexes:
            h.ClueMatches.add(cl)

populateclues()

def inputAIclue():
    global ai_clue
    goodinput = False
    while not goodinput:
        print("List of all possible clues:")
        for cl in AllClues:
            cl.display()
        ai_clue = int(input("Please enter your clue number from the list above: "))
        if ai_clue in range(len(AllClues)):
            goodinput = True
        else:
            print("Unrecognised clue.")
    ai_clue=AllClues[ai_clue]

inputAIclue()

# define hexes which haven't yet got anybody's cube on them - these are
# the only legal places to ask or search.

NonCubedHexes = AllHexes.copy()

# Currently there is no need to record individual cube/disk placements.
# When a player places a piece, all clues inconsistent with that placement are
# eliminated, which then means that asking them about that hex again will give
# no new information - hence it will never be suggested as a move. If changing
# the strategy, you may need to implement this record-keeping.

# For each player we define (and will maintain) a list of clues that are compatible with their plays so far.
# Initially this is set to all clues.

consistent_clues = dict()
for p in playerorder:
    consistent_clues[p]=set(AllClues.copy())

def PlacePiece(player=None,x=None,y=None,piece=None,confirm=True):
    # set confirm = False to skip move confirmation
    accept_placement = False
    global consistent_clues
    global NonCubedHexes
    while not accept_placement:
        if player in abbrevs_to_playernames:
            player = abbrevs_to_playernames[player]
        if player not in playerorder:
            goodinput = False
            while not goodinput:
                print("\nWho is placing now? Options are:")
                for p in playerorder:
                    print(p)
                player = input()
                if player in abbrevs_to_playernames:
                    player = abbrevs_to_playernames[player]
                if player in playerorder:
                    goodinput = True
                else:
                    print("Invalid input.\n")
        if x is None:
            goodinput = False
        elif int(x)-1 not in range(x_size):
            goodinput = False
        else:
            goodinput = True
        while not goodinput:
            print("\nEnter x-coordinate, counting from 1 = left-most column.")
            x = int(input())
            if x-1 in range(x_size):
                goodinput = True
            else:
                print("Invalid input.\n")
        x=x-1 # convert to 0-indexed form
        if y is None:
            goodinput = False
        elif int(y)-1 not in range(y_size):
            goodinput = False
        else:
            goodinput = True
        while not goodinput:
            print("\nEnter y-coordinate, counting from 1 = left-most column.")
            y = int(input())
            if y-1 in range(y_size):
                goodinput = True
            else:
                print("Invalid input.\n")
        y=y-1 # convert to 0-indexed form
        placement_hex = coords_to_hexes[(x,y)]
        if placement_hex not in NonCubedHexes:
            raise Exception("Attempted to place a piece in a hex that already has a cube.")
            # should make this prompt re-entry rather than crashing out.
        if (player == ai_player):
            if placement_hex in ai_clue.Hexes:
                print("Automatically placing disc")
                piece = "d"
            else:
                print("Automatically placing cube")
                piece = "c"
        if piece in {"c","d"}:
            goodinput = True
        else:
            goodinput = False
        while not goodinput:
            print("\nWhat piece are they playing? (c = cube, d = disc)")
            piece = input()
            if piece in {"c","d"}:
                goodinput = True
            else:
                print("Invalid input.\n")
        if confirm:
            print("Player",player,"placing",("cube" if piece is "c" else "disc"),"at",int(x+1),",",int(y+1))
            confirm_check=input("Is this correct? (y/n)")
            if confirm_check.upper() in {"Y","YES","TRUE"}:    
                confirm_check = True
                accept_placement = True
            else:
                confirm_check = False
                print("Re-enter move.")
        else:
            accept_placement = True
        if piece == "d":
            consistent_clues[player].intersection_update(placement_hex.ClueMatches)
        elif piece == "c":
            consistent_clues[player].difference_update(placement_hex.ClueMatches)
            NonCubedHexes.remove(placement_hex)
        else:
            raise Exception("Unexpected piece type.")
            

def ShowConsistentClues():
    for p in playerorder:
        print("Player",p,"has",str(len(consistent_clues[p])),"possible clues, based only on their own plays:")
        hexcounts=dict() # counts how many possible clues for this player are consistent with each hex
        for cl in consistent_clues[p]:
            cl.display()
            for h in cl.Hexes:
                hexcounts[h]=hexcounts.get(h,0)+1
        closest_dist_to_half = min({abs(hexcounts[h]-0.5*len(consistent_clues[p])) \
                                    for h in NonCubedHexes.intersection(set(hexcounts))})
        most_informative_hexes = {h for h in NonCubedHexes.intersection(set(hexcounts))\
                                  if abs(hexcounts[h]-0.5*len(consistent_clues[p])) == closest_dist_to_half}
        #if len(consistent_clues[p]) > 1:
        #    print("Most informative hexes to ask this player would be:")
        #    for h in most_informative_hexes:
        #        print(h.X+1,",",h.Y+1)
        # The closer a hex is to 50% of the player's possible clues, the more information you
        # get from asking them about it. However, the optimal choice is probably one with a
        # slightly higher than 50% chance of a disc since this reduces the chance that you'll
        # have to place a cube yourself and give info to the other player.
        # This criterion assumed we're just trying to find one player's clues, but this has been
        # superseded by better methods below.

# Find the least informative place an AI player could place a cube
# Currently the criterion for this is just to maximise the number of
# clues that are consistent with AI's placements so far; it doesn't
# attempt to factor in other players' concealed knowledge or uniqueness etc.
def LeastInformativeCube():
    hexcounts=dict()
    legalcubeplacements=NonCubedHexes.difference(ai_clue.Hexes)
    for h in legalcubeplacements:
        hexcounts[h]=0
    for cl in consistent_clues[ai_player]:
        for h in legalcubeplacements.intersection(cl.Hexes):
            hexcounts[h]=hexcounts.get(h,0)+1
    lowest_num_clues = min({hexcounts[h] for h in hexcounts})
    least_informative_hexes = {h for h in hexcounts if hexcounts[h] == lowest_num_clues}
    print("Best cube placement eliminates",str(lowest_num_clues),"of your possible clues. Best options are:")
    for h in least_informative_hexes:
        print(h.X+1,",",h.Y+1)



def FindConsistentClueCombos(verbose=True):
    # this can be computation-heavy early in the game, especially with lots of players
    # and/or advanced game.
    old_tuples = {()}
    for p in playerorder:
        new_tuples = set()
        if p == ai_player:
            new_bits = {ai_clue}
        else:
            new_bits = consistent_clues[p]
        for t_o in old_tuples:
            for new_bit in new_bits:
                new_tuples.add(t_o + (new_bit,))
        old_tuples = new_tuples
    if verbose:
        print("There are a total of",len(new_tuples),"clue combinations consistent with AI's clue and all player moves so far")
    possible_clue_tuples = set() # unlike the format of old_tuples, these will include the solution hex as the last member of the tuple
    possible_solution_hexes = set()
    repeat_solution_counts = dict()
    for t in new_tuples:
        # check how many hexes each tuple of clues defines and discard all that don't define exactly one
        hexes_in_tuple_clues=NonCubedHexes.copy()
        for i in range(len(t)):
            hexes_in_tuple_clues.intersection_update(t[i].Hexes)
        if len(hexes_in_tuple_clues) == 1:
            solhex = list(hexes_in_tuple_clues)[0]
            possible_clue_tuples.add(t + (solhex,))
            possible_solution_hexes.add(solhex)
            repeat_solution_counts[solhex] = repeat_solution_counts.get(solhex,0)+1
    num_viable_tuples = len(possible_clue_tuples)
    max_repeats = max(repeat_solution_counts.values())
    most_likely_hexes = {h for h in repeat_solution_counts if repeat_solution_counts[h] == max_repeats}
    if verbose:
        print("Of these,",num_viable_tuples,"would give a unique solution hex, and a total of",\
              len(possible_solution_hexes),"different hexes are viable solutions.")
        print("Shannon entropy is:", ShannonEntropy(possible_clue_tuples))
        print("The most likely candidate or candidates show up in",max_repeats,"different possible clue combinations with estimated",float(max_repeats/num_viable_tuples),"probability of being correct. They are:")
    for h in most_likely_hexes:
        print(h.X+1,",",h.Y+1)
#    # Identify the most informative place to ask, if trying to reduce number of possible clue combinations - now obsolete
#    hex_by_player=dict()
#    for t in possible_clue_tuples:
#        for i in range(len(t)-1): # the last place of this tuple is the corresponding solution hex
#            player = playerorder[i]
#            clue = t[i]
#            for h in clue.Hexes:
#                hex_by_player[(player,h)] = hex_by_player.get((player,h),0)+1
#    closest_to_half = min({abs(v-0.5*len(possible_clue_tuples)) for v in hex_by_player.values()})
#    good_to_ask = {key for key in hex_by_player if closest_to_half == abs(hex_by_player[key]-0.5*len(possible_clue_tuples))}
    # This method aims to reduce the total number of possible clue
    # scenarios as quickly as possible - but perhaps it would be
    # better to reduce entropy on possible locations? Can probably
    # determine location faster than getting all clues?
#    if verbose2:
#        print("Good options to ask for reducing total possible clue combos:")
#        for key in good_to_ask:
#            print(key[0],key[1].X+1,",",key[1].Y+1)
    return possible_clue_tuples

# function: given a set of possible clue combinations including their solution hexes
# e.g. possible_clue_tuples as calculated above, calculate the Shannon entropy of that set
def ShannonEntropy(clue_tuple_combos):
    se = 0
    hex_frequencies = dict()
    for t in clue_tuple_combos:
        combo_hex=t[len(t)-1]
        hex_frequencies[combo_hex] = hex_frequencies.get(combo_hex,0)+1
    for h in hex_frequencies:
        p_i = hex_frequencies[h]/len(clue_tuple_combos)
        se = se - p_i*math.log(p_i)
    return se

# function: given the set of all possible clue tuples, find which question achieves best expected
# reduction in Shannon entropy for solution location.

def FindBestSEQuery(possible_clue_tuples=None):
    if possible_clue_tuples is None:
        possible_clue_tuples = FindConsistentClueCombos(True)
    se_current = ShannonEntropy(possible_clue_tuples)
    if se_current == 0:
        h = (list(possible_clue_tuples)[0])[len(playerorder)]
        print("Time to search! The cryptid is at hex",str(h.X+1),",",str(h.Y+1))
    else:    
        best_expected_se = math.inf
        best_question = None
        candidate_hexes = {t[len(t)-1] for t in possible_clue_tuples}
        for h in NonCubedHexes:
            for p_num in range(len(playerorder)):
                disc_tuples = {t for t in possible_clue_tuples if t[p_num] in h.ClueMatches}
                cube_tuples = possible_clue_tuples.difference(disc_tuples)
                # split the tuples into those we'd have left if we asked this player and got a disc,
                # vs. those we'd have left if we got a cube.
                se_disc = ShannonEntropy(disc_tuples)
                se_cube = ShannonEntropy(cube_tuples)
                expected_se = (se_disc*len(disc_tuples)+se_cube*len(cube_tuples))/(len(disc_tuples)+len(cube_tuples))
                # entropy of each possible outcome state, weighted by probability of getting that outcome
                if(expected_se < best_expected_se):
                    best_expected_se = expected_se
                    best_question = (playerorder[p_num],h)
        h=best_question[1]
        print("Best question (entropy reduction strategy): ask player", best_question[0],"about hex",str(h.X+1),",",str(h.Y+1))
        print("Expected entropy reduction: ",str(se_current-best_expected_se))


def ShowDeducedPossibleClues(possible_clue_tuples=None,max_p_p=10):
    # similar to ShowConsistentClues, but this eliminates clues that are deduced to be impossible
    if possible_clue_tuples is None:
        possible_clue_tuples = FindConsistentClueCombos(True)
    for p_num in range(len(playerorder)):
        possible_clues = {t[p_num] for t in possible_clue_tuples}
        if(len(possible_clues) > max_p_p):
            print ("Total of ",str(len(possible_clues)),"possible clues for player",playerorder[p_num],)
        else:
            print ("\nPossible clues remaining for player",playerorder[p_num],"are:")
            for cl in possible_clues:
                cl.display()

def infodump():
    #LeastInformativeCube()
    possible_clue_tuples = FindConsistentClueCombos(True)
    ShowDeducedPossibleClues(possible_clue_tuples)
    FindBestSEQuery(possible_clue_tuples)



def playgame():
    print("Starting game.")
    print("Initial cube placement!")
    for i in range(2):
        for p in playerorder:
            print("Placing cube no.",str(i+1),"for player",p)
            if p == ai_player:
                print("Play recommendations:")
                LeastInformativeCube()
            goodinput=False
            while not goodinput:
                xval=int(input("Enter x-coordinate for cube:"))
                yval=int(input("Enter y-coordinate for cube:"))
                if coords_to_hexes[(xval-1,yval-1)] in NonCubedHexes:
                    goodinput=True
                else:
                    print("Illegal placement, there is already a cube here. Try again.")
            PlacePiece(p,xval,yval,"c",False)
    print("Completed initial cube placement.")
    finished = False
    while not finished:
        choice=input("Enter 1 to input a cube or disc placement by any player, 2 for advice on where to place a cube, 3 for advice on where to ask, 4 for information about other players' clues, or 5 to finish: ")
        if choice == "1":
            PlacePiece()
        elif choice == "2":
            LeastInformativeCube()
        elif choice == "3":
            FindBestSEQuery()
        elif choice == "4":
            ShowConsistentClues()
            ShowDeducedPossibleClues()
        elif choice == "5":
            finished = True
    print("\nThanks for playing!")
        

playgame()
