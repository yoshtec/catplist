#!/usr/bin/env zsh

/usr/libexec/PlistBuddy -c "Add integer1 integer 1" ./integers.plist
/usr/libexec/PlistBuddy -c "Add integer2 integer 100000" ./integers.plist

/usr/libexec/PlistBuddy -c "Add :stringdict:python string 🐍" ./strings.plist
/usr/libexec/PlistBuddy -c "Add :stringdict:japanese string 日本語もできる" ./strings.plist
/usr/libexec/PlistBuddy -c "Add :stringdict:chinese string 他没喝啤酒" ./strings.plist

#/usr/libexec/PlistBuddy -c "Add date date 0000-12-30" ./date.plist