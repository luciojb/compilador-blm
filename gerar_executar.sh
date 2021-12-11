python main.py
llc -filetype=obj output.ll
gcc -no-pie output.o -o output
./output