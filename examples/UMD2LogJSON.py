"""
An example of passing messages using observer (Notifier[T] -> Listener[T]) pattern

Scheme:
                          bytes               TSLEvent                RossEvent                  string
socket - - - > UDPServer -------> UMDDecoder ----------> RossDecoder ----------> RossEventToJSON ----==

==----> ListenerLogger - - - > loguru
"""

if __name__ == "__main__":
    import sys

    sys.path.append('../')
    from UDPServer import UDPServer
    from JSONEncoder import RossEventToJson
    from RossServer import RossDecoder
    from UMDDecoder import UMDDecoder
    from UtilityDecoders import ListenerLogger

    listenerLogger = ListenerLogger()
    jsonEncoder = RossEventToJson(listenerLogger)
    rossDecoder = RossDecoder(jsonEncoder)
    umdDecoder = UMDDecoder(rossDecoder)
    udpServer = UDPServer(umdDecoder, host="127.0.0.1", port=1337)
    udpServer.run()