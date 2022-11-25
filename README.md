
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

The options ``` -a, --analysis``` is used to run the program in analysis mode
This will create an analysis output file where the format is:
```Puzzle Number	 Algorithm	 Heuristic	 Solution Length	 Search Length	 Runtime```

Run to generate analysis file
```
python main.py -a -f {input_file_name}.txt
```

Run to generate solution and search files
```
python main.py -f {input_file_name}.txt
```