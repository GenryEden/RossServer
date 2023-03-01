"""
An example of passing messages using observer (Notifier[T] -> Listener[T]) pattern

Scheme:
                          bytes               TSLEvent
socket - - - > UDPServer -------> UMDDecoder ----------> ListenerLogger - - - > loguru
"""

if __name__ == "__main__":
    import sys

    sys.path.append('../')
    from UDPServer import UDPServer
    from UMDDecoder import UMDDecoder
    from UtilityDecoders import ListenerLogger

    listenerLogger = ListenerLogger()
    umdDecoder = UMDDecoder(listenerLogger)
    udpServer = UDPServer(umdDecoder, host="127.0.0.1", port=1337)
    udpServer.run()
