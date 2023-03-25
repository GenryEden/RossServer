"""
An example of passing messages using observer (Notifier[T] -> Listener[T]) pattern

Scheme:
                          bytes               TSLEvent
socket - - - > UDPServer -------> UMDDecoder ----------> ListenerLogger - - - > loguru
"""
<<<<<<< HEAD
=======

>>>>>>> ae1e08c (Added "JSONEncoder.py" and example file "UMD2LogJSON.py")

if __name__ == "__main__":
    import sys

    sys.path.append('../')
    from UDPServer import UDPServer
    from RossServer import RossDecoder
    from UMDDecoder import UMDDecoder
    from UtilityDecoders import ListenerLogger

    listenerLogger = ListenerLogger()
    rossDecoder = RossDecoder(listenerLogger)
    umdDecoder = UMDDecoder(rossDecoder)
    udpServer = UDPServer(umdDecoder, host="127.0.0.1", port=1337)
    udpServer.run()
