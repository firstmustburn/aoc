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

	var err error

	// f, err := os.Create("Day12.prof")
	// if err != nil {
	// 	panic(err)
	// }
	// pprof.StartCPUProfile(f)
	// defer pprof.StopCPUProfile()

	d := &Day12{}

	err = h.Dispatch(os.Args, d)
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

const SPRING_GOOD_C byte = '.'
const SPRING_BAD_C byte = '#'
const SPRING_UNKNOWN_C byte = '?'

const SPRING_GOOD = string(SPRING_GOOD_C)
const SPRING_BAD = string(SPRING_BAD_C)
const SPRING_UNKNOWN = string(SPRING_UNKNOWN_C)

var TRY_VALUES = []string{SPRING_GOOD, SPRING_BAD}

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
	segments := make([]int, 0, 10)
	lastChar := byte(0)

	currentSegmentSize := 0
	for index, r := range values {
		c := byte(r)
		if c == SPRING_GOOD_C {
			if currentSegmentSize > 0 {
				segments = append(segments, currentSegmentSize)
				currentSegmentSize = 0
			}
		} else if c == SPRING_BAD_C {
			currentSegmentSize += 1
		} else if c == SPRING_UNKNOWN_C {
			if index == 0 {
				lastChar = SPRING_UNKNOWN_C
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

func FindValidConfigsTOOSLOW(values string, targetSegments []int) int {
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
				if lastChar == SPRING_GOOD_C {
					//if it was good, the values must be equal or we prune
					//because we can't make the existing groups bigger
					if newSegments[index] != targetSegments[index] {
						slog.Info("Pruning search last seg neq with good")
						continue
					}
				} else if lastChar == SPRING_BAD_C {
					//if it was bad, we only prune if the value is greater than the target value
					// because equal would be okan and less than might make a bigger group with
					// more unknowns
					if newSegments[index] > targetSegments[index] {
						slog.Info("Pruning search last seg greater with bad")
						continue
					}
				} else if lastChar == SPRING_UNKNOWN_C {
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
		newFindCount := FindValidConfigsTOOSLOW(newValues, targetSegments)
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
	d.FindAll(FindValidConfigs2)
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

func TryPeel(values string, segmentSize int) (bool, string) {
	if len(values) < segmentSize {
		//can't peel if not enough values
		return false, values
	}
	if strings.Contains(values[:segmentSize], SPRING_GOOD) {
		//can't peel because one of the starting segmentSize values is good
		return false, values
	}
	if len(values) > segmentSize {
		//if there is a trailing value, it has to be good value or an unknown
		if values[segmentSize] == SPRING_GOOD_C || values[segmentSize] == SPRING_UNKNOWN_C {
			return true, values[segmentSize+1:]
		} //else we can't peel
		return false, values
	} else {
		//no trailing value to check, so we can peel the remaining values
		return true, ""
	}
}

func TrimGoodAndUnknown(values string) (string, bool) {
	isChanged := false

	searcher := func(r rune) bool {
		if byte(r) == SPRING_GOOD_C || byte(r) == SPRING_UNKNOWN_C {
			isChanged = true
			return true
		}
		return false
	}

	trimmed := strings.TrimLeftFunc(values, searcher)
	return trimmed, isChanged
}

func HasEnoughValues(values string, targetGroups []int) bool {
	h.Assert(len(targetGroups) > 0, "must have target groups")
	//check how many values we need
	minLength := h.SumSlice[int](targetGroups) + (len(targetGroups) - 1)
	return len(values) >= minLength
}

var configCache = make(map[string]int, 10000)

func CacheKey(values string, targetGroups []int) string {
	return fmt.Sprintf("%s-%v", values, targetGroups)
}

func FindValidConfigs2(values string, targetGroups []int) int {
	cacheKey := CacheKey(values, targetGroups)
	{
		cachedCount, ok := configCache[cacheKey]
		if ok {
			return cachedCount
		}
	}

	foundCount := 0

	//we can skip any leading good springs
	values = strings.TrimLeft(values, SPRING_GOOD)

	if !HasEnoughValues(values, targetGroups) {
		configCache[cacheKey] = foundCount
		return foundCount
	}

	{
		didPeel, remainingValues := TryPeel(values, targetGroups[0])
		if didPeel {
			//we can take the first targetSegments[0] values as a group match
			remainingGroups := targetGroups[1:]

			//halting condition
			if len(remainingGroups) == 0 {
				//no more segments, so see if there are any other bad springs
				//any mix of good and unknown springs represents one solution, otherwise there are none
				if !strings.Contains(remainingValues, SPRING_BAD) {
					foundCount += 1
				} //else no solution found
			} else {
				//more segments, so recurse
				subFoundCount := FindValidConfigs2(remainingValues, remainingGroups)
				foundCount += subFoundCount
			}
		}
	}

	//regardless of whether we peeled, if there is a leading ?, remove it and recurse
	if values[0] == SPRING_UNKNOWN_C {
		//we use the original targetGroups because on this path we have not taken any groups
		subFoundCount := FindValidConfigs2(values[1:], targetGroups)
		foundCount += subFoundCount
	}

	//save the result
	configCache[cacheKey] = foundCount
	return foundCount
}

func (d *Day12) Part2() {
	fmt.Println("Part 2")
	records := make([]Record, 0, len(d.records))
	for _, r := range d.records {
		records = append(records, r.Expand(5))
	}
	d.records = records
	// fmt.Println(d.records)

	d.FindAll(FindValidConfigs2)
}
