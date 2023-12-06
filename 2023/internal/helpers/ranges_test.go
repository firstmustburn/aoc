package helpers

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestRangeBasic(t *testing.T) {

	// 100 r1  5 10      56789
	// 200 r2  0  5 01234
	// 300 r3  2  7   23456
	// 400 r4  6  7       6

	r1 := CreateRange[int64](5, 10, []int64{100})
	r2 := CreateRange[int64](0, 5, []int64{200})
	r3 := CreateRange[int64](2, 7, []int64{300})
	r4 := CreateRange[int64](6, 7, []int64{400})

	assert.Equal(t, RangeOrdinalType(5), r1.Start)
	assert.Equal(t, RangeOrdinalType(10), r1.End)
	assert.Equal(t, []int64{100}, r1.Metadata)
	assert.Equal(t, RangeOrdinalType(5), r1.Length())

	assert.Equal(t, RangeOrdinalType(0), r2.Start)
	assert.Equal(t, RangeOrdinalType(5), r2.End)
	assert.Equal(t, []int64{200}, r2.Metadata)
	assert.Equal(t, RangeOrdinalType(5), r2.Length())

	assert.Equal(t, RangeOrdinalType(2), r3.Start)
	assert.Equal(t, RangeOrdinalType(7), r3.End)
	assert.Equal(t, []int64{300}, r3.Metadata)
	assert.Equal(t, RangeOrdinalType(5), r3.Length())

	assert.Equal(t, RangeOrdinalType(6), r4.Start)
	assert.Equal(t, RangeOrdinalType(7), r4.End)
	assert.Equal(t, []int64{400}, r4.Metadata)
	assert.Equal(t, RangeOrdinalType(1), r4.Length())

}

func TestRangeOperations(t *testing.T) {

	type RangeSpec struct {
		s      RangeOrdinalType
		e      RangeOrdinalType
		con    bool
		disj   bool
		lefti  bool
		righti bool
		contig bool
	}
	original := CreateRange[int64](5, 8, []int64{100})
	testCases := []RangeSpec{
		//grow across orig
		{s: 0, e: 4, con: false, disj: true, lefti: false, righti: false, contig: false},
		{s: 0, e: 5, con: false, disj: true, lefti: false, righti: false, contig: false},
		{s: 0, e: 6, con: false, disj: false, lefti: true, righti: false, contig: false},
		{s: 0, e: 7, con: false, disj: false, lefti: true, righti: false, contig: false},
		{s: 0, e: 8, con: false, disj: false, lefti: false, righti: false, contig: false},
		{s: 0, e: 9, con: false, disj: false, lefti: false, righti: false, contig: false}, //contains
		//shrink across orig
		{s: 4, e: 9, con: false, disj: false, lefti: false, righti: false, contig: false},
		{s: 5, e: 9, con: false, disj: false, lefti: false, righti: false, contig: false},
		{s: 6, e: 9, con: false, disj: false, lefti: false, righti: true, contig: false},
		{s: 7, e: 9, con: false, disj: false, lefti: false, righti: true, contig: false},
		{s: 8, e: 9, con: false, disj: true, lefti: false, righti: false, contig: true},
		//larger window sweep
		{s: 0, e: 4, con: false, disj: true, lefti: false, righti: false, contig: false},
		{s: 1, e: 5, con: false, disj: true, lefti: false, righti: false, contig: false},
		{s: 2, e: 6, con: false, disj: false, lefti: true, righti: false, contig: false},
		{s: 3, e: 7, con: false, disj: false, lefti: true, righti: false, contig: false},
		{s: 4, e: 8, con: false, disj: false, lefti: false, righti: false, contig: false},
		{s: 5, e: 9, con: false, disj: false, lefti: false, righti: false, contig: false},
		{s: 6, e: 10, con: false, disj: false, lefti: false, righti: true, contig: false},
		{s: 7, e: 11, con: false, disj: false, lefti: false, righti: true, contig: false},
		{s: 8, e: 12, con: false, disj: true, lefti: false, righti: false, contig: true},
		{s: 9, e: 13, con: false, disj: true, lefti: false, righti: false, contig: false},
		//equal window sweep
		{s: 1, e: 4, con: false, disj: true, lefti: false, righti: false, contig: false},
		{s: 2, e: 5, con: false, disj: true, lefti: false, righti: false, contig: false},
		{s: 3, e: 6, con: false, disj: false, lefti: true, righti: false, contig: false},
		{s: 4, e: 7, con: false, disj: false, lefti: true, righti: false, contig: false},
		{s: 5, e: 8, con: true, disj: false, lefti: false, righti: false, contig: false},
		{s: 6, e: 9, con: false, disj: false, lefti: false, righti: true, contig: false},
		{s: 7, e: 10, con: false, disj: false, lefti: false, righti: true, contig: false},
		{s: 8, e: 11, con: false, disj: true, lefti: false, righti: false, contig: true},
		{s: 9, e: 12, con: false, disj: true, lefti: false, righti: false, contig: false},
		//smaller window sweep
		{s: 2, e: 4, con: false, disj: true, lefti: false, righti: false, contig: false},
		{s: 3, e: 5, con: false, disj: true, lefti: false, righti: false, contig: false},
		{s: 4, e: 6, con: false, disj: false, lefti: true, righti: false, contig: false},
		{s: 5, e: 7, con: true, disj: false, lefti: false, righti: false, contig: false},
		{s: 6, e: 8, con: true, disj: false, lefti: false, righti: false, contig: false},
		{s: 7, e: 9, con: false, disj: false, lefti: false, righti: true, contig: false},
		{s: 8, e: 10, con: false, disj: true, lefti: false, righti: false, contig: true},
		{s: 9, e: 11, con: false, disj: true, lefti: false, righti: false, contig: false},
	}

	for index, testCase := range testCases {
		other := CreateRange[int64](testCase.s, testCase.e, []int64{200})
		assert.Equal(t,
			testCase.con, original.Contains(other),
			"Contains for test index %d, other=%#v", index, other)
		assert.Equal(t,
			testCase.disj, original.IsDisjoint(other),
			"IsDisjoint for test index %d, other=%#v", index, other)
		assert.Equal(t,
			testCase.lefti, original.IsLeftIntersect(other),
			"IsLeftIntersect for test index %d, other=%#v", index, other)
		assert.Equal(t,
			testCase.righti, original.IsRightIntersect(other),
			"IsRightIntersect for test index %d, other=%#v", index, other)
		assert.Equal(t,
			testCase.contig, original.IsContiguous(other),
			"IsContiguous for test index %d, other=%#v", index, other)
	}
}

func TestRangeIntersect(t *testing.T) {

	type RangeSpec struct {
		s              RangeOrdinalType
		e              RangeOrdinalType
		expectedRanges []Range[int64]
	}
	original := CreateRange[int64](5, 8, []int64{100})
	testCases := []RangeSpec{
		//grow across orig
		{0, 4, []Range[int64]{{0, 4, []int64{200}}, {5, 8, []int64{100}}}},
		{0, 5, []Range[int64]{{0, 5, []int64{200}}, {5, 8, []int64{100}}}},
		{0, 6, []Range[int64]{{0, 5, []int64{200}}, {5, 6, []int64{100, 200}}, {6, 8, []int64{100}}}},
		{0, 7, []Range[int64]{{0, 5, []int64{200}}, {5, 7, []int64{100, 200}}, {7, 8, []int64{100}}}},
		{0, 8, []Range[int64]{{0, 5, []int64{200}}, {5, 8, []int64{100, 200}}}},
		{0, 9, []Range[int64]{{0, 5, []int64{200}}, {5, 8, []int64{100, 200}}, {8, 9, []int64{200}}}},
		// //shrink across orig
		{4, 9, []Range[int64]{{4, 5, []int64{200}}, {5, 8, []int64{100, 200}}, {8, 9, []int64{200}}}},
		{5, 9, []Range[int64]{{5, 8, []int64{100, 200}}, {8, 9, []int64{200}}}},
		{6, 9, []Range[int64]{{5, 6, []int64{100}}, {6, 8, []int64{100, 200}}, {8, 9, []int64{200}}}},
		{7, 9, []Range[int64]{{5, 7, []int64{100}}, {7, 8, []int64{100, 200}}, {8, 9, []int64{200}}}},
		{8, 9, []Range[int64]{{5, 8, []int64{100}}, {8, 9, []int64{200}}}},
		{8, 9, []Range[int64]{{5, 8, []int64{100}}, {8, 9, []int64{200}}}},
		// //larger window sweep
		{0, 4, []Range[int64]{{0, 4, []int64{200}}, {5, 8, []int64{100}}}},
		{1, 5, []Range[int64]{{1, 5, []int64{200}}, {5, 8, []int64{100}}}},
		{2, 6, []Range[int64]{{2, 5, []int64{200}}, {5, 6, []int64{100, 200}}, {6, 8, []int64{100}}}},
		{3, 7, []Range[int64]{{3, 5, []int64{200}}, {5, 7, []int64{100, 200}}, {7, 8, []int64{100}}}},
		{4, 8, []Range[int64]{{4, 5, []int64{200}}, {5, 8, []int64{100, 200}}}},
		{5, 9, []Range[int64]{{5, 8, []int64{100, 200}}, {8, 9, []int64{200}}}},
		{6, 10, []Range[int64]{{5, 6, []int64{100}}, {6, 8, []int64{100, 200}}, {8, 10, []int64{200}}}},
		{7, 11, []Range[int64]{{5, 7, []int64{100}}, {7, 8, []int64{100, 200}}, {8, 11, []int64{200}}}},
		{8, 12, []Range[int64]{{5, 8, []int64{100}}, {8, 12, []int64{200}}}},
		{9, 13, []Range[int64]{{5, 8, []int64{100}}, {9, 13, []int64{200}}}},
		// //equal window sweep
		{1, 4, []Range[int64]{{1, 4, []int64{200}}, {5, 8, []int64{100}}}},
		{2, 5, []Range[int64]{{2, 5, []int64{200}}, {5, 8, []int64{100}}}},
		{3, 6, []Range[int64]{{3, 5, []int64{200}}, {5, 6, []int64{100, 200}}, {6, 8, []int64{100}}}},
		{4, 7, []Range[int64]{{4, 5, []int64{200}}, {5, 7, []int64{100, 200}}, {7, 8, []int64{100}}}},
		{5, 8, []Range[int64]{{5, 8, []int64{100, 200}}}},
		{6, 9, []Range[int64]{{5, 6, []int64{100}}, {6, 8, []int64{100, 200}}, {8, 9, []int64{200}}}},
		{7, 10, []Range[int64]{{5, 7, []int64{100}}, {7, 8, []int64{100, 200}}, {8, 10, []int64{200}}}},
		{8, 11, []Range[int64]{{5, 8, []int64{100}}, {8, 11, []int64{200}}}},
		{9, 12, []Range[int64]{{5, 8, []int64{100}}, {9, 12, []int64{200}}}},
		// //smaller window sweep
		{2, 4, []Range[int64]{{2, 4, []int64{200}}, {5, 8, []int64{100}}}},
		{3, 5, []Range[int64]{{3, 5, []int64{200}}, {5, 8, []int64{100}}}},
		{4, 6, []Range[int64]{{4, 5, []int64{200}}, {5, 6, []int64{100, 200}}, {6, 8, []int64{100}}}},
		{5, 7, []Range[int64]{{5, 7, []int64{100, 200}}, {7, 8, []int64{100}}}},
		{6, 8, []Range[int64]{{5, 6, []int64{100}}, {6, 8, []int64{100, 200}}}},
		{7, 9, []Range[int64]{{5, 7, []int64{100}}, {7, 8, []int64{100, 200}}, {8, 9, []int64{200}}}},
		{8, 10, []Range[int64]{{5, 8, []int64{100}}, {8, 10, []int64{200}}}},
		{9, 11, []Range[int64]{{5, 8, []int64{100}}, {9, 11, []int64{200}}}},
	}

	for index, testCase := range testCases {
		fmt.Println("Running test case ", index)
		other := CreateRange[int64](testCase.s, testCase.e, []int64{200})
		actualRanges := original.Intersect(other)
		//check for the expected result
		assert.Equal(t,
			testCase.expectedRanges, actualRanges,
			"Intersect for test index %d, other=%#v", index, other)
		//make sure the results are ordered
		for index := 0; index < len(actualRanges)-1; index++ {
			//make sure that the ranges are ordered
			assert.True(t, actualRanges[index].Start <= actualRanges[index+1].Start)
		}
		//make sure the results are disjoint
		for i1 := 0; i1 < len(actualRanges); i1++ {
			for i2 := i1 + 1; i2 < len(actualRanges); i2++ {
				assert.True(t, actualRanges[i1].IsDisjoint(actualRanges[i2]))
				assert.True(t, actualRanges[i2].IsDisjoint(actualRanges[i1]))
			}
		}
	}
}

func TestRangePanicOnEmpty(t *testing.T) {

	// 100 r1  5 10      56789
	// 200 r2  0  5 01234
	// 500 r3  6  6       |

	r1 := CreateRange[int64](5, 10, []int64{100})
	assert.Equal(t, RangeOrdinalType(5), r1.Start)
	assert.Equal(t, RangeOrdinalType(10), r1.End)
	assert.Equal(t, []int64{100}, r1.Metadata)
	assert.Equal(t, RangeOrdinalType(5), r1.Length())

	r2 := CreateRange[int64](0, 5, []int64{200})
	assert.Equal(t, RangeOrdinalType(0), r2.Start)
	assert.Equal(t, RangeOrdinalType(5), r2.End)
	assert.Equal(t, []int64{200}, r2.Metadata)
	assert.Equal(t, RangeOrdinalType(5), r2.Length())

	r3 := CreateRange[int64](6, 6, []int64{500})
	assert.Equal(t, RangeOrdinalType(6), r3.Start)
	assert.Equal(t, RangeOrdinalType(6), r3.End)
	assert.Equal(t, []int64{500}, r3.Metadata)
	assert.Equal(t, RangeOrdinalType(0), r3.Length())

	//value to call empth and length on empty ranges
	assert.False(t, r1.Empty())
	assert.False(t, r2.Empty())
	assert.True(t, r3.Empty())
	assert.Equal(t, RangeOrdinalType(5), r1.Length())
	assert.Equal(t, RangeOrdinalType(5), r2.Length())
	assert.Equal(t, RangeOrdinalType(0), r3.Length())

	//make sure everything else panics with empty ranges

	testCases := [][]Range[int64]{
		{r1, r3},
		{r3, r1},
		{r2, r3},
		{r3, r2},
	}

	for _, pair := range testCases {
		ra := pair[0]
		rb := pair[1]
		assert.Panics(t, func() { ra.Contains(rb) })
		assert.Panics(t, func() { ra.IsDisjoint(rb) })
		assert.Panics(t, func() { ra.IsLeftIntersect(rb) })
		assert.Panics(t, func() { ra.IsRightIntersect(rb) })
		assert.Panics(t, func() { ra.IsContiguous(rb) })
		assert.Panics(t, func() { ra.Intersect(rb) })
	}

}
