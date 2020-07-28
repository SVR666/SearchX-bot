import os
import re
print("\n\n"\
      "        Bot is not able to search in subfolder so if you likes to search\n"\
      "        in a specific folder then u can add that folder id to search\n\n"
      "        drive/folder NAME      -->   anything that u likes\n"\
      "        drive/folder ID        -->   drive id or folder id of folders in which u likes to search\n"\
      "        drive/folder INDEX URL -->   enter index url. If its a folder then open your index site\n" \
      "                                     goto the respective folder and copy the url from address bar\n")
msg = ''
if os.path.exists('drive_folder'):
    with open('drive_folder', 'r+') as f:
        lines = f.read()
    if not re.match(r'^\s*$', lines):
        print(lines)
        print("\n\n"\
              "      DO YOU WISH TO KEEP THE ABOVE DETAILS THAT YOU PREVIOUSLY ADDED???? ENTER (y/n)\n"\
              "      IF NOTHING SHOWS ENTER n")
        while (1):
            choice = input()
            if choice == 'y' or choice == 'Y':
                msg = f'{lines}'
                break
            elif choice == 'n' or choice == 'N':
                break
            else:
                print("\n\n      DO YOU WISH TO KEEP THE ABOVE DETAILS ???? y/n <=== this is option ..... OPEN YOUR EYES & READ...")
num = int(input("    How Many Drive/Folder You Likes To Add : "))
count = 1
while count <= num :
    print(f"\n        > DRIVE/FOLDER - {count}\n")
    name  = input("    Enter Drive/Folder NAME  (anything)     : ")
    id    = input("    Enter Drive/Folder ID                   : ")
    index = input("    Enter Drive/Folder INDEX URL (optional) : ")
    if not name or not id:
        print("\n\n        ERROR : Dont leave the name/id without filling.")
        exit(1) 
    name=name.replace(" ", "_")
    if index:
        if index[-1] == "/":
            index = index[:-1]
    else:
        index = ''
    count+=1
    msg += f"{name} {id} {index}\n"
with open('drive_folder', 'w') as file:
    file.truncate(0)
    file.write(msg)
print("\n\n    Done!")