import os
import random
import unittest
import stat
import tempfile

from watarray import WatArray, BitArray, NOTFOUND


def RandomQuery(n):
    while True:
        beg = random.randint(0, n - 1)
        end = random.randint(0, n)
        if beg != end:
            break
    if beg > end:
        beg, end = end, beg
    return beg, end


def SetVals(rq, array, vals):
    for i in range(rq[0], rq[1]):
        vals.append((array[i], i))
    vals.sort()


def UniqCount(vals, ret):
    if not vals:
        return
    prev = vals[0][0]
    count = 1
    for i in range(1, len(vals)):
        if prev != vals[i][0]:
            ret.append((prev, count))
            prev = vals[i][0]
            count = 1
        else:
            count += 1
    ret.append((prev, count))


def FilterRange(char_range, uniq_counts):
    return [c for c in uniq_counts
            if (char_range[0] <= c[0] < char_range[1])]


def FreqComp(x):
    return x[1], -x[0]

FreqCompLR = FreqComp


def WatRandomInitialize(wa, array, alphabet_num, n):
    freq = [0] * alphabet_num
    for i in range(n):
        c = random.randint(0, alphabet_num - 1)
        array.append(c)
        freq[c] += 1
    wa.Init(array)


class TestBitArray(unittest.TestCase):
    def test_trivial(self):
        ba = BitArray()
        self.assertEqual(ba.length(), 0)
        self.assertEqual(ba.one_num(), 0)

        _, filename = tempfile.mkstemp()
        ba.dump(filename)
        data = ba.dumps()
        del ba

        ba = BitArray()
        ba.load(filename)
        os.remove(filename)
        self.assertEqual(ba.length(), 0)
        self.assertEqual(ba.one_num(), 0)
        del ba

        ba = BitArray()
        ba.loads(data)
        self.assertEqual(ba.length(), 0)
        self.assertEqual(ba.one_num(), 0)
        del ba

    def test_selectblock(self):
        x = 0
        ba = BitArray()

        notx = 2 ** 64 - 1
        for i in range(64):
            self.assertEqual(ba.SelectInBlock(notx, i + 1), i)

        for i in range(64):
            x |= 1 << i

        for i in range(64):
            self.assertEqual(ba.SelectInBlock(x, i + 1), i)

    def test_trivial_zero(self):
        N = 100
        ba = BitArray(N)

        ba.Build()
        self.assertEqual(ba.length(), N)
        for i in range(ba.length()):
            self.assertEqual(ba.Lookup(i), 0)
            self.assertEqual(ba.Rank(0, i), i)
            self.assertEqual(ba.Select(0, i + 1), i)

    def test_tirivial_one(self):
        N = 1000
        ba = BitArray(N)
        for i in range(1000):
            ba.SetBit(1, i)

        ba.Build()
        self.assertEqual(ba.length(), N)
        for i in range(ba.length()):
            self.assertEqual(ba.Lookup(i), 1)
            self.assertEqual(ba.Rank(1, i), i)
            self.assertEqual(ba.Select(1, i + 1), i)

    def test_random(self):
        N = 100000
        ba = BitArray(N)
        B = []
        for i in range(N):
            b = random.randint(0, 1)
            ba.SetBit(b, i)
            B.append(b)

        ba.Build()
        self.assertEqual(ba.length(), N)
        sum = 0
        for i in range(ba.length()):
            self.assertEqual(ba.Lookup(i), B[i])
            if B[i]:
                self.assertEqual(ba.Rank(1, i), sum)
                self.assertEqual(ba.Select(1, sum + 1), i)
            else:
                self.assertEqual(ba.Rank(0, i), i - sum)
                self.assertEqual(ba.Select(0, i - sum + 1), i)
            sum += B[i]


class TestWatArray(unittest.TestCase):
    def test_example(self):
        wa = WatArray()
        A = [5, 1, 0, 4, 2, 2, 0, 3]
        wa.Init(A)
        self.assertEqual(wa.length(), 8)
        self.assertEqual(wa.Lookup(3), 4)
        self.assertEqual(wa.Rank(2, 6), 2)
        self.assertEqual(wa.Select(2, 2), 5)
        self.assertEqual(wa.RankLessThan(4, 5), 3)
        self.assertEqual(wa.RankMoreThan(4, 5), 1)
        self.assertEqual(wa.FreqRange(2, 5, 2, 6), 3)
        self.assertEqual(wa.RankAll(4, 5), (1, 3, 1))
        self.assertEqual(wa.RankAll(7, 5), (NOTFOUND, NOTFOUND, NOTFOUND))
        self.assertEqual(wa.MaxRange(1, 6), (3, 4))
        self.assertEqual(wa.MinRange(1, 6), (2, 0))
        self.assertEqual(wa.QuantileRange(1, 6, 3), (4, 2))
        self.assertEqual(wa.ListModeRange(2, 5, 1, 6, 3), [(2, 2), (4, 1)])
        self.assertEqual(
            wa.ListMinRange(1, 5, 1, 6, 3), [(1, 1), (2, 2), (4, 1)])
        self.assertEqual(
            wa.ListMaxRange(1, 5, 1, 6, 3), [(4, 1), (2, 2), (1, 1)])

        fname = tempfile.mkstemp()[1]

        wa.dump(fname)
        wa.Clear()
        self.assertEqual(wa.length(), 0)
        wa.load(fname)
        self.assertEqual(wa.length(), 8)
        os.remove(fname)

        s = wa.dumps()
        wa.Clear()
        self.assertEqual(wa.length(), 0)
        wa.loads(s)
        self.assertEqual(wa.length(), 8)

        wa.Clear()
        del wa

    def test_trivial(self):
        wa = WatArray()
        self.assertEqual(wa.alphabet_num(), 0)
        self.assertEqual(wa.length(), 0)
        self.assertEqual(wa.Rank(0, 0), NOTFOUND)
        self.assertEqual(wa.Select(0, 0), NOTFOUND)
        self.assertEqual(wa.Lookup(0), NOTFOUND)
        self.assertEqual(wa.Freq(0), NOTFOUND)
        self.assertEqual(wa.FreqSum(0, 1), NOTFOUND)

        rank, rank_less_than, rank_more_than = wa.RankAll(0, 0)
        self.assertEqual(rank, NOTFOUND)
        self.assertEqual(rank_less_than, NOTFOUND)
        self.assertEqual(rank_more_than, NOTFOUND)

        pos, val = wa.MaxRange(0, 0)
        self.assertEqual(pos, NOTFOUND)
        self.assertEqual(val, NOTFOUND)

        _, filename = tempfile.mkstemp()
        wa.dump(filename)
        data = wa.dumps()
        del wa

        wa = WatArray()
        wa.load(filename)
        os.remove(filename)
        self.assertEqual(wa.Rank(0, 0), NOTFOUND)
        self.assertEqual(wa.Select(0, 0), NOTFOUND)
        self.assertEqual(wa.Lookup(0), NOTFOUND)
        del wa

        wa = WatArray()
        wa.loads(data)
        self.assertEqual(wa.Rank(0, 0), NOTFOUND)
        self.assertEqual(wa.Select(0, 0), NOTFOUND)
        self.assertEqual(wa.Lookup(0), NOTFOUND)
        del wa

    def test_alphanum_one(self):
        A = [0] * 5

        wa = WatArray()
        wa.Init(A)
        self.assertEqual(wa.length(), 5)
        self.assertEqual(wa.alphabet_num(), 1)
        self.assertEqual(wa.Freq(0), 5)
        self.assertEqual(wa.FreqSum(0, 1), 5)
        for i in range(wa.length()):
            self.assertEqual(wa.Rank(0, i), i)
            self.assertEqual(wa.RankLessThan(0, i), 0)
            self.assertEqual(wa.RankMoreThan(0, i), 0)
            self.assertEqual(wa.Select(0, i + 1), i)
            for j in range(i + 1, wa.length() + 1):
                pos, val = wa.MaxRange(i, j)
                self.assertEqual(pos, i)
                self.assertEqual(val, 0)

                pos, val = wa.MinRange(i, j)
                self.assertEqual(pos, i)
                self.assertEqual(val, 0)

                lrs = wa.ListMinRange(0, 1, i, j, j - i)
                self.assertEqual(len(lrs), 1)
                self.assertEqual(lrs[0][0], 0)
                self.assertEqual(lrs[0][1], j - i)

                lrs = wa.ListModeRange(0, 1, i, j, j - i)
                lrs.sort()
                self.assertEqual(len(lrs), 1)
                self.assertEqual(lrs[0][0], 0)
                self.assertEqual(lrs[0][1], j - i)

    def test_save(self):
        A = [1, 1, 1, 1, 3, 0, 1, 1, 1, 1, 3, 1, 2, 2]
        wa = WatArray()
        wa.Init(A)
        self.assertEqual(wa.Rank(3, 14), 2)

        _, filename = tempfile.mkstemp()
        wa.dump(filename)
        data = wa.dumps()
        del wa

        wa = WatArray()
        wa.load(filename)
        os.remove(filename)
        self.assertEqual(wa.Rank(3, 14), 2)
        del wa

        wa = WatArray()
        wa.loads(data)
        self.assertEqual(wa.Rank(3, 14), 2)
        del wa

    def test_small(self):
        alphabet_num = 200
        array = range(alphabet_num)
        length = len(array)

        wa = WatArray()
        wa.Init(array)
        self.assertEqual(wa.alphabet_num(), alphabet_num)
        self.assertEqual(wa.length(), length)

        for i in range(alphabet_num):
            self.assertEqual(wa.Freq(i), 1)
            for j in range(i, alphabet_num):
                self.assertEqual(wa.FreqSum(i, j), j - i)

        self.assertEqual(wa.Rank(wa.alphabet_num() - 1, wa.length()), 1)
        self.assertEqual(wa.Rank(wa.alphabet_num(),     wa.length()), NOTFOUND)
        self.assertEqual(wa.Rank(wa.alphabet_num() + 1, wa.length()), NOTFOUND)

        counts = [0] * alphabet_num
        for i in range(length):
            c = array[i]
            self.assertEqual(c, wa.Lookup(i))
            sum = 0
            for j in range(alphabet_num):
                self.assertEqual(wa.Rank(j, i), counts[j])
                self.assertEqual(wa.RankLessThan(j, i), sum)
                self.assertEqual(wa.RankMoreThan(j, i), i - sum - counts[j])
                sum += counts[j]
            counts[c] += 1
            self.assertEqual(wa.Select(c, counts[c]), i)

            for j in range(i + 1, wa.length() + 1):
                pos, val = wa.MaxRange(i, j)
                self.assertEqual(pos, j - 1)
                self.assertEqual(val, j - 1)

                pos, val = wa.MinRange(i, j)
                self.assertEqual(pos, i)
                self.assertEqual(val, i)

                lrs = wa.ListMinRange(0, alphabet_num, i, j, j - i)

                for k in range(len(lrs)):
                    self.assertEqual(lrs[k][0], i + k)
                    self.assertEqual(lrs[k][1], 1)

                lrs = wa.ListModeRange(0, alphabet_num, i, j, j - i)
                lrs.sort()
                for k in range(len(lrs)):
                    self.assertEqual(lrs[k][0], i + k)
                    self.assertEqual(lrs[k][1], 1)

    def test_random(self):
        array = []
        alphabet_num = 100
        n = 10000
        freq = [0] * alphabet_num

        for i in range(n):
            c = random.randint(0, alphabet_num - 1)
            array.append(c)
            freq[c] += 1

        wa = WatArray()
        wa.Init(array)

        self.assertEqual(wa.alphabet_num(), alphabet_num)
        self.assertEqual(wa.length(), n)
        for i in range(alphabet_num):
            self.assertEqual(wa.Freq(i), freq[i])

        counts = [0] * alphabet_num
        for i in range(len(array)):
            c = array[i]

            self.assertEqual(wa.Lookup(i), c)
            s = 0
            for j in range(alphabet_num):
                if random.randint(0, 100 - 1) == 0:
                    self.assertEqual(wa.Rank(j, i), counts[j])
                    self.assertEqual(wa.RankLessThan(j, i), s)
                    self.assertEqual(wa.RankMoreThan(j, i), i - s - counts[j])
                s += counts[j]
            counts[c] += 1

            self.assertEqual(wa.Select(c, counts[c]), i)

    def test_min_range(self):
        wa = WatArray()
        array = []
        WatRandomInitialize(wa, array, 100, 1000)

        for iter in range(10):
            rq = RandomQuery(wa.length())
            vals = []
            SetVals(rq, array, vals)

            min_pos, min_val = wa.MinRange(rq[0], rq[1])
            self.assertEqual(vals[0][0], min_val)
            self.assertEqual(vals[0][1], min_pos)

    def test_quantile_range(self):
        wa = WatArray()
        array = []
        WatRandomInitialize(wa, array, 100, 1000)

        for iter in range(10):
            rq = RandomQuery(wa.length())
            vals = []
            SetVals(rq, array, vals)

            k = random.randint(0, rq[1] - rq[0] - 1)
            kth_pos, kth_val = wa.QuantileRange(rq[0], rq[1], k)
            self.assertEqual(vals[k][0], kth_val)

    def test_max_range(self):
        wa = WatArray()
        array = []
        WatRandomInitialize(wa, array, 100, 1000)

        for iter in range(10):
            rq = RandomQuery(wa.length())
            vals = []
            SetVals(rq, array, vals)

            max_pos, max_val = wa.MaxRange(rq[0], rq[1])
            self.assertEqual(vals[-1][0], max_val)

    def test_freq_range(self):
        wa = WatArray()
        array = []
        WatRandomInitialize(wa, array, 100, 1000)

        for iter in range(10):
            rq = RandomQuery(wa.length())
            arq = RandomQuery(wa.alphabet_num())
            count = 0
            for i in range(rq[0], rq[1]):
                if arq[0] <= array[i] < arq[1]:
                    count += 1

            if arq[1] >= wa.alphabet_num():
                count = NOTFOUND

            self.assertEqual(wa.FreqRange(arq[0], arq[1], rq[0], rq[1]), count)

    def test_list_mode_range(self):
        wa = WatArray()
        array = []
        WatRandomInitialize(wa, array, 100, 1000)

        for iter in range(10):
            rq = RandomQuery(wa.length())
            arq = RandomQuery(wa.alphabet_num())

            vals = []
            SetVals(rq, array, vals)

            uniq_counts = []
            UniqCount(vals, uniq_counts)
            uniq_counts.sort(key=FreqComp)
            uniq_counts = FilterRange(arq, uniq_counts)

            num = rq[1] - rq[0]
            lrs = wa.ListModeRange(arq[0], arq[1], rq[0], rq[1], num)
            lrs.sort(key=FreqCompLR)

            for i in range(min(len(lrs), len(uniq_counts))):
                self.assertEqual(lrs[i][0], uniq_counts[i][0])
                self.assertEqual(lrs[i][1], uniq_counts[i][1])

    def test_list_min_range(self):
        wa = WatArray()
        array = []
        WatRandomInitialize(wa, array, 100, 1000)

        for iter in range(10):
            rq = RandomQuery(wa.length())
            arq = RandomQuery(wa.alphabet_num())
            vals = []
            SetVals(rq, array, vals)
            uniq_counts = []
            UniqCount(vals, uniq_counts)
            uniq_counts = FilterRange(arq, uniq_counts)

            num = rq[1] - rq[0]
            lrs = wa.ListMinRange(arq[0], arq[1], rq[0], rq[1], num)
            for i in range(min(len(lrs), len(uniq_counts))):
                self.assertEqual(lrs[i][0], uniq_counts[i][0])
                self.assertEqual(lrs[i][1], uniq_counts[i][1])

    def test_list_max_range(self):
        wa = WatArray()
        array = []
        WatRandomInitialize(wa, array, 100, 1000)

        for iter in range(10):
            rq = RandomQuery(wa.length())
            arq = RandomQuery(wa.alphabet_num())
            vals = []
            SetVals(rq, array, vals)
            vals = vals[::-1]
            uniq_counts = []
            UniqCount(vals, uniq_counts)
            uniq_counts = FilterRange(arq, uniq_counts)

            num = rq[1] - rq[0]
            lrs = wa.ListMaxRange(arq[0], arq[1], rq[0], rq[1], num)
            for i in range(min(len(lrs), len(uniq_counts))):
                self.assertEqual(lrs[i][0], uniq_counts[i][0])
                self.assertEqual(lrs[i][1], uniq_counts[i][1])

    def test_error(self):
        wa = WatArray()
        _, filename = tempfile.mkstemp()

        mode = os.stat(filename)[0] \
            & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH
        os.chmod(filename, mode)
        self.assertRaises(IOError, lambda: wa.dump(filename))

        mode = mode & stat.S_IWUSR
        os.chmod(filename, mode)
        os.remove(filename)
        self.assertRaises(IOError, lambda: wa.load(filename))


def main():
    import sys
    test = sys.modules[__name__]
    suite = unittest.defaultTestLoader.loadTestsFromModule(test)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    unittest.main()
