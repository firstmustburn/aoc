package helpers

import "fmt"

type Direction int

const NORTH Direction = 0
const NORTH_EAST Direction = 1
const EAST Direction = 2
const SOUTH_EAST Direction = 3
const SOUTH Direction = 4
const SOUTH_WEST Direction = 5
const WEST Direction = 6
const NORTH_WEST Direction = 7

type Coord struct {
	Row int
	Col int
}

// Opposite returns the direction opposite of this direction
func (d Direction) Opposite() Direction {
	if d == NORTH {
		return SOUTH
	} else if d == NORTH_EAST {
		return SOUTH_WEST
	} else if d == EAST {
		return WEST
	} else if d == SOUTH_EAST {
		return NORTH_WEST
	} else if d == SOUTH {
		return NORTH
	} else if d == SOUTH_WEST {
		return NORTH_EAST
	} else if d == WEST {
		return EAST
	} else if d == NORTH_WEST {
		return SOUTH_EAST
	} else {
		panic(fmt.Errorf("unknown direction %d", d))
	}
}

// GetDirection returns the direction you travel if you go from the |from| coord to the |to| coord
// panics if the two coords are identical
func GetDirection(from Coord, to Coord) Direction {

	if to.Row > from.Row {
		//larger to row = south
		if to.Col > from.Col {
			//larger to Col = east
			return SOUTH_EAST
		} else if to.Col < from.Col {
			//smaller to Col = west
			return SOUTH_WEST
		} else {
			//same col
			return SOUTH
		}
	} else if to.Row < from.Row {
		//smaller to row = north
		if to.Col > from.Col {
			//larger to Col = east
			return NORTH_EAST
		} else if to.Col < from.Col {
			//smaller to Col = west
			return NORTH_WEST
		} else {
			return NORTH
		}
	} else {
		//same row, so it has to be east or west
		if to.Col > from.Col {
			//larger to Col = east
			return EAST
		} else if to.Col < from.Col {
			//smaller to Col = west
			return WEST
		} else {
			//if they are the same row and column, they are the same coord
			panic("unreachable")
		}
	}
}

func (c Coord) Dir(dir Direction) Coord {
	if dir == NORTH {
		return c.N()
	} else if dir == NORTH_EAST {
		return c.NE()
	} else if dir == EAST {
		return c.E()
	} else if dir == SOUTH_EAST {
		return c.SE()
	} else if dir == SOUTH {
		return c.S()
	} else if dir == SOUTH_WEST {
		return c.SW()
	} else if dir == WEST {
		return c.W()
	} else if dir == NORTH_WEST {
		return c.NW()
	} else {
		panic(fmt.Errorf("unknown direction %d", dir))
	}
}

func (c Coord) N() Coord {
	return Coord{c.Row - 1, c.Col}
}

func (c Coord) NE() Coord {
	return Coord{c.Row - 1, c.Col + 1}
}

func (c Coord) E() Coord {
	return Coord{c.Row, c.Col + 1}
}

func (c Coord) SE() Coord {
	return Coord{c.Row + 1, c.Col + 1}
}

func (c Coord) S() Coord {
	return Coord{c.Row + 1, c.Col}
}

func (c Coord) SW() Coord {
	return Coord{c.Row + 1, c.Col - 1}
}

func (c Coord) W() Coord {
	return Coord{c.Row, c.Col - 1}
}

func (c Coord) NW() Coord {
	return Coord{c.Row - 1, c.Col - 1}
}

// Adjacent returns a list of adjacent coordinates in the clockwise direction
// if includeDiagonals is true, then diagonal corners are included and the list starts from NW
// if includeDiagonals is false, then diagonal coners are not included and list starts from N
func (c Coord) Adjacent(includeDiagonals bool) []Coord {
	if includeDiagonals {
		return []Coord{c.NW(), c.N(), c.NE(), c.E(), c.SE(), c.S(), c.SW(), c.W()}
	} else {
		return []Coord{c.N(), c.E(), c.S(), c.W()}
	}
}

// Left returns the adjacent coordinates to the left, including the diagonal ones, in clockwise order
func (c Coord) Left() []Coord {
	return []Coord{c.SW(), c.W(), c.NW()}
}

// Top returns the adjacent coordinates to the top, including the diagonal ones, in clockwise order
func (c Coord) Top() []Coord {
	return []Coord{c.NW(), c.N(), c.NE()}
}

// Right returns the adjacent coordinates to the right, including the diagonal ones, in clockwise order
func (c Coord) Right() []Coord {
	return []Coord{c.NE(), c.E(), c.SE()}
}

// Bottom returns the adjacent coordinates to the bottom, including the diagonal ones, in clockwise order
func (c Coord) Bottom() []Coord {
	return []Coord{c.SE(), c.S(), c.SW()}
}

type Region struct {
	upperLeft  Coord
	lowerRight Coord
}

// CreateRegion creates a region spanning the rectangular area defined by the two coordinates
// The two coordinates do not have to be in any particular order
func CreateRegion(c1 Coord, c2 Coord) Region {
	//convert the given coordinates into upper left and lower right using min and max over the
	//rows and columns
	return Region{
		upperLeft: Coord{
			Row: min(c1.Row, c2.Row),
			Col: min(c1.Col, c2.Col),
		},
		lowerRight: Coord{
			Row: max(c1.Row, c2.Row),
			Col: max(c1.Col, c2.Col),
		},
	}
}

func (r Region) UpperLeft() Coord {
	return r.upperLeft
}

func (r Region) UpperRight() Coord {
	//row of upperLeft, col of lowerRight
	return Coord{r.upperLeft.Row, r.lowerRight.Col}
}

func (r Region) LowerRight() Coord {
	return r.lowerRight
}

func (r Region) LowerLeft() Coord {
	//row of lowerRight, col of upperleft
	return Coord{r.lowerRight.Row, r.upperLeft.Col}
}

// Width returns the number of columns in the region
func (r Region) Width() int {
	return r.lowerRight.Col - r.upperLeft.Col + 1
}

// Height returns the number of rows in the region
func (r Region) Height() int {
	return r.lowerRight.Row - r.upperLeft.Row + 1
}

func (r Region) Walk(f func(Coord)) {
	for row := r.upperLeft.Row; row <= r.lowerRight.Row; row++ {
		for col := r.upperLeft.Col; col <= r.lowerRight.Col; col++ {
			f(Coord{row, col})
		}
	}
}

// Adjacent returns the coordinates that are adjacent to the region starting from the top left
// corner and going around clockwise.
// If includeDiagonals is true, the diagonal corners are included in the sequence, so the
// sequence will start with the top left diagonal corner.
func (r Region) Adjacent(includeDiagonals bool) []Coord {

	//if the diagOffset is set to 1, each side starts off back by one to include the
	//diagonal at the beginning fo that side. The end diagonal is picked up by the next side.
	diagOffset := 0
	if includeDiagonals {
		diagOffset = 1
	}

	adj := make([]Coord, 0, (r.Width()+r.Height())*2+(4*diagOffset))

	{
		//do the top row from left to right
		row := r.upperLeft.Row - 1
		for col := r.upperLeft.Col - diagOffset; col <= r.lowerRight.Col; col++ {
			adj = append(adj, Coord{row, col})
		}
	}
	{
		//do the right column from top to the bottom
		col := r.lowerRight.Col + 1
		for row := r.upperLeft.Row - diagOffset; row <= r.lowerRight.Row; row++ {
			adj = append(adj, Coord{row, col})
		}
	}
	{
		//do the bottom row from the right to the left
		row := r.lowerRight.Row + 1
		for col := r.lowerRight.Col + diagOffset; col >= r.upperLeft.Col; col-- {
			adj = append(adj, Coord{row, col})
		}
	}
	{
		//do the left column from bottom to top
		col := r.upperLeft.Col - 1
		for row := r.lowerRight.Row + diagOffset; row >= r.upperLeft.Row; row-- {
			adj = append(adj, Coord{row, col})
		}
	}
	return adj
}

func (r Region) ContainsCoord(c Coord) bool {
	return c.Row >= r.upperLeft.Row && c.Row <= r.lowerRight.Row &&
		c.Col >= r.upperLeft.Col && c.Col <= r.lowerRight.Col
}

func (r Region) ContainsRegion(other Region) bool {
	return other.upperLeft.Row >= r.upperLeft.Row &&
		other.upperLeft.Col >= r.upperLeft.Col &&
		other.lowerRight.Row <= r.lowerRight.Row &&
		other.lowerRight.Col <= r.lowerRight.Col
}

func (r Region) IntersectsRegion(other Region) bool {
	return r.upperLeft.Col < other.lowerRight.Col && r.lowerRight.Col > other.upperLeft.Col &&
		r.upperLeft.Row < other.lowerRight.Row && r.lowerRight.Row > other.upperLeft.Row
}

type Grid[V any] struct {
	data [][]V
	rows int
	cols int
}

func CreateGrid[V any](rows int, cols int) *Grid[V] {
	//initialize the data
	grid := Grid[V]{}
	grid.data = make([][]V, rows)
	for index := range grid.data {
		grid.data[index] = make([]V, cols)
	}
	grid.rows = rows
	grid.cols = cols
	return &grid
}

func (g Grid[V]) Rows() int {
	return g.rows
}

func (g Grid[V]) Cols() int {
	return g.cols
}

func (g Grid[V]) AsRegion() Region {
	return Region{Coord{0, 0}, Coord{g.rows - 1, g.cols - 1}}
}

func (g Grid[V]) Get(c Coord) V {
	return g.data[c.Row][c.Col]
}

func (g Grid[V]) GetRC(row int, col int) V {
	return g.data[row][col]
}

func (g Grid[V]) ContainsCoord(c Coord) bool {
	return c.Row >= 0 && c.Row < g.rows && c.Col >= 0 && c.Col < g.cols
}

// AdjacentToCoord returns a list of adjacent coordinates startingfrom the North orientation and
// proceeding clockwise, omitting any coordinates that are out of range for the grid
func (g Grid[V]) AdjacentToCoord(c Coord, includeDiagonals bool) []Coord {
	adj := []Coord{}
	//filter the full adjacent list from the coordinate
	for _, c := range c.Adjacent(includeDiagonals) {
		if g.ContainsCoord(c) {
			adj = append(adj, c)
		}
	}
	return adj
}

// AdjacentToRegion returns a list of adjacent coordinates starting from the top left corner and
// and omitting any coordinates that are out of range for the grid.
func (g Grid[V]) AdjacentToRegion(r Region, includeDiagonals bool) []Coord {
	adj := []Coord{}
	//filter the full adjacent list from the region
	for _, c := range r.Adjacent(includeDiagonals) {
		if g.ContainsCoord(c) {
			adj = append(adj, c)
		}
	}
	return adj
}

func (g *Grid[V]) Set(c Coord, newValue V) {
	g.data[c.Row][c.Col] = newValue
}

func (g *Grid[V]) SetRC(row int, col int, newValue V) {
	g.data[row][col] = newValue
}

func (g Grid[V]) Walk(f func(Coord)) {
	for row := 0; row < g.rows; row++ {
		for col := 0; col < g.cols; col++ {
			f(Coord{row, col})
		}
	}
}

func (g Grid[V]) WalkV(f func(Coord, V)) {
	for row := 0; row < g.rows; row++ {
		for col := 0; col < g.cols; col++ {
			f(Coord{row, col}, g.data[row][col])
		}
	}
}

func (g Grid[V]) WalkRC(f func(int, int)) {
	for row := 0; row < g.rows; row++ {
		for col := 0; col < g.cols; col++ {
			f(row, col)
		}
	}
}

func (g Grid[V]) WalkRCV(f func(int, int, V)) {
	for row := 0; row < g.rows; row++ {
		for col := 0; col < g.cols; col++ {
			f(row, col, g.data[row][col])
		}
	}
}
