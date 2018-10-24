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

def searchID(db, userid, follow = 1):
    cont = '1'
    while cont == '1':
        foll_id = input('Search ID: ')
        search = db.users.find_one({'id': foll_id}, {'_id':0, 'id':1, 'name':1, 'profile': 1})
        if not search:
            print('\nNo result. Would you like to try again? [1/0] ')
            cont = input()
            continue
        elif foll_id == userid:
            if follow == 1:
                print('\nYou cannot follow yourself. Would you like to try again? [1/0] ')
            else:
                print('\nYou cannot blacklist yourself. Would you like to try again? [1/0]')
            cont = input()
            continue

        print('\n\nSearch result\n')
        print('ID'.ljust(15), 'Name'.ljust(15), 'Profile')
        print(foll_id.ljust(15), search['name'].ljust(15), search['profile'])

        if follow == 1:
            follow_ok = input('\n\nWould you like to follow this user? [1/0] ')
            if follow_ok != '1':
                print('Going back to the user page')
                break
            else:
                black = db.users.find({'id':foll_id, 'blacklist':userid})
                dup = db.users.find({'id': userid, 'following': {'$in': [foll_id]}}).count()
                if dup != 0:
                    print('You are already following', foll_id)
                    break
                if not black:
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
                else:
                    print('[ERROR] Failed following', foll_id)
                    break
        else:
            return foll_id


def searchName(db, userid, follow = 1):
    cont, page, idxx = '1', 1, None
    while cont == '1':
        foll_name = input('Search Name: ')
        search = list(db.users.find({'$text': {'$search': foll_name}}))
        print(search)
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
        if follow == 1:
            idxx = input('\nType the user number that you want to follow. Type q to search for another name. ')
        else:
            idxx = input('\nType the user number that you want to blacklist. Type q to search for another name. ')
            
        if idxx == 'q': continue
        foll_id = search[int(idxx)]['id']
        if foll_id == userid:
            if follow == 1:
                print('You cannot follow yourself. Would you like to try again? [1/0] ')
            else:
                print('\nYou cannot blacklist yourself. Would you like to try again? [1/0]')
                
            cont = input()
            continue
            
        black = db.users.find_one({'id':foll_id, 'blacklist':userid})
        dup = db.users.find({'id': userid, 'following': {'$in': [foll_id]}}).count()
        if dup != 0 and follow == 1:
            print('You are already following', foll_id)
            break
            
        if follow == 1 and black:
            print('\n[ERROR] Failed following', foll_id)
            
        elif follow == 1 and not black:
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
        
        else:
            return foll_id








def unfollowNew(db, userid):
    """
    Unfollow someone.
    A user hopes to unfollows follwings.
    You can think that this function is the same as the follow but the action is opposite.
    The information apply to followings and followers both.
    Again, the confimation is helpful whether the user really wants to unfollow others.
    """
    while True:
        menu = input('\nSelect Menu\n1. Unfollow \n2. Blacklist\n3. Exit\n')
        if menu == '1':
            following = db.users.find_one({'id': userid}, {'following':1, '_id':0})['following']
            #print(following)
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
        elif menu == '2':
            blackList(db, userid)
        
        else:
            break
                      
def blackList(db, userid):
    try:
        while True:
            print('''
Please select the options below.
1. Put on a blacklist
2. Remove from a blacklist
3. Back
                  ''')
            opt = int(input(''))            
            if opt == 1:
                print('''
Please select the options below.
1. Search by ID
2. Search by name
3. Back
                      ''')
                want = int(input('Enter :'))
                if want == 1:
                    blck_id = searchID(db, userid, 0)
                elif want == 2:
                    blck_id = searchName(db, userid, 0)
                else: 
                    print('Going back to the userpage')
                    break

                if db.users.find_one({'id':userid, 'blacklist':blck_id}):
                    print(blck_id,' is already on the blacklist')
                    break

                else:
                    before = input('Do you really want to put', blck_id,'on your blacklist? [Y/N]')
                    if before in ['Y', 'y', 'yes','YES','Yes']:
                        check = db.users.update_one({'id':userid}, {'$push':{'blacklist':blck_id}})
                        my_info = db.users.find_one({'id':userid})
                        if_following = int(foll_id in my_info['following'])
                        if_follower = int(foll_id in my_info['follower'])

                        if check.modified_count == 1:
                            if if_following:
                                res1 = db.users.update_one({'id': userid}, {'$pull': {'following': foll_id}})
                                res2 = db.users.update_one({'id': foll_id}, {'$pull': {'follower': userid}})
                                if if_follwer:
                                    res3 = db.users.update_one({'id': userid}, {'$pull': {'follower': foll_id}})
                                    res4 = db.users.update_one({'id': foll_id}, {'$pull': {'following': userid}})
                                    if res1.modified_count + res2.modified_count + res3.modified_count + res4.modified_count == 4:
                                        print('\n*** Successfully added to the blacklist ***')
                                  
                                    else:
                                        print('\n[ERROR] Failed blacklisting', foll_id, 'Would you like to try again? [1/0] ')
                                        cont = input()
                                        if cont != '1':
                                            break
                                            
                                else:
                                    if res1.modified_count + res2.modified_count == 2:
                                        print('\n*** Successfully blacklisting ***')
                                  
                                    else:
                                        print('\n[ERROR] Failed blacklisting', foll_id, 'Would you like to try again? [1/0] ')
                                        cont = input()
                                        if cont != '1':
                                            break
                                            
                            else:
                                if if_follwer:
                                    res3 = db.users.update_one({'id': userid}, {'$pull': {'follower': foll_id}})
                                    res4 = db.users.update_one({'id': foll_id}, {'$pull': {'following': userid}})
                                    if res1.modified_count + res2.modified_count + res3.modified_count + res4.modified_count == 4:
                                        print('\n*** Successfully added to the blacklist ***')
                                  
                                    else:
                                        print('\n[ERROR] Failed blacklisting', foll_id, 'Would you like to try again? [1/0] ')
                                        cont = input()
                                        if cont != '1':
                                            break
                                else:
                                    print('\n*** Successfully added to the blacklist ***')

                        else: 
                            print('\n[ERROR] Failed blacklisting', foll_id, 'Would you like to try again? [1/0] ')
                            cont = input()
                            if cont != '1':
                                break
                    else:
                        print('\n*** Going back to the menu ***')
                        break
                 

            elif opt == 2:
                black_list = db.users.find_one({'id':userid})['blacklist']
                if black_list:
                    print('** YOUR BLACKLIST **')
                    for i in range(len(black_list)):
                        print('{:>5} {:>10}'.format(i+1, black_list[i] ))


                    idxx = input('\nType the user number that you want to remove from your blacklist. Type q to go back to the user page. ')
                    if idxx == 'q': break
                    else:
                        before = input('Do you really want to remove from your blacklist? [Y/N]')
                        if before in ['Y', 'y', 'yes','YES','Yes']:
                            check = db.users.update_one({'id':userid},{'$pull':{'blacklist': {'$in':[blck_id]}}})
                            if check.modified_count ==1:
                                print('\n*** Successfully removed ***')

                            else:
                                print('\n[ERROR] Failed removing', foll_id, ' from your blacklist. Would you like to try again? [1/0] ')
                                cont = input()
                                if cont != '1':
                                    break
                        else:
                            print('\n*** Going back to the menu ***')
                            break
                            
                else:
                    cont = input('\nEmpty list...Would you like to try again? [1/0]')
                    if cont != '1':
                        break
                    
            else:
                break
                

    except:
        raise
        print('Failed following. Try again.')
