from bson.son import SON

def followNew(db, userid):
    """
    Get the followers.
    This function updates information that is user's followers or followings.
    Note that if a user asks following to someone, the follower's information should be also updated.
    Remember, you may regard duplicates and the situation that the follower does not exists.
    """
    while True:

        following = db.users.find_one({'id': userid}, {'following':1, '_id':0})
        print('''
Please select the options below.
1. Search by ID
2. Search by name
3. Back
              ''')
        try:
            opt = int(input(''))            
            if opt == 1:
                searchID(db, userid)
            elif opt == 2:
                searchName(db, userid)
            else:
                break
        except:
            raise
            print('Failed following. Try again.')


    #ins_res = db.users.insert_one({'id':id_, 'password':password, 'name':name, 'profile':profile, 'following':[], 'follower':[]})

def searchID(db, userid):
    cont = '1'
    while cont == '1':
        foll_id = input('Search ID: ')
        search = db.users.find_one({'id': foll_id}, {'_id':0, 'id':1, 'name':1, 'profile': 1})
        if not search:
              print('\nNo result. Would you like to try again? [1/0] ')
              cont = input()
              continue
        elif foll_id == userid:
            print('\nYou cannot follow yourself. Would you like to try again? [1/0] ')
            cont = input()
            continue

        print('\n\nSearch result\n')
        print('ID'.ljust(15), 'Name'.ljust(15), 'Profile')
        print(foll_id.ljust(15), search['name'].ljust(15), search['profile'])

        follow_ok = input('\n\nWould you like to follow this user? [1/0] ')
        if follow_ok != '1':
              print('Going back to the user page')
              break
        else:
              dup = db.users.find({'id': userid, 'following': {'$in': [foll_id]}}).count()
              if dup != 0:
                  print('You are already following', foll_id)
                  break
              try:
                  res1 = db.users.update_one({'id': userid}, {'$push':{'following': foll_id}})
                  res2 = db.users.update_one({'id': foll_id}, {'$push': {'follower': userid}})
                  if res1.modified_count == 1 and res2.modified_count == 1:
                      print('Successfully followed', foll_id)
                      break
                  else:
                      print('[ERROR] Failed following', foll_id, 'Would you like to try again? [1/0] ')
                      cont = input()
                      continue
              except:
                  print('[ERROR] Failed following', foll_id)
                  
        break


def searchName(db, userid):
    cont, page, idxx = '1', 1, None
    while cont == '1':
        foll_name = input('Search Name: ')
        search = list(db.users.find({'$text': {'$search': foll_name}}))
        total_pages = len(search)//10 if len(search) % 10 ==0 else len(search)//10 + 1
        
        if not search:
            print('\nNo result. Would you like to try again? [1/0] ')
            cont = input()
            continue

        print('\n\nSearch result\n')
        print('Num'.ljust(10), 'ID'.ljust(15), 'Name'.ljust(15), 'Profile')

        while page > 0:
            for idx, user in enumerate(search[(page - 1) * 10:page * 10]):
                print(str(idx).ljust(10), user['id'].ljust(15), user['name'].ljust(15), user['profile'])
            print('\n',page,'/', total_pages)
            a = 0
            if total_pages != 1:
                a = input('Do you wish to see another page? [1/0] ')
            if a == '1':
                try:
                    page = eval(input('\nWhat page do you want to see?: '))
                    while page > total_pages:
                        print('There are only', total_pages, 'pages.')
                        page = eval(input('\nWhat page do you want to see?: '))
                    continue
                   
                except:
                    print('[ERROR]')
            else:
                break
        idxx = input('\nType the user number that you want to follow. Type q to search for another name. ')
        if idxx == 'q': continue
        foll_id = search[int(idxx)]['id']
        if foll_id == userid:
            print('You cannot follow yourself. Would you like to try again? [1/0] ')
            cont = input()
            continue
        dup = db.users.find({'id': userid, 'following': {'$in': [foll_id]}}).count()
        if dup != 0:
            print('You are already following', foll_id)
            break
        try:
            res1 = db.users.update_one({'id': userid}, {'$push':{'following': foll_id}})
            res2 = db.users.update_one({'id': foll_id}, {'$push': {'follower': userid}})
            if res1.modified_count == 1 and res2.modified_count == 1:
                print('Successfully followed', foll_id)
                break
            else:
                print('[ERROR] Failed following', foll_id, 'Would you like to try again? [1/0] ')
                cont = input()
                continue
        except:
            print('[ERROR] Failed following', foll_id)








def unfollowNew(db, userid):
    """
    Unfollow someone.
    A user hopes to unfollows follwings.
    You can think that this function is the same as the follow but the action is opposite.
    The information apply to followings and followers both.
    Again, the confimation is helpful whether the user really wants to unfollow others.
    """
    while True:
        following = db.users.find_one({'id': userid}, {'following':1, '_id':0})['following']
        print('Num'.ljust(10), 'ID'.ljust(15), 'Name'.ljust(15), 'Profile')        
        for k, i in enumerate(following):
            person = db.users.find_one({'id': i}, {'_id':0})
            print(str(k).ljust(10), i.ljust(15), person['name'].ljust(15), person['profile'])
        idxx = input('\nType the user number that you want to unfollow. Type q to go back to the user page. ')
        if idxx == 'q': break
        try:
            foll_id = following[int(idxx)]
            areyousure = input('Do you wish to unfollow '+str(foll_id)+'? [1/0] ')
            if areyousure != '1':
                continue
            res1 = db.users.update_one({'id': userid}, {'$pull': {'following': foll_id}})
            res2 = db.users.update_one({'id': foll_id}, {'$pull': {'follower': userid}})
            if res1.modified_count == 1 and res2.modified_count == 1:
                print('Successfully unfollowed', foll_id)
                break
            else:
                print('[ERROR] Failed unfollowing', foll_id, 'Would you like to try again? [1/0] ')
                cont = input()
                if cont != '1':
                    break
                    
        except IndexError:
            print('[ERROR] Unavailable number')
            
        except:
            print('[ERROR]')
            
            
            
            
            
