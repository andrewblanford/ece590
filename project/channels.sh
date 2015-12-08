ROBOT_PT_DRIVE_CHAN='robot-pt-drive'
ROBOT_TIME_CHAN='robot-time'
ROBOT_VID_CHAN='robot-vid-chan'

MakeAch()
{

	ach -1 -C $ROBOT_PT_DRIVE_CHAN -m 10 -n 3000 
	ach -1 -C $ROBOT_TIME_CHAN     -m 10 -n 3000 
	ach -1 -C $ROBOT_VID_CHAN      -m 30 -n 3000000
}

KillAch()
{

	sudo rm /dev/shm/robot*  
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
		
