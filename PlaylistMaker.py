import pathlib, regex as re
from mutagen import File

def get_duration(lis:list)->dict:
    info_dict={}
    for item in lis:
        audio=File(str(item[0])) #Extracts all data from  file
        info_dict[item[1]]=(audio.info.length,item[0]) #Adds duration and path tuple to Title key in info_dict
    return info_dict

#This function divides the songs into sub lists based on language
def language_detection(file_paths:list)->list:

    english=r"^[\u0000-\u007F]+$" #Regex pattern for english
    english_jp = r'^[\u0000-\u007F\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\uFF00-\uFFEF]+$' #Regex for JP
    english_list=[]
    jp_list=[]
    unclassified=[]
    for item in file_paths:
        
        if re.match(english,item.stem): #If name regex pattern matches english regex pattern
            english_list.append([item.absolute(),item.stem])
            
        
        elif re.match(english_jp,item.stem):
            jp_list.append([item.absolute(),item.stem])
        
        else:
            unclassified.append(item)
    
    return english_list, jp_list, unclassified

print(f"{"PlaylistMaker by KalerKaler":*^40}")

extensions=(".mp3",".flac",".m4a",".ogg")
music_paths = [_ for _ in pathlib.Path(".").rglob("*") if _.suffix.lower() in extensions] #Finds files with the pre-defined extentions
if not music_paths:
    print("No files found! Make sure music files exist in the same directory.")
    exit()
    
english_list, jp_list, unknown=language_detection(music_paths)

print(f"Found {len(english_list)} English songs.")
print(f"Found {len(jp_list)} Japanese songs.")
print(f"Found {len(unknown)} songs in an unknown language.")

lists=(english_list, jp_list)

for index, item in enumerate(lists):
    if item:
        duration_dict=get_duration(item)
        playlist_name=input(f"Enter the name for {"Japanese" if index else "English"} playlist\n")
        with open(playlist_name+".m3u","w", encoding="UTF-8") as plt:
            plt.write("#EXTM3U\n")
            for itm in duration_dict:
                plt.write(f"#EXTINF:{duration_dict[itm][0]}, {duration_dict[itm][1]}\n")
            
print("Done! Have fun listening :)")
