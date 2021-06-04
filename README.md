# catplist

`catplist` is a small python utility to print apple plists 
([Information Property List](https://developer.apple.com/documentation/bundleresources/information_property_list/)) 
in a readable and comprehensible manner.

## Rationale

While `plistutil` exists to convert plists from binary to xml and vice versa plists are usually still hard to 
read for humans or parse from the command line with tools like grep. `catplist` aims to make this task easier.
It's main focus is to print a **human-readable** and parsable representation of the plist. Additionally, plists
often contain binary data, or some strange nested key value structures originating from 
[NSArchiver](https://developer.apple.com/documentation/foundation/nsarchiver)
or [NSKeyedArchiver](https://developer.apple.com/documentation/foundation/nskeyedarchiver) serialization. 
`catplist` aims to deliver a good readable representation by unwrapping those structures. 

Try it on some Metadata out of your iPhone Photo library like `*.albummetadata`, `*.memorymetadata`, `*.facemetadata`, 
`*.foldermetadata` or just regular `*.plist` files. 

For editing and more accurate/original representation of plists or search for PlistBuddy, XCode, plutil. 

## Features

* wildcard support 
* recurse into directories

* reads binary and xml plists
  
* NSArchiver: unwraps nsarchiver plists that just add an layer of indirectness into the key value store.
* Nested plists: in some plists apple stores plist as a value. `catplist` unwraps those nested plists.
* Interpretation of some of Binary Data stored within plists, usually consisting of:
  * UUID data
  * xz compressed data
  * binary plists
  
## Usage

```
catplist myplist.plist
```

```
> catplist --help

Usage: catplist [OPTIONS] [FILE]...

  This is catplist: display your plist for human reading and easy grepping.

Options:
  -R, --raw      print raw plist contents, will not unpack nested data & plists
  -r, --recurse  recurse into subdirs, reads all files ignores non plist files
  --help         Show this message and exit.
```

## Install

Installation via PyPi:
```
pip install catplist
```