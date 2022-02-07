#!/bin/zsh


BREWFILE=$HOME/Brewfile


function ask_confirmation {
    printf "\nContents of: $HOME/Brewfile\n\n"
    cat $BREWFILE
    printf "\n"

    read -q "RESPONSE?Install Brewfile? [y/N]: "

    if [[ $RESPONSE = "n" ]] then;
        printf "\nAborting Installation!\n"
        exit 0
    fi
}


function install_brewfile {
    printf "\n\nInstalling Brewfile...\n\n"
    brew bundle --file=$BREWFILE

    # Disable Homebrew analytics
    brew analytics off
}


function init_yabai {
    printf "\n\nInstalling yabai scripting addition...\n"
    sudo yabai --install-sa
    sudo yabai --load-sa
    brew services start yabai
    echo "--------------------------------------------------------------------"
    echo " Finalize yabai installation:"
    echo
    echo " 1. In 'System Preferences' > 'Mission Control' check 'Displays have"
    echo "    separate Spaces'. Or run:"
    echo
    echo "        defaults write com.apple.spaces spans-displays -bool false"
    echo
    echo " 2. To automatically load yabai scripting addition on startup, run:"
    echo
    echo "        sudo visudo -f /etc/sudoers.d/yabai"
    echo
    echo "    Add the following line:"
    echo
    echo "        $(whoami) ALL = (ALL) NOPASSWD: $(which yabai) --load-sa"
    echo
    echo " 3. Include the following at the top of your yabairc config."
    echo
    echo "        sudo yabai --load-sa"
    echo "        yabai -m signal --add event=dock_did_restart action=\"sudo yabai --load-sa\""
    echo
    echo " See https://github.com/koekeishiya/yabai/wiki for more info."
    echo "--------------------------------------------------------------------"
}


function init_skhd {
    brew services start skhd
}


function zsh_info {
    echo "--------------------------------------------------------------------"
    echo " Finalize zsh-completions installation:"
    echo
    echo " If you see the following error:"
    echo
    echo "     zsh compinit: insecure directories, run compaudit for list."
    echo
    echo " Run the following command:"
    echo
    echo "     compaudit | xargs chmod g-w"
    echo
    echo " See https://stackoverflow.com/a/22753363 for more info."
    echo "--------------------------------------------------------------------"

    # Error: The following directories are not writable by your user:
    # /usr/local/share/zsh
    # /usr/local/share/zsh/site-functions
    #
    # You should change the ownership of these directories to your user.
    #   sudo chown -R $(whoami) /usr/local/share/zsh /usr/local/share/zsh/site-functions
    #
    # And make sure that your user has write permission.
    #   chmod u+w /usr/local/share/zsh /usr/local/share/zsh/site-functions
}


function main {
    ask_confirmation
    install_brewfile
    init_yabai
    init_skhd
    zsh_info
}


main
