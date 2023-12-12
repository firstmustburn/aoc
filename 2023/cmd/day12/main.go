package main

import (
	h "aoc2023/internal/helpers"
	"fmt"
	"os"
	"slices"
	"strings"
)

func main() {

	d := &Day12{}

	err := h.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

type Day12 struct {
	lines   []string
	records []Record
}

func (d *Day12) Setup(filename string) {
	fmt.Println("Setup")
	d.lines = h.ReadFileToLines(filename)

	for _, line := range d.lines {
		tokens := strings.Split(line, " ")
		segments := h.ParseIntList(tokens[1], ",")
		d.records = append(d.records, Record{
			Values:   tokens[0],
			Segments: segments,
		})
	}

}

const SPRING_GOOD byte = '.'
const SPRING_BAD byte = '#'
const SPRING_UNKNOWN byte = '?'

var TRY_VALUES = []byte{SPRING_GOOD, SPRING_BAD}

type Record struct {
	Values   string
	Segments []int
}

func HasUnknowns(values string) bool {
	return strings.Contains(values, string(SPRING_UNKNOWN))
}

// FindSegments returns segments it found up to the first ? and the last character before the ?,
// or 0 if it reached the end
func FindSegments(values string) ([]int, byte) {
	segments := []int{}
	lastChar := byte(0)

	currentSegmentSize := 0
	for index, r := range values {
		c := byte(r)
		if c == SPRING_GOOD {
			if currentSegmentSize > 0 {
				segments = append(segments, currentSegmentSize)
				currentSegmentSize = 0
			}
		} else if c == SPRING_BAD {
			currentSegmentSize += 1
		} else if c == SPRING_UNKNOWN {
			if index == 0 {
				lastChar = SPRING_UNKNOWN
			} else {
				lastChar = byte(values[index-1])
			}
			break
		}
	}
	if currentSegmentSize > 0 {
		segments = append(segments, currentSegmentSize)
	}
	return segments, lastChar
}

func FindValidConfigs(values string, targetSegments []int) int {
	// halting condition for recursion
	if !HasUnknowns(values) {
		// fmt.Println("    Complete value", values)
		segments, lastChar := FindSegments(values)
		h.Assert(lastChar == 0, "should be complete")
		if slices.Equal(segments, targetSegments) {
			// fmt.Printf("   Valid config: %s, %v\n", values, targetSegments)
			return 1
		} else {
			return 0
		}
	}

	foundCount := 0
	//main algo: find the first unknown and try all the values
	unkInd := strings.Index(values, string(SPRING_UNKNOWN))
	for _, tryValue := range TRY_VALUES {
		newValues := values[:unkInd] + string(tryValue) + values[unkInd+1:]
		//check our new value to see if it makes an invalid config
		newSegments, lastChar := FindSegments(values)
		//prune if too many segments
		if len(newSegments) > len(targetSegments) {
			// fmt.Printf("   Pruning search at %s %v\n", newValues, newSegments)
			return 0
		}
		//if the last character was a bad spring, that last segment
		for index := 0; index < len(newSegments); index++ {
			//special case for the last value
			if index == len(newSegments)-1 {
				if lastChar == SPRING_GOOD {
					//if it was good, the values must be equal or we prune
					//because we can't make the existing groups bigger
					if newSegments[index] != targetSegments[index] {
						// fmt.Printf("   Pruning search at %s %v\n", newValues, newSegments)
						return 0
					}
				} else if lastChar == SPRING_BAD {
					//if it was bad, we only prune if the value is greater than the target value
					// because equal would be okan and less than might make a bigger group with
					// more unknowns
					if newSegments[index] > targetSegments[index] {
						// fmt.Printf("   Pruning search at %s %v\n", newValues, newSegments)
						return 0
					}
				} else if lastChar == SPRING_UNKNOWN {
					//this happens if the first character is unknown, we just keep going
				} else {
					panic("unreachable")
				}
			} else {
				//for any other value, the segments from our partial search must be equal or we prune
				if newSegments[index] != targetSegments[index] {
					// fmt.Printf("   Pruning search at %s %v\n", newValues, newSegments)
					return 0
				}
			}
		}
		//target values
		// fmt.Println("Not pruned", newValues)
		//if we get here, the newValue is not pruned, so keep going
		newFindCount := FindValidConfigs(newValues, targetSegments)
		foundCount += newFindCount
	}
	return foundCount
}

func (d *Day12) FindAll() {
	// fmt.Println(d.records)
	totalFindCount := 0
	for _, r := range d.records {
		fmt.Println("Searching", r)
		findCount := FindValidConfigs(r.Values, r.Segments)
		totalFindCount += findCount
		fmt.Printf("Found %d configs for %v\n", findCount, r)
	}
	fmt.Println("------------------")
	fmt.Println("Total found:", totalFindCount)

}

func (d *Day12) Part1() {
	fmt.Println("Part 1")
	d.FindAll()
}

func (r Record) Expand(multiplier int) Record {

	segments := make([]int, 0, len(r.Segments)*multiplier)

	//initial value
	values := r.Values
	segments = append(segments, r.Segments...)

	//add multiplier-1 more
	for i := 1; i < multiplier; i++ {
		values += "?" + r.Values
		segments = append(segments, r.Segments...)
	}
	return Record{
		Values:   values,
		Segments: segments,
	}
}

func (d *Day12) Part2() {
	fmt.Println("Part 2")
	records := make([]Record, 0, len(d.records))
	for _, r := range d.records {
		records = append(records, r.Expand(5))
	}
	d.records = records
	// fmt.Println(d.records)

	d.FindAll()
}
