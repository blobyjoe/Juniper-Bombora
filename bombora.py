print('Loading Modules')
import pandas as pd
from glob import glob

print("Loading files")
#locate most recent data files downloaded
accounts = glob('Accounts_Surging_crosstab*')
accounts.sort()
print("Using ", accounts[-1])
contacts = glob('Contact_Sheet_crosstab*')
contacts.sort()
print("Using ", contacts[-1])

#import account list
accountsSurging = pd.read_csv(accounts[-1], skiprows=1, delimiter='\t', encoding="UTF-16")
print(accountsSurging.head(5))

#remove company duplicates that result from hyping on multiple keywords
accountsSurging.drop_duplicates(subset ="Domain", keep = 'first', inplace = True)

#import contact list
contactList = pd.read_csv(contacts[-1], delimiter='\t', encoding="UTF-16")
try:
    accountsSurging, contactList
except NameError:
    print("Files not found!")
else:
    print("Files loaded.")

#Third attempt: Pandas Vectorization. Supposed to not need a loop, improving search time, WORK IN PROGRESS

# surgingList = surgingList.append(contactList.loc[contactList['Domain'] == accountsSurging['Domain']], ignore_index=true)


#New Stackoverflow Attempt based on index and boolean finding. !!This works but is slow, ABOUT 3 MIN runtime!!

surgingList = pd.DataFrame(columns = ['Company Name','Domain','Employee First Name','Employee Last Name','Employee Title','Employee Job Functions','Employee Work Email','Employee Direct Phone','Industry','Company HQ Phone','Employee LinkedIn URL','Company Revenue','Company IT Budget (Mil)','Number of Employees','Company IT Employees'])

#Third attempt: Pandas Vectorization. Supposed to not need a loop, improving search time.

# surgingList = surgingList.append(contactList.loc[contactList['Domain'] == accountsSurging['Domain']], ignore_index=true)



#New Stackoverflow Attempt based on index and boolean finding. !!This works but is extremely slow!!
print("Searching for contacts, please wait...")

for domain in accountsSurging['Domain']:
    if not contactList.loc[contactList['Domain'] == domain].empty:
        data = contactList.loc[contactList['Domain'] == domain]
        surgingList = surgingList.append(data, ignore_index=True, sort=False)



#Original Attempt. Doesn't work at all, because I never set the blank surgingList dataframe to be the new .concat() value

# for domain in accountsSurging['Domain']:
#      print(domain)
#     if not contactList[contactList['Domain'].str.match(domain)].empty:
#         print(contactList[contactList['Domain'].str.match(domain)])
#         surgingList.append(contactList[contactList['Domain'].str.match(domain)], ignore_index=True)
#     else:
#         print(contactList['Domain'].str.match(domain))
#         surgingList.append(contactList[contactList['Domain'].str.match(domain)], ignore_index=True)
#         pd.concat([surgingList, contactList], sort=False)


print("Contacts found. Rearranging columns and sending list to Output.csv in this directory.")
#surgingList = surgingList.reindex(surgingList.columns.tolist() + ['Lead Owner','Inside Sales Source','Campaign ID','Campaign Status','Lead Source','Lead Type','Lead Status','Inside Sales Event','Telemarketing','Rating','Theater','Description','Country','Salutaion','Self Reported Employee Count','Address Line 1','Address Line 2','Address Line 3','City','Postal Code'], axis=1)


surgingList.to_csv('Output.csv')
print("Done!")
