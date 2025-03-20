#!/bin/bash

# ANSI color codes
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to display explosion animation
show_explosion() {
    clear
    for i in {1..3}; do
        # Phase 1: Initial star compression
        echo -e "${YELLOW}"
        cat << "EOF"
          ★    
       .  ⭐  .
     . * ★ ✧ * .
    . * ★ ⭐ ★ * .
     . * ★ ✧ * .
       .  ⭐  .
          ★    
EOF
        sleep 0.2
        clear
        
        # Phase 2: Core collapse
        echo -e "${RED}"
        cat << "EOF"
        ✺ ✹ ✺
     ✺ ✹ ✺ ✹ ✺ 
   ✺ ✹ ✺ ✹ ✺ ✹ ✺
  ✺ ✹ ✺ ✹ ✺ ✹ ✺ ✹
   ✺ ✹ ✺ ✹ ✺ ✹ ✺
     ✺ ✹ ✺ ✹ ✺
        ✺ ✹ ✺
EOF
        sleep 0.2
        clear
        
        # Phase 3: Supernova explosion
        echo -e "${CYAN}"
        cat << "EOF"
      ⭐ ✺ ★ ✺
   ✧ ⭐ ✺ ★ ✺ ⭐ ✧
 ★ ✺ ⭐ ✧ ★ ✧ ⭐ ✺ ★
✺ ⭐ ✧ ★ ✺ ★ ✧ ⭐ ✺
 ★ ✺ ⭐ ✧ ★ ✧ ⭐ ✺ ★
   ✧ ⭐ ✺ ★ ✺ ⭐ ✧
      ⭐ ✺ ★ ✺
EOF
        sleep 0.2
        clear
        
        # Phase 4: Final burst
        echo -e "${YELLOW}"
        cat << "EOF"
    ✷ ⭐ ✺ ★ ✺ ⭐ ✷
  ✧ ⭐ ✺ ★ ✺ ★ ✺ ⭐ ✧
 ★ ✺ ⭐ ✧ ★ ✧ ⭐ ✺ ★ ✧
✺ ⭐ ✧ ★ ✺ ★ ✧ ⭐ ✺ ⭐
 ★ ✺ ⭐ ✧ ★ ✧ ⭐ ✺ ★ ✧
  ✧ ⭐ ✺ ★ ✺ ★ ✺ ⭐ ✧
    ✷ ⭐ ✺ ★ ✺ ⭐ ✷
EOF
        sleep 0.2
        clear
    done
}

cat << "EOF"
${CYAN}
 ____                                            
/ ___| _   _ _ __   ___ _ __ _ __   _____   ____ _ 
\___ \| | | | '_ \ / _ \ '__| '_ \ / _ \ \ / / _` |
 ___) | |_| | |_) |  __/ |  | | | | (_) \ V / (_| |
|____/ \__,_| .__/ \___|_|  |_| |_|\___/ \_/ \__,_|
            |_|                                      
EOF

echo -e "${YELLOW}🌟 PREPARING TO OBLITERATE ALL GIT REPOSITORIES...${NC}"
echo -e "${CYAN}Starting in current directory: ${NC}$(pwd)"

# Find and display git repositories
echo -e "\n${CYAN}╔════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║      DETECTED GIT REPOSITORIES          ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════╝${NC}\n"

# Store and display found repositories
git_repos=()
while IFS= read -r dir; do
    if [ -d "$dir/.git" ]; then
        # Check if this is actually a git repository root
        if (cd "$dir" && git rev-parse --is-inside-work-tree > /dev/null 2>&1); then
            # Get the absolute path to avoid duplicates
            absolute_path=$(cd "$dir" && pwd)
            git_repos+=("$dir")
        fi
    fi
done < <(find . -name ".git" -type d -prune -exec dirname {} \; | sort)

git_count=${#git_repos[@]}

if [ $git_count -eq 0 ]; then
    echo -e "${RED}💫 No Git repositories found in:${NC}"
    echo -e "${CYAN}$(pwd)${NC}"
    echo -e "${YELLOW}Nothing to obliterate!${NC}"
    exit 0
fi

# Display repositories with cool formatting
for repo in "${git_repos[@]}"; do
    depth=$(echo "$repo" | tr -cd '/' | wc -c)
    indent=$(printf '%*s' "$depth" '')
    echo -e "${YELLOW}$indent└─⚡️ ${RED}$repo${NC}"
done

echo -e "\n${CYAN}╔════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  ${RED}$git_count${CYAN} repositories will be obliterated!    ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════╝${NC}\n"

# Confirmation prompt
echo -e "${YELLOW}☢️  Are you sure you want to delete ALL these repositories? ${NC}"
echo -e "${RED}    This action cannot be undone!${NC}"
read -p "$(echo -e ${YELLOW}Type 'SUPERNOVA' to confirm: ${NC})" confirmation

if [ "$confirmation" != "SUPERNOVA" ]; then
    echo -e "\n${CYAN}Operation aborted. Your repositories are safe.${NC}"
    exit 1
fi

echo -e "\n${RED}💥 INITIATING REPOSITORY OBLITERATION SEQUENCE...${NC}"
show_explosion
echo -e "\n${RED}💥 REMOVING ALL GIT REPOSITORIES...${NC}"
find . -name ".git" -type d -exec rm -rf {} +

echo -e "\n${RED}💥 TARGETING .gitignore FILES...${NC}"
show_explosion
echo -e "${RED}💥 REMOVING ALL .gitignore FILES...${NC}"
find . -name ".gitignore" -type f -exec rm -f {} +

echo -e "${YELLOW}✨ Done! Removed ${RED}$git_count${YELLOW} Git repositories and their .gitignore files${NC}"
