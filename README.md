# Protobuf Utility Purpose
The goal of this utility is to provide a collection of modules that contribute to an overall open source infrastructure project to enable event driven data stream logging, real time processing, translation, schema management, and analysis for a well defined protobuf management tool. In other words, it provides the infrastructure to take the compelxity out of building a data pipeline. The protobuf_utility_module is a lean one size fits all solution to this problem. It is designed to require very few 3rd party dependencies and provide a single point of entry for all steps of protobuf management. It is a powerful local developer tool and it provides a good foundation on which more powerful data pipeline automation can occur. The weaknesses of this module are that it does not take advantage of many third party tools that could drastically enhance the capabilities of this tool, making it more effective right out of the box, and it is one size fits all. The breadth of this module improves its usability but results in unncessary logic when it is being utilized for a very specific purpose. My vision for this project is that it forms the back bone of a data pipeline and in that context we need only one aspect of the utility for any given step in the pipeline. This means all other logic and their associated dependencies are just bloat for that specific step. To remedy this problem all other modules in this repo take an aspect of the protobuf_utility_module and specialize in it. This enables utilizing domain specific dependencies and makes this utility modularized in a way that is conducive to populating steps of a data pipeline.

# Introduction
[Google's Protobuf Documentation](https://developers.google.com/protocol-buffers)

When an system uses a collection of microservices to accomplish its goal, one of the problems you must solve is defining a common message definition and libraries around that definition for each language you utilize in your microservice architecture so they can all communicate with each other effectively. Google solved this problem with their protobuf project which is actively maintained, public, and well documented. This makes it an ideal project to utilize in production.

There are many benefits to using the system outlined above that I will not get into here because they are discussed more effectively elsewhere (I recommend "Building Microservices" by Sam Newman) but one of the biggests cons is an increase in complexity around managing such a system. One chunk of that complexity is low latency handling of the messages being streamed between microservices. There is significant value in using those messages to gain real time insight into the health of your system and for deep analysis later on. That is where this protobuf utility comes into play. It provides infrastructure for logging the streamed messages, transforms to automate the data ingestion pipeline, and finally some data analysis tools.

# Protobuf Logger
This part of the protobuf utility handles logging the live stream of protobuf messages.

# Translation
This part of the protobuf utility handles converting the logged protobuf data into different formats.

# Protobuf to Schema
This part of the protobuf-db utility converts a collection of protobuf message definitions as python objects into an sql schema.

# Protobuf Change to Schema Migration Script
This part of the protobuf-db utility takes a collection of protobuf message definitions, compares it to another collection in order to generate a migration sql file.

# Playback simulation
This part of the protobuf-db utility takes a collection of protobuf message objects that were collected using the logger utility and replays them for testing purposes. This utility gives you the flexibility to specify what data types of the stream to replay and to what broker.

# Developer GUI
This part of the protobuf utility provides tools to convert protobufs to a graphql schema.

# Out of Scope
- Services
- Options

# Future Work
1. Implement logging functionality in a lower level language such as C
2. implement real time processing infrastructure in a lower level language such a C
