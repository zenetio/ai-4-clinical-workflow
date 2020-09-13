if [[ ! -e /opt/OrthancBuild ]]; then
	echo "Setting up Orthanc. This may take a moment."
    # Copy Orthanc Build out of mounted disk to solve Sqlite issues
    cp -r /opt/aihcnd-applications/OrthancBuild /opt/OrthancBuild &
    PID=$!
    i=1
    sp="/-\|"
    echo -n ' '
    while [ -d /proc/$PID ]
    do
      printf "\b${sp:i++%${#sp}:1}"
      sleep 0.5
    done
fi

/opt/OrthancBuild/Orthanc /opt/OrthancBuild/Configuration.json