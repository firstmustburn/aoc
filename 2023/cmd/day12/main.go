package main

import (
	h "aoc2023/internal/helpers"
	"fmt"
	"log/slog"
	"os"
	"slices"
	"strings"
)

func main() {

	var programLevel = new(slog.LevelVar) // Info by default
	handler := &slog.HandlerOptions{
		Level: programLevel,
		ReplaceAttr: func(groups []string, a slog.Attr) slog.Attr {
			// Remove time from the output for predictable test output.
			if a.Key == slog.TimeKey {
				return slog.Attr{}
			}
			// Remove the level output
			if a.Key == slog.LevelKey {
				return slog.Attr{}
			}

			return a
		},
	}
	logger := slog.New(slog.NewTextHandler(os.Stdout, handler))
	slog.SetDefault(logger)
	// programLevel.Set(slog.LevelInfo)
	programLevel.Set(slog.LevelWarn)

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
	foundCount := 0
	//main algo: find the first unknown and try all the values
	unkInd := strings.Index(values, string(SPRING_UNKNOWN))
	for _, tryValue := range TRY_VALUES {
		newValues := values[:unkInd] + string(tryValue) + values[unkInd+1:]
		//compute segments for our new value
		newSegments, lastChar := FindSegments(newValues)
		slog.Info("Testing",
			"newValues", newValues,
			"targetSegments", targetSegments,
			"newSegments", newSegments)

		//halting condition for recursion - all unknowns converted to values
		if lastChar == 0 {
			if slices.Equal(newSegments, targetSegments) {
				slog.Warn("Found matching config", "value", newValues, "segments", newSegments)
				foundCount += 1
			} else {
				slog.Info("NOT a matching config")
			}
			continue
		}

		//check our new value to see if anything lets us prune this branch of the search

		//prune if too many segments
		if len(newSegments) > len(targetSegments) {
			slog.Info("Pruning search too many seg")
			continue
		}

		//look at pruning cases by comparing segments
		for index := 0; index < len(newSegments); index++ {
			//special case for the last segment in the new value
			//do something different based on the last character
			if index == len(newSegments)-1 {
				if lastChar == SPRING_GOOD {
					//if it was good, the values must be equal or we prune
					//because we can't make the existing groups bigger
					if newSegments[index] != targetSegments[index] {
						slog.Info("Pruning search last seg neq with good")
						continue
					}
				} else if lastChar == SPRING_BAD {
					//if it was bad, we only prune if the value is greater than the target value
					// because equal would be okan and less than might make a bigger group with
					// more unknowns
					if newSegments[index] > targetSegments[index] {
						slog.Info("Pruning search last seg greater with bad")
						continue
					}
				} else if lastChar == SPRING_UNKNOWN {
					//this happens if the first character is unknown, we just keep going
				} else {
					panic("unreachable")
				}
			} else {
				//for any segment other than the last, the segments from our partial search must be equal or we prune
				if newSegments[index] != targetSegments[index] {
					slog.Info("Pruning search unequal seg", "segment", index)
					continue
				}
			}
		}
		//if we get here, the newValue is not pruned or halted, so keep going with recursion
		slog.Info("NOT pruning", "newValues", newValues)
		newFindCount := FindValidConfigs(newValues, targetSegments)
		foundCount += newFindCount
	}
	if foundCount > 0 {
		slog.Info("Matching configs found so far", "found", foundCount, "values", values)
	}
	return foundCount
}

func (d *Day12) FindAll(findFunc func(string, []int) int) {
	// fmt.Println(d.records)
	totalFindCount := 0
	for _, r := range d.records {
		// fmt.Println("Searching", r)
		findCount := findFunc(r.Values, r.Segments)
		totalFindCount += findCount
		fmt.Printf("Found %d configs for %v\n", findCount, r)
		fmt.Println("------------------------------------------------------------------")
	}
	fmt.Println("Total found:", totalFindCount)

}

func (d *Day12) Part1() {
	fmt.Println("Part 1")
	d.FindAll(FindValidConfigs)
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

	d.FindAll(FindValidConfigs)
}
