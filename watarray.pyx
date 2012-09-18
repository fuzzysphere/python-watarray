#cython: embedsignature=True 
from cython cimport address
from cython.operator import dereference, preincrement
from libc cimport stdlib
from libc.stdint cimport uint64_t
from libcpp.vector cimport vector
from libcpp.string cimport string

cimport cpp_watarray
from cpp_watarray cimport ListResult, dump, load, dumps, loads

NOTFOUND = <uint64_t> cpp_watarray.NOTFOUND

cdef class WatArray:
    cdef cpp_watarray.WatArray *thisptr
    def __cinit__(self):
        self.thisptr = new cpp_watarray.WatArray()
        if self.thisptr is NULL:
            raise MemoryError
    def __dealloc__(self):
        del self.thisptr
    def Init(self, iterable, *args):
        self._Init(iterable)
    cdef _Init(self, iterable):
        cdef vector[uint64_t] *v = new vector[uint64_t]()
        if v is NULL:
            raise MemoryError
        cdef uint64_t c
        for c in iterable:
            v.push_back(c)
        self.thisptr.Init(dereference(v))
        del v
    def Clear(self):
        self.thisptr.Clear()
    def Lookup(self, uint64_t pos):
        return self.thisptr.Lookup(pos)
    def Rank(self, uint64_t c, uint64_t pos):
        return self.thisptr.Rank(c, pos)
    def Select(self, uint64_t c, uint64_t rank):
        return self.thisptr.Select(c, rank)
    def RankLessThan(self, uint64_t c, uint64_t pos):
        return self.thisptr.RankLessThan(c, pos)
    def RankMoreThan(self, uint64_t c, uint64_t pos):
        return self.thisptr.RankMoreThan(c, pos)
    def RankAll(self, uint64_t c, uint64_t pos):
        cdef uint64_t rank = NOTFOUND, rank_less_than = NOTFOUND, rank_more_than = NOTFOUND
        self.thisptr.RankAll(c, pos, rank, rank_less_than, rank_more_than)
        return (rank, rank_less_than, rank_more_than)
    def FreqRange(self, uint64_t min_c, uint64_t max_c, uint64_t beg_pos, uint64_t end_pos):
        if max_c >= self.alphabet_num():
            return NOTFOUND
        return self.thisptr.FreqRange(min_c, max_c, beg_pos, end_pos)
    def MaxRange(self, uint64_t beg_pos, uint64_t end_pos):
        cdef uint64_t pos = NOTFOUND, val = NOTFOUND
        self.thisptr.MaxRange(beg_pos, end_pos, pos, val)
        return (pos, val)
    def MinRange(self, uint64_t beg_pos, uint64_t end_pos):
        cdef uint64_t pos = NOTFOUND, val = NOTFOUND
        self.thisptr.MinRange(beg_pos, end_pos, pos, val)
        return (pos, val)
    def QuantileRange(self, uint64_t beg_pos, uint64_t end_pos, uint64_t k):
        cdef uint64_t pos = NOTFOUND, val = NOTFOUND
        self.thisptr.QuantileRange(beg_pos, end_pos, k, pos, val)
        return (pos, val)
    def ListModeRange(self, uint64_t min_c, uint64_t max_c, uint64_t beg_pos, uint64_t end_pos, uint64_t num):
        cdef vector[ListResult] res = vector[ListResult]()
        self.thisptr.ListModeRange(min_c, max_c, beg_pos, end_pos, num, res)
        r = self._ListRange(res)
        return r
    def ListMinRange(self, uint64_t min_c, uint64_t max_c, uint64_t beg_pos, uint64_t end_pos, uint64_t num):
        cdef vector[ListResult] res = vector[ListResult]()
        self.thisptr.ListMinRange(min_c, max_c, beg_pos, end_pos, num, res)
        r = self._ListRange(res)
        return r
    def ListMaxRange(self, uint64_t min_c, uint64_t max_c, uint64_t beg_pos, uint64_t end_pos, uint64_t num):
        cdef vector[ListResult] res = vector[ListResult]()
        self.thisptr.ListMaxRange(min_c, max_c, beg_pos, end_pos, num, res)
        r = self._ListRange(res)
        return r
    cdef _ListRange(self, vector[ListResult]& res):
        r = []
        cdef vector[ListResult].iterator it = res.begin()
        while it != res.end():
            r.append((dereference(it).c, dereference(it).freq))
            preincrement(it)
        return r
    def Freq(self, uint64_t c):
        return self.thisptr.Freq(c)
    def FreqSum(self, uint64_t min_c, uint64_t max_c):
        return self.thisptr.FreqSum(min_c, max_c)
    def alphabet_num(self):
        return self.thisptr.alphabet_num()
    def length(self):
        return self.thisptr.length()
    def dump(self, filename):
        if isinstance(filename, unicode):
            filename = filename.encode('utf-8')
        dump(self.thisptr, <char *>filename)
    def load(self, filename):
        if isinstance(filename, unicode):
            filename = filename.encode('utf-8')
        load(self.thisptr, <char *>filename)
    def dumps(self):
        cdef string str
        dumps(self.thisptr, str)
        cdef bytes data
        data = str.c_str()[:str.size()] # libcpp.string.data is not implemented
        return data
    def loads(self, bytes data):
        cdef string str = string(data, len(data))
        loads(self.thisptr, str)
        

cdef class BitArray:
    cdef cpp_watarray.BitArray *thisptr
    def __cinit__(self, uint64_t size = 0):
        self.thisptr = new cpp_watarray.BitArray(size)
    def __dealloc__(self):
        del self.thisptr
    def Init(self, uint64_t size):
        self.thisptr.Init(size)
    def Clear(self):
        self.thisptr.Clear()
    def length(self):
        return self.thisptr.length()
    def one_num(self):
        return self.thisptr.one_num()
    def SetBit(self, uint64_t bit, uint64_t pos):
        self.thisptr.SetBit(bit, pos)
    def Build(self):
        self.thisptr.Build()
    def Rank(self, uint64_t bit, uint64_t pos):
        return self.thisptr.Rank(bit, pos)
    def Select(self, uint64_t bit, uint64_t rank):
        return self.thisptr.Select(bit, rank)
    def Lookup(self, uint64_t pos):
        return self.thisptr.Lookup(pos)
    def PopCount(self, uint64_t x):
        return self.thisptr.PopCount(x)
    def PopCountMask(self, uint64_t x, uint64_t offset):
        return self.thisptr.PopCountMask(x, offset)
    def SelectInBlock(self, uint64_t x, uint64_t rank):
        return self.thisptr.SelectInBlock(x, rank)
    def GetBitNum(self, uint64_t one_num, uint64_t num, uint64_t bit):
        return self.thisptr.GetBitNum(one_num, num, bit)
    def dump(self, filename):
        if isinstance(filename, unicode):
            filename = filename.encode('utf-8')
        dump(self.thisptr, <char *>filename)
    def load(self, filename):
        if isinstance(filename, unicode):
            filename = filename.encode('utf-8')
        load(self.thisptr, <char *>filename)
    def dumps(self):
        cdef string str
        dumps(self.thisptr, str)
        cdef bytes data
        data = str.c_str()[:str.size()] # libcpp.string.data is not implemented
        return data
    def loads(self, bytes data):
        cdef string str = string(data, len(data))
        loads(self.thisptr, str)

__version__ = '0.6dev'
