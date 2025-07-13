# Network Clipboard Share

A Python CLI application that allows machines on the same network to discover each other and share clipboard contents in real-time.

## Features

- **Network Discovery**: Finds other machines running the application on the same network
- **Clipboard Sharing**: Enables real-time clipboard sharing between connected machines
- **Dual Protocol**: Uses both TCP and UDP sockets for different operations
- **Threaded Architecture**: Implements threading for concurrent operations
- **Graceful Shutdown**: Custom shutdown procedure for clean exits

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/shahradArianNezhad/clipboard-over-internet.git
   cd clipboard-over-internet
   ```
2. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the application with:
```bash
python main.py
```

## Options

- **--port or -p**: Specify a custom port (default: 6969)

## How it works

1. **Discovery Phase**:  

    - Uses UDP broadcast to find other instances on the network  
    - Establishes initial contact between machines  
2. **Connection Phase**:  
    - Sets up TCP connections between discovered peers  
    - Maintains persistent connections for clipboard sharing
3. **Clipboard Sync**:  
    - Monitors local clipboard for changes  
    - Sends updates to connected peers  
    - Receives and applies updates from peers  

## Requirements:  
- Python 3.6+
- pyperclip (or similar clipboard library for your OS)
- xclip for linux machines (sudo apt-get install xclip or sudo pacman -S xclip)

## Future Plans:
- adding file transfer
- adding a gui
- mobile phone compatibility