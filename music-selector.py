import glob
import os
from random import shuffle
from distutils.dir_util import copy_tree
from __init__ import *


source_folder = "D:/Librairies/Music"
destination_folder = "C:/Users/laurent/Desktop/phone music"
max_size = 6e9 # bytes

always = {
    'America': ALL,
    'Daniel Bélanger': ALL,
    'First Aid Kit': ALL,
    'Genesis': ['1971 - Nursery Cryme', '1973 - Selling England by the Pound'],
    'Gentle Giant': ['(1971) Acquiring The Taste', '(1972) Octopus', '(1974) The Power And The Glory', '(1975) Free Hand', 'Moog Fugue'],
    'Harmonium': ALL,
    'Jack Johnson': ['In Between Dreams'],
    'Jean-Pierre Ferland': ALL,
    'Klô Pelgag': ALL,
    'La revoir': ALL,
    'Leloup': ['À Paradis City', 'La Vallée des Réputations'],
    'Les Cowboys Fringants': ['La Grand-Messe'],
    'Los Jaivas': ['1975 - Alturas De Macchu Picchu'],
    'Malajube': ALL,
    'Maneige': ALL,
    'Manu Chao': ['Clandestino'],
    'Naomi Shore': ALL,
    'Neil Young': ALL,
    'Noem': ALL,
    'Opus 5': ALL,
    'Pink Floyd': ['The Dark Side of the Moon', 'Animals'],
    # 'Sara Bareilles': ALL,
    'Simon & Garfunkel': ['Greatest Hits'],
    'Sloche': ALL,
    'Snarky Puppy': ALL,
    'Supertramp': ['Crime Of The Century'],
    'Tame Impala': ALL,
    'Tangerine Dream': ALL,
    'Temples': ALL,
    'The Alan Parsons Project': ALL,
    'The Black Keys': ['Turn Blue', 'El Camino'],
    'Tom Rosenthal': ALL,
}

ignore = {
    'JeanPierreFerland': ALL,
    'moi': ALL,
}

### ------------------------------------------------------------------------------------------------- ###

# Make sure destination folder is empty
if os.path.exists(destination_folder) and os.path.isdir(destination_folder):
    if len(os.listdir(destination_folder)) != 0:
        raise RuntimeError("Directory is not empty")
else:
    print("Given Directory don't exists")

# Convert 'always' and ignore' into list of tuples
always_list = []
for artist, albums in always.items():
    if albums == ALL:
        # get actual albums
        for album in [f.name for f in os.scandir(source_folder + '/' + artist) if f.is_dir()]:
            always_list.append((artist, album)) 
    else:
        for album in albums:
            always_list.append((artist, album)) 
            
ignore_list = []
for artist, albums in ignore.items():
    if albums == ALL:
        # get actual albums
        for album in [f.name for f in os.scandir(source_folder + '/' + artist) if f.is_dir()]:
            ignore_list.append((artist, album)) 
    else:
        for album in albums:
            ignore_list.append((artist, album)) 


# Extract list of all albums
all_albums = []
for artist in [f for f in os.scandir(source_folder) if f.is_dir()]:
    for album in [g for g in os.scandir(artist.path) if g.is_dir()]:
        # Check if album in 'ignore', if so don't append.
        if artist.name in ignore.keys():
            if (album.name in ignore[artist.name]) or (ignore[artist.name] == ALL):
                continue
        # Check if album in 'always', if so don't append. 
        # Will be appended for sure at the end, avoids to be selected twice.
        if artist.name in always.keys():
            if (album.name in always[artist.name]) or (always[artist.name] == ALL):
                continue
        all_albums.append((artist.name, album.name))


# Shuffle albums and append after "always" list
shuffle(all_albums)
selected_albums = always_list + all_albums


# Copy folders over to selection folder until max_size is busted

current_size = 0
for artist, album in selected_albums:
    from_ = source_folder + '/' + artist + '/' + album
    to_ = destination_folder + '/' + artist + '/' + album

    current_size += album_size(from_)
    print('Total size:', current_size/1e9, 'GB', '- Added', album, 'from', artist)
    if current_size > max_size:
        break
    copy_tree(from_, to_)

