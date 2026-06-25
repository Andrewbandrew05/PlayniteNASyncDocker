import asyncio

import sharedUtility

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Connection from {addr}")
    
    data = await reader.read(1024)
    message = data.decode('utf-8')
    print(f"Received: {message}")

    if "fileTransfer" in message:
        messageList = message.split("|")
        print(messageList, flush = True)
        await sharedUtility.sharedMethods.transferFolderWithRsync(messageList[1], messageList[2])
    
    writer.write(f"ACK: {message}".encode('utf-8'))
    await writer.drain()
    writer.close()

async def run_tcp_server():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 8081)
    print("TCP Server running on 9999")
    async with server:
        await server.serve_forever()