
## Model Answer 9

A model answer is provided in the `kafka_solution` folder, which is available on OLAT. To run the scripts, start six consoles and run six scripts simultaneously (starting the consumers first). You can then observe the messages making their way through the streaming pipeline and being processed by the different operators.

A small note concerning the `if received_messages == ...` statements breaking out of the loop: they are not strictly necessary. If you do not include them, you just have to end the consumers with Ctrl-C.
