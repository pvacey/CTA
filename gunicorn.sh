#!/bin/bash
PORT=8002

start(){
	echo starting gunicorn
	venv/bin/gunicorn web:api -D -b localhost:$PORT
}

stop(){
	echo stopping gunicorn
	ps aux | grep '[v]env/bin/gunicorn web:api ' | awk '{print $2}' | xargs kill
} 

debug(){
	venv/bin/gunicorn web:api -b localhost:$PORT
}

if [ "$1" == "start" ]; then
	start
elif [ "$1" == "stop" ]; then
	stop
elif [ "$1" == "restart" ]; then
	stop
	sleep 2
	start
elif [ "$1" == "status" ]; then
	if ps aux | grep "venv/bin/gunicorn web:api" | grep -v grep > /dev/null; then
		echo gunicorn status: up
	else
		echo gunicorn status: down
	fi
elif [ "$1" == "debug" ]; then
	debug
else
	echo $0: invalid option \"$1\"
fi
