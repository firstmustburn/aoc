package main

import (
	h "aoc2023/internal/helpers"
	"fmt"
	"os"
	"strconv"
)

func main() {

	d := &Day3{}

	err := h.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

type Day3 struct {
	grid    *h.Grid[byte]
	numbers []NumberEntry
}

type NumberEntry struct {
	Location h.Region //location of the first digit
	Value    int
}

func (d Day3) findNumbers() []NumberEntry {
	numbers := make([]NumberEntry, 0)

	isNumberPending := false
	currentNumber := ""
	currentStartCol := 0

	addNumber := func(currentRow int) {
		parsedNumber, err := strconv.Atoi(currentNumber)
		if err != nil {
			panic(fmt.Sprintf("Failed to make a number out of %s: %s", currentNumber, err))
		}
		newNumber := NumberEntry{
			Location: h.CreateRegion(
				h.Coord{Row: currentRow, Col: currentStartCol},
				h.Coord{Row: currentRow, Col: currentStartCol + len(currentNumber) - 1}),
			Value: parsedNumber,
		}
		numbers = append(numbers, newNumber)
		//reset number tracking state
		isNumberPending = false
		currentNumber = ""
		currentStartCol = 0
	}

	for rowIndex := 0; rowIndex < d.grid.Rows(); rowIndex++ {
		for colIndex := 0; colIndex < d.grid.Cols(); colIndex++ {
			c := d.grid.GetRC(rowIndex, colIndex)
			if h.IsDigit(c) {
				//found a numeric digit
				if !isNumberPending {
					//start a new number
					currentStartCol = colIndex
					isNumberPending = true
				}
				//for both new and existing numbers, add the character to the number string
				currentNumber += string(c)
			} else {
				//not a numeric digit -- finish a pending number if there is one
				if isNumberPending {
					addNumber(rowIndex)
				}
			}
		}
		//end of the row, see if we have a pending number
		if isNumberPending {
			addNumber(rowIndex)
		}
	}

	return numbers
}

func IsSymbol(c byte) bool {
	//it's a symbol if it's not a digit and not a period
	isSymbol := !h.IsDigit(c) && c != '.'
	// fmt.Println("is symbol:", isSymbol)
	return isSymbol
}

func (d Day3) NumberHasSymbol(number NumberEntry) bool {
	//check the values around the number for symbols
	for _, coord := range d.grid.AdjacentToRegion(number.Location, true) {
		val := d.grid.Get(coord)
		if IsSymbol(val) {
			return true
		}
	}
	//no symbol in any adjacent cell
	return false
}

func (d Day3) NumbersAdjacent(symbolCoord h.Coord) []NumberEntry {
	adjNumbers := make([]NumberEntry, 0)

	//helper for addint numbers to adjNumbers while skipping duplicates
	var addNumberEntry = func(newEntry NumberEntry) {
		for _, existingNumber := range adjNumbers {
			if existingNumber.Location == newEntry.Location {
				//we already have this one, so don't add it
				return
			}
		}
		//not unique, so do add it
		adjNumbers = append(adjNumbers, newEntry)
	}

	//iterate through the cells around the symbol.  If those cells are contained by a number,
	//then add that number to the adjacent numbers list
	for _, coord := range d.grid.AdjacentToCoord(symbolCoord, true) {
		for _, number := range d.numbers {
			if number.Location.ContainsCoord(coord) {
				addNumberEntry(number)
				break
			}
		}
	}
	//print results
	if len(adjNumbers) > 0 {
		fmt.Printf("Numbers adjacent to %v are:\n", symbolCoord)
		for _, adjNumber := range adjNumbers {
			fmt.Printf("   %d\n", adjNumber.Value)
		}
	}

	return adjNumbers
}

func (d *Day3) Setup(filename string) {

	lines := h.ReadFileToLines(filename)
	rowCount := len(lines)
	colCount := len(lines[0])
	d.grid = h.CreateGrid[byte](rowCount, colCount)
	for row := 0; row < rowCount; row++ {
		for col := 0; col < colCount; col++ {
			d.grid.SetRC(row, col, lines[row][col])
		}
	}

	d.numbers = d.findNumbers()

}

func (d *Day3) Part1(filename string) error {

	d.Setup(filename)

	numberSum := 0

	for _, number := range d.numbers {
		fmt.Printf("%#v\n", number)
		if d.NumberHasSymbol(number) {
			numberSum += number.Value
			fmt.Println("  HAS symbol")
		} else {
			fmt.Println("  has NO symbol")
		}
	}

	fmt.Println("Number sum is", numberSum)

	return nil
}

func (d *Day3) Part2(filename string) error {

	d.Setup(filename)

	gearRatioSum := 0

	walker := func(row int, col int, c byte) {
		if c == '*' {
			adjNumbers := d.NumbersAdjacent(h.Coord{Row: row, Col: col})
			if len(adjNumbers) == 2 {
				gearRatio := adjNumbers[0].Value * adjNumbers[1].Value
				fmt.Printf("Found gear ratio for %d, %d:  %d\n", row, col, gearRatio)
				gearRatioSum += gearRatio
			}
		}
	}

	d.grid.WalkRCV(walker)

	fmt.Println("gear ratio sum is", gearRatioSum)

	return nil
}
