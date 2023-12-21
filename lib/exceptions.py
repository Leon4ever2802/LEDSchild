# -----------------------------------------------------------------------------
# Author               :   Leon Reusch
# -----------------------------------------------------------------------------

class SocketNotListeningError(Exception):
    """
    Exception raised when Socket is not able to accept connections because it has not been started.
    """

    def __init__(self, message="Socket is not listening because it has not been started"):
        super().__init__(message)