#!/usr/bin/env python

from essentia_test import *
from essentia import *
from numpy import sort

class TestSlicer(TestCase):

    def slice(self, startTimes, endTimes):
        nSlices = len(startTimes)
        if nSlices != len(endTimes):
            print "Test cannot be computed"
            exit(1)
        input = range(max(endTimes))

        # expected values:
        expected = []
        orderedTimes = []
        for i in range(nSlices):
            time = (startTimes[i], endTimes[i])
            orderedTimes.append(time)
        orderedTimes = sorted(orderedTimes, lambda x,y:x[0]-y[0])

        for i in range(nSlices):
            expected.append(input[orderedTimes[i][0]:orderedTimes[i][1]])

        result = Slicer(startTimes = startTimes,
                        endTimes = endTimes,
                        timeUnits="samples")(input)

        self.assertEqual(len(result), len(expected))
        for i in range(nSlices):
            self.assertEqualVector(result[i], expected[i])

    def testEqualSize(self):
        startTimes = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
        endTimes =   [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        self.slice(startTimes, endTimes)

    def testDifferentSize(self):
        startTimes = [0, 11, 22, 33, 44, 55, 66, 77, 88, 99]
        endTimes =   [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        self.slice(startTimes, endTimes)

    def testOverlap(self):
        startTimes = [0, 11, 22, 33, 44, 0, 6, 5, 88, 19]
        endTimes   = [30, 60, 45, 100, 50, 60, 10, 50, 100, 99]
        self.slice(startTimes, endTimes)

    def testInvalidParam(self):
        # startTime later than endTime:
        startTimes = [35, 11]
        endTimes   = [30, 60]
        self.assertConfigureFails(Slicer(), {'startTimes' : startTimes,
                                             'endTimes' : endTimes})

        self.assertConfigureFails(Slicer(), {'timeUnits' : 'unknown'})

    def testEmpty(self):
        startTimes = [0, 11]
        endTimes   = [30, 60]
        result = Slicer(startTimes = startTimes,
                        endTimes = endTimes,
                        timeUnits="samples")([])
        self.assertEqualVector(result, [])

    def testOneSample(self):
        startTimes = [0]
        endTimes   = [1.0/44100.0]
        result = Slicer(startTimes = startTimes,
                        endTimes = endTimes,
                        timeUnits="seconds")([1])
        self.assertEqualVector(result, [1])

    def testVeryLargeStartAndEndTimes(self):
        # no slices if times are beyond the input length:
        startTimes = [100]
        endTimes   = [101]
        result = Slicer(startTimes = startTimes,
                        endTimes = endTimes,
                        timeUnits="samples")([1]*50)
        self.assertEqual(result, [])

    def testEndTimePastEof(self):
        # no slices if times are beyond the input length:
        startTimes = [0]
        endTimes   = [100]
        result = Slicer(startTimes = startTimes,
                        endTimes = endTimes,
                        timeUnits="seconds")([1])
        self.assertEqualVector(result, [])

    def Overflow(self):
        self.assertConfigureFails(Slicer(), {'sampleRate' : 44100,
                                             'startTimes' : [2147483649.0],
                                             'endTimes' : [2147483649.5],
                                             'timeUnits' : 'seconds'})

suite = allTests(TestSlicer)

if __name__ == '__main__':
    TextTestRunner(verbosity=2).run(suite)