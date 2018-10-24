# main.py

from user import *
from pymongo import MongoClient
import pymongo

client = MongoClient()
db = client.snsproject

# Index already created
# db.posts.create_index([('posting_id', 1), ('date', -1)], unique = True)
# db.users.create_index([('name', pymongo.TEXT)])

def mainpage(db):
    '''
    call signup() or signin()
    '''
    while True:
        print('='*50)
        print('Welcome to Mongostagram of Mingyeong and GoEun')
        print('=' *50,'\n')
        print(' '.rjust(16),'*'*16)
        print('Select Menu'.rjust(30))
        print(' '.rjust(16),'*'*16)
    
        print('1. Sign Up'.rjust(30))
        print('2. Sign In'.rjust(30))
        print('3. Exit'.rjust(27))
        print(' '.rjust(16),'*'*16,'\n')

        try:
    
            menu_num = input('Select Menu (by number!): '.rjust(10))
            print()
            switcher = {
                '1': signup,
                '2': signin,
                '3': 'exit'
                }
    
            selected_func = switcher.get(menu_num, wrong_number)
            if selected_func == 'exit': 
                break
            else:
                selected_func(db)
        except:
            print('')

def wrong_number(db):
    print('\nWrong Number')
    return 

def exit(db):
    client.close()
    print('Bye!')
    return

if __name__ == "__main__":
    mainpage(db)
    '''
    call mainpage()
    '''
