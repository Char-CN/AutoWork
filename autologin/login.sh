source ~/.bash_profile

echo "===================================="
echo "====================================  phantomjs"
echo "===================================="
phantomjs /Users/hyy/AutoWork/autologin/login.js

flag=`curl "https://raw.githubusercontent.com/Char-CN/Signal/master/sunlog_restart"`
echo "==================================== sunlog_restart : $flag"

if [[ "$flag" = "true" ]];
then
    echo "===================================="
    echo "====================================  killall SunloginClient"
    echo "===================================="
    killall SunloginClient

    echo "===================================="
    echo "====================================  open -a SunloginClient"
    echo "===================================="
    open -a SunloginClient
fi


