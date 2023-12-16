package main

import (
	h "aoc2023/internal/helpers"
	"fmt"
	"log/slog"
	"os"
	"slices"
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

	// f, err := os.Create("day16.prof")
	// if err != nil {
	// 	panic(err)
	// }
	// pprof.StartCPUProfile(f)
	// defer pprof.StopCPUProfile()

	d := &Day16{}

	err = h.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

type GridData struct {
	value byte
	dirs  []h.Direction
}

type Beam struct {
	Position  h.Coord
	Direction h.Direction
}

func (d *Day16) DumpGridValue() {
	walker := func(r int, c int, v GridData) {
		if c == 0 {
			fmt.Println("")
		}
		fmt.Printf("%s", string(v.value))
	}
	d.grid.WalkRCV(walker)
	fmt.Println("")
}

func (d *Day16) DumpGridIsEnergized() {
	walker := func(r int, c int, v GridData) {
		if c == 0 {
			fmt.Println("")
		}
		if len(v.dirs) > 0 {
			fmt.Printf("%s", string(TILE_ENERGIZED))
		} else {
			fmt.Printf("%s", string(TILE_EMPTY))
		}
	}
	d.grid.WalkRCV(walker)
	fmt.Println("")
}

type Day16 struct {
	lines     []string
	grid      *h.Grid[GridData]
	nullCoord h.Coord
}

func (d *Day16) Setup(filename string) {
	fmt.Println("Setup")
	d.lines = h.ReadFileToLines(filename)

	rows := len(d.lines)
	cols := len(d.lines[0])
	d.grid = h.CreateGrid[GridData](rows, cols)

	//fill the grid
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			d.grid.SetRC(r, c, GridData{d.lines[r][c], []h.Direction{}})
		}
	}

	//the nullCoord is outside the grid
	d.nullCoord = h.Coord{Row: rows * 2, Col: cols * 2}

}

const TILE_EMPTY byte = '.'
const TILE_LEFT_MIRROR byte = '/'
const TILE_RIGHT_MIRROR byte = '\\'
const TILE_SPLIT_VERTICAL byte = '|'
const TILE_SPLIT_HORIZONTAL byte = '-'
const TILE_ENERGIZED byte = '#'

var LEFT_MIRROR_MAP = map[h.Direction]h.Direction{
	h.WEST:  h.SOUTH,
	h.NORTH: h.EAST,
	h.EAST:  h.NORTH,
	h.SOUTH: h.WEST,
}
var RIGHT_MIRROR_MAP = map[h.Direction]h.Direction{
	h.WEST:  h.NORTH,
	h.NORTH: h.WEST,
	h.EAST:  h.SOUTH,
	h.SOUTH: h.EAST,
}

// returns the beams propagating out of the cell and true if the cell was energized for the
// first time
func (d *Day16) Propagate(inputs []Beam) []Beam {
	outputs := make([]Beam, 0, len(inputs))

	for _, input := range inputs {
		newPos := input.Position.Dir(input.Direction)
		if !d.grid.ContainsCoord(newPos) {
			//propagated off the grid, so nothing to return
			continue
		}
		ogData := d.grid.Get(newPos)
		if slices.Contains(ogData.dirs, input.Direction) {
			//skip this one because we've already shone light this way on this tile
			continue
		} else {
			//mark the tile and set the return value
			d.grid.Set(newPos, GridData{ogData.value, append(ogData.dirs, input.Direction)})
		}

		//set the propagation outputs
		if ogData.value == TILE_EMPTY {
			//keep the same direction
			outputs = append(outputs, Beam{newPos, input.Direction})
		} else if ogData.value == TILE_LEFT_MIRROR {
			//map the direction
			outputs = append(outputs, Beam{newPos, LEFT_MIRROR_MAP[input.Direction]})
		} else if ogData.value == TILE_RIGHT_MIRROR {
			//map the direction
			outputs = append(outputs, Beam{newPos, RIGHT_MIRROR_MAP[input.Direction]})
		} else if ogData.value == TILE_SPLIT_VERTICAL {
			if input.Direction == h.NORTH || input.Direction == h.SOUTH {
				//keep the same direction
				outputs = append(outputs, Beam{newPos, input.Direction})
			} else {
				//split into two directions
				outputs = append(outputs, Beam{newPos, h.NORTH})
				outputs = append(outputs, Beam{newPos, h.SOUTH})
			}
		} else if ogData.value == TILE_SPLIT_HORIZONTAL {
			if input.Direction == h.EAST || input.Direction == h.WEST {
				//keep the same direction
				outputs = append(outputs, Beam{newPos, input.Direction})
			} else {
				//split into two directions
				outputs = append(outputs, Beam{newPos, h.EAST})
				outputs = append(outputs, Beam{newPos, h.WEST})
			}
		} else {
			panic("unhandled")
		}
	}
	return outputs
}

func (d *Day16) Part1() {
	fmt.Println("Part 1")
	d.DumpGridValue()

	beams := []Beam{
		{
			Position:  h.Coord{Row: 0, Col: -1},
			Direction: h.EAST,
		},
	}
	for len(beams) > 0 {
		beams = d.Propagate(beams)
		// d.DumpGridIsEnergized()
	}

	d.DumpGridIsEnergized()

	energizedCount := d.CountEnergized()
	fmt.Println("energized", energizedCount)
}

func (d *Day16) CountEnergized() int {
	//count energized
	energizedCount := 0
	walker := func(row int, col int, value GridData) {
		if len(value.dirs) > 0 {
			energizedCount += 1
		}
	}
	d.grid.WalkRCV(walker)
	return energizedCount
}

func (d *Day16) ResetGrid() {
	walker := func(row int, col int, value GridData) {
		d.grid.SetRC(row, col, GridData{value.value, []h.Direction{}})
	}
	d.grid.WalkRCV(walker)
}

func (d *Day16) RunGrid(initial Beam) int {
	d.ResetGrid()
	beams := []Beam{initial}

	for len(beams) > 0 {
		beams = d.Propagate(beams)
	}

	return d.CountEnergized()

}

func (d *Day16) StartingBeams() []Beam {
	beams := make([]Beam, 0, (d.grid.Rows()+d.grid.Cols())*2)
	for row := 0; row < d.grid.Rows(); row++ {
		beams = append(beams, Beam{h.Coord{Row: row, Col: -1}, h.EAST})
		beams = append(beams, Beam{h.Coord{Row: row, Col: d.grid.Cols()}, h.WEST})
	}
	for col := 0; col < d.grid.Cols(); col++ {
		beams = append(beams, Beam{h.Coord{Row: -1, Col: col}, h.SOUTH})
		beams = append(beams, Beam{h.Coord{Row: d.grid.Rows(), Col: col}, h.NORTH})
	}
	return beams
}

func (d *Day16) Part2() {
	fmt.Println("Part 2")

	maxEnergized := 0
	for _, beam := range d.StartingBeams() {
		numEnergized := d.RunGrid(beam)
		if numEnergized > maxEnergized {
			maxEnergized = numEnergized
			fmt.Printf("NEW MAX: %d energized for beam %v;\n", numEnergized, beam)
		} else {
			fmt.Printf("%d energized for beam %v;\n", numEnergized, beam)
		}
	}
	fmt.Println("maxEnergized", maxEnergized)

}
