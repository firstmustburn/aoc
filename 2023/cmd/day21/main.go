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

	// f, err := os.Create("day21.prof")
	// if err != nil {
	// 	panic(err)
	// }
	// pprof.StartCPUProfile(f)
	// defer pprof.StopCPUProfile()

	d := &Day21{}

	err = h.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

type Day21 struct {
	lines     []string
	grid      *h.Grid[GridData]
	nullCoord h.Coord

	//state for part 2
	SearchStepCount   int //how many steps we should search to find patterns
	RegionCompareSize int //how many region tiles we track in pattern search
	TargetStepCount   int //how many steps we are trying to compute the reachable count for

	OddSteadyStateReachableCount  int
	EvenSteadyStateReachableCount int

	RegionHistory               []map[h.Coord]int //a map of the regionIds for all the regions for the Ith step
	RegionsFound                []string          //the string represntation of each region identified -- the index in this list is the region's ID
	RegionIndexToReachableCount map[int]int       //mapping from region IDs to the number of reachable tiles

}

const TILE_ROCK_C = '#'
const TILE_GARDEN_C = '.'
const TILE_START_C = 'S'
const TILE_ROCK = "#"
const TILE_GARDEN = "."
const TILE_START = "S"

// type ReachableState int

// const REACHABLE_UNKNOWN = 0
// const REACHABLE_EVEN = 1
// const REACHABLE_ODD = 2

type GridData struct {
	Value byte
}

func (d *Day21) DumpGridValue() {
	walker := func(r int, c int, v GridData) {
		if c == 0 {
			fmt.Println("")
		}
		fmt.Printf("%s", string(v.Value))
	}
	d.grid.WalkRCV(walker)
	fmt.Println("")
}

func (d *Day21) Setup(filename string) {
	fmt.Println("Setup")
	d.lines = h.ReadFileToLines(filename)

	rows := len(d.lines)
	cols := len(d.lines[0])
	d.grid = h.CreateGrid[GridData](rows, cols)

	//fill the grid
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			d.grid.SetRC(r, c, GridData{Value: d.lines[r][c]})
		}
	}

	//the nullCoord is outside the grid
	d.nullCoord = h.Coord{Row: rows * 2, Col: cols * 2}

}

func (d *Day21) GetAdjacentGarden(coord h.Coord) []h.Coord {
	adjCoords := []h.Coord{}
	for _, adj := range d.grid.AdjacentToCoord(coord, false) {
		val := d.grid.Get(adj)
		if val.Value == TILE_GARDEN_C || val.Value == TILE_START_C {
			adjCoords = append(adjCoords, adj)
		}
	}
	return adjCoords
}

func (d *Day21) FindStart() h.Coord {
	var startCoord h.Coord
	ret := d.grid.WalkVUntil(func(coord h.Coord, value GridData) bool {
		if value.Value == TILE_START_C {
			startCoord = coord
			return false
		}
		return true
	})
	h.Assert(!ret, "could not find start")
	return startCoord
}

func (d *Day21) Part1() {
	fmt.Println("Part 1")
	// d.DumpGridValue()

	startCoord := d.FindStart()

	fmt.Println("Start", startCoord)
	generation := make(map[h.Coord]struct{}, 1)
	generation[startCoord] = struct{}{}

	stepCount := 64

	for i := 0; i < stepCount; i++ {
		newGeneration := make(map[h.Coord]struct{}, len(generation)*3)
		for currentLoc := range generation {
			for _, adj := range d.GetAdjacentGarden(currentLoc) {
				_, ok := newGeneration[adj]
				if !ok {
					newGeneration[adj] = struct{}{}
				}
			}
		}
		generation = newGeneration
		fmt.Printf("After %d steps, there are %d possible locations\n", i+1, len(generation))
	}

}

func (d *Day21) GetAdjacentGardenTiled(coord h.Coord) []h.Coord {
	adjCoords := []h.Coord{}

	//use coord.Adjacent which doesn't filter out based on grid bounds
	for _, adj := range coord.Adjacent(false) {
		//getTiled gets the infinite grid value
		val := d.grid.GetTiled(adj)
		//only keep adjacent coords that are gardens
		if val.Value == TILE_GARDEN_C || val.Value == TILE_START_C {
			adjCoords = append(adjCoords, adj)
		}
	}
	return adjCoords
}

func (d *Day21) MakeRegionString(r int, c int, reachable *map[h.Coord]struct{}) string {
	var builder strings.Builder
	// builder.WriteString(fmt.Sprintf("% 2d,% 2d|i=% 4d|e=%d|  ", r, c, index, index%2))
	walker := func(c h.Coord) {
		_, ok := (*reachable)[c]
		if ok {
			builder.WriteString("O")
		} else {
			builder.WriteByte(d.grid.GetTiled(c).Value)
		}
	}
	region := d.grid.GetTileRegion(r, c)
	region.Walk(walker)
	return builder.String()
}

func (d *Day21) CountReachableInRegion(r int, c int, reachable *map[h.Coord]struct{}) int {
	reachableCount := 0
	walker := func(c h.Coord) {
		_, ok := (*reachable)[c]
		if ok {
			reachableCount += 1
		}
	}
	region := d.grid.GetTileRegion(r, c)
	region.Walk(walker)
	return reachableCount
}

// returns the ID of the region at r,c -- if the region has no ID, it is added to the
// region state and its ID is its index in the list
func (d *Day21) GetRegionId(r int, c int, reachable *map[h.Coord]struct{}) int {
	count := d.CountReachableInRegion(r, c, reachable)
	s := d.MakeRegionString(r, c, reachable)
	index := slices.Index(d.RegionsFound, s)
	if index == -1 {
		d.RegionsFound = append(d.RegionsFound, s)
		index = len(d.RegionsFound) - 1
		d.RegionIndexToReachableCount[index] = count
	}
	return index
}

func (d *Day21) DoRegionSearch() {
	startCoord := d.FindStart()
	fmt.Println("Start", startCoord)

	//this is the first generation
	generation := map[h.Coord]struct{}{
		startCoord: {},
	}

	//initialize search state
	d.RegionHistory = make([]map[h.Coord]int, 0, d.SearchStepCount)
	// d.RegionsFound = []string{}
	d.RegionIndexToReachableCount = map[int]int{}

	for i := 1; i <= d.SearchStepCount; i++ {
		newGeneration := make(map[h.Coord]struct{}, 4)
		// newGenerationBound := d.grid.AsRegion()
		for currentLoc := range generation {
			for _, adj := range d.GetAdjacentGardenTiled(currentLoc) {
				_, ok := newGeneration[adj]
				if !ok {
					newGeneration[adj] = struct{}{}
					// newGenerationBound = newGenerationBound.Expand(adj)
				}
			}
		}
		generation = newGeneration
		fmt.Printf("Iteration %d has %d possible locations\n", i, len(generation))
		// fmt.Printf("final bound is %v\n", newGenerationBound)

		//fill out a mapping of region coordinates to region IDs
		regionMap := make(map[h.Coord]int, (d.RegionCompareSize*2+1)*(d.RegionCompareSize*2+1))
		for r1 := -d.RegionCompareSize; r1 < d.RegionCompareSize+1; r1++ {
			for c1 := -d.RegionCompareSize; c1 < d.RegionCompareSize+1; c1++ {
				id := d.GetRegionId(r1, c1, &generation)
				regionMap[h.Coord{Row: r1, Col: c1}] = id
				// fmt.Printf("% 5d, ", id)
			}
			// fmt.Println()
		}
		// fmt.Println()
		//add the map for this step to the history list
		d.RegionHistory = append(d.RegionHistory, regionMap)

		//dump the grid with the reachable tiles marked
		// fmt.Println("---------------")
		// // for r := newGenerationBound.UpperLeft().Row; r <= newGenerationBound.LowerRight().Row; r++ {
		// for r := -40; r <= 50; r++ {
		// 	fmt.Printf("%d  ", r)
		// 	// for c := newGenerationBound.UpperLeft().Col; c <= newGenerationBound.LowerRight().Col; c++ {
		// 	for c := -40; c <= 50; c++ {
		// 		coord := h.Coord{Row: r, Col: c}
		// 		_, ok := generation[coord]
		// 		var cellVal string
		// 		if ok {
		// 			cellVal = "O"
		// 		} else {
		// 			cellVal = string(d.grid.GetTiled(coord).Value)
		// 		}
		// 		fmt.Printf("%s", string(cellVal))
		// 	}
		// 	fmt.Println()
		// }
		// fmt.Printf("final bound is %v\n", newGenerationBound)
	}

	//use this to print region histories if desired
	// fmt.Println("Region histories:")
	// for r1 := -regionCompareSize; r1 < regionCompareSize+1; r1++ {
	// 	for c1 := -regionCompareSize; c1 < regionCompareSize+1; c1++ {
	// 		fmt.Printf("r=%d,c=%d: ", r1, c1)
	// 		for i := 0; i < len(regionHistory); i++ {
	// 			fmt.Printf("%d,", regionHistory[i][h.Coord{Row: r1, Col: c1}])
	// 		}
	// 		fmt.Println()
	// 	}
	// }

}

// search through the center grid until we find the steady state oscillation
// return values are oddReachableCount, evenReachableCount
func (d *Day21) FindSteadyStateGridPattern() {
	var evenId, oddId int

	coord := h.Coord{Row: 0, Col: 0}
	for i := 0; i < d.SearchStepCount-4; i++ {
		id1 := d.RegionHistory[i][coord]
		id2 := d.RegionHistory[i+1][coord]
		id3 := d.RegionHistory[i+2][coord]
		id4 := d.RegionHistory[i+3][coord]
		if id1 == id3 && id2 == id4 {
			//found a match
			if i%2 == 0 {
				//we're on an even step, so id1 is even and id2 is odd
				evenId = id1
				oddId = id2
			} else {
				//w're on an odd step, so reverse
				evenId = id2
				oddId = id1
			}
			break
		}
	}
	h.Assert(evenId > 0 && oddId > 0, "no steady state found")
	d.OddSteadyStateReachableCount = d.RegionIndexToReachableCount[oddId]
	d.EvenSteadyStateReachableCount = d.RegionIndexToReachableCount[evenId]
}

// returns the first step where the regionID for the row and column is not 0
func (d *Day21) FindFirstNonemptyGridId(row int, col int) (int, int) {
	for i := 0; i < d.SearchStepCount; i++ {
		regionId := d.RegionHistory[i][h.Coord{Row: row, Col: col}]
		if regionId > 0 {
			return i, regionId
		}
	}
	panic("found no nonempty for row")
}

// find the column where we first get a repeating pattern in new column regionIDs
// returns:
// - the step where the first pattern column appears,
// - the offset between the pattern starts
// - the column index of the first pattern column
func (d *Day21) FindPatternColumnStartForRow(row int) (int, int, int, int) {

	for col1 := 1; col1 < d.RegionCompareSize-1; col1++ {
		col2 := col1 + 1
		upColStartStep1, upColStartRegionId1 := d.FindFirstNonemptyGridId(row, col1)
		upColStartStep2, upColStartRegionId2 := d.FindFirstNonemptyGridId(row, col2)
		downColStartStep1, downColStartRegionId1 := d.FindFirstNonemptyGridId(row, -col1)
		downColStartStep2, downColStartRegionId2 := d.FindFirstNonemptyGridId(row, -col2)

		if upColStartRegionId1 != upColStartRegionId2 || //region IDs don't match across pattern
			downColStartRegionId1 != downColStartRegionId2 || //region ID's don't match across pattern
			upColStartStep1 != downColStartStep1 { //the up and down patterns don't start at the same place
			//no match, so keep searching
			continue
		}
		//check the secondary column region IDs
		upSecondaryRegionID1 := d.RegionHistory[upColStartStep1][h.Coord{Row: row, Col: col1 - 1}]
		upSecondaryRegionID2 := d.RegionHistory[upColStartStep2][h.Coord{Row: row, Col: col2 - 1}]
		downSecondaryRegionID1 := d.RegionHistory[downColStartStep1][h.Coord{Row: row, Col: col1 - 1}]
		downSecondaryRegionID2 := d.RegionHistory[downColStartStep2][h.Coord{Row: row, Col: col2 - 1}]

		if upSecondaryRegionID1 != upSecondaryRegionID2 || downSecondaryRegionID1 != downSecondaryRegionID2 {
			continue
		}

		//match found
		return upColStartStep1, upColStartStep2, upColStartStep2 - upColStartStep1, col1
	}
	panic("no pattern for column starts found")
}

// func (d *Day21) ExtrapolateReachableCountForRow(row int) int {

// 	colStartStep, colPatternOffset, patternCol := d.FindPatternColumnStartForRow(row)

// 	//number of columns we make up to the start of the pattern columns
// 	middleColumnCount := 2*patternCol - 3 //minus three because there are two secondary columns in the pattern

// 	//the number of whole patterns (new columns) we have up the target
// 	//note this is integer division so it rounds down
// 	patternCount := (d.TargetStepCount - colStartStep) / colPatternOffset

// 	// how far into the next pattern we are, which dictates which regionID the additional column
// 	// will have
// 	patternRemainder := (d.TargetStepCount - colStartStep) % colPatternOffset

// 	//figure out the region IDs for the partial pattern state left over
// 	remainderPatternRegionIds := []int{
// 		//the two tiles on the positive end
// 		d.RegionHistory[colStartStep+patternRemainder][h.Coord{Row: row, Col: patternCol}],
// 		d.RegionHistory[colStartStep+patternRemainder][h.Coord{Row: row, Col: patternCol - 1}],
// 		//the two tiles on the negative end
// 		d.RegionHistory[colStartStep+patternRemainder][h.Coord{Row: row, Col: -patternCol}],
// 		d.RegionHistory[colStartStep+patternRemainder][h.Coord{Row: row, Col: -(patternCol - 1)}],
// 	}

// 	//now sum up the reachable counts for everything
// 	reachableCount := 0

// 	//add the patterns for the steady state columns
// 	steadyStateTotalCols := middleColumnCount + 2*patternCount
// 	h.Assert(steadyStateTotalCols%2 == 1, "number of steady cols is not odd")

// 	//reachable counts for the balance (one odd, one even)
// 	reachableCount += (steadyStateTotalCols - 1) / 2 * (d.OddSteadyStateReachableCount + d.EvenSteadyStateReachableCount)

// 	//the remaining steady state column is the opposite one of the oddness of the last step
// 	if d.TargetStepCount%2 == 0 {
// 		//step count is even, so extra count is odd
// 		reachableCount += d.OddSteadyStateReachableCount
// 	} else {
// 		//step count is odd, so extra count is even
// 		reachableCount += d.EvenSteadyStateReachableCount
// 	}

// 	//add the counts for the remainders
// 	for _, regionID := range remainderPatternRegionIds {
// 		reachableCount += d.RegionIndexToReachableCount[regionID]
// 	}

// 	return reachableCount

// }

func (d *Day21) Part2() {
	fmt.Println("Part 2")

	//the search values are determined hueristically / by inspection
	d.SearchStepCount = 100
	d.RegionCompareSize = 10
	//how many steps we want to find a reachable count for
	d.TargetStepCount = 5000

	d.DoRegionSearch()

	//now that we have populated our region search, we look for row patterns taht we can
	//extrapolate out to the large target step counts

	//all grid regions eventually reach a steady state that oscillates between two states
	//we need the reachable counts for these states
	d.FindSteadyStateGridPattern()

	startStep1, startStep2, patternOffset, patternCol := d.FindPatternColumnStartForRow(0)

	fmt.Println(startStep1, startStep2, patternOffset, patternCol)

	startOffset := (d.TargetStepCount - startStep2) % patternOffset
	startStep := startStep2 + startOffset

	h.Assert((d.TargetStepCount-startStep)%patternOffset == 0, "startStep is not an even number of pattern offsets from the target")

	numIterations := (d.TargetStepCount - startStep) / patternOffset

	//get the number of reachable tiles at our starting step
	initialReachableCount := 0
	startStepRegionMap := &d.RegionHistory[startStep]
	for _, regionId := range *startStepRegionMap {
		regionCount := d.RegionIndexToReachableCount[regionId]
		initialReachableCount += regionCount
	}

	//sum up the values for the 1 and -1 columns
	cycleIncrementToAdd := 0
	for row := -d.RegionCompareSize; row < d.RegionCompareSize; row++ {
		for _, col := range []int{1, -1} {
			regionId := (*startStepRegionMap)[h.Coord{Row: row, Col: col}]
			regionCount := d.RegionIndexToReachableCount[regionId]
			cycleIncrementToAdd += regionCount
		}
	}

	evenOddToAdd := 3 // add three each of even and odd counts, then increment this number by 2 earch loop

	reachableCount := initialReachableCount
	for i := 0; i < numIterations; i++ {
		reachableCount += cycleIncrementToAdd
		reachableCount += evenOddToAdd * (d.EvenSteadyStateReachableCount + d.OddSteadyStateReachableCount)
		evenOddToAdd += 2
	}

	fmt.Println("Reachable tiles = ", reachableCount)

	// fmt.Println(startOffset, startStep, (d.TargetStepCount-startStep)%patternOffset)

	// //find the step where we have a non-zero regionID in region row,0
	// startStep, startRegionId := d.FindFirstNonemptyGridId(row, 0)

	// //find the place where two rows start with the same grid pattern
	// findRowGridPattern := func(searchUp bool) (int, int, int) {
	// 	var rowStart, rowEnd, rowIncrement int
	// 	if searchUp {
	// 		rowStart = 1
	// 		rowEnd = regionCompareSize
	// 		rowIncrement = 1
	// 	} else {
	// 		rowStart = -1
	// 		rowEnd = -regionCompareSize
	// 		rowIncrement = -1
	// 	}
	// 	for row1 := rowStart; row1 < rowEnd; row1 += rowIncrement {
	// 		row2 := row1 + rowIncrement
	// 		//see if this row and the next row have the same starting region pattern
	// 		offset1, regionId1 := findFirstNonemptyGridId(row1)
	// 		offset2, regionId2 := findFirstNonemptyGridId(row2)
	// 		if regionId1 == regionId2 {
	// 			//pattern found
	// 			return row1, offset1, offset2 - offset1
	// 		}
	// 	}
	// 	panic("no pattern found")
	// }

	// upPatternStartRow, upRowFirstIndex, upRowNextIndex := findRowGridPattern(true)
	// downPatternStartRow, downRowFirstIndex, downRowNextIndex := findRowGridPattern(false)

	// //now apply the patterns to compute how many reachable steps there are

	// //number of complete rows in the middle
	// middleRows := (upPatternStartRow - downPatternStartRow) - 1

}
