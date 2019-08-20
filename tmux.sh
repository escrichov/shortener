#!/bin/bash

SESSIONNAME="shortener"

TAB3="server"
TAB2="shell"
TAB1="djangoshell"

DEFAULTTAB=$TAB1

tmux has-session -t $SESSIONNAME &> /dev/null

#if not existing, lets create one
if [ $? != 0 ]
 then
    #create a new session and name the window(tab) in it using -n
    #detaching is needed as in the last line will attach to it
    tmux new-session -s $SESSIONNAME -n $TAB1 -d
    tmux send-keys -t 0 "pipenv run python manage.py shell" C-m

    #open a second window(tab)
    tmux new-window -t $SESSIONNAME:1 -n $TAB2
    tmux send-keys -t 0 C-m

    tmux new-window -t $SESSIONNAME:2 -n $TAB3
    tmux send-keys -t 0 "make run" C-m

    #default window you want to see when entering the session
    tmux select-window -t $SESSIONNAME:$DEFAULTTAB
fi

tmux attach -t $SESSIONNAME
