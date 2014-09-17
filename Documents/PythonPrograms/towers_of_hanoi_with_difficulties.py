#Tower of Hanoi with Multiple difficulties
#Author Nate Epply
#Date 16SEP14

play = 'yes'
yes = ['y','Y','YES','yes','Yes']

easy = ['easy','EASY','Easy']

moderate = ['moderate','MODERATE','Moderate']

hard = ['hard','Hard','HARD']

def difficulty(user_difficulty):
    if user_difficulty in easy:
        return 3 #number of disks
    elif user_difficulty in moderate:
        return 5 #number of disks
    elif user_difficulty in hard:
        return 7 #number of disks

chosen_difficulty = difficulty(input("Please choose your level of difficulty: "))

while play in yes:
    

    #setting variables
    peg_one = list(range(1,chosen_difficulty +1))

    peg_two = []

    peg_three = []

    names_peg_one = ['peg_one','PEG_ONE','one','1','ONE','One']

    names_peg_two = ['peg_two','PEG_TWO','two','2','TWO','Two']

    names_peg_three = ['peg_three','PEG_THREE','3','THREE','Three']

    moves = 0

    peg_list = names_peg_one + names_peg_two + names_peg_three

    print (peg_one,peg_two,peg_three)

    minimum_moves = (2 ** chosen_difficulty) -1

    print ("\nThe minimum number of moves to complete Towers of Hanoi with this number of disks is %s." % minimum_moves)

    #Function that moves the disk from one peg to another.
    def move_disk(origin_peg,dest_peg):
        x = origin_peg[0]
        print
        if dest_peg == []:
            dest_peg.append(x)
            origin_peg.remove(x)
            return (peg_one,peg_two,peg_three)
        elif x < dest_peg[0]:
            dest_peg.insert(0,x)
            origin_peg.remove(x)
            return (peg_one,peg_two,peg_three)
        elif x > dest_peg[0]:
            print ("Cannot perform that move.")

    #Loop to keep game going until all disks are on peg_three
    while peg_three != list(range(1,chosen_difficulty +1)):
        origin_peg_str = input("Which peg would you like to move a disk from? ")
        dest_peg_str = input("Which peg would you like to move the disk to? ")

        if origin_peg_str in names_peg_one:
            origin_peg = peg_one
        elif origin_peg_str in names_peg_two:
            origin_peg = peg_two
        elif origin_peg_str in names_peg_three:
            origin_peg = peg_three

        if dest_peg_str in names_peg_one:
            dest_peg = peg_one
        elif dest_peg_str in names_peg_two:
            dest_peg = peg_two
        elif dest_peg_str in names_peg_three:
            dest_peg = peg_three

        if origin_peg == []:
            print ("There are no disks on that origin peg, please try again.")
            continue
        if origin_peg_str not in peg_list or dest_peg_str not in peg_list:
            print ("Those pegs do not exhist, please try again.")
            continue
 
        move_disk(origin_peg,dest_peg)
        moves += 1
        print (peg_one,"Peg 1")
        print (peg_two,'Peg 2')
        print (peg_three,'Peg 3')

    #Game Winner to print message once all disk are on peg_three and ask to play game again
    if peg_three == list(range(1,chosen_difficulty +1)):
        print ("Congratulations You Won!")
        print ("You completed it in %s moves." % moves)
        print ("That is %s move(s) more than the required number needed to solve the puzzle." % (moves - minimum_moves))

    play = input("Would you like to play again? ")



