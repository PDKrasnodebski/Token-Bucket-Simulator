from FlowCons import Bit_stream_cons
import time
from Monitor import Monitor
from TokenBucket import TokenBucket


if __name__=="__main__":

        bucket1 = TokenBucket(3, 2, True)

        bucket2 = TokenBucket(3, 2, True)

        bucket1.set_with_lock(742, 75000)

        t = [Bit_stream_cons(50,50,4,6), Bit_stream_cons(50,50,4,6), Bit_stream_cons(50,50,4,6)]
        #t2 = [Bit_stream_cons(50,50,4,6), Bit_stream_cons(50,50,4,6), Bit_stream_cons(50,50,4,6)]

        Mon1 = Monitor(bucket1, t, 1, 15)

        #Mon2 = Monitor(bucket2, t2, 1, 7)

        Mon1.start_observation()
        #Mon2.start_observation()


