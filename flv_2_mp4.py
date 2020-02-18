# -*- coding: UTF-8 -*-
#----Folder Define----
rec_dir = "/mnt/download/_record"
out_dir = "/mnt/download/_output" 
#----Other Define-----
cores = 1             #ffmpeg using cores
file_time = 10        #Minuets of wating files

import os
import sys
import time
import subprocess

def file_gothrough(path,suffix):
    file_list=[]
    for root,dirs,files in os.walk(path):
        for file in files:
            if file[-3:]==suffix:
               file_list.append(os.path.join(root,file))
    return file_list

flv_files=file_gothrough(rec_dir,'flv')
os.system("cd "+ rec_dir + "&& find . -type d | cpio -pdvm "+ out_dir +">/dev/null 2>&1")

for flv_file in flv_files:
    mtime = os.stat(flv_file).st_mtime
    now_time = time.time()
    time_diff = (now_time - mtime)/file_time
    mp4_file = flv_file.replace(".flv", ".mp4")
    mp4_file = mp4_file.replace(rec_dir,out_dir)
    if time_diff > 30 :
        print("Converting..." + flv_file)
        subprocess.call(['nice', '-n', '-10', 'ffmpeg', '-loglevel', 'quiet', '-y', '-threads', 'cores' , '-i', flv_file, '-c', 'copy', mp4_file])
        print("Done..." + mp4_file)
        #Check and Delete
        mp4_size=os.path.getsize(mp4_file)
        flv_size=os.path.getsize(flv_file)
        if (mp4_size * 100 / flv_size) > 96 :
            print ("File Good")
            os.remove(flv_file)
#Clear Folder
os.system("find "+rec_dir+" -type d -empty | xargs -n 1 rm -rf")
os.system("find "+out_dir+" -type d -empty | xargs -n 1 rm -rf")