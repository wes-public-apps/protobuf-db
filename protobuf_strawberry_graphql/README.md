# Purpose
The goal of this module is to provide the infrastructure to automatically convert a protobuf object to a graphql object. To accomplish this I chose the strawberry-graphql python library due to its rapidly growing popularity, effective documentation, and active maintainers.

# Usage Instructions
TBD

# Installation
TBD

# Testing
Point the python unittest discover program to the tests folder. 

# Known Limitations
1. when utilizing definition_to_type method a local copy of any dependency is created. So globally across multiple defintion conversions you might have duplicate object definitions. There is no real way around this without having the complete global set of definitions provided all at once. This also does not have any usage implications to my knowledge because from a client perspective the same data structure gets presented no matter the specific implementation of a duplicate definition. Lets use an example, lets say I have a common message called RawMsg that contains an id and data. I also have mesg1 which contains a list of RawMsgs and mesg2 which has a single field called raw that is of type RawMsg. I will pass mesg1 to the definition_to_type method which will generate the objects for mesg1 and RawMsg within one file. I will then pass mesg2 to the method which will separately generate the objects for mesg2 and RawMsg. Now I have two copies of the RawMsg definition. 
2. 

# Future Work
1. minor - Convert this to a language that can be compiled so we do not depend on python being installed.
