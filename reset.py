import os,shutil

if input("Are you sure you want to reset the system (yes/no)?\n").lower() == 'yes': # confirm #1
    if input("Confirm one more time (yes/no)?\n").lower() == 'yes': # confirm #2
        try:shutil.rmtree('slides')
        except:0
        os.remove('database.db')