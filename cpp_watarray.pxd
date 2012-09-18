from libc.stdint cimport uint64_t
from libcpp.vector cimport vector
from libcpp.string cimport string

cdef extern from "<ostream>" namespace "std":
    cdef cppclass ostream:
        pass

cdef extern from "<istream>" namespace "std":
    cdef cppclass istream:
        pass

cdef extern from "<wat_array/wat_array.hpp>" namespace "wat_array":
    cdef enum:
        NOTFOUND
    ctypedef struct ListResult:
        uint64_t c
        uint64_t freq
    cdef cppclass WatArray:
        WatArray() except +
        void Init(vector[uint64_t]& array) except +
        void Clear() except +
        uint64_t Lookup(uint64_t pos)
        uint64_t Rank(uint64_t c, uint64_t pos)
        uint64_t Select(uint64_t c, uint64_t rank)
        uint64_t RankLessThan(uint64_t c, uint64_t pos)
        uint64_t RankMoreThan(uint64_t c, uint64_t pos)
        void RankAll(uint64_t c, uint64_t pos,
                     uint64_t& rank, uint64_t& rank_less_than, uint64_t& rank_more_than)
        uint64_t FreqRange(uint64_t min_c, uint64_t max_c, uint64_t beg_pos, uint64_t end_pos)
        void MaxRange(uint64_t beg_pos, uint64_t end_pos, uint64_t& pos, uint64_t& val)
        void MinRange(uint64_t beg_pos, uint64_t end_pos, uint64_t& pos, uint64_t& val)
        void QuantileRange(uint64_t beg_pos, uint64_t end_pos, uint64_t k, uint64_t& pos, uint64_t& val)
        void ListModeRange(uint64_t min_c, uint64_t max_c, uint64_t beg_pos, uint64_t end_pos, uint64_t num,
                           vector[ListResult]& res)
        void ListMinRange(uint64_t min_c, uint64_t max_c, uint64_t beg_pos, uint64_t end_pos, uint64_t num,
                          vector[ListResult]& res)
        void ListMaxRange(uint64_t min_c, uint64_t max_c, uint64_t beg_pos, uint64_t end_pos, uint64_t num,
                          vector[ListResult]& res)
        uint64_t Freq(uint64_t c)
        uint64_t FreqSum(uint64_t min_c, uint64_t max_c)
        uint64_t alphabet_num()
        uint64_t length()
        void Save(ostream&)
        void Load(istream&)
    cdef cppclass BitArray:
        BitArray() except +
        BitArray(uint64_t size) except +
        void Init(uint64_t size) except +
        void Clear() except +
        uint64_t length()
        uint64_t one_num()
        void SetBit(uint64_t bit, uint64_t pos)
        void Build()
        uint64_t Rank(uint64_t bit, uint64_t pos)
        uint64_t Select(uint64_t bit, uint64_t rank)
        uint64_t Lookup(uint64_t pos)
        uint64_t PopCount(uint64_t x)
        uint64_t PopCountMask(uint64_t x, uint64_t offset)
        uint64_t SelectInBlock(uint64_t x, uint64_t rank)
        uint64_t GetBitNum(uint64_t one_num, uint64_t num, uint64_t bit)
        void Save(ostream&)
        void Load(istream&)

cdef extern from "io.hpp" namespace "cpp_watarray":
    void dump(WatArray *wa, char *filename) except +
    void dump(BitArray *ba, char *filename) except +
    void load(WatArray *wa, char *filename) except +
    void load(BitArray *ba, char *filename) except +
    void dumps(WatArray *wa, string& str) except +
    void dumps(BitArray *ba, string& str) except +
    void loads(WatArray *wa, string str) except +
    void loads(BitArray *ba, string str) except +
