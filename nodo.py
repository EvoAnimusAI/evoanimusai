import asyncio
import websockets
import json

class NodoP2P:
    def __init__(self, puerto, peers=[]):
        self.puerto = puerto
        self.peers = peers  # Lista de ws://... de peers
        self.conexiones = set()

    async def servidor(self, websocket, path):
        print(f"Nuevo peer conectado")
        self.conexiones.add(websocket)
        try:
            async for mensaje in websocket:
                print(f"Recibí: {mensaje}")
        except:
            pass
        finally:
            self.conexiones.remove(websocket)
            print(f"Peer desconectado")

    async def conectar_peers(self):
        for uri in self.peers:
            try:
                ws = await websockets.connect(uri)
                self.conexiones.add(ws)
                print(f"Conectado a peer: {uri}")
                asyncio.create_task(self.escuchar(ws))
            except Exception as e:
                print(f"Error conectando a {uri}: {e}")

    async def escuchar(self, websocket):
        try:
            async for mensaje in websocket:
                print(f"Mensaje de peer: {mensaje}")
        except:
            self.conexiones.remove(websocket)
            print("Peer desconectado")

    async def enviar_mensaje(self, mensaje):
        if self.conexiones:
            await asyncio.wait([ws.send(mensaje) for ws in self.conexiones])
        else:
            print("No hay peers conectados para enviar mensajes")

    async def run(self):
        servidor = await websockets.serve(self.servidor, "localhost", self.puerto)
        print(f"Servidor corriendo en ws://localhost:{self.puerto}")
        await self.conectar_peers()

        while True:
            msg = input("Mensaje para enviar a peers: ")
            await self.enviar_mensaje(msg)

if __name__ == "__main__":
    import sys

    # Ejemplo de uso:
    # python nodo.py 8765 ws://localhost:8766
    puerto = int(sys.argv[1])
    peers = sys.argv[2:]
    nodo = NodoP2P(puerto, peers)
    asyncio.run(nodo.run())
