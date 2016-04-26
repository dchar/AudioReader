# AudioReader Prototype #

Python prototype for finding a reader's position in a book using their 
audiobook progress. Scans audiobook .mp3 files in the directory, using
metadata to find total duration. Then requests an XML string containing
information about the file currently playing in VLC Media Player. The user's
completion percentage for the audiobook is then used to approximate their
location within a viewable version.


