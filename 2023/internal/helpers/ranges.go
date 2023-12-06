package helpers

import (
	"fmt"
	"slices"
)

type RangeOrdinalType int64

// half open range from start to end-1
// carries a list of possible metadata values
// see the Intersect method for how metadata is combined
type Range[V any] struct {
	Start    RangeOrdinalType
	End      RangeOrdinalType
	Metadata []V
}

func CreateRange[V any](startVal RangeOrdinalType, endVal RangeOrdinalType, metadata []V) Range[V] {
	if endVal < startVal {
		panic(fmt.Errorf("invalid range parameters [%d,%d)]", startVal, endVal))
	}
	return Range[V]{
		Start:    startVal,
		End:      endVal,
		Metadata: metadata,
	}
}

func (r Range[V]) ToString() string {
	return fmt.Sprintf("%d -> %d: %v", r.Start, r.End, r.Metadata)
}

func (r Range[V]) Length() RangeOrdinalType {
	return r.End - r.Start
}

func (r Range[V]) Empty() bool {
	return r.End == r.Start
}

func checkEmpty[V any](r Range[V], funcName string, context string) {
	if r.Empty() {
		panic(fmt.Errorf("invalid call to %s with %s that is empty", funcName, context))
	}
}

// Contains returns true if the other range is completely within the range (including if they are equal)
func (r Range[V]) Contains(other Range[V]) bool {
	checkEmpty(r, "Contains", "r")
	checkEmpty(other, "Contains", "other")
	return other.Start >= r.Start && other.End <= r.End
}

func (r Range[V]) IsDisjoint(other Range[V]) bool {
	checkEmpty(r, "Disjoint", "r")
	checkEmpty(other, "Disjoint", "other")
	return other.Start >= r.End || other.End <= r.Start
}

// IsLeftIntersect returns true if other overlaps the start of the range but ends inside the range
// 1 5:  AAAA   <- original
// 0 1: X       <- A and X are disjoint
// 0 2: BB      <- these Bs should all be A.IsleftIntersect(B) -> True
// 0 3: BBB
// 0 4: BBBB
// 0 5: XXXXX   <- X contains A
func (r Range[V]) IsLeftIntersect(other Range[V]) bool {
	checkEmpty(r, "IsLeftIntersect", "r")
	checkEmpty(other, "IsLeftIntersect", "other")
	return other.Start < r.Start &&
		(other.End > r.Start && other.End < r.End)
}

// IsRightIntersect returns true if other starts in the the range but ends outside it
// 1 5:  AAAA   <- original
// 1 6:  XXXXX  <- X contains A
// 2 6:   BBBB  <- these Bs should all be A.IsRightIntersect(B) -> True
// 3 6:    BBB
// 4 6:     BB
// 5 6:      X  <- X is disjoint from A
func (r Range[V]) IsRightIntersect(other Range[V]) bool {
	checkEmpty(r, "IsRightIntersect", "r")
	checkEmpty(other, "IsRightIntersect", "other")
	return (other.Start > r.Start && other.Start < r.End) &&
		(other.End > r.End)
}

// IsContinguous returns true if other starts where r ends
func (r Range[V]) IsContiguous(other Range[V]) bool {
	checkEmpty(r, "IsContiguous", "r")
	checkEmpty(other, "IsContiguous", "other")
	return other.Start == r.End
}

// Intersect returns a set of ranges that represent the intersection of the two ranges
// The output should be disjoint ranges whose start values are in increasing order
// If any of the resulting ranges would be empty, they are omitted form the result
func (r Range[V]) Intersect(other Range[V]) []Range[V] {
	checkEmpty(r, "Intersect", "r")
	checkEmpty(other, "Intersect", "other")

	//helper to create the combined metadata
	makeCombinedMetadata := func() []V {
		// we always maintain the order of r before other regardless of the relative positions of
		// r and other in numeric terms
		combinedMetadata := make([]V, 0, len(r.Metadata)+len(other.Metadata))
		combinedMetadata = append(combinedMetadata, r.Metadata...)
		combinedMetadata = append(combinedMetadata, other.Metadata...)
		return combinedMetadata
	}

	//return up to three ranges for the left part of outer, the middle overlap, the right part of outer
	//if any of the resulting ranges would be empty, they are omitted form the result
	containIntersect := func(outer Range[V], inner Range[V]) []Range[V] {
		return RemoveEmptyRanges[V]([]Range[V]{
			CreateRange(outer.Start, inner.Start, outer.Metadata),
			CreateRange(inner.Start, inner.End, makeCombinedMetadata()),
			CreateRange(inner.End, outer.End, outer.Metadata),
		})
	}

	//return three ranges repesenting the non-overlapped part of left, the overlapped part of
	//left and right, and the non-overlapped part of right.
	//if any of the resulting ranges would be empty, they are omitted form the result
	leftIntersect := func(left Range[V], right Range[V]) []Range[V] {
		return RemoveEmptyRanges[V]([]Range[V]{
			CreateRange(left.Start, right.Start, left.Metadata),
			CreateRange(right.Start, left.End, makeCombinedMetadata()),
			CreateRange(left.End, right.End, right.Metadata),
		})
	}

	if r.IsDisjoint(other) {
		//disjoint, so just use the original ranges, but sort them
		if r.Start < other.Start {
			return []Range[V]{r, other}
		} else {
			return []Range[V]{other, r}
		}
	} else if r.Contains(other) {
		return containIntersect(r, other)
	} else if other.Contains(r) {
		return containIntersect(other, r)
	} else if r.IsLeftIntersect(other) {
		return leftIntersect(other, r)
	} else if other.IsLeftIntersect(r) {
		return leftIntersect(r, other)
	} else {
		panic(fmt.Errorf("unhandled condition for r=%#v and other=%#v", r, other))
	}
}

func RemoveEmptyRanges[V any](ranges []Range[V]) []Range[V] {
	out := make([]Range[V], 0)
	for _, rangeVal := range ranges {
		if rangeVal.Length() > 0 {
			out = append(out, rangeVal)
		}
	}
	return out
}

func DeduplicateRangeList[V comparable](input []Range[V]) []Range[V] {
	output := make([]Range[V], 0, len(input))
	for _, inputRange := range input {
		searchFun := func(v Range[V]) bool {
			if v.Start != inputRange.Start || v.End != inputRange.End {
				return false
			}
			//if we get here the start and end are equal, but panic if the metadata is not equal
			if !slices.Equal(v.Metadata, inputRange.Metadata) {
				panic(fmt.Errorf("equal start and end but unequal metetadata for %#v and %#v", v, inputRange))
			}
			return true
		}
		if slices.ContainsFunc(output, searchFun) {
			continue
		}
		output = append(output, inputRange)

	}
	return output
}
