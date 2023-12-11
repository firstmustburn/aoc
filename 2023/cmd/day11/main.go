package main

import (
	h "aoc2023/internal/helpers"
	"fmt"
	"os"
	"slices"
)

func main() {

	d := &Day11{}

	err := h.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

type GridData struct {
	value byte
}

type Day11 struct {
	lines     []string
	grid      *h.Grid[GridData]
	nullCoord h.Coord
}

func (d *Day11) DumpGrid() {
	walker := func(r int, c int, v GridData) {
		if c == 0 {
			fmt.Println("")
		}
		fmt.Printf("%s", string(v.value))
	}
	d.grid.WalkRCV(walker)
	fmt.Println("")
}

const TILE_GALAXY byte = '#'
const TILE_EMPTY byte = '.'

// func expandIntList(length int, insertLocations []int, valToInsert int) []int {
// 	result := make([]int, 0, length)
// 	for i := 0; i < length; i++ {
// 		result = append(result, i)
// 	}
// 	for insertInd, insertLoc := range insertLocations {
// 		actualInsertLoc := insertLoc + insertInd // because every time we do an insert, we expand the list
// 		result = append(result[:actualInsertLoc+1], result[actualInsertLoc:]...)
// 		result[actualInsertLoc] = valToInsert
// 	}

// 	fmt.Println("For length", length, "and inserts at", insertLocations)
// 	fmt.Println("Created list", result)
// 	return result
// }

func (d *Day11) GetEmptyRowsAndCols() ([]int, []int) {
	emptyRows := []int{}
	emptyCols := []int{}

	for r := 0; r < d.grid.Rows(); r++ {
		isEmpty := true
		for c := 0; c < d.grid.Cols(); c++ {
			if d.grid.GetRC(r, c).value == TILE_GALAXY {
				isEmpty = false
				break
			}
		}
		if isEmpty {
			emptyRows = append(emptyRows, r)
		}
	}

	for c := 0; c < d.grid.Cols(); c++ {
		isEmpty := true
		for r := 0; r < d.grid.Rows(); r++ {
			if d.grid.GetRC(r, c).value == TILE_GALAXY {
				isEmpty = false
				break
			}
		}
		if isEmpty {
			emptyCols = append(emptyCols, c)
		}
	}
	return emptyRows, emptyCols
}

// func (d *Day11) ExpandEmptyGrid() {

// 	emptyRows, emptyCols := d.GetEmptyRowsAndCols()

// 	//now make an expanded grid
// 	expandedRows := expandIntList(d.grid.Rows(), emptyRows, -1)
// 	expandedCols := expandIntList(d.grid.Cols(), emptyCols, -1)

// 	newGrid := h.CreateGrid[GridData](len(expandedRows), len(expandedCols))
// 	newGrid.Fill(GridData{TILE_EMPTY})

// 	for newRow, oldRow := range expandedRows {
// 		for newCol, oldCol := range expandedCols {
// 			if oldRow == -1 || oldCol == -1 {
// 				continue
// 			}
// 			newGrid.SetRC(newRow, newCol, d.grid.GetRC(oldRow, oldCol))
// 		}
// 	}

// 	d.grid = newGrid
// }

func GetEmptyValuesBetween(first int, last int, emptyList []int) int {
	count := 0
	//swap so we go in the increasing dir
	if first > last {
		temp := last
		last = first
		first = temp
	}
	for i := first + 1; i < last; i++ {
		if slices.Contains(emptyList, i) {
			count += 1
		}
	}
	return count
}

func (d *Day11) GetGalaxyDistances(emptyExpansionValue int) {

	emptyRows, emptyCols := d.GetEmptyRowsAndCols()

	galaxies := []h.Coord{}
	walker := func(coord h.Coord, d GridData) {
		if d.value == TILE_GALAXY {
			galaxies = append(galaxies, coord)
		}
	}
	d.grid.WalkV(walker)

	fmt.Printf("There are %d galaxies: %v\n", len(galaxies), galaxies)

	//iterate through galaxy pairs getting distances
	pairCount := 0
	totalDist := 0
	for i1 := 0; i1 < len(galaxies); i1++ {
		for i2 := i1 + 1; i2 < len(galaxies); i2++ {
			pairCount += 1
			g1 := galaxies[i1]
			g2 := galaxies[i2]
			emptyRowsCrossed := GetEmptyValuesBetween(g1.Row, g2.Row, emptyRows)
			emptyColsCrossed := GetEmptyValuesBetween(g1.Col, g2.Col, emptyCols)
			dist := h.AbsInt(g1.Row-g2.Row) + h.AbsInt(g1.Col-g2.Col) +
				(emptyColsCrossed+emptyRowsCrossed)*emptyExpansionValue
			totalDist += dist
			// fmt.Printf("G1 %v and G2 %v are %d apart\n", g1, g2, dist)
		}
	}
	fmt.Printf("distance for %d pairs is %d\n", pairCount, totalDist)

}

func (d *Day11) Setup(filename string) {
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

func (d *Day11) Part1() {
	fmt.Println("Part 1")
	d.DumpGrid()
	fmt.Println("*******************************************")
	// d.ExpandEmptyGrid()
	// d.DumpGrid()
	d.GetGalaxyDistances(1)
}

func (d *Day11) Part2() {
	fmt.Println("Part 2")
	d.DumpGrid()
	fmt.Println("*******************************************")
	// d.ExpandEmptyGrid()
	// d.DumpGrid()
	d.GetGalaxyDistances(999999)
}
