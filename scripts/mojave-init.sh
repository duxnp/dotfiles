#!/usr/bin/env bash


###############################################################################
# 	For macOS Mojave version 10.14.1 (18B75)                                  #
###############################################################################


###############################################################################
# git and bash                                                                #
###############################################################################

# Create symlinks to .bashrc, .bash_profile, .gitconfig and .gitignore
#   via. ~/.dotfiles/
ln -s $HOME"/.dotfiles/.bashrc" $HOME"/.bashrc"
ln -s $HOME"/.dotfiles/.bash_profile" $HOME"/.bash_profile"
ln -s $HOME"/.dotfiles/.gitconfig" $HOME"/.gitconfig"
ln -s $HOME"/.dotfiles/.gitignore" $HOME"/.gitignore"


###############################################################################
# Homebrew                                                                    #
###############################################################################

# Create symlink to Brewfile and restore apps with Homebrew
#   via. ~/.dotfiles/Brewfile
ln -s $HOME"/.dotfiles/Brewfile" $HOME"/Brewfile"
cd && brew bundle


###############################################################################
# Fonts                                                                       #
###############################################################################

# Install fonts
#   via. ~/.dotfiles/fonts/
find $HOME"/.dotfiles/fonts" \
    \( -name "*.ttf" -or -name "*.otf" \) \
    -exec cp -v {} $HOME"/Library/Fonts" \;


###############################################################################
# Terminal                                                                    #
###############################################################################

# Set Terminal theme
osascript <<EOD

    set themeName to "Pro"
    set fontSize to "11"

	tell application "Terminal"

		set default settings to settings set themeName
		set font size of default settings to fontSize

	end tell

EOD


###############################################################################
# Moom                                                                        #
###############################################################################

# Restore Moom preferences
#   via ~/.dotfiles/moom/com.manytricks.Moom.plist
cp -f $HOME"/.dotfiles/moom/com.manytricks.Moom.plist" \
    $HOME"/Library/Preferences"


###############################################################################
# VSCode                                                                      #
###############################################################################

# Install Settings Sync Extension
code --install-extension Shan.code-settings-sync

echo "Mojave Initilization Done!"
