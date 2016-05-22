## AudioReader Prototype ##

##### vlc_prototype #####
+ Python prototype for finding a reader's position in a book using their 
audiobook progress. Scans audiobook .mp3 files in the directory, using
metadata to find total duration. Then requests an XML string containing
information about the file currently playing in VLC Media Player. The user's
completion percentage for the audiobook is then used to approximate their
location within a viewable version.

##### epub_prototype #####
+ Convert an epub file to text using ebook-convert and search for specific
phrases contained within. Using the index of those phrases and the total 
number of pages contained within a physical copy, approximate the reader's
position within a physical copy.
+ TODO: Automate epub-to-text conversions for each of the WOT books
+ TODO: Search for substrings based on speech-to-text conversion (could
alternatively transcribe using VLC and mp3 metadata)
+ TODO: Improve phrase searching using linear regressions

