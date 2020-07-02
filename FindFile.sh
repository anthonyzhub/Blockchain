#! /usr/bin/bash

# Ask for directory of file's location
read -p "Enter file's directory: " dir

# If user enters ".", replace "." with current working directory
# If user enters "~", replace "~" with home directory
# Search and replace -> ${parameter/search/replacement}
if [ "$dir" == "." ]
then
    # Search and replace
    dir=${dir/"."/$PWD}
elif [ "$dir" == "~" ]
then
    dir=${dir/"~"/$HOME}
fi

# Check if directory exists
# ! -> Negate
# -d -> Check if directory exists
if [ ! -d "$dir" ]
then
    echo "Directory does not exist"
    exit
fi

# Change directory and ask for file
cd $dir
read -p "Enter filename: " file

# Check if file exists
if [ ! -f "$file" ]
then
    echo "File does not exist"
    exit
fi

# Output file's content
cat $file