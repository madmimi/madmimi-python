# Mad Mimi for Python

Written, and released into the public domain by tav@espians.com

# General Usage

mimi = MadMimi('your username', 'your api key')

mimi.lists() <-	retrieve your current lists

mimi.delete_list('test') <- delete a list

mimi.add_list('test_list') <- add a list

mimi.add_contact(['Tav', 'Espian', 'tav@espians.com']) <- add a new contact

mimi.subscribe('tav@espians.com, 'test_list') <- subscribe a contact to a certain list

mimi.subscriptions('tav@espians.com') <- get subscriptions for a certain email

mimi.unsubscribe('tav@espians.com', 'test_list') <- unsubscribe a certain email