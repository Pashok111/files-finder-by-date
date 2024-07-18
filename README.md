# Files Finder (by time)
Module with only one class `FilesFinderByDate` for finding files by given start and end dates.

After finding process, in terminal will be printed how many files are founded and where information will be saved.

Actual info about founded files will be saved into "founded_table.txt" file in output folder
(and "founded_list_sorted.txt", "founded_table_sorted.txt" files if `sort_info` parameter is True).

Info files will be created automatically, but only if they don't exist in output folder,
otherwise new info will be appended to existing files.

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

### Methods (of `FilesFinderByDate`):

- `find_files()`: Find files by given start and end dates.

### Parameters (of `FilesFinderByDate`):

- `root`: path to work folder, if None - work folder will be current folder (where script is located).
- `start_date`: start date in format "YYYY-MM-DD" (see `include_time` parameter),
if None - start date will be current date minus 7 days
(if today is 14.01.2022 - start date will be 07.01.2022).
- `end_date`: end date in format "YYYY-MM-DD" (see `include_time` parameter),
if None - end date will be current date.
- `include_time`: if True - you can include time in dates parameters in format
"YYYY-MM-DD HH:MM:SS", False by default.
- `output_info_to`: path to output folder where one or three files will be saved
(see `sort_info` parameter), if None - output folder will be `root`.
- `extensions`: iterable with extensions (as strings) to find, if None - all files will be found.
Extensions are case-insensitive and can be with or without dot at the beginning (".TXT", "md").
- `sort_info`: if True - files will be sorted after finding process and saved in
"founded_list_sorted.txt" and "founded_table_sorted.txt" files,
but "founded_table.txt" will be anyway. False by default.

### Example:
```python
from files_finder_by_date import FilesFinderByDate

ff = FilesFinderByDate(
    root="/home/user/Documents",
    start_date="2022-01-14 10:00:00",
    end_date="2022-01-15 16:36:59",
    include_time=True,
    output_info_to="/home/user/Notes",
    extensions=["TXT", ".md"],
    sort_info=True
)
ff.find_files()
```