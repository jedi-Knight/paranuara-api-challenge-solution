source ./bin/activate

echo "Now starting server at http://0.0.0.0:8080/  .."

python server.py >> ../logs/log.txt 2>&1 &

#python #uncomment to get a python shell for debugging