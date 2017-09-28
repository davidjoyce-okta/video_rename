# Video Rename for BlackHat/DEFCON videos

- Set up a Python 2.7.x virtual environment
- Run: `pip install -r requirements.txt`

Run via the command line:

```bash
python video_rename.py -i "/Users/someguy/Documents/Defcon & BlackHat 2017/BlackHat 2017/BlackHat2017.html" -m "/Users/someguy/Documents/Defcon & BlackHat 2017/BlackHat 2017/movies"
```

Usage:
```bash
usage: video_rename.py [-h] -i INDEX -m MOVIES [-d]

video_rename: Rename all the videos

optional arguments:
  -h, --help            show this help message and exit
  -i INDEX, --index INDEX
                        Path to index file to parse
  -m MOVIES, --movies MOVIES
                        Path to directory containing video files
  -d, --dryrun          Dry-run, will not actually rename
```
