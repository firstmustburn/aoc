package main

import (
	h "aoc2023/internal/helpers"
	"fmt"
	"log/slog"
	"math"
	"os"
	"slices"
	"strconv"
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

	// f, err := os.Create("day18.prof")
	// if err != nil {
	// 	panic(err)
	// }
	// pprof.StartCPUProfile(f)
	// defer pprof.StopCPUProfile()

	d := &Day18{}

	err = h.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

type Day18 struct {
	lines        []string
	instructions []Instruction
	grid         *h.SparseGrid[GridCell]
	path         []h.Coord
}

func (d *Day18) Setup(filename string) {
	fmt.Println("Setup")
	d.lines = h.ReadFileToLines(filename)

	dirMap := map[string]h.Direction{
		"R": h.EAST,
		"D": h.SOUTH,
		"L": h.WEST,
		"U": h.NORTH,
	}

	for _, line := range d.lines {
		tokens := strings.Split(line, " ")
		h.Assert(len(tokens) == 3, "wrong number of tokens")

		direction, ok := dirMap[tokens[0]]
		h.Assert(ok, "no match for direction")
		distance, err := strconv.Atoi(tokens[1])
		h.Assert(err == nil, "Could not parse direction as int")
		color := tokens[2]
		d.instructions = append(d.instructions, Instruction{
			Direction: direction,
			Distance:  distance,
			Color:     color})
	}

	d.grid = h.CreateSparseGrid[GridCell]()
}

type GridCell struct {
	IsDug bool
	Color string
}

func (d *Day18) DumpGrid() {
	fmt.Println("----------------------------")
	for row := d.grid.MinRow(); row <= d.grid.MaxRow(); row++ {
		for col := d.grid.MinCol(); col <= d.grid.MaxCol(); col++ {
			coord := h.Coord{Row: row, Col: col}
			value := d.grid.Get(coord)
			if value == nil {
				fmt.Printf(".")
			} else {
				fmt.Printf("#")
			}
		}
		fmt.Println()
	}
	fmt.Println("----------------------------")
}

func (d *Day18) Flood(startCoord h.Coord) {

	toFlood := []h.Coord{startCoord}

	for len(toFlood) > 0 {
		//flood the first cell on the list
		current := toFlood[0]
		toFlood = toFlood[1:]

		d.grid.Set(current, &GridCell{false, ""})

		for _, adjacent := range current.Adjacent(false) {
			if !d.grid.IsSet(adjacent) {
				toFlood = append(toFlood, adjacent)
			}
		}
	}
}

func (d *Day18) IsVertical(coord h.Coord) bool {
	return d.grid.IsSet(coord.N()) && d.grid.IsSet(coord.S())
}

func (d *Day18) IsCrossing(coord h.Coord) (bool, h.Coord) {
	//our ray cast is moving to the left, so the coord we start with is already the rightmost
	h.Assert(!d.grid.IsSet(coord.E()), "start coord is not rightmost"+fmt.Sprintf("%v", coord)) //just make sure

	leftmost := coord
	for d.grid.IsSet(leftmost.W()) {
		leftmost = leftmost.W()
	}

	//now see if the rightmost and leftmost have same or opposite sides set
	leftUp := d.grid.IsSet(leftmost.N())
	leftDown := d.grid.IsSet(leftmost.S())
	rightUp := d.grid.IsSet(coord.N())
	rightDown := d.grid.IsSet(coord.S())

	isCrossing := (leftUp && rightDown) || (leftDown && rightUp)
	return isCrossing, leftmost
}

func (d *Day18) CountEnclosed() int64 {
	enclosedCount := int64(0)
	for row := d.grid.MinRow(); row <= d.grid.MaxRow(); row++ {
		//do columns from right to left
		hitCount := 0
		for col := d.grid.MaxCol(); col >= d.grid.MinCol(); col-- {
			coord := h.Coord{Row: row, Col: col}
			if d.grid.IsSet(coord) {
				//this is an edge, so adjust the hit count accordingly
				if d.IsVertical(coord) {
					hitCount += 1
				} else {
					//else, horizontal
					isCrossing, leftMostCoord := d.IsCrossing(coord)
					if isCrossing {
						hitCount += 1
					}
					//fast forward to the end of the edge
					col = leftMostCoord.Col
				}
			} else {
				//not an edge, so increment
				if hitCount%2 == 1 {
					//when hit count is odd, we are inside
					enclosedCount += 1
				}
			}
		}
		fmt.Println("Row done", row)
	}
	return enclosedCount
}

func (d *Day18) IsEnclosed(coord h.Coord) bool {
	//can't be enclosed if it's part of the loop
	if d.grid.IsSet(coord) {
		return false
	}
	//ray cast to the left
	hitCount := 0

	testCoord := coord.W()
	for testCoord.Col >= d.grid.MinCol() {

		if !slices.Contains(d.path, testCoord) {
			//can't be a hit if it's not on the path
			testCoord = testCoord.W()
			continue
		}

		//vertical case
		if d.IsVertical(testCoord) {
			hitCount += 1
			testCoord = testCoord.W()
			continue
		}

		//horizontal case, so see if it is crossing or not
		isCrossing, crossingLeftmost := d.IsCrossing(testCoord)
		if isCrossing {
			hitCount += 1
		}
		testCoord = crossingLeftmost.W()
		continue
	}
	//if we have an odd number of hits, it is enclosed.
	return (hitCount % 2) == 1
}

type Point struct {
	x float64
	y float64
}

type Instruction struct {
	Direction h.Direction
	Distance  int
	Color     string
	//the xy point associated with this instruction
	Point Point
}

type DPair struct {
	d1 h.Direction
	d2 h.Direction
}

func (d *Day18) Part1() {
	fmt.Println("Part 1")

	x := 0.0
	y := 0.0
	for index := range d.instructions {
		instruction := &d.instructions[index]
		if instruction.Direction == h.EAST {
			x += float64(instruction.Distance)
		} else if instruction.Direction == h.WEST {
			x -= float64(instruction.Distance)
		} else if instruction.Direction == h.NORTH {
			//+y is south to be the same as rows
			y -= float64(instruction.Distance)
		} else if instruction.Direction == h.SOUTH {
			y += float64(instruction.Distance)
		} else {
			panic("unreachable")
		}
		//set the point
		instruction.Point = Point{x, y}
	}

	//map of path direciton pairs that define corners and how
	//to more the corner point to grow the corner to the outside
	//remember the +y is south/down
	//these values also assume a clockwise traversal
	deltaMap := map[DPair]Point{
		{h.EAST, h.NORTH}: {-0.5, -0.5},
		{h.EAST, h.SOUTH}: {0.5, -0.5},
		{h.WEST, h.NORTH}: {-0.5, 0.5},
		{h.WEST, h.SOUTH}: {0.5, 0.5},
		{h.NORTH, h.EAST}: {-0.5, -0.5},
		{h.NORTH, h.WEST}: {-0.5, 0.5},
		{h.SOUTH, h.EAST}: {0.5, -0.5},
		{h.SOUTH, h.WEST}: {0.5, 0.5},
	}

	for index := 0; index < len(d.instructions); index += 1 {
		nextIndex := (index + 1) % len(d.instructions)
		deltaVal := deltaMap[DPair{
			d.instructions[index].Direction,
			d.instructions[nextIndex].Direction,
		}]
		d.instructions[index].Point.x += deltaVal.x + 0.5
		d.instructions[index].Point.y += deltaVal.y + 0.5
	}

	for _, i := range d.instructions {
		fmt.Printf("%.0f %.0f\n", i.Point.x, i.Point.y)
	}

	shoelace1 := 0.0
	shoelace2 := 0.0
	for index := 0; index < len(d.instructions); index += 1 {
		nextIndex := (index + 1) % len(d.instructions)
		shoelace1 += d.instructions[index].Point.x * d.instructions[nextIndex].Point.y
		shoelace2 += d.instructions[index].Point.y * d.instructions[nextIndex].Point.x
	}
	enclosedArea := math.Abs((shoelace1 - shoelace2) / 2)

	fmt.Println("Enclosed area is", strconv.FormatFloat(enclosedArea, 'f', 0, 64))

	// currentCoord := h.Coord{Row: 0, Col: 0}
	// d.grid.Set(currentCoord, &GridCell{true, ""})
	// d.path = append(d.path, currentCoord)
	// for _, instruction := range d.instructions {
	// 	for i := 0; i < instruction.Distance; i++ {
	// 		currentCoord = currentCoord.Dir(instruction.Direction)
	// 		d.grid.Set(currentCoord, &GridCell{true, instruction.Color})
	// 		d.path = append(d.path, currentCoord)
	// 	}
	// }

	// d.DumpGrid()

	// fmt.Println("Dug out", d.grid.Len())

	// fmt.Println("Rows", d.grid.MinRow(), d.grid.MaxRow())
	// fmt.Println("Cols", d.grid.MinCol(), d.grid.MaxCol())

	// enclCount := d.CountEnclosed()
	// fmt.Println("Enclosed ", enclCount)

	// fmt.Println("Total Dug out", enclCount+int64(d.grid.Len()))

}

func (d *Day18) Part2() {
	fmt.Println("Part 2")

	//0 means R, 1 means D, 2 means L, and 3 means U.
	dirMap := map[string]h.Direction{
		"0": h.EAST,
		"1": h.SOUTH,
		"2": h.WEST,
		"3": h.NORTH,
	}

	//rewrite the instructions
	newInstructions := make([]Instruction, 0, len(d.instructions))
	for _, instruction := range d.instructions {
		distance, err := strconv.ParseInt(instruction.Color[2:7], 16, 32)
		h.Assert(err == nil, "could not parse hex value to distance")
		direction := dirMap[string(instruction.Color[7])]
		newInstructions = append(newInstructions, Instruction{
			Direction: direction,
			Distance:  int(distance),
		})
	}
	d.instructions = newInstructions
	// for _, i := range d.instructions {
	// 	fmt.Println(i)
	// }
	d.Part1()
}
