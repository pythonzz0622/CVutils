pid=$(ps aux | grep "infer_args.py" | grep -v grep | awk "{print $2}")
if [ ! -z "$pid" ]; then
    kill $pid
    echo "Process infer_args.py (PID: $pid) has been terminated."
else
    echo "No process named infer_args.py found."
fi