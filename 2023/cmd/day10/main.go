package main

import (
	h "aoc2023/internal/helpers"
	"fmt"
	"os"
	"slices"
)

func main() {

	d := &Day10{}

	err := h.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

type GridData struct {
	c byte //the character for this byte
}

type Day10 struct {
	lines     []string
	grid      *h.Grid[GridData]
	nullCoord h.Coord
	path      []h.Coord
}

func (d *Day10) Setup(filename string) {
	fmt.Println("Setup")
	d.lines = h.ReadFileToLines(filename)

	rows := len(d.lines)
	cols := len(d.lines[0])

	d.grid = h.CreateGrid[GridData](rows, cols)
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			d.grid.SetRC(r, c, GridData{d.lines[r][c]})
		}
	}

	//the nullCoord is outside the grid
	d.nullCoord = h.Coord{Row: rows * 2, Col: cols * 2}

}

func (d *Day10) DumpGrid() {
	walker := func(r int, c int, v GridData) {
		if c == 0 {
			fmt.Println("")
		}
		fmt.Printf("%s", string(v.c))
	}
	d.grid.WalkRCV(walker)
	fmt.Println("")
}

const TILE_START byte = 'S'
const TILE_VERTICAL byte = '|'
const TILE_HORIZONTAL byte = '-'
const TILE_NORTH_EAST byte = 'L'
const TILE_NORTH_WEST byte = 'J'
const TILE_SOUTH_EAST byte = 'F'
const TILE_SOUTH_WEST byte = '7'
const TILE_NONE byte = '.'

var CORNERS []byte = []byte{TILE_NORTH_EAST, TILE_NORTH_WEST, TILE_SOUTH_EAST, TILE_SOUTH_WEST}

func OppositeTile(t byte) byte {
	if t == TILE_NORTH_EAST {
		return TILE_SOUTH_WEST
	}
	if t == TILE_NORTH_WEST {
		return TILE_SOUTH_EAST
	}
	if t == TILE_SOUTH_EAST {
		return TILE_NORTH_WEST
	}
	if t == TILE_SOUTH_WEST {
		return TILE_NORTH_EAST
	}
	panic("No opposite for given tile")
}

func Directions(c byte) []h.Direction {
	if c == TILE_VERTICAL {
		return []h.Direction{h.NORTH, h.SOUTH}
	} else if c == TILE_HORIZONTAL {
		return []h.Direction{h.EAST, h.WEST}
	} else if c == TILE_NORTH_EAST {
		return []h.Direction{h.NORTH, h.EAST}
	} else if c == TILE_NORTH_WEST {
		return []h.Direction{h.NORTH, h.WEST}
	} else if c == TILE_SOUTH_EAST {
		return []h.Direction{h.SOUTH, h.EAST}
	} else if c == TILE_SOUTH_WEST {
		return []h.Direction{h.SOUTH, h.WEST}
	} else if c == TILE_NONE {
		return []h.Direction{}
	} else if c == TILE_START {
		return []h.Direction{h.NORTH, h.SOUTH, h.EAST, h.WEST}
	} else {
		panic(fmt.Errorf("unknown tile %d", c))
	}
}

// FindConnected finds a coordinate adjacent to coord that is not notCoord
func (d *Day10) FindConnected(coord h.Coord, notCoord h.Coord) h.Coord {
	coordVal := d.grid.Get(coord).c
	for _, adjacentDir := range Directions(coordVal) {
		adjacentCoord := coord.Dir(adjacentDir)
		if adjacentCoord == notCoord {
			continue
		}
		if !d.grid.ContainsCoord(adjacentCoord) {
			continue //skip for coords not in the map
		}
		adjacentVal := d.grid.Get(adjacentCoord).c
		if slices.Contains(Directions(adjacentVal), adjacentDir.Opposite()) {
			return adjacentCoord
		}
	}
	panic("Didn't find an adjacent coord")
}

func (d *Day10) Part1() {
	fmt.Println("Part 1")

	path := []h.Coord{}

	//find the start
	{
		walker := func(coord h.Coord, v GridData) {
			if v.c == TILE_START {
				path = append(path, coord)
			}
		}
		d.grid.WalkV(walker)
	}

	//get the next connected node
	path = append(path, d.FindConnected(path[0], d.nullCoord))
	for {
		//
		nextCoord := d.FindConnected(path[len(path)-1], path[len(path)-2])
		if nextCoord == path[0] {
			//come to the start, so stop
			break
		}
		path = append(path, nextCoord)
	}

	for _, c := range path {
		fmt.Println(c)
	}
	fmt.Println("max steps:", len(path)/2)
	d.path = path

}

func (d *Day10) ReplaceStartInGrid() {
	//figure out what kind of tile the start tile is and replace it with that in the grid
	startCoord := d.path[0]
	directions := []h.Direction{
		h.GetDirection(startCoord, d.path[1]),
		h.GetDirection(startCoord, d.path[len(d.path)-1]),
	}
	if slices.Contains(directions, h.NORTH) && slices.Contains(directions, h.EAST) {
		d.grid.Set(startCoord, GridData{c: TILE_NORTH_EAST})
	} else if slices.Contains(directions, h.NORTH) && slices.Contains(directions, h.WEST) {
		d.grid.Set(startCoord, GridData{c: TILE_NORTH_WEST})
	} else if slices.Contains(directions, h.SOUTH) && slices.Contains(directions, h.WEST) {
		d.grid.Set(startCoord, GridData{c: TILE_SOUTH_WEST})
	} else if slices.Contains(directions, h.SOUTH) && slices.Contains(directions, h.EAST) {
		d.grid.Set(startCoord, GridData{c: TILE_SOUTH_EAST})
	} else {
		panic("Unreachable")
	}

	fmt.Println("New start coord value is", string(d.grid.Get(startCoord).c))
}

// IsEnclosed returns true if the path encloses |coord|.
// IsEnclosed uses a raycast algorithm to count the number of times the ray from the point of interest
// to the west crosses the path.
// Crossing the path means:
//   - hitting a vertical: |
//   - hitting a F---J (crosses from top to bottom, the horizontals are ignored)
//   - hitting a L---7 (crosses from bottom to top, the horizontals are ignored)
//
// These are not path crossings becaue they go back the same way
//   - F---7
//   - L---J
func (d *Day10) IsEnclosed(coord h.Coord) bool {
	//can't be enclosed if it's part of the loop
	if slices.Contains(d.path, coord) {
		return false
	}
	//ray cast to the left
	hitCount := 0
	lastHit := TILE_NONE
	for col := coord.Col - 1; col >= 0; col-- {
		testCoord := h.Coord{Row: coord.Row, Col: col}
		testCoordVal := d.grid.Get(testCoord).c

		if !slices.Contains(d.path, testCoord) {
			//can't be a hit if it's not on the path
			continue
		}

		//vertical case is easy
		if testCoordVal == TILE_VERTICAL {
			hitCount += 1
			continue
		}

		if lastHit == TILE_NONE {
			//looking to start another hit test if we get a corner
			if slices.Contains(CORNERS, testCoordVal) {
				//found a starting corner, so remember it
				lastHit = testCoordVal
				continue
			}
			if testCoordVal == TILE_NONE {
				//skip none tiles
				continue
			}
			//not a corner, not vertical, not None
			//cannot be anything else
			panic("unreachable")
		} else {
			//we already hit a corner, so go until we hit another one
			if slices.Contains(CORNERS, testCoordVal) {
				//if the corner is the opposite corner, then it counts as a hit
				if testCoordVal == OppositeTile(lastHit) {
					hitCount += 1
				} //else no hit
				//reset the lastHit and continue
				lastHit = TILE_NONE
				continue
			}
			if testCoordVal == TILE_HORIZONTAL {
				//ignore horizontal tiles between corners
				continue
			}
			//not a corner, not horizontal
			//cannot be anything else
			panic("unreachable")
		}
		// panic("unreachable")
	}
	//if we have an odd number of hits, it is enclosed.
	return (hitCount % 2) == 1
}

func (d *Day10) Part2() {
	fmt.Println("Part 2")
	d.Part1()
	d.ReplaceStartInGrid()

	enclosedCount := 0

	walker := func(c h.Coord) {
		if d.IsEnclosed(c) {
			enclosedCount += 1
		}
	}
	d.grid.Walk(walker)
	fmt.Println("Enclosed tiles", enclosedCount)

}
