import pathlib, regex as re
from mutagen import File

def get_duration(lis:list)->dict:
    info_dict={}
    for item in lis:
        audio=File(str(item[0]))
        info_dict[item[1]]=(audio.info.length,item[0])
    return info_dict

def language_detection(file_paths:list):

    for item in file_paths:
        
        english=r"^[\u0000-\u007F]+$"
        english_jp = r'^[\u0000-\u007F\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\uFF00-\uFFEF]+$'
        english_list=[]
        jp_list=[]
        if re.match(english,item.stem):
            english_list.append([item.absolute(),item.stem])
        
        elif re.match(english_jp,item.stem):
            jp_list.append([item.absolute(),item.stem])
        
        return english_list, jp_list

print(f"{"PlaylistMaker by KalerKaler":*^40}")

music_paths = list(pathlib.Path('.').rglob("*.mp3"))
if not music_paths:
    print("No files found! Make sure .mp3 files exist in the same directory.")
    exit()
english_list,jp_list=language_detection(music_paths)


print(f"Found {len(english_list)} English songs.")
print(f"Found {len(jp_list)} Japanese songs.")

english_duration_dict=get_duration(english_list)
english_playlist_name=input("Enter the name for the English playlist file\n")
with open(english_playlist_name+".m3u","w") as eng:
    eng.write("#EXTM3U\n")
    for item in english_duration_dict:
        eng.write(f"#EXTINF:{english_duration_dict[item][0]}, {english_duration_dict[item][1]}\n")
        eng.write(f"{item}\n")

japanese_duration_dict=get_duration(jp_list)
japanese_playlist_name=input("Enter the name for the Japanese playlist file\n")
with open(japanese_playlist_name+".m3u","w",encoding="UTF-8") as jp:
    jp.write("#EXTM3U\n")
    for item in japanese_duration_dict:
        jp.write(f"#EXTINF:{japanese_duration_dict[item][0]}, {japanese_duration_dict[item][1]}\n")
        jp.write(f"{item}\n")
