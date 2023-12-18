package helpers

type SparseGrid[V any] struct {
	data      map[Coord]*V
	minRow    int
	minCol    int
	maxRow    int
	maxCol    int
	boundsSet bool
}

func CreateSparseGrid[V any]() *SparseGrid[V] {
	//initialize the data
	grid := SparseGrid[V]{}
	grid.data = make(map[Coord]*V, 1000)
	grid.boundsSet = false
	return &grid
}

func (g SparseGrid[V]) Len() int {
	return len(g.data)
}

func (g SparseGrid[V]) Rows() int {
	Assert(g.boundsSet, "bounds not set")
	return g.maxRow - g.minRow + 1
}

func (g SparseGrid[V]) MinRow() int {
	Assert(g.boundsSet, "bounds not set")
	return g.minRow
}

func (g SparseGrid[V]) MaxRow() int {
	Assert(g.boundsSet, "bounds not set")
	return g.maxRow
}

func (g SparseGrid[V]) Cols() int {
	Assert(g.boundsSet, "bounds not set")
	return g.maxCol - g.minCol + 1
}

func (g SparseGrid[V]) MinCol() int {
	Assert(g.boundsSet, "bounds not set")
	return g.minCol
}

func (g SparseGrid[V]) MaxCol() int {
	Assert(g.boundsSet, "bounds not set")
	return g.maxCol
}

func (g SparseGrid[V]) Get(c Coord) *V {
	return g.data[c]
}

func (g SparseGrid[V]) GetRC(row int, col int) *V {
	return g.Get(Coord{row, col})
}

func (g SparseGrid[V]) IsSet(c Coord) bool {
	_, ok := g.data[c]
	return ok
}

// func (g SparseGrid[V]) IsInBounds(c Coord) bool {
//     Assert(g.boundsSet, "bounds not set")

// 	return c.Row >= 0 && c.Row < g.rows && c.Col >= 0 && c.Col < g.cols
// }

func (g *SparseGrid[V]) updateBounds(c Coord) {
	if !g.boundsSet {
		//first call to set bounds
		g.minCol = c.Col
		g.maxCol = c.Col
		g.minRow = c.Row
		g.maxRow = c.Row
		g.boundsSet = true
	} else {
		g.minRow = min(g.minRow, c.Row)
		g.maxRow = max(g.maxRow, c.Row)
		g.minCol = min(g.minCol, c.Col)
		g.maxCol = max(g.maxCol, c.Col)
	}
}

func (g *SparseGrid[V]) Set(c Coord, newValue *V) {
	g.updateBounds(c)
	g.data[c] = newValue
}

// func (g SparseGrid[V]) Walk(f func(Coord)) {
// 	for row := 0; row < g.rows; row++ {
// 		for col := 0; col < g.cols; col++ {
// 			f(Coord{row, col})
// 		}
// 	}
// }

// func (g SparseGrid[V]) WalkV(f func(Coord, V)) {
// 	for row := 0; row < g.rows; row++ {
// 		for col := 0; col < g.cols; col++ {
// 			f(Coord{row, col}, g.data[row][col])
// 		}
// 	}
// }

// func (g SparseGrid[V]) WalkRC(f func(int, int)) {
// 	for row := 0; row < g.rows; row++ {
// 		for col := 0; col < g.cols; col++ {
// 			f(row, col)
// 		}
// 	}
// }

// func (g SparseGrid[V]) WalkRCV(f func(int, int, V)) {
// 	for row := 0; row < g.rows; row++ {
// 		for col := 0; col < g.cols; col++ {
// 			f(row, col, g.data[row][col])
// 		}
// 	}
// }

// func (g SparseGrid[V]) WalkRCVFrom(f func(int, int, V), dir Direction) {
// 	walker := func(coord Coord, value V) {
// 		f(coord.Row, coord.Col, value)
// 	}
// 	g.WalkVFrom(walker, dir)
// }

// func (g SparseGrid[V]) WalkVFrom(f func(Coord, V), dir Direction) {
// 	if dir == NORTH {
// 		for row := 0; row < g.rows; row++ {
// 			for col := 0; col < g.cols; col++ {
// 				f(Coord{row, col}, g.data[row][col])
// 			}
// 		}
// 	} else if dir == SOUTH {
// 		for row := g.rows - 1; row >= 0; row-- {
// 			for col := 0; col < g.cols; col++ {
// 				f(Coord{row, col}, g.data[row][col])
// 			}
// 		}
// 	} else if dir == WEST {
// 		for col := 0; col < g.cols; col++ {
// 			for row := 0; row < g.rows; row++ {
// 				f(Coord{row, col}, g.data[row][col])
// 			}
// 		}
// 	} else if dir == EAST {
// 		for col := g.cols - 1; col >= 0; col-- {
// 			for row := 0; row < g.rows; row++ {
// 				f(Coord{row, col}, g.data[row][col])
// 			}
// 		}
// 	} else {
// 		panic("unhandled direction")
// 	}
// }
