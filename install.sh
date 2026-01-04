#!/bin/bash

GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    while ps -p $pid > /dev/null 2>&1; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
    echo -e "${GREEN}[DONE]${NC}"
}

clear
echo -e "${CYAN}"
echo "
░▒█░░▒█░█▀▀░█▀▀▄░▒█▀▀▀░▄▀▀▄░█░█
░▒█▒█▒█░█▀▀░█▀▀▄░▒█▀▀░░█░░█░▄▀▄
░▒▀▄▀▄▀░▀▀▀░▀▀▀▀░▒█░░░░░▀▀░░▀░▀
"
echo -e "-- WEBFOX SETUP WIZARD V3.01--${NC}\n"

if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}[!] Please run as root (sudo ./install.sh)${NC}"
    exit 1
fi

echo -e "${YELLOW}[*] Initializing System Configuration...${NC}\n"

echo -e "${CYAN}[1/4] Updating System Repositories...${NC}"
echo -ne "    > Synchronizing package lists"
sudo apt-get update -qq > /dev/null 2>&1 &
spinner $!

echo -e "\n${CYAN}[2/4] Installing Core Dependencies...${NC}"
echo -ne "    > Installing Python3, Pip & Firefox"
sudo apt-get install -y python3 python3-pip python3-venv git wget curl unzip firefox-esr > /dev/null 2>&1 &
spinner $!

echo -e "\n${CYAN}[3/4] Installing Python Libraries...${NC}"
echo -ne "    > Installing required modules"
pip3 install builtwith --break-system-packages > /dev/null 2>&1
pip3 install -r requirements.txt --break-system-packages > /dev/null 2>&1 &
spinner $!

echo -e "\n${CYAN}[4/4] Configuring Geckodriver (v0.36.0)...${NC}"
echo -ne "    > Downloading driver binary"

DOWNLOAD_URL="https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz"

rm -f geckodriver-v0.36.0-linux64.tar.gz
rm -f /usr/bin/geckodriver

wget -q --show-progress -O driver.tar.gz "$DOWNLOAD_URL"

if [ -f "driver.tar.gz" ]; then
    tar -xf driver.tar.gz
    chmod +x geckodriver
    mv geckodriver /usr/bin/geckodriver
    rm driver.tar.gz
    echo -e "${GREEN}    > Driver Installed Successfully${NC}"
else
    echo -e "${RED}    [!] Download Failed. Check connection.${NC}"
    exit 1
fi

echo -e "\n${GREEN}=========================================="
echo -e "   [✓] SYSTEM UPDATE COMPLETE"
echo -e "   [✓] DEPENDENCIES INSTALLED"
echo -e "   [✓] ENVIRONMENT READY"
echo -e "==========================================${NC}"
echo -e "${YELLOW}   Usage: python3 test.py -help${NC}\n"
