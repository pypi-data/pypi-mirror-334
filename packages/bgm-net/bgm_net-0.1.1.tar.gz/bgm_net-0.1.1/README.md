# BGM
Python library made for python multiplayer games.

## About
This library made for python multilplayer games. It uses UDP protocol for transfering packets, library requires central server also packets are not encrypted but it gonna be soon.

## Packets
1. Connect packet
```
CONNECT|[From ip]|[To ip]|[From port]|[To port]
```
2. Disconnect packet
```
DISCONNECT|[From ip]|[To ip]
```

Other packets are made by user.

## Functions
### Server
1. Recive event - runs function everytime server recives message. Can be used as decorator
```
BGM_Server.recive_event(callback: Callable (data: Tuple, address: Tuple) ) 
```
2. Connect event - runs function everytime server recives connection. Can be used as decorator
```
BGM_Server.connect_event(callback: Callable (address: Tuple) )
```
3. Disconnect event - runs function everytime server recives disconnection. Can be used as decorator
```
BGM_Server.disconnect_event(callback: Callable (address: Tuple) )
```
4. Start server - Starts server on defined ip and port
```
BGM_Server.start_server()
```
5. Broadcast - Sends a same packet to everyone
```
BGM_Server.broadcast(message: Bytes)
```
6. Constructor - Construct packet with data given and type.
```
Packets.Constructor(data: Dict, type: String)
```
7. Deconstructor - Deconstructs packet given in arg.
```
Packets.Deconstructor(message: Str)
```
### Client
1. Connect - Connects to server with given information
```
BGM_Client.connect(ip: Str, port: Int)
```
2. Send - Send packet to connected server with given information.
```
BGM_Client.send(data: Dict, packet: Str)
```
3. Recive Event - If u are connected to any server it will call callback everytime u recive message (can be used more that 1 time)
```
BGM_Client.recive_event(callback: Callable)
```
4. Disconnect - Disconnects you from connected server
```
BGM_Client.disconnect()
```
5. Constructor - Construct packet with data given and type.
```
Packets.Constructor(data: Dict, type: String)
```
6. Deconstructor - Deconstructs packet given in arg.
```
Packets.Deconstructor(message: Str)
```
7. Disconnect - Returns constructed packet for disconnect
```
Packets.disconnect(fromip: Str, toip: Str)
```
8. Deconstructor - Returns constructed packet for connection
```
Packets.connect(fromip: Str, toip: Str, fromport: Int, toport: Int)
```

## Credits
Made by danxvo