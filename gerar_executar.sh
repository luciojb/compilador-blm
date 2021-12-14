source venv/bin/activate
python3 main.py code.blm
llc -filetype=obj output.ll
gcc -no-pie output.o -o output
./output