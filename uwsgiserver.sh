#!/bin/bash
if [ ! -n "$1" ]
then
    echo "Usages: sh uwsgiserver.sh [start|stop|restart|status|log]"
    exit 0
fi

if [ $1 = start ]
then
    psid=`ps aux | grep "uwsgi" | grep "iHealth_site" | grep -v "grep" | wc -l`
    if [ $psid -gt 5 ]
    then
        echo "iHealth_site'uwsgi is running!"
        exit 0
    else
        uwsgi --ini uwsgi.ini --daemonize log/uwsgi.log --module iHealth_site.wsgi
        echo "Start iHealth_site'uwsgi service [OK]"
    fi
    

elif [ $1 = stop ];then
    ps -ef | grep "iHealth_site" | grep -v grep | cut -c 10-15 | xargs kill -9
    echo "Stop iHealth_site'uwsgi service [OK]"

elif [ $1 = restart ];then
    ps -ef | grep "iHealth_site" | grep -v grep | cut -c 10-15 | xargs kill -9
    echo "Stop iHealth_site'uwsgi service [OK]"
    sleep 2
    uwsgi --ini uwsgi.ini --daemonize log/uwsgi.log --module iHealth_site.wsgi
    echo "Start iHealth_site'uwsgi service [OK]"

elif [ $1 = status  ];then
    ps -ef | grep "iHealth_site" | grep -v grep

elif [ $1 = log  ];then
    tail -f log/uwsgi.log
        
else
    echo "Usages: sh uwsgiserver.sh [start|stop|restart|status|log]"
fi
