# user.py
from post import *
from wall import *
from main import *
from follow import *
import getpass

def signup(db):
    '''
    1. Get his/her information.
    2. Check if his/her password is equal. Confirm the password.
    3. Check if the userid already exists.
    4. Make the user document.
    5. Insert the document into users collection.
    '''
    
    cont = 1
    while cont:
        #Get his/her information.
        id_ = input('ID: ')

        #Check if the userid already exists.
        if list(db.users.find({'id':id_})):
            print('Already exist')
            cont =eval(input('Do you want to try again? [1/0]'))
        
        else:
            password = 'abc'
            while len(password) < 5: 
                print('Enter password (more than 5 characters)')
                password = getpass.getpass('PASSWORD: ')
            re_pw = getpass.getpass('(RECHECK!) PASSWORD ')

            #Check if his/her password is equal. Confirm the password.
            if password == re_pw:
                print('We confirm your password successfully!')
            
                name = input('NAME: ')
                profile = input('PROFILE: ')
                
                #Make the user document & Insert the document into users collection.
                ins_res = db.users.insert_one({'id':id_, 'password':password, 'name':name, 'profile':profile, 'following':[], 'follower':[]})
                if ins_res.inserted_id:
                    
                    print('Sign up complete! Please sign in to use Monogostagram.')
                    
                    cont = 0
                else:
                    print('Failed to make an account.')
                    cont =eval(input('Do you want to try again? [1/0]'))
            else: 
                print('Fail! They are not equal')
                cont =eval(input('Do you want to try again? [1/0]'))


def signin(db):
    '''
    1. Get his/her information.
    2. Find him/her in users collection.
    3. If exists, print welcome message and call userpage()
    '''
    
    id_ = input('ID: ')
    password = getpass.getpass('PASSWORD: ')
    try:
        res = list(db.users.find({'id': id_, 'password': password}, {'name':1, '_id':0}))
        if len(res) != 1:
            print('We cannot find your ID. Please check your id or password. You can also sign up!')
            return 
        
    except:
        print('We cannot find your account. Please check your id or password. You can also sign up!')
        return 
    username = res[0]['name']
    print('\nWelcome, ', username, '.')
    return userpage(db, id_)
    
def mystatus(db, user):
    '''
    print user profile, # followers, and # followings
    '''
    print()
    print('='*50)
    print('\t\tMy status')
    print('='*50+'\n\n')
    result = list(db.users.find({'id': user}, {'profile':1, 'following':1, '_id':0, 'follower':1}))[0]
    profile = result['profile']
    following = len(result['following'])
    followers = len(result['follower'])
    print('Profile\n', profile, '\n\n')
    print('Following :', following, '\tFollowers:', followers)
    print()
    return userpage(db, user)


def userpage(db, user):
    '''
    user page
    '''
    print('\n:::::   User Page   :::::')

    print()
    print('1. My status')
    print('2. Newsfeed')
    print('3. Wall')
    print('4. Post')
    print('5. Search')
    print('6. Follow')
    print('7. Unfollow')
    print('8. Logout')
    print()
    menu_num = input('Enter: ')
    switcher = {
        '1': mystatus,
        '2': newsfeed,
        '3': wall,
        '4': post,
        '5': search,
        '6': follow,
        '7': unfollow,
        '8': logout}

    selected_func = switcher.get(menu_num, wrong_number)

    if selected_func == 'logout':
        pass
    else:
        selected_func(db, user)
        
def newsfeed(db, user):
    getNewsfeed(db,user)
    return userpage(db,user)

def wall(db, user):
    getPosts(db, user)
    return userpage(db, user)

def post(db, user):
    postInterface(db, user)
    return userpage(db, user)

def search(db, user):
    Hashtags(db, user)
    return userpage(db,user)
    
def follow(db, user):
    followNew(db, user)
    return userpage(db, user)

def unfollow(db, user):
    unfollowNew(db, user)
    return userpage(db, user)

        
def logout(db, user):
    print('Successfully logged out','\n')
    return 

def wrong_number(db, user):
    print('\nWrong Number')
    return userpage(db, user)
