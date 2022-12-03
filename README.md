
Repository Link: https://github.com/NichHarris/rush-hour-state-space-search

COMP 472 - Mini Project 2
## Running program

Options Available:
```
options:
  -h, --help            show this help message and exit
  --file FILE, -f FILE
  --analysis, -a
```

>Note: The input file to be used should be stored under the `/input` directory.
>The directory does not need to be referenced when running the script, just the file name

The options ``` -a, --analysis``` is used to run the program in analysis mode
This will create an analysis output file, under `/output/analysis.txt` where the format is:
```Puzzle_Number	 Algorithm	 Heuristic	 Solution_Length	 Search_Length	 Runtime```

Run to generate analysis file
```
python main.py -a -f {input_file_name}.txt
```

Run to generate solution and search files
```
python main.py -f {input_file_name}.txt
```