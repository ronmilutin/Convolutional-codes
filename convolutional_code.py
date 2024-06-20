from typing import List
class ConvolutionalCode:
    """The code assumes zero state termination, and k=1"""
    def __init__(self, generators: tuple):
        """
        :param generators: each element in the tuple represents a single generator polynomial. The convention
        we use is: 1+D=b011=3 (and not 1+D=6)
        """
        pass

    def encode(self, data: bytes) -> List[int]:
        """
        encode input data bytes. Uses zero tail termination

        :param data: data to be encoded
        :return: encoded data
        :rtype: List[int]
        """
        pass

    def decode(self, data: List[int]) -> (bytes, int):
        """
        decode data bytes. The function assumes initial and final state of encoder was at the zero state.

        :param data: coded data to be decoded, list of ints representing each received bit.
        :return: return a tuple of decoded data, and the amount of corrected errors.
        :rtype: (bytes, int)
        """
        pass



