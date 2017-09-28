import argparse
import logging
import os
import traceback

from bs4 import BeautifulSoup
from slugify import slugify

log = logging.getLogger(__name__)


class VideoRename:
    def __init__(self, index_file, movie_path, dry_run):
        self.index_file = index_file
        if movie_path[-1] == '\\':
            movie_path = movie_path[:-1]
        self.movie_path = movie_path
        self.dry_run = dry_run

    def rename(self):
        with open(self.index_file, 'r') as file_handle:
            soup = BeautifulSoup(file_handle, 'lxml')

        for file_name in soup.find_all('p', attrs={'class': 'filename'}):
            original_file_name = file_name.text.split(': ')[1]
            title_link = file_name.findPrevious('a', attrs={'class': 'title'})
            new_file_name = '{}-{}.mp4'.format(original_file_name[:-4], slugify(title_link.text))

            file_name.contents[1].replaceWith(new_file_name)
            title_link['href'] = 'movies/{}'.format(new_file_name)

            if not self.dry_run:
                try:
                    os.rename('{}/{}'.format(self.movie_path, original_file_name),
                              '{}/{}'.format(self.movie_path, new_file_name))
                except OSError:
                    pass

                log.info('File {} renamed to {}'.format(original_file_name, new_file_name))
            else:
                log.info('Generated new file name for {}: {}'.format(original_file_name, new_file_name))

        if not self.dry_run:
            with open(self.index_file, 'w') as file_handle:
                file_handle.write(soup.prettify().encode('utf-8'))
            log.info('New index file generated with updated filenames')


def setup_logger():
    logging.basicConfig(level=logging.DEBUG,
                        handlers=[logging.StreamHandler(), ],
                        format='%(asctime)s::%(name)s::%(levelname)s::%(message)s')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='video_rename: Rename all the videos')
    parser.add_argument('-i', '--index',
                        required=True,
                        help='Path to index file to parse')
    parser.add_argument('-m', '--movies',
                        required=True,
                        help='Path to directory containing video files')
    parser.add_argument('-d', '--dryrun',
                        action='store_true',
                        help='Dry-run, will not actually rename')

    args = parser.parse_args()
    setup_logger()

    try:
        video_rename = VideoRename(index_file=args.index, movie_path=args.movies, dry_run=args.dryrun)
        video_rename.rename()
    except KeyboardInterrupt:
        log.info('Exiting due to keyboard interrupt...')
    except Exception as e:
        log.error('Exiting due to unknown exception: {}'.format(traceback.format_exc()))
