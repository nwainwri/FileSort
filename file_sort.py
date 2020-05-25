"""
Final Project for Standford 'Code In Place'

Program designed to take in a directory where user has alot of files unorganized,
create a directory tree based on a name user inputs, and organize them by year/month/day
with the date format being chosen by user.

Currently will not go into subdirectories, or move/copy any hidden files either.

Designed in mind for either large photo dumps from personal phones/tablets, or a large amount
of photos from multiple camera cards in a single folder.

**ONLY CURRENTLY WORKING ON MAC OS**

"""

import os
from datetime import datetime
import os.path
from shutil import copyfile
from shutil import move
import sys


def main():
    working_directory = get_user_directory_input()
    destination_folder_name = get_user_destination_folder()
    date_format = get_user_date_format()
    list_of_files = get_list_of_files(working_directory)
    file_dates = get_file_dates_and_names(working_directory, list_of_files, date_format)

    choice = get_user_move_or_copy_choice()
    if choice == True:
        create_filedate_directories(file_dates, destination_folder_name, working_directory)
        # at this point, create desination folder, and directory structure! incause user quits.
        move_files(list_of_files, working_directory, file_dates, destination_folder_name, date_format)
    elif choice == False:
        create_filedate_directories(file_dates, destination_folder_name, working_directory)
        copy_files(list_of_files, working_directory, file_dates, destination_folder_name, date_format)

"""
Pre Condition: none
Post Condition: User has inputted the name for the destination folder,
               for sorted files, no limits on it, as OSX doesn't 
               worry about invalid characters in folder names.
"""
def get_user_destination_folder():
    return input('Please enter name for destination folder: ')

"""
Pre Condition: User has inputted directory where files are location, 
              and named destination folder.
Post Condition: User has decided to either Move or Copy the files,
               also has the option to quit at this point in time.
"""

def get_user_move_or_copy_choice():
    global invalid_choice
    invalid_choice = True
    while invalid_choice:
        choice = input("Would you like to [M]ove or [C]opy the files, or [Q]uit: ")
        if (choice == "M") or (choice == "m"):
            invalid_choice = False
            return True
        elif (choice == "C") or (choice == "c"):
            invalid_choice = False
            return False
        elif (choice == 'q') or (choice == 'Q'):
            sys.exit("** Program Exited **")
        else:
            print("Invalid Option, please enter either [M]ove or [C]opy the files, or [Q]uit: ")

"""
Pre Condition: Dateformat isn't set for the destination directory sub-directories
Post Condition: User has inputted which of the four date formats they would like used,
               also has the option to quit.
"""

def get_user_date_format():
    print("What date format would you like to use?")
    global invalid_choice
    invalid_choice = True
    while invalid_choice:
        user_choice = input("[1] YYYY-MM-DD [2] YYYY-DD-MM [3] DD-YYYY-MM [4] MM-YYYY-DD , or [Q]uit: ")
        if user_choice == '1':
            invalid_choice = False
            return "%Y-%m-%d"
        elif user_choice == '2':
            invalid_choice = False
            return "%Y-%d-%m"
        elif user_choice == '3':
            invalid_choice = False
            return "%d-%m-%Y"
        elif user_choice == '4':
            invalid_choice = False
            return "%m-%Y-%d"
        elif (user_choice == 'q') or (user_choice == 'Q'):
            invalid_choice = False
            sys.exit("** Program Exited **")
        else:
            print("** Invalid Option. **")

"""
Pre Condition: none
Post Condition: Helper function, to get the date of the file currently being read,
               and formatting the date with the format chosen by User.
"""

def get_file_date(file, date_format):
    time_stamp = os.path.getctime(file)
    return datetime.fromtimestamp(time_stamp).strftime(date_format)

"""
Pre Condition: Takes in the current working directory, list of files to be sorted, 
              and users chosen date format.
Post Condition: Will return a dictionary where the keys are dates found in the list of files,
               and each date has a list of files attached that are valid for each of those dates.
"""

def get_file_dates_and_names(working_directory, list_of_files, date_format):

    # this will just created dictionary with file dates ONLY
    file_dates = {}
    for each in list_of_files:
        # need working dir
        current_file = working_directory + '/' + each
        file_dates[get_file_date(current_file, date_format)] = []

    # this will iterate thru that list again,
    # and check each file date, against key, if match, append to the list
    # that's IN that' Keys spot.
    for each in list_of_files:
        current_file = working_directory + '/' + each
        current_date = get_file_date(current_file, date_format)
        if (current_date) in file_dates:
            file_dates[current_date].append(current_file)
    return file_dates

"""
Pre Condition: Takes in, file_dates dictionary, the destination folder name, and 
              working directory.
Post Condition: Will then create the subdirectories, in the destination folder,
               using the keys (dates) in file_dates as the names for those folders.
"""

def create_filedate_directories(file_dates, destination_folder_name, working_directory):
    path = working_directory + '/' + destination_folder_name
    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("** Created destination folder: %s " % path)

    for key in file_dates:
        path = working_directory + '/' + destination_folder_name + "/" + key
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        # else:
        #     print("Successfully created the directory %s " % path)
    print("** Successfully created the sub-folders for the sorted files.")

"""
Pre Condition: Takes in the list of files, working directory, file dates dictionary, destination folder
              name, and date format.
Post Condition: Will then copy the files from original working directory, to the destination folder,
               in the appropriate sub folder under that files date, according to the date format chosen.
"""

def copy_files(list_of_files, working_directory, file_dates, destination_folder_name, date_format):
    #copy files into appropriate directories
    # progress bar pulled from :: https://stackoverflow.com/questions/3002085/python-to-print-out-status-bar-and-percentage
    for index, each in enumerate(list_of_files):
        sys.stdout.write('\r')
        source = working_directory + '/' + each
        current_date = get_file_date(source, date_format)
        if (current_date) in file_dates:
            destination = working_directory + '/' + destination_folder_name + '/' + current_date + '/' + each
            copyfile(source, destination)
        current = index + 1
        # sys.stdout.write("[%-20s] %d%%" % ('=' * current, current/len(list_of_files)*100))
        sys.stdout.write("** %d%%" % (current/len(list_of_files)*100))
        sys.stdout.flush()
    sys.stdout.write('\r')
    print('** Done Copying Files **')

"""
Pre Condition: Takes in the list of files, working directory, file dates dictionary, destination folder
              name, and date format.
Post Condition: Will then move the files from original working directory, to the destination folder,
               in the appropriate sub folder under that files date, according to the date format chosen.
"""

def move_files(list_of_files, working_directory, file_dates, destination_folder_name, date_format):
    #copy files into appropriate directories
    for index, each in enumerate(list_of_files):
        sys.stdout.write('\r')
        source = working_directory + '/' + each
        current_date = get_file_date(source, date_format)
        if (current_date) in file_dates:
            destination = working_directory + '/' + destination_folder_name + '/' + current_date + '/' + each
            move(source, destination)
        current = index + 1
        sys.stdout.write("** %d%%" % (current / len(list_of_files) * 100))
        sys.stdout.flush()
    sys.stdout.write('\r')
    print('** Done Moving Files **')

"""
Pre Condition: none
Post Condition: User has inputted the directory 
                where files are to be sorted from,
                function will output a list of filenames.
"""
def get_user_directory_input():
    global directory_invalid
    directory_invalid = True
    print('** NOTE: this program will only copy directories with non-hidden files only.')
    print('** It will also ** IGNORE ** subdirectories, in the working directory.')
    print('** The final location of the moved/copied files will be in the ** DESTINATION ** directory.')
    print('** You have the option to [Q]uit')
    while directory_invalid:
        user_choice = input('Where are your files located? [DIRECTORY]: ')
        if os.path.isdir(user_choice):
            directory_invalid = False
        elif (user_choice == 'q') or (user_choice == 'Q'):
            sys.exit("** Program Exited **")
        else:
            print("Directory isn't valid, please enter a valid location.")

    last_char = len(user_choice) - 1
    if user_choice[last_char] == '/':
        # have this incase user adds "/"
        return user_choice[:-1]
    else:
        return user_choice

"""
Pre Condition: Takes in the working directory location.
Post Condition: Will output a list of files, as strings; will ignore hidden
               files, and sub-folders.
"""

def get_list_of_files(working_directory):
    list_of_files = []
    for file in files(working_directory):
        if file[0] != '.': #ignore hidden files (starting with '.'
            list_of_files.append(file)
    total_number_of_files = len(list_of_files)
    print('** Total number of files to be sorted: ', total_number_of_files)
    return list_of_files

"""
Pre Condition: none
Post Condition: Helper function to be able to quickly check if file is a directory, 
               will only return valid files, not directories.
"""

# https://stackoverflow.com/questions/14176166/list-only-files-in-a-directory
# found this to be a simpler method, then double looping/sorting, and for efficiency/speed.
def files(path):
    for file in os.listdir(path):
        #ensure that only files are being copied, no whole directories
        if os.path.isfile(os.path.join(path, file)):
            yield file

if __name__ == '__main__':
    main()
