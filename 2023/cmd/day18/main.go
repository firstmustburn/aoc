package main

import (
	h "aoc2023/internal/helpers"
	"fmt"
	"log/slog"
	"math"
	"os"
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
