#!/bin/bash
# install srim




# ================================================================
# ================================================================
# ================================================================
# ================================================================
# ================================================================

# READ SIZE OF TERM
read -r rows cols < <(stty size)
((cols=cols+2))
while [ 1 ]; do

CHOICES=$(whiptail --separate-output --checklist "Choose options" 20 $cols 14 \
		       --cancel-button "EXIT" \
  "wine" "Install wine" OFF \
  "ini" "Initialize wine" OFF \
  "dwnl" "Download srim" OFF \
  "extr" "Extract srim to wine directory" OFF \
  "lib" "copy libraries" OFF \
  "run" "run wine srim" OFF \
  "bug" "If there is problem with locale-read" OFF \
  "quit" "Quit" OFF 3>&1 1>&2 2>&3)


if [ -z "$CHOICES" ]; then
    echo "X... No option was selected (user hit Cancel or unselected all options)"

    exit 2
else
  for CHOICE in $CHOICES; do
    case "$CHOICE" in
    "wine")
	echo "$CHOICE"
	sudo -H apt -y install wine
	# I use x  invisible framebuffer
	sudo -H apt -y install xvfb
	echo ================== DONE
	;;

    "ini")
	echo "$CHOICE"
	wine notepad
	#wine SRIM-2013-Pro.e
	#wine SRIM.exe
	echo ================== DONE
	;;

    "dwnl")
	echo "$CHOICE"
	# cd ~/Downloads
	cd ~/.wine/drive_c/Program\ Files/
	mkdir SRIM
	cd SRIM
	# wget http://www.srim.org/SRIM/SRIM-2013-Pro.e
	# smaller version
	wget http://www.srim.org/SRIM/SRIM-2013-Std.e
	echo ================== DONE
	;;

    "extr")
	echo "$CHOICE"
	ls -l  ~/.wine/drive_c/Program\ Files/SRIM
	cd ~/.wine/drive_c/Program\ Files/SRIM
	wine SRIM-2013-Std.e
	echo ================== DONE
	sleep 3
	;;


    "lib")
	echo "$CHOICE"
	# find libs
	find . ~/.local/lib -name libs2013.tgz
	echo ... sleep 1 ...
	sleep 1
	IFS=$'\n'
	paths=($(find . ~/.local/lib -name libs2013.tgz ))
	unset IFS

	printf "%s\n" "${paths[@]}"
	echo "I     SELECT LIB-TGZ :"  ${paths[0]}
	echo "I NOT SELECT LIB-TGZ :"  ${paths[1]}
	sleep 1

	#find . -name libs2013.tgz
	cp ${paths[0]} ~/.wine/drive_c/windows/
	cd ~/.wine/drive_c/windows/
	tar -xvzf  libs2013.tgz
	echo ... sleeping 5s
	sleep 5
	echo ================== DONE
	;;

    "run")
	echo "$CHOICE"
	cd ~/.wine/drive_c/Program\ Files/SRIM
	wine SRIM.exe

	echo ================== DONE
	echo ... sleep 3 ...
	sleep 3
	;;


    "bug")
	echo "$CHOICE"
	echo "# There can happen that locale produces numbers with decimal "
	echo "# Check it with"
	echo "wine regedit"
	echo "# see MyComputer/HKEY_CURRENT_USER/ControlPanel/International/sDecimal"
	echo "# you may need to completely delete all your ~/.wine"
	echo "# change locale to en_US.utf8 (or en_GB) and start 'wine notepad'"

	wine regedit
	echo ... sleep 6s
	sleep 6
	echo ================== DONE
	;;


    "quit")
	echo "_______________________________________________________________"
	echo "$CHOICE"
	exit 0
	echo ================== DONE
	;;

    *)
	echo "_______________________________________________________________"
	echo "Unsupported item $CHOICE!  Some ERRORRRRRRR" >&2
      exit 1
      ;;
    esac
  done
        # if else -z CHOICES
fi


done

exit 0



















############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################













############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################

izsh() {
  # Use colors, but only if connected to a terminal, and that terminal
  # supports them.
  if which tput >/dev/null 2>&1; then
      ncolors=$(tput colors)
  fi
  if [ -t 1 ] && [ -n "$ncolors" ] && [ "$ncolors" -ge 8 ]; then
    RED="$(tput setaf 1)"
    GREEN="$(tput setaf 2)"
    YELLOW="$(tput setaf 3)"
    BLUE="$(tput setaf 4)"
    BOLD="$(tput bold)"
    NORMAL="$(tput sgr0)"
  else
    RED=""
    GREEN=""
    YELLOW=""
    BLUE=""
    BOLD=""
    NORMAL=""
  fi

  # Only enable exit-on-error after the non-critical colorization stuff,
  # which may fail on systems lacking tput or terminfo
  set -e

  CHECK_ZSH_INSTALLED=$(grep /zsh$ /etc/shells | wc -l)
  if [ ! $CHECK_ZSH_INSTALLED -ge 1 ]; then
      printf "${YELLOW}Zsh is not installed!${NORMAL} Please install zsh first!\n"
      sudo apt -y install zsh
      if [ "$?" != "0" ]; then
	  echo PROBLEM... I couldnt install zsh
	  exit
      fi
  fi
  unset CHECK_ZSH_INSTALLED

  if [ ! -n "$ZSH" ]; then
    ZSH=~/.oh-my-zsh
  fi

  if [ -d "$ZSH" ]; then
    printf "${YELLOW}You already have Oh My Zsh installed.${NORMAL}\n"
    printf "You'll need to remove $ZSH if you want to re-install.\n"
    exit
  fi

  # Prevent the cloned repository from having insecure permissions. Failing to do
  # so causes compinit() calls to fail with "command not found: compdef" errors
  # for users with insecure umasks (e.g., "002", allowing group writability). Note
  # that this will be ignored under Cygwin by default, as Windows ACLs take
  # precedence over umasks except for filesystems mounted with option "noacl".
  umask g-w,o-w

  printf "${BLUE}Cloning Oh My Zsh...${NORMAL}\n"
  hash git >/dev/null 2>&1 || {
    echo "Error: git is not installed"
    exit 1
  }
  # The Windows (MSYS) Git is not compatible with normal use on cygwin
  if [ "$OSTYPE" = cygwin ]; then
    if git --version | grep msysgit > /dev/null; then
      echo "Error: Windows/MSYS Git is not supported on Cygwin"
      echo "Error: Make sure the Cygwin git package is installed and is first on the path"
      exit 1
    fi
  fi
  env git clone --depth=1 https://github.com/robbyrussell/oh-my-zsh.git $ZSH || {
    printf "Error: git clone of oh-my-zsh repo failed\n"
    exit 1
  }


  printf "${BLUE}Looking for an existing zsh config...${NORMAL}\n"
  if [ -f ~/.zshrc ] || [ -h ~/.zshrc ]; then
    printf "${YELLOW}Found ~/.zshrc.${NORMAL} ${GREEN}Backing up to ~/.zshrc.pre-oh-my-zsh${NORMAL}\n";
    mv ~/.zshrc ~/.zshrc.pre-oh-my-zsh;
  fi

  printf "${BLUE}Using the Oh My Zsh template file and adding it to ~/.zshrc${NORMAL}\n"
  cp $ZSH/templates/zshrc.zsh-template ~/.zshrc
  sed "/^export ZSH=/ c\\
  export ZSH=$ZSH
  " ~/.zshrc > ~/.zshrc-omztemp
  mv -f ~/.zshrc-omztemp ~/.zshrc

  # If this user's login shell is not already "zsh", attempt to switch.
  TEST_CURRENT_SHELL=$(expr "$SHELL" : '.*/\(.*\)')
  if [ "$TEST_CURRENT_SHELL" != "zsh" ]; then
    # If this platform provides a "chsh" command (not Cygwin), do it, man!
    if hash chsh >/dev/null 2>&1; then
      printf "${BLUE}Time to change your default shell to zsh!${NORMAL}\n"
      chsh -s $(grep /zsh$ /etc/shells | tail -1)
    # Else, suggest the user do so manually.
    else
      printf "I can't change your shell automatically because this system does not have chsh.\n"
      printf "${BLUE}Please manually change your default shell to zsh!${NORMAL}\n"
    fi
  fi

  printf "${GREEN}"
  echo '         __                                     __   '
  echo '  ____  / /_     ____ ___  __  __   ____  _____/ /_  '
  echo ' / __ \/ __ \   / __ `__ \/ / / /  /_  / / ___/ __ \ '
  echo '/ /_/ / / / /  / / / / / / /_/ /    / /_(__  ) / / / '
  echo '\____/_/ /_/  /_/ /_/ /_/\__, /    /___/____/_/ /_/  '
  echo '                        /____/                       ....is now installed!'
  echo ''
  echo ''
  echo 'Please look over the ~/.zshrc file to select plugins, themes, and options.'
  echo ''
  echo 'p.s. Follow us at https://twitter.com/ohmyzsh.'
  echo ''
  echo 'p.p.s. Get stickers and t-shirts at https://shop.planetargon.com.'
  echo ''
  printf "${NORMAL}"
  #env zsh
}






# ================================================================
# ================================================================
# ================================================================
# ================================================================
# ================================================================

PS3='Please enter your choice: '

options=("install oh-my-zsh" "cp .zshrc .emacs .screenrc .config/mpv tjkirch_mod2" "APT INSTALL net-tools ntpstat ntpsec-ntpdate opencv socat screen v4l-utils scrot" "APT INSTALL htop terminator duf dfc mpv cmus ncdu pydf debian-goodies bmon iftop sntop nload cbm rlwrap" "PIP INSTALL grc bpytop speedtest-cli rsyncy" "PIP INSTALL flashcam notifator virtualenvwrapper tdb_io" "UTILS sshconf.py pycompres.py terminat.py pingy.py vnc.py symp" "influx" "cern root" "Quit")


select opt in "${options[@]}"
do
    case $opt in
        "install oh-my-zsh")
            echo "install zsh and bc"
	    izsh
	    sudo apt -y install bc
            ;;
        "cp .zshrc .emacs .screenrc .config/mpv tjkirch_mod2")
            echo "cp .zshrc .emacs .screenrc .config/mpv tjkirch_mod2"
	    echo "================= .zshrc .screenrc .emacs .mpv ============="
	    echo "
	    cp  .zshrc    ~/
	    cp  tjkirch_mod2.zsh-theme ~/.oh-my-zsh/themes/
	    cp  .screenrc ~/
	    cp  .emacs    ~/
	    cp -R mpv ~/.config
"
	    cp  .zshrc    ~/
	    cp  tjkirch_mod2.zsh-theme ~/.oh-my-zsh/themes/
	    cp  .screenrc ~/
	    cp  .emacs    ~/
	    cp -R mpv ~/.config
	    echo ================== DONE
            ;;
        "APT INSTALL net-tools ntpstat ntpsec-ntpdate opencv socat screen v4l-utils scrot")
            echo "you chose choice $REPLY which is $opt"
	    echo =========================================================
	    echo NETSTAT net-tools FOR CANEMRA
	    echo NTPSTAT ntpsec-ntpdate FOR DISCOVERY
	    echo python3-OPENCV
	    echo python3-pip
	    echo socat FOR SEREAD
	    echo wireless-tools FOR PIADDR on RPI3B
	    echo =========================================================
	    sudo -H apt -y install wireless-tools
	    sudo -H apt -y install net-tools
	    sudo -H apt -y install ntpstat
	    sudo -H apt -y install ntpsec-ntpdate
	    sudo -H apt -y install python3-opencv
	    sudo -H apt -y install python3-pip
	    sudo -H apt -y install socat
	    sudo -H apt -y install screen
	    sudo -H apt -y install v4l-utils
	    sudo -H apt -y install scrot



	    echo ================== DONE
            ;;

        "APT INSTALL htop terminator duf dfc mpv cmus ncdu pydf debian-goodies bmon iftop sntop nload cbm rlwrap")
            echo "dpigs ... from debian-goodies"
	    echo =========================================================
	    echo =========================================================
	    sudo -H apt -y install htop
	    sudo -H apt -y install terminator
	    sudo -H apt -y install duf
	    sudo -H apt -y install dfc
	    sudo -H apt -y install mpv
	    sudo -H apt -y install cmus
	    sudo -H apt -y install ncdu
	    sudo -H apt -y install pydf
	    sudo -H apt -y install debian-goodies
	    sudo -H apt -y install bmon
	    sudo -H apt -y install iftop
	    sudo -H apt -y install sntop
	    sudo -H apt -y install nload
	    sudo -H apt -y install cbm
	    sudo -H apt -y install rlwrap
	    sudo -H apt -y install dstat # wdr ?
	    sudo -H apt -y install iotop

	    echo ================== DONE
	    ;;


        "PIP INSTALL grc bpytop speedtest-cli rsyncy")
            echo "PIP "
	    echo =========================================================
	    echo =========================================================
	    ME=`whoami`
	    if [ "$ME" != "root" ]; then

		which pip
		if [ "$?" != "0" ]; then
		    echo X...  you need to install python3-pip
		    echo X...  you need to install python3-pip
		    echo X...  you need to install python3-pip
		else
		    #pip install wdr
		    pip install grc
		    pip install bpytop
		    pip install speedtest-cli
		    pip install rsyncy
		    #pip install
		    #pip install

		fi
	    else
		echo X...  I dont think you should do PIP as root....
	    fi
	    echo ================== DONE
	    ;;

	"PIP INSTALL flashcam notifator virtualenvwrapper tdb_io")
	    ME=`whoami`
	    if [ "$ME" != "root" ]; then

		which pip
		if [ "$?" != "0" ]; then
		    echo X...  you need to install python3-pip
		    echo X...  you need to install python3-pip
		    echo X...  you need to install python3-pip
		else
		    pip install flashcam
		    pip install virtualenvwrapper
		    pip install tdb_io
		    pip install notifator
		fi
	    else
		echo o X...  I dont think you should do PIP as root....
	    fi
	    echo ================== DONE
	    ;;

	"UTILS sshconf.py pycompres.py terminat.py pingy.py vnc.py symp")
	    pwd
	    which pip
	    if [ "$?" != "0" ]; then
		echo X...  you need to install python3-pip
		echo X...  you need to install python3-pip
		echo X...  you need to install python3-pip
	    else
		cur=`pwd`
		cd $HOME/02_GIT/GITLAB/linux/02_utilities/
		pwd
		sudo cp sshconf.py /usr/local/bin/
		pip install terminaltables
		pip install colorclass
		pip install influxdb
		sudo cp pycompres.py /usr/local/bin/
		sudo cp terminat.py /usr/local/bin/
		sudo cp pingy.py /usr/local/bin/
		sudo cp vnc.py /usr/local/bin/
		sudo cp symp /usr/local/bin/
		sudo cp ulopy.py /usr/local/bin/
		cd $cur
	    fi
	    echo ================== DONE
	    ;;

	"influx")
	    echo NOTHING FOR NOW
	    ;;


        "cern root")
	    echo PREINSTALLATIONS .... 2x
	    sudo apt-get -y install dpkg-dev
	    sudo apt-get -y install cmake
	    sudo apt-get -y install g++
	    sudo apt-get -y install gcc
	    sudo apt-get -y install binutils
	    sudo apt-get -y install libx11-dev
	    sudo apt-get -y install libxpm-dev
	    sudo apt-get -y install libxft-dev
	    sudo apt-get -y install libxext-dev
	    sudo apt-get -y install python
	    sudo apt-get -y install libssl-dev
	    echo PREINSTALLATIONS 1/2 DONE
	    sudo apt-get -y install gfortran
	    sudo apt-get -y install libpcre3-dev
	    sudo apt-get -y install xlibmesa-glu-dev
	    sudo apt-get -y install libglew-dev
	    sudo apt-get -y install libftgl-dev
	    sudo apt-get -y install libmysqlclient-dev
	    sudo apt-get -y install libfftw3-dev
	    sudo apt-get -y install libcfitsio-dev
	    sudo apt-get -y install graphviz-dev
	    sudo apt-get -y install libavahi-compat-libdnssd-dev
	    sudo apt-get -y install libldap2-dev
	    sudo apt-get -y install python-dev
	    sudo apt-get -y install libxml2-dev
	    sudo apt-get -y install libkrb5-dev
	    sudo apt-get -y install libgsl0-dev
	    sudo apt-get -y install qtwebengine5-dev
	    echo PREINSTALLATIONS 2/2 DONE

	    cd ~/Downloads
	    cat /etc/issue.net | grep "Ubuntu 22.04"
	    if [ "$?" = 0 ]; then
		wget https://root.cern/download/root_v6.26.10.Linux-ubuntu22-x86_64-gcc11.3.tar.gz
		tar -xvzf root_v6.26.10.Linux-ubuntu22-x86_64-gcc11.3.tar.gz
		ls ~/ | grep root
		echo ====================== YOU MUST DO THIS =================
		echo mv ~/Downloads/root ~/
		echo mv  ~/Downloads/root ~/
		echo mv  ~/Downloads/root ~/
	    fi
	    cat /etc/issue.net | grep "Ubuntu 20.04"
	    if [ "$?" = 0 ]; then
 		wget https://root.cern/download/root_v6.26.06.Linux-ubuntu20-x86_64-gcc9.4.tar.gz
 		tar -xvzf root_v6.26.06.Linux-ubuntu20-x86_64-gcc9.4.tar.gz
		ls ~/ | grep root
		echo mv  ~/Downloads/root ~/
		echo mv  ~/Downloads/root ~/
		echo mv  ~/Downloads/root ~/
	    fi
	    echo ================== DONE
            ;;


        "rclocal4rpi")
	    echo ... You should be on raspberry...the test should be HERE...
	    sleep 1
	    if [ -e /etc/rclocal ]; then
		echo X.... rc.local EXISTS ALREADY ..............
		echo "_________________________________________________ "
		cat /etc/rc.local
		echo "_________________________________________________ "
		read -p "Replace /etc/rc.local: (y/n)"  ans
	    else
		read -p "Create new /etc/rc.local: (y/n)"  ans
	    fi
	    echo $ans
	    if [ "$ans" = "y" ]; then
		cp -i 09_raspberry/rc.local.rpi_all /etc/rc.local
	    else
		echo X... better not ... right
	    fi
	    echo ================== DONE
            ;;

        "Quit")
            break
	    echo ================== DONE
            ;;


        *) echo "invalid option $REPLY";;
    esac
done


exit 0

# echo "COPY TO HOME            .zshrc   .emacs .screenrc  "
# echo "COPY TO /usr/local/bin: terminat.py  create_prj   pingy"
# echo "RSYNC TO HOME :          mpv.config_with_scripts "
# echo "NOT ANYMORE .xbindkeysrc"
# echo "rkhunter.conf  "
# echo "apt50 unattended upgrades"

# #for (( i=1; i>=0; i--)); do
# #  echo $i
# #  sleep 1
# #done

# # Executive part:

#   echo "================= DONE - now SUDO  ============="
#   #  cp  .emacs.d.install_straight.el    ~/.emacs.d/install_straight.el
#   # not enough
# 	# I DONT KNOW !!!!!!!!!!!!!!!!!!!!!!
# #  cp  -R emacs.straight/*    ~/.emacs.d/straight/
# #  rsync -av --progress ./mpv/ ~/.config/mpv/



#   function colobi(){
#       TO=$2
#       COM=$3
#       LEN=${#TO}

#       if [ "$LEN" -lt "3" ]; then
# 	  TO="/usr/local/bin"
#       fi
#       TO=${TO}/

#       # echo "============================= " $1 "=================="
#       # echo "PROGRAM TO COPY :" $1
#       # echo "DESTINATION      " $TO "LEN=" $LEN
#       # echo "                 " $COM

#       #echo sudo cp $1 $TO
#       sudo cp $1 $TO
#       ERR=$?
#       if [ "$ERR" = "0" ]; then
# 	  ERR="[OK]"
#       else
# 	  ERR="[xx]"
#       fi
#       printf  " %-30s %-20s  %-45s ... %-10s \n" $1 $TO "$COM" $ERR

#       #echo $?
#       #sleep 1
#   }
# #  colobi TEST

#   function pipastall(){
#       PACKA=$1
#       echo i... checking $PACKA
#       pip3 show $PACKA > /dev/null
#       if [ "$?" != "0" ]; then
# 	  pip3 install $PACKA --upgrade
#       fi
#   }

# echo =========================================================
# echo this is PYTHON PART ...
# echo =========================================================
# echo notifator ipython3 sumpy scipy pandas h5py matplotlib
# sleep 1
# echo ======== ok I go =============

# pipastall "notifator"
# pipastall "ipython"
# pipastall "sympy"
# pipastall "scipy"
# pipastall "pandas"
# pipastall "matplotlib"
# pipastall "h5py"
# pipastall "twine"
# pipastall "bumpversion"


# echo I NEED DISCOVER8086 and  RUNNING CAMERA
# pipastall "influxdb"
# pipastall "flask"
# pipastall "gunicorn"
# pipastall "flask_httpauth"
# pipastall "numpy"
# pipastall "imutils"
# pipastall "pantilthat"
# pipastall "imagezmq"
# pipastall "virtualenvwrapper"



# pip3 install dask distributed --upgrade
# echo "pip3 install lz4 --upgrade"
# echo "pip3 install lz4 --upgrade"
# echo "pip3 install lz4 --upgrade"



# echo =========================================================
# echo THIS IS ROOT APT PART ... CAN BE SKIPPED Ctrl-c
# echo NETSTAT net-tools FOR CANEMRA
# echo NTPSTAT FOR DISCOVER
# echo BIGGEST  python3-OPENCV
# echo socet FOR SEREAD
# echo ...  after there comes copying user files to  /usr/local/bin
# echo =========================================================
# sudo -H apt install net-tools
# sudo -H apt install ntpstat
# sudo -H apt install python3-opencv
# sudo -H apt install socat






# echo sshborg ..... "???"
# #PACKA="sshborg"
# #pip3 show $PACKA
# #if [ "$?" != "0" ]; then
# #    pip3 install $PACKA --upgrade
# #fi



# echo =========================================================
# echo THIS IS ROOT USER PART ... CAN BE SKIPPED Ctrl-c
# echo =========================================================
# echo vncpy pingypy terminat createprj pycompress kdeconnect symp sshconf
# sleep 1
# echo CONF: rkhunter 50unattended 10periodic 20auto-upgrades 10sec_sysd joursize
# sleep 1
# echo ======== ok I go =============
# #  colobi 02_utilities/pingy     . "PING WITH LARGE FONT AND COLOR"

#   colobi 02_utilities/vnc.py        . "vnc.py server run/kill/view/list  skvl"
#   colobi 02_utilities/pingy.py      . "PING WITH LARGE FONT AND COLOR"
#   colobi 02_utilities/terminat.py   . "TERMINATOR WITH A preDEFINED LAYOUT+CMDS"
#   colobi 02_utilities/create_prj.py . "CREATE BASE PYTHON PROJECT"
#   colobi 02_utilities/create_org.py . "CREATE ORG form file"
#   colobi 02_utilities/pycompres.py  . "SHOW ALL ARIANTS OF DIR/FILE  COMPRESSIONS"
#   colobi 02_utilities/kdeconnect.py . "EASILY SEND A FILE TO active PHONE"

#   colobi 02_utilities/symp . "RUN isympy with few definitions"

#   colobi 02_utilities/sshconf.py . "PING tool - input from .ssh/config"
#   # colobi 02_utilities/btrfs.sh .  "IN NOTIFATORCHECK STATUS - RUN FROM CRON ROOT"

#   colobi 02_utilities/cpuspeed.py . "CPU evaluation on cosine similarity numpy"


#   colobi security/rkhunter.conf    /etc     "change it to comply with apt"
#   colobi security/50unattended-upgrades /etc/apt/apt.conf.d "NO UNATTENDED UPGRADES !!! "
#   colobi security/10periodic      /etc/apt/apt.conf.d "NO UNATTENDED "
#   colobi security/20auto-upgrades /etc/apt/apt.conf.d "NO UNATTENDED "
#   colobi security/system.conf     /etc/systemd  "10 seconds systemd wait "
#   colobi security/journald.conf /etc/systemd "limit journal size - 200MB "

# echo i... ALL DONE
