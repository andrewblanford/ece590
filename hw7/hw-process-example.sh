MakeAch()
{

	ach -1 -C example-chan-1 -m 10 -n 3000 
	ach -1 -C example-chan-2 -m 10 -n 3000 
	ach -1 -C example-chan-3 -m 10 -n 3000 
}

KillAch()
{

	sudo rm /dev/shm/example-chan*  
}

Start()
{
	sudo chmod 777 "$1"
	KillAch
	MakeAch
}

Kill()
{
	KillAch
}


case "$1" in
	'start' )
		Start $2
	;;

	'kill' )
		Kill
	;;

esac
exit 0
		
