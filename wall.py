import datetime

def getPosts(db,userid, delete = 0):
    """
    Display your posts. Of course, get all posts would be fine.
    However, the function that supports displaying a few posts, e.g., five posts, looks much better than displaying all posts.
    Remind the lab8 that dealt with cursor.
    """
    try:
        data = list(db.posts.find({'posting_id':userid}).sort('date', -1))
        
        if len(data) == 0:
            print('There are no posts.')
            return 
        
        total_pages = len(data)//5 if len(data) % 5 ==0 else len(data)//5 + 1
        page = 1
            
        a = 1
        while a:

            if page <= total_pages:
                print()
                print('Num'.ljust(10), 'Date'.ljust(25), 'Content'.ljust(10))
                if page == total_pages:
                    end = len(data)-1
                    for order in range((page-1)*5, len(data)):
                        print(str(order+1).ljust(10), str(data[order]['date'])[:-7].ljust(25), str(data[order]['text']).ljust(10))
                else:
                    end = page*5-1
                    for order in range((page-1)*5, page*5):
                        print(str(order+1).ljust(10), str(data[order]['date'])[:-7].ljust(25), str(data[order]['text']).ljust(10))
                        
                print('\n',page,'/', total_pages)
                
                if delete == 0:
                    #1-based indexing
                    comm = eval(input('\nIf you want to see comments, please enter the post number. Enter 0 to go back: '))
                    if (page-1)*5 <= comm - 1 <= end:
                        print('\n[comments]\n')
                        print('{:>10} {:>10} {:>10}'.format('name', 'comment', 'date'))
                        comments = data[comm-1]['comments']
                        for i in comments:
                            print(i)

                
                print('\nTotal page number: ', total_pages)
                a = eval(input('\nDo you wish to see another page? [1/0]: '))
                if a == 1:
                    page = eval(input('\nWhat page do you want to see?: '))

            else:
                print('\nNo page!')
                a = eval(input('\nContinue? [1/0]: '))
                if a == 1:
                    print('\nTotal page number: ', total_pages)
                    page = eval(input('\nWhat page do you want to see?: '))
    
        if delete == 1:
            return data
    
    except:
        print('Error!')


def getNewsfeed(db,user):
    try:
        following_list = db.users.find_one({'id':user, },{'_id':0, 'following':1})['following']  #following하고 있는 사람들만 보여주기
        data = list(db.posts.find({'posting_id':{'$in':following_list}}).sort('date', -1))
        
        if len(data) == 0:
            print('There are no posts.')
            return 
        
        total_pages = len(data)//5 if len(data) % 5 ==0 else len(data)//5 + 1
        page = 1
            
        a = 1
        while a:

            if page <= total_pages:
                print('Num'.ljust(10), 'Date'.ljust(25), 'Name'.ljust(10), 'Content'.ljust(10))
                if page == total_pages:
                    end = len(data)-1
                    for order in range((page-1)*5, len(data)):
                        print(str(order+1).ljust(10), str(data[order]['date'])[:-7].ljust(25),str(data[order]['posting_name']).ljust(10),
                              str(data[order]['text']).ljust(10))
                else:
                    end = page*5-1
                    for order in range((page-1)*5, page*5):
                        print(str(order+1).ljust(10), str(data[order]['date'])[:-7].ljust(25), str(data[order]['posting_name']).ljust(10),
                              str(data[order]['text']).ljust(10))
                        
                        
                print('\n',page,'/', total_pages)
                

                #1-based indexing
                comm = eval(input('\nIf you want to see comments, please enter the post number. Enter 0 to go back: '))
                if (page-1)*5 <= comm - 1 <= end:
                    print('\n[comments]\n')
                    print('Num'.ljust(10), 'Date'.ljust(25), 'Name'.ljust(10), 'Content'.ljust(10))
                    comments = data[comm-1]['comments']
                    for i in range(len(comments)):
                        current = comments[i]
                        print(str(i+1).ljust(10), str(current['date'])[:-7].ljust(25),str(current['name']).ljust(10),
                              str(current['comment']).ljust(10))
                

                    comment = input('\nSelect Menu \n 1. Commenting on this post \n 2. Delete your comments \n 3. Exit\n ')
                    if comment == '1':
                        commentFunc(db, user, data[comm-1], 1)
                        data = list(db.posts.find({'posting_id':{'$in':following_list}}).sort('date', -1))

                    if comment == '2':
                        commentFunc(db, user, data[comm-1], 2)
                        data = list(db.posts.find({'posting_id':{'$in':following_list}}).sort('date', -1))
                    
                else:
                        a = eval(input('\nDo you wish to see another page? [1/0]: '))
                        if a == 1:
                            print('\nTotal page number: ', total_pages)
                            page = eval(input('\nWhat page do you want to see?: '))

            else:
                print('\nNo page!')
                a = eval(input('\nContinue? [1/0]: '))
                if a == 1:
                    print('\nTotal page number: ', total_pages)
                    page = eval(input('\nWhat page do you want to see?: '))

    
    except:
        print('Error!')
        
        
def commentFunc(db, user, posting, new = 1):
    try:
        if new == 1:
            name = db.users.find_one({'id':user}, {'name':1, '_id':0})['name']
            new_comment = input('\nComment :')
            b = db.posts.update({'_id':posting['_id']},
                                {'$push':{'comments':{'id': user, 'name':name, 'comment': new_comment, 'date': datetime.datetime.utcnow()}}})
            if b['nModified'] == 1:
                print('\nCommented successfully!')
                
            else:
                print('\nFailed! Please try again')
                
        elif new == 2:
            num = eval(input('\nplease enter the comment number you want to delete\n'))
            if posting['comments'][num-1]['id'] == user:
                check = db.posts.update({'_id':posting['_id']}, {'$pull':{'comments': {'$in':[posting['comments'][num-1]]}}})
                if check['nModified'] == 1:
                    print('\nDeleted successfully!\n')
                else:
                    print('\nFailed! Please try again\n')
            
            else:
                print('\nThis is not your comment.\n')
    except:
        print('\n[ERROR]\n')
    
        
        
def Hashtags(db, user):
    try:
        a = 1
        while a:
            search = input('\nEnter a hashtag: ')
            search = '#' + search
            data = list(db.posts.find({'hashtags':search}))

            total_pages = len(data)//5 if len(data) % 5 ==0 else len(data)//5 + 1
            page = 1
        
        
            if data:    
                if page <= total_pages:
                    print('Num'.ljust(10), 'Date'.ljust(25), 'Name'.ljust(10), 'Content'.ljust(10))
                    #print('{:>10} {:>10} {:>10}'.format('num','Date', 'Content'))
                    if page == total_pages:
                        end = len(data)-1
                        for order in range((page-1)*5, len(data)):
                            print(str(order+1).ljust(10), str(data[order]['date'])[:-7].ljust(25),str(data[order]['posting_name']).ljust(10),
                                  str(data[order]['text']).ljust(10))
                    else:
                        end = page*5-1
                        for order in range((page-1)*5, page*5):
                            print(str(order+1).ljust(10), str(data[order]['date'])[:-7].ljust(25), str(data[order]['posting_name']).ljust(10),
                                  str(data[order]['text']).ljust(10))

                    print('\n',page,'/', total_pages)


                    #1-based indexing
                    comm = eval(input('\nIf you want to see comments, please enter the post number. Enter 0 to go back: '))
                    if (page-1)*5 <= comm - 1 <= end:
                        print('\n[comments]\n')
                        print('{:>10} {:>10} {:>10}'.format('name', 'comment', 'date'))
                        comments = data[comm-1]['comments']
                        for i in comments:
                            print(i)


                    print('\nTotal page number: ', total_pages)
                    a = eval(input('\nDo you wish to search for another hashtag? [1/0]: '))
                        
                else:
                    print('\nNo page!')
                    a = eval(input('\nContinue? [1/0]: '))
                    if a == 1:
                        print('\nTotal page number: ', total_pages)
                        page = eval(input('\nWhat page do you want to see?: '))
            else:
                print('\nNo result')
                a = eval(input('\nDo you wish to search for another hashtag? [1/0]: '))

    
    except:
        print('Error!')

