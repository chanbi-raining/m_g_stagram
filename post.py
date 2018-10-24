from user import *
from wall import getPosts
import datetime
import re

def postInterface(db, user):
    """
    Implementing the interface to post your text.
    There are three or more items to choose functions such as inserting and deleting a text.
    """
    try:
        while True:
            print()
            print('1. Insert Post')
            print('2. Delete Post')
            print('3. Back')
            print()
       
            menu_num = input('Enter: ')
        
            if menu_num == '1':
                username = db.users.find({'id': user})[0]['name']
                return insertPost(db, user, username)
            
            elif menu_num == '2':
                return deletePost(db, user)
            
            elif menu_num == '3':
                return
            
            else: 
                print('\nWrong Number')

        
    except:
        print('[Error] Sorry, please try again')
        return userpage(db, user)
    

def insertPost(db, userid, username):
    """
    Insert user's text. You should create the post schema including,
    for example, posting date, posting id or name, and comments.
    
    You should consider how to delete the text.
    """
    try:
        while True:
            text = input('Insert whatever you want! \n')
            check = input('[Recheck] Do you want to post ? [1/0] \n')
            

            if check == '1':
                hashtags = re.findall('#\w+',text)
                result = db.posts.insert_one({'posting_id': userid, 'posting_name': username, 
                                     'date':datetime.datetime.utcnow(), 'text': text, 'comments':[], 'hashtags':hashtags})
                if result.inserted_id:
                    print('Posted successfully!')
                    break
                else:
                    print('Failed... please try again')

            else: 
                print('Back to the user page')
                break

    except:
        print('[Error] Sorry, please try again')


    


def deletePost(db, user):
    """
    Delete user's text.
    With the post schema, you can remove posts by some conditions that you specify.
    """

    """
    Sometimes, users make a mistake to insert or delete their text.
    We recommend that you write the double-checking code to avoid the mistakes.
    """
    try:
        data = getPosts(db, user, delete = 1)
        number = eval(input('Tell me the number you want to delete: '))
        a = input('[Recheck] Are you sure you want to delete this post? [1/0] ')
        if a == '0':
            print('Back to the user page.')
            return
        id_ = data[number - 1]['_id']
        
        result = db.posts.delete_one({'_id': id_})
        if result.deleted_count:
            print('Deleted successfully!')
        else:
            print('Failed... please try again')
 
    except:
        print('Error!')


    
    
def wrong_number(db, user):
    print('\nWrong Number')
    return postInterface(db, user)
