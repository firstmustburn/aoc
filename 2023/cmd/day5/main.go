package main

import (
	h "aoc2023/internal/helpers"
	"fmt"
	"math"
	"os"
	"slices"
	"sort"
	"strings"
)

func main() {

	d := &Day5{}

	err := h.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

type Day5 struct {
	lines []string
	seeds []int64
	maps  []SparseMap
}

type SparseMapEntry struct {
	DestStart   int64
	SourceStart int64
	Length      int64
}

type SparseMap struct {
	Name    string
	Entries []SparseMapEntry
}

func (m SparseMap) Traverse(input int64) int64 {
	for _, entry := range m.Entries {
		if input >= entry.SourceStart && input < entry.SourceStart+entry.Length {
			//the input is mapped by this entry
			offset := input - entry.SourceStart
			output := entry.DestStart + offset
			// fmt.Printf("   %d -> %d using %v\n", input, output, entry)
			return output
		}
	}
	//if we get here, no entry matched
	// fmt.Printf("   %d -> %d by default\n", input, input)
	return input
}

func (d *Day5) Parse() {
	//parse seeds
	{
		tokens := strings.Split(d.lines[0], ":")
		h.Assert(len(tokens) == 2, "tokens not len 2")

		d.seeds = h.ParseInt64List(tokens[1], " ")
	}

	//parse maps
	{

		isMapPending := false
		pendingMap := &SparseMap{}

		finishMap := func() {
			if isMapPending {
				d.maps = append(d.maps, *pendingMap)
				//reset state
				pendingMap = &SparseMap{}
				isMapPending = false
			}
		}

		for _, line := range d.lines[2:] {
			if !isMapPending {
				//start a new map
				isMapPending = true
				h.Assert(strings.HasSuffix(line, ":"), "name line does end in a colon")
				pendingMap.Name = strings.TrimRight(line, ":")
			} else {
				//alread a map pending
				if len(line) > 0 {
					//add an entry for this line
					values := h.ParseInt64List(line, " ")
					entry := SparseMapEntry{
						DestStart:   values[0],
						SourceStart: values[1],
						Length:      values[2],
					}
					pendingMap.Entries = append(pendingMap.Entries, entry)
				} else {
					//empty line
					finishMap()
				}
			}
		}
		//finished with all lines, close out the last map if there is one
		finishMap()
	}

}

func (d *Day5) Setup(filename string) {
	fmt.Println(os.Getwd())

	fmt.Println("Setup")
	d.lines = h.ReadFileToLines(filename)

	d.Parse()

	fmt.Println("seeds:", d.seeds)
	fmt.Println("Maps")
	fmt.Printf("%#v\n", d.maps)
}

func (d *Day5) SeedToLocation(seed int64) int64 {
	// fmt.Printf("Mapping location for seed %d\n", seed)
	currentValue := seed
	for _, sparseMap := range d.maps {
		currentValue = sparseMap.Traverse(currentValue)
	}
	// fmt.Printf("  final location is %d\n", currentValue)
	return currentValue
}

func (d *Day5) Part1() {
	fmt.Println("Part 1")

	locations := make([]int64, 0, len(d.seeds))
	for _, seed := range d.seeds {
		//traverse all the maps for this seed
		locations = append(locations, d.SeedToLocation(seed))
	}

	minLoc := slices.Min(locations)
	fmt.Println("Minimum location is ", minLoc)
}

func (d *Day5) Part2() {
	// d.Part2BruteForce()
	d.Part2Optimized()
}

func (d *Day5) Part2BruteForce() {

	fmt.Println("Part 2")

	var minLocation int64 = math.MaxInt64

	//count seeds
	var seedCount int64 = 0
	for index := 0; index < len(d.seeds); index += 2 {
		length := d.seeds[index+1]
		seedCount += length
	}
	fmt.Println("Processing # seeds: ", seedCount)

	//go through seeds two at a time as start and length
	var seedsComplete int64 = 0
	for index := 0; index < len(d.seeds); index += 2 {
		start := d.seeds[index]
		length := d.seeds[index+1]
		for seed := start; seed < start+length; seed++ {
			seedsComplete += 1
			minLocation = min(minLocation, d.SeedToLocation(seed))
			if seedsComplete%10000000 == 0 {
				fmt.Printf(
					"%f %% complete min loc is %d\n",
					100.0*float64(seedsComplete)/float64(seedCount),
					minLocation)
			}
		}
	}
	fmt.Println("Minimum location is ", minLocation)

}

//**************************************************************************************************
//**************************************************************************************************
//***  Optimized Part 2 code
//**************************************************************************************************
//**************************************************************************************************

type MRMD int64 //MapRangeMetadata type

func (m SparseMap) ToRanges() []h.Range[MRMD] {
	ranges := make([]h.Range[MRMD], 0, len(m.Entries))
	for _, entry := range m.Entries {
		rStart := h.RangeOrdinalType(entry.SourceStart)
		rEnd := h.RangeOrdinalType(entry.SourceStart + entry.Length)
		//metadata is the offset -- the amount you add to the source to get to the destination
		rMetadata := []MRMD{MRMD(entry.DestStart - entry.SourceStart)}
		rangeEntry := h.CreateRange[MRMD](rStart, rEnd, rMetadata)
		ranges = append(ranges, rangeEntry)
	}
	//sort the list
	sort.Slice(ranges, func(i, j int) bool { return ranges[i].Start < ranges[j].Start })

	return ranges
}

func RangesToString(ranges []h.Range[MRMD]) string {
	out := "["
	for _, r := range ranges {
		out += r.ToString() + "; "
	}
	out += "]"
	return out
}

// func IntersectRangeLists[V comparable](list1 []Range[V], list2 []Range[V]) []Range[V] {

// 	workingList := list1

// 	//intersect each element of r2 across the working list
// 	for _, r2 := range list2 {
// 		//the output list will be at least as big as the working list
// 		outputList := make([]Range[V], 0, len(workingList))
// 		foundIntersection := false
// 		for _, workingRange := range workingList {
// 			if workingRange.IsDisjoint(r2) {
// 				//no intersection, so just pass through to the output
// 				outputList = append(outputList, workingRange)
// 			} else {
// 				intersectedRanges := workingRange.Intersect(r2)
// 				outputList = append(outputList, intersectedRanges...)
// 				foundIntersection = true
// 			}
// 		}
// 		//if r2 doesn't intersect any of the ranges in the working list, we need to add it
// 		if !foundIntersection {
// 			outputList = append(outputList, r2)
// 		}
// 		workingList = DeduplicateRangeList(outputList)
// 		//sort the list
// 		sort.Slice(workingList, func(i, j int) bool { return workingList[i].Start < workingList[j].Start })

// 	}
// 	return workingList

// }

func MapRanges(rangesToMap []h.Range[MRMD], targets []h.Range[MRMD]) []h.Range[MRMD] {

	zeroMetadata := []MRMD{0}

	//accumulate the output (remapped) values here
	output := make([]h.Range[MRMD], 0)

	for _, rangeToMap := range rangesToMap {
		//for each item we need to map

		h.Assert(
			len(rangeToMap.Metadata) == 1 && rangeToMap.Metadata[0] != 0,
			"missing nonzero offset on rangeToMap")

		// this list accumulates targets that we don't match agains tthe current rangeToMap
		// so that we can use them in the next round
		nextTargets := make([]h.Range[MRMD], 0)

		// iterate throught the target list applying the range offsets to intersections and
		// passing everything else through
		for _, target := range targets {

			h.Assert(slices.Equal(target.Metadata, zeroMetadata), "expected zeroed metadata on targets")

			if rangeToMap.IsDisjoint(target) {
				//just pass the target through, it is not modified by this range mapping
				nextTargets = append(nextTargets, target)
			} else {
				intersectedRanges := target.Intersect(rangeToMap)

				fmt.Printf("(%s).Intersect(%s) created %s\n", target.ToString(), rangeToMap.ToString(), RangesToString(intersectedRanges))

				//there are three cases for the intersected ranges:
				// - it's just the rangeToMap value -- we can discard it
				// - it's an overlap between the rangeToMap value and the target value -- we remap it
				// - it's just the target values -- put it in nextTargets for next time
				for _, ir := range intersectedRanges {
					if slices.Equal(ir.Metadata, rangeToMap.Metadata) {
						//just the rangeToMap.Metadata so do nothing and discard it
					} else if slices.Equal(ir.Metadata, zeroMetadata) {
						//just the target metadata, so add it to nextTargets
						nextTargets = append(nextTargets, ir)
						fmt.Printf("  Saving non-overlapping target fragment %s \n", ir.ToString())
					} else {
						//it's an overlap between the target and the rangeToMap, so remap it and
						//save it in the output
						offset := h.RangeOrdinalType(h.SumSlice(ir.Metadata))
						newRange := h.Range[MRMD]{
							Start:    ir.Start + offset,
							End:      ir.End + offset,
							Metadata: []MRMD{0},
						}
						fmt.Printf("  Remapped %s to new range %s\n", ir.ToString(), newRange.ToString())
						output = append(output, newRange)
					}
				}
			}
		}
		//done processing the target list so replace it with our nextTargets list
		targets = nextTargets
	}
	//before we finish, we need to save any unmatched targets into our outputs
	output = append(output, targets...)

	//sort the list
	sort.Slice(output, func(i, j int) bool { return output[i].Start < output[j].Start })

	return output

}

func DumpRangeList(ranges []h.Range[MRMD], title string) {
	fmt.Println("**********************************")
	fmt.Println(title)
	for _, r := range ranges {
		fmt.Println(r.ToString())
	}
	fmt.Println("**********************************")
}

func (d *Day5) Part2Optimized() {

	fmt.Println("Part 2")

	seedRanges := make([]h.Range[MRMD], 0, len(d.seeds)/2)

	//make initial ranges
	for index := 0; index < len(d.seeds); index += 2 {
		start := d.seeds[index]
		length := d.seeds[index+1]
		seedRanges = append(seedRanges, h.CreateRange[MRMD](
			h.RangeOrdinalType(start),
			h.RangeOrdinalType(start+length),
			[]MRMD{0})) //0 offset metdata for the initial ranges
	}

	workingRanges := seedRanges
	DumpRangeList(workingRanges, "initial ranges")

	for _, mapVal := range d.maps {

		mapValRanges := mapVal.ToRanges()
		DumpRangeList(mapValRanges, "map ranges")

		workingRanges = MapRanges(mapValRanges, workingRanges)
		DumpRangeList(workingRanges, "after mapping")
	}

	//now find the minimum from the ranges
	minVal := h.RangeOrdinalType(math.MaxInt64)
	for _, r := range workingRanges {
		minVal = min(r.Start, minVal)
	}
	fmt.Println("Minimum location is", minVal)

}
