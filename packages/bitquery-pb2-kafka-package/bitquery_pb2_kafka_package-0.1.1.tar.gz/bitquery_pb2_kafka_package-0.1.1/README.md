# Solana Package

A Python library containing pb2 files to simplify parsing Solana blockchain data  on Kafka.

## Installation

Install easily via pip:

```bash
pip install bitquery-pb2-kafka-package
```

## Usage

Importing and using protobuf messages:
You can import and use the protobuf-generated Python classes as follows:


```
from solana import block_message_pb2

# Create a new BlockMessage instance
block_message = block_message_pb2.BlockMessage()

# Assign fields (replace with actual fields)
block_message.field_name = "value"

# Serialize the message to bytes
serialized_message = block_message.SerializeToString()

# Deserialize bytes back into a message
received_message = block_message_pb2.BlockMessage()
received_message.ParseFromString(serialized_message)

print(received_message)

```

## Available Protobuf Messages

-   `block_message_pb2.BlockMessage`
-   `dex_block_message_pb2.DexBlockMessage`
-   `ohlc_message_pb2.OhlcMessage`
-   `parsed_idl_block_message_pb2.ParsedIdlBlockMessage`
-   `token_block_message_pb2.TokenBlockMessage`
