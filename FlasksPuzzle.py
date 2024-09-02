import os
from bqueue import BoundedQueue
from bstack import BoundedStack
flask_size = 3

os.system("")


def clear_screen():
    '''
    Clear terminal screen
    in: none
    out: none
    '''
    os.system("clear")
    
def print_location(x, y, text):
    '''
    Prints text at the specified location on the terminal.
    in:
        - x (int): row number
        - y (int): column number
        - text (str): text to print
    out: none
    '''
    print (f"\033[{x};{y}H{text}")   
    
def move_cursor(x, y):
    '''
    in:
        - x (int): row number
        - y (int): column number
    out: none
    '''
    print("\033[{1};{0}H".format(x, y), end='')    

def parse(filename):
    """
    turn text files into list of bounded stacks to represent the flasks
    in: text file name
    out: list of bounded stacks
    """
    file = open(filename,"r")
    lines = file.read().split("\n")
    numbers = lines[0].strip().split()
    flask_num = int(numbers[0])
    chemical_num = int(numbers[1])
    lines.pop(0)
    
    b_queue = BoundedQueue(4)
    flasks = []
    for i in range(flask_num):
        flasks.append(BoundedStack(4))
    
    for i in lines:
        #is length(i)<3, that line is a chemical, not a command
        if len(i) < 3:
            try:
                b_queue.enqueue(i)
            except:
                #if the queue is full just move on to the next line
                pass
        if len(i) >= 3:
            num = int(i[0])
            flask = int(i[2])-1
            for j in range(num):
                try:
                    flasks[flask].push(b_queue.dequeue())
                except:
                    #if the queue is full just move on to the next one
                    pass
    return flasks
            
            
def colour_element(element):
    """
    Makes string with correct colours based on the element. 
    This is just because this code is very ugly and I would like it to not be with the other stuff.
    in: string of the element printed
    out: string with ansi codes
    """    
    ANSI = {
    "HRED": "\033[41m",
    "HGREEN": "\033[42m",
    "HBLUE": "\033[44m",
    "HORANGE": "\033[48;2;255;165;0m",
    "HYELLOW": "\033[43m",
    "HMAGENTA": "\033[45m",
    "RESET": "\033[0m",
    }    
    ret = ""
    if element == "AA":
        ret = ANSI["HRED"] + element + ANSI["RESET"]
    elif element == "BB":
        ret = ANSI["HBLUE"] + element + ANSI["RESET"]
    elif element == "CC":
        ret = ANSI["HGREEN"] + element + ANSI["RESET"]
    elif element == "DD":
        ret = ANSI["HORANGE"] + element + ANSI["RESET"]
    elif element == "EE":
        ret = ANSI["HYELLOW"] + element + ANSI["RESET"]  
    elif element == "FF":
        ret = ANSI["HMAGENTA"] + element + ANSI["RESET"]   
    return ret
    
def flask_num_colour(row, red_num, green_num):
    """
    print string of the flask numbering with the correct colours
    this code is very ugly :(   
    in: boolean (true if this is the second row), the source num (red) and destination (green)
    out: None, but prints.
    """
    ANSI = {
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "RESET": "\033[0m",
    }  
    
    if red_num == None: #no colouring at all.
        if not row:
            print_location(10, 0, "  1     2     3     4")
        else:
            print_location(17, 0, "  5     6     7     8")
            
    else: #there is colouring to do.
        string = ""
        for i in range(4):
            if not row and i == red_num: #row 1, source
                string += ANSI["RED"] + str(red_num + 1) + "     " + ANSI["RESET"]
            elif not row and i == green_num: #row 1, destination
                string += ANSI["GREEN"] + str(green_num + 1) + "     " + ANSI["RESET"]
            elif not row: #row 1, regular flask
                string += str(i + 1) + "     "
                
            elif row and i + 4 == red_num: #row 2, source
                string += ANSI["RED"] + str(red_num + 1) + "     " + ANSI["RESET"]
            elif row and i + 4 == green_num: #row 2, destination
                string += ANSI["GREEN"] + str(green_num + 1)+ "     " + ANSI["RESET"]
            elif row: #row 2, regular flask
                string += str(i + 5) + "     "
            
        #print the coloured text            
        if not row:
            print_location(10, 0, string)
        else:
            print_location(17, 0, string)

def printline(flasks, second_row):
    """
    prints only one row of flasks, one line at a time.
    in: list of bounded stacks, boolean
    out: none, but it does print stuff
    """   
    
    #i is the row of the flasks. i = 0 is the top line that is printed
    for i in range(flask_size+1):
        string = ""
        #j = 0 is the first flask
        for j in range(flask_size+1):
            
            #if statement code runs if we are on the top row and this is a *completed* flask
            if flasks[j].isComplete() and i == 0:
                string += "+--+  "
            
            else:
                string += "|"
                items = flasks[j].getItems()
            
                #this if statement only runs if the length of the stack reaches the line we are printing.
                #aka if the flask is filled to the level we are on
                if len(items) > flask_size-i:
                    string += colour_element(items[flask_size-i])                      
                    
                #empty space in flask
                else:
                    string += "  "
                string += "|  "
                
        if second_row:
            print_location(12 + i, 0, string)
            print_location(16, 0, "+--+  +--+  +--+  +--+") #bottom of flasks
        else:
            print_location(5 + i, 0, string)
            print_location(9, 0, "+--+  +--+  +--+  +--+") #bottom of flasks
            
             

def main():
    """
    controls flow of game
    in: none
    out: none
    """
    flasks = parse("chemicals.txt")# <--------CHANGE FILE NAME HERE
    win = False #True if the game is won
    clear_screen()
    print_location( 0, 0, "Magical Flask Game\n")
    
    printline(flasks, False)
    flask_num_colour(False, None, None)
    if len(flasks) == 8:
        printline(flasks[4:], True)
        flask_num_colour(True, None, None)
        
        
    #MAIN GAME LOOP
    
    while not win:
        print_location(0, 0, "Magical Flask Game")
        text1 = "Select source flask: "
        text2 = "Select destination flask: "        
        
        valid = False
        while not valid: #runs until a valid source is chosen by user
            print_location(2, 0, text1 + "                   ")
            print_location(3, 0, text2 + "                   ")
            move_cursor(len(text1) + 1, 2)           
            source = input()
            
            if source == "exit":
                clear_screen()
                exit()
            try:
                source = int(source)-1
                assert source < len(flasks)
            except:
                print_location(4, 0, "Invalid input. Try again.")
            else:   
                #flask is empty or closed (complete)
                if flasks[source].isEmpty() or flasks[source].isComplete():
                    print_location(4, 0, "Cannot pour out of that flask. Try again.")
                else:
                    valid = True              
            
        valid = False
        while not valid: #runs until a valid destination is chosen by user
            print_location(2, 0, text1)
            print_location(3, 0, text2+ "                    ")
            move_cursor(len(text2) + 1, 3)           
            destination = input()
            if destination == "exit":
                clear_screen()
                exit()            
            try:
                destination = int(destination)-1
                assert destination < len(flasks)
            except:
                print_location(4, 0, "Invalid input. Try again.")            
            else:
                #if flask is closed (complete) or full
                if flasks[destination].isComplete() or flasks[destination].isFull():
                    print_location(4, 0, "Cannot pour into that flask. Try again.")
                else:
                    valid = True        
        
        flasks[destination].push(flasks[source].pop())
        
        #print new state of flasks
        printline(flasks, False)
        flask_num_colour(False, source, destination)
        if len(flasks) == 8:
            printline(flasks[4:], True)
            flask_num_colour(True, source, destination)           
            
        #checks if game is won.
        uncomplete_count = 0
        for i in flasks:
            if not i.isComplete() and not i.isEmpty():
                uncomplete_count += 1
        if uncomplete_count == 0:
            print("You win!")
            win = True        
        
if __name__ == "__main__":
    main()