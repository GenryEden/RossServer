"""
An example of passing messages using observer (Notifier[T] -> Listener[T]) pattern
Scheme:
                          bytes               TSLEvent                RossEvent                  bytes
socket - - - > UDPServer -------> UMDDecoder ----------> RossDecoder ----------> RossEventToEzTSLUMD ----==

==----> ListenerLogger - - - > loguru
"""

if __name__ == "__main__":
    import sys

    sys.path.append('../')
    from UDPServer import UDPServer
    from EzTSLUMDEncoder import RossEventToEzTSLUMD
    from RossServer import RossDecoder
    from UMDDecoder import UMDDecoder
    from UtilityDecoders import ListenerLogger

    listenerLogger = ListenerLogger()
    eztslumdEncoder = RossEventToEzTSLUMD(listenerLogger)
    rossDecoder = RossDecoder(eztslumdEncoder)
    umdDecoder = UMDDecoder(rossDecoder)
    udpServer = UDPServer(umdDecoder, host="127.0.0.1", port=1337)
    udpServer.run()
