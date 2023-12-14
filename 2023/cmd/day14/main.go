package main

import (
	h "aoc2023/internal/helpers"
	"fmt"
	"log/slog"
	"os"
	"time"
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

	// f, err := os.Create("day14.prof")
	// if err != nil {
	// 	panic(err)
	// }
	// pprof.StartCPUProfile(f)
	// defer pprof.StopCPUProfile()

	d := &Day14{}

	err = h.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

type GridData struct {
	value byte
}

func (d *Day14) DumpGrid() {
	walker := func(r int, c int, v GridData) {
		if c == 0 {
			fmt.Println("")
		}
		fmt.Printf("%s", string(v.value))
	}
	d.grid.WalkRCV(walker)
	fmt.Println("")
}

const TILE_FIXED byte = '#'
const TILE_ROLLING byte = 'O'
const TILE_EMPTY byte = '.'

type Day14 struct {
	lines     []string
	grid      *h.Grid[GridData]
	nullCoord h.Coord
}

func (d *Day14) Setup(filename string) {
	fmt.Println("Setup")
	d.lines = h.ReadFileToLines(filename)

	rows := len(d.lines)
	cols := len(d.lines[0])
	d.grid = h.CreateGrid[GridData](rows, cols)

	//fill the grid
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			d.grid.SetRC(r, c, GridData{d.lines[r][c]})
		}
	}

	//the nullCoord is outside the grid
	d.nullCoord = h.Coord{Row: rows * 2, Col: cols * 2}
}

func (d *Day14) Tilt(dir h.Direction) bool {
	didChange := false
	//simulate the tilt of the grid in one direction
	walker := func(startCoord h.Coord, data GridData) {
		//only need to process rolling tiles
		if data.value != TILE_ROLLING {
			return
		}
		//this is where we want to roll to
		destCoord := startCoord.Dir(dir)
		if !d.grid.ContainsCoord(destCoord) {
			//no movement because we're at the edge of the grid
			return
		}

		if d.grid.Get(destCoord).value == TILE_EMPTY {
			//we can roll into the tile
			d.grid.Set(destCoord, GridData{TILE_ROLLING})
			d.grid.Set(startCoord, GridData{TILE_EMPTY})
			didChange = true
		}

	}
	d.grid.WalkVFrom(walker, dir)
	return didChange
}

func (d *Day14) TiltToStop(dir h.Direction) {
	for {
		didChange := d.Tilt(dir)
		//no change so done rolling
		if !didChange {
			break
		}
	}
}

func (d *Day14) SpinCycle() {
	d.TiltToStop(h.NORTH)
	d.TiltToStop(h.WEST)
	d.TiltToStop(h.SOUTH)
	d.TiltToStop(h.EAST)
}

func (d *Day14) Weigh() int {

	totalWeight := 0

	walker := func(coord h.Coord, data GridData) {
		//only need to process rolling tiles
		if data.value != TILE_ROLLING {
			return
		}
		//compute the weight
		weight := d.grid.Rows() - coord.Row
		totalWeight += weight
	}
	d.grid.WalkV(walker)
	return totalWeight
}

func (d *Day14) Part1() {
	fmt.Println("Part 1")
	d.DumpGrid()

	d.TiltToStop(h.NORTH)

	d.DumpGrid()
	fmt.Println("Total north weight", d.Weigh())

}

func (d *Day14) GridString() string {
	strVal := ""

	walker := func(row int, col int, data GridData) {
		strVal += string(data.value)
	}
	d.grid.WalkRCV(walker)
	return strVal
}

func (d *Day14) Part2() {
	fmt.Println("Part 2")

	prevStates := make(map[string]int, 10000)

	//find a state we have previously
	cycleNumber := 0
	var firstRepeatStart int

	targetCycles := 1000000000

	for {
		d.SpinCycle()
		cycleNumber += 1
		cycleString := d.GridString()
		// fmt.Println(cycleString)
		var ok bool
		firstRepeatStart, ok = prevStates[cycleString]
		if !ok {
			//not found, so add to the previous states
			prevStates[cycleString] = cycleNumber
		} else {
			break
		}
	}
	fmt.Println("first repeat from", firstRepeatStart, "to", cycleNumber)

	remainingCycles := (targetCycles - firstRepeatStart) % (cycleNumber - firstRepeatStart)
	fmt.Println("Run remaining cycles", remainingCycles)

	for i := 0; i < remainingCycles; i++ {
		d.SpinCycle()
		// cycleString := d.GridString()
		// fmt.Println(cycleString)
	}

	fmt.Println("Total north weight", d.Weigh())
}

// just for grins, to see how long it would take
func (d *Day14) Part2BF() {
	fmt.Println("Part 2")

	startTime := time.Now()
	targetCycles := 1000000000

	for i := 0; i < targetCycles; i++ {
		d.SpinCycle()
		// cycleString := d.GridString()
		// fmt.Println(cycleString)
		if i%1000 == 0 {
			progress := (float64(i) / float64(targetCycles))
			elapsed := time.Since(startTime)
			remaining := (1.0 - (progress * 100)) * (elapsed.Seconds() / progress)
			fmt.Printf("%f%% done after %f seconds, %f days remaining\n", progress*100.0, elapsed.Seconds(), remaining/3600.0/24.0)
		}
	}

	fmt.Println("Total north weight", d.Weigh())
}
