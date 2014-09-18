#Reversed Computer Number Guessing Game
#Computer will try and guess a number you are thinking of
#Author Nate Epply
#Date 17SEP14

#importing the randint function
from random import randint

#Welcoming the player
print ("Welcome to the Number Guessing Game, where I the computer will try and guess the number you are thinking of.")

#setting the initial upper and lower bounds
lower_bound = int(input("\nPlease tell me the lower bound of the range I am guessing in? "))

upper_bound = int(input("\nPlease tell me the upper bound of the range I am guessing in? "))

#Asking human to think of a number
print ("\nNow please think of a number between %s and %s." % (lower_bound,upper_bound))

input("\nPress any key once you have thought of a number.")

#Guess Function, just the randint function randomly picking a number between two bounds
def guess_number(lower,upper):
    return randint(lower,upper)

#establish the initial guess
guess = guess_number(lower_bound,upper_bound)

guess_count = 0

print ("\nMy first guess will be the number %s." % guess)

correct = (input("\nWas that your number? ").lower())

yes = ['yes','y']

no = ['no','n']

#loop to keep guessing until the correct number is guessed
while correct not in yes:
    guess_count += 1
    if guess_count >= 10:
        print ("\nAre you sure you didn't change the number you were thinking of? Hmm let me see...")
    if guess_count >= 2:
        print ("\nHow about the number %s." % guess)
        correct = (input("\nWas that your number? ").lower())
    if correct in no:
        high_low = (input("\nOk, was I too high, or too low? ").lower())
        if high_low == 'high':
            upper_bound = guess - 1
        elif high_low == 'low':
            lower_bound = guess + 1
    guess = guess_number(lower_bound,upper_bound)

#after guessing the correct number printing the results
if guess_count == 0:
    print ("\nHahahaha the mighty computer guessed your number on the first try.")
else:
    print ("\nHaha, I knew that was the number you were thinking of, because I can read your mind!")
    print ("\nI was able to guess your number in only %s turns." % guess_count)


