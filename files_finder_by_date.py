import os
import time
import datetime
from typing import Iterable


class FilesFinderByDate:
    """
    Class for finding files by given start and end dates.

    After finding process, in terminal will be printed
    how many files are founded and where information will be saved.

    Actual info about founded files will be saved into
    "founded_table.txt" file in output folder
    (and "founded_list_sorted.txt", "founded_table_sorted.txt" files
    if `sort_info` parameter is True).

    Info files will be created automatically, but only
    if they don't exist in output folder, otherwise
    new info will be appended to existing files.

    The output files will contain:

    - script start time

    - start date for finding files

    - end date for finding files

    - table (or list) of founded files

    And then the table (or list) of founded files will contain:

    - file name

    - file creation time

    - file modification time

    - file access time

    Methods:

    :meth:`find_files()`: Find files by given start and end dates.

    :param root: path to work folder, if None - work folder will be
     current folder (where script is located).
    :param start_date: start date in format "YYYY-MM-DD"
     (see `include_time` parameter), if None - start date will be
     current date minus 7 days
     (if today is 14.01.2022 - start date will be 07.01.2022).
    :param end_date: end date in format "YYYY-MM-DD"
     (see `include_time` parameter), if None - end date will be
     current date.
    :param include_time: if True - you can include time in
     dates parameters in format "YYYY-MM-DD HH:MM:SS",
     False by default.
    :param output_info_to: path to output folder where one
     or three files will be saved (see `sort_info` parameter),
     if None - output folder will be `root`.
    :param extensions: iterable with extensions (as strings) to find,
     if None - all files will be found. Extensions are
     case-insensitive and can be with or without dot
     at the beginning (".TXT", "md").
    :param sort_info: if True - files will be sorted after
     finding process and saved in "founded_list_sorted.txt"
     and "founded_table_sorted.txt" files, but
     "founded_table.txt" will be anyway. False by default.

     Example:
     >>> ff = FilesFinderByDate(
     ...     root="/home/user/Documents",
     ...     start_date="2022-01-14 10:00:00",
     ...     end_date="2022-01-15 16:36:59",
     ...     include_time=True,
     ...     output_info_to="/home/user/Notes",
     ...     extensions=["TXT", ".md"],
     ...     sort_info=True
     ... )
     >>> ff.find_files()
    """
    def __init__(
            self,
            root: str | None = None,
            start_date: str | None = None,
            end_date: str | None = None,
            include_time: bool = False,
            output_info_to: str | None = None,
            extensions: Iterable[str] | None = None,
            sort_info: bool = False):
        self._root = root
        self._output_info_to = output_info_to
        date_format = '%Y-%m-%d' if not include_time else '%Y-%m-%d %H:%M:%S'
        self._start_date = (datetime.datetime.strptime(start_date, date_format)
                            if start_date
                            else (datetime.datetime.now() -
                            datetime.timedelta(days=7)).replace(
                            hour=0, minute=0, second=0, microsecond=0))
        self._end_date = (datetime.datetime.strptime(end_date, date_format)
                          if end_date else datetime.datetime.now())
        if not include_time:
            self._end_date = self._end_date.replace(
                hour=23, minute=59, second=59)
        self._sort_info = sort_info
        if extensions:
            self._extensions = {(f"{'.' if not ext.startswith('.') else ''}"
                                 f"{ext.lower()}")
                                for ext in extensions}

    def _walker(self, write_file):
        walker = os.walk(self._root)
        start_date = self._start_date.timestamp()
        end_date = self._end_date.timestamp()
        files_founded = 0
        files_list = []
        for root, dirs, files in walker:
            for file in files:
                file_path = os.path.join(root, file)
                if not os.path.exists(file_path):
                    # stuff sometimes happened and files that already
                    # in `walker` was deleted or moved by user or system
                    # that is why this is here
                    continue
                file_ext = os.path.splitext(file_path)[1].lower()
                ctime = os.path.getctime(file_path)
                mtime = os.path.getmtime(file_path)
                atime = os.path.getatime(file_path)
                if self._extensions and file_ext not in self._extensions:
                    continue
                if (start_date < mtime < end_date
                        or start_date < ctime < end_date
                        or start_date < atime < end_date):
                    files_founded += 1
                    if self._sort_info:
                        files_list.append((file_path, mtime, ctime, atime))
                    with open(write_file, 'a') as f:
                        f.write(f"file={file_path} | "
                                f"mtime={time.ctime(mtime)} | "
                                f"ctime={time.ctime(ctime)} | "
                                f"atime={time.ctime(atime)}\n")
        return files_founded, files_list if self._sort_info else None

    @staticmethod
    def _sorter(list_file, table_file, files_list):
        from operator import itemgetter
        # import is here because why we need it if we don't sort anything
        files_list.sort(key=itemgetter(2, 1, 3, 0))
        infos_list = []
        infos_table = []
        for i in files_list:
            info = (f"file: {i[0]}\n"
                    f"created: {time.ctime(i[2])}\n"
                    f"modified: {time.ctime(i[1])}\n"
                    f"accessed: {time.ctime(i[3])}\n")
            info_table = (f"file={i[0]}   |   "
                          f"mtime={time.ctime(i[2])}   |   "
                          f"ctime={time.ctime(i[1])}   |   "
                          f"atime={time.ctime(i[3])}")
            infos_list.append(info)
            infos_table.append(info_table)
        with open(list_file, 'a') as f:
            f.write("\n".join(infos_list) + "\n\n")
        with open(table_file, 'a') as f:
            f.write("\n".join(infos_table))

    def find_files(self):
        if self._output_info_to:
            self._output_info_to = os.path.abspath(self._output_info_to)
        if self._root:
            os.chdir(self._root)
        self._root = os.getcwd()
        self._output_info_to = (self._output_info_to if self._output_info_to
                                else self._root)
        self._output_info_to = os.path.abspath(self._output_info_to)

        write_table = os.path.join(
            self._output_info_to, 'founded_table.txt')
        starting_text = (f'script started at: {datetime.datetime.now()}\n'
                         f'start date: {self._start_date}\n'
                         f'end date: {self._end_date}\n'
                         '     file     |     modified     |'
                         '     created     |     accessed\n')
        if not os.path.exists(write_table):
            with open(write_table, 'w') as f:
                f.write(starting_text)
        else:
            with open(write_table, 'a') as f:
                f.write("\n\n\n" + starting_text)

        files_founded, files_list = self._walker(write_table)

        if self._sort_info:
            write_list_sorted = os.path.join(
                self._output_info_to, 'founded_list_sorted.txt')
            write_table_sorted = os.path.join(
                self._output_info_to, 'founded_table_sorted.txt')
            if not os.path.exists(write_list_sorted):
                with open(write_list_sorted, 'w') as f:
                    f.write(starting_text[:-67] + '\n\n')
            else:
                with open(write_list_sorted, 'a') as f:
                    f.write("\n\n\n" + starting_text[:-67] + '\n\n')
            if not os.path.exists(write_table_sorted):
                with open(write_table_sorted, 'w') as f:
                    f.write(starting_text)
            else:
                with open(write_table_sorted, 'a') as f:
                    f.write("\n\n\n" + starting_text)
            self._sorter(write_list_sorted, write_table_sorted, files_list)

        print(f'Files founded: {files_founded}')
        print(f'Output info to: {self._output_info_to} folder')
