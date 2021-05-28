# catplist

catplist is a small python utility to print apple plists (Property List) in a readable and comprehenhsible manner.

## Rationale

While plistutil exists to convert plists from binary to xml and vice versa plists are usually still hard to 
read for humans or parse from the command line with tools like grep. catplist aims to make this task easier.
It main focus is to print a human readable and parsable representation of the plist. Additionally plists
often contain binary data or some strange nested key value structures coming from the NSArchiver
serialization. catplist aims to deliver a good readable approximation by unpacking. 

## Features

* reads binary and xml plists
* NSArchiver: unwraps nsarchiver plists that just add an layer of indirectness into the key value store.
* Nested plists: in some plists apple stores plist as a value. catplist unwraps those nested plists.
* Interpretation of some of Binary Data stored within plists:
  * UUID data
  * xz compressed
  * binary plists


## Usage

```
catplist myplist.plist
```