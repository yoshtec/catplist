#!/usr/bin/env zsh

/usr/libexec/PlistBuddy -c "Add integer1 integer 1" ./integers.plist
/usr/libexec/PlistBuddy -c "Add integer2 integer 100000" ./integers.plist

/usr/libexec/PlistBuddy -c "Add :stringdict:python string ๐" ./strings.plist
/usr/libexec/PlistBuddy -c "Add :stringdict:japanese string ๆฅๆฌ่ชใใงใใ" ./strings.plist
/usr/libexec/PlistBuddy -c "Add :stringdict:chinese string ไปๆฒกๅๅค้" ./strings.plist

#/usr/libexec/PlistBuddy -c "Add date date 0000-12-30" ./date.plist