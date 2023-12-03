package main

import (
	"aoc2023/internal/helpers"
	"fmt"
	"os"
	"strings"
)

func main() {

	d := &Day2{}

	err := helpers.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

type ColorSet struct {
	Red   int
	Blue  int
	Green int
}

func (t ColorSet) IsPossible(red int, green int, blue int) bool {
	return t.Red <= red && t.Blue <= blue && t.Green <= green
}

func (t *ColorSet) Parse(input string) {
	colorTokens := strings.Split(input, ",")

	//assign colors for each token
	for _, token := range colorTokens {
		colorNum, colorLabel := helpers.ParseLabeledValue(strings.TrimSpace(token), true)
		if colorLabel == "red" {
			t.Red = colorNum
		} else if colorLabel == "blue" {
			t.Blue = colorNum
		} else if colorLabel == "green" {
			t.Green = colorNum
		} else {
			panic(fmt.Sprintf("Unrecognized color %s", colorLabel))
		}
	}
}

type Game struct {
	ID    int
	Tries []ColorSet
}

func (g Game) IsPossible(red int, green int, blue int) bool {
	for _, try := range g.Tries {
		if !try.IsPossible(red, green, blue) {
			return false
		}
	}
	return true
}

func (g Game) GetMinColorSet() ColorSet {
	minSet := ColorSet{
		Red:   0,
		Green: 0,
		Blue:  0,
	}

	//the minset is the smallest set of cubes that contains all the observed values, so we're actually
	//looking for the max of each value
	for _, try := range g.Tries {
		minSet.Red = max(try.Red, minSet.Red)
		minSet.Green = max(try.Green, minSet.Green)
		minSet.Blue = max(try.Blue, minSet.Blue)
	}

	return minSet
}

func (g *Game) Parse(input string) {
	gameTokens := strings.Split(input, ":")
	helpers.Assert(len(gameTokens) == 2, "token length != 2")

	//get the ID
	gameID, gameStr := helpers.ParseLabeledValue(strings.TrimSpace(gameTokens[0]), false)
	helpers.Assert(gameStr == "Game", "Expected Game label")
	g.ID = gameID

	//process the remainder as tries
	tryTokens := strings.Split(gameTokens[1], ";")
	for _, tryToken := range tryTokens {
		try := ColorSet{}
		try.Parse(tryToken)
		g.Tries = append(g.Tries, try)
	}
}

type Day2 struct {
}

func (d *Day2) Part1(filename string) error {

	lines := helpers.ReadFileToLines(filename)

	possibleRed := 12
	possibleGreen := 13
	possibleBlue := 14
	possibleSum := 0

	for _, line := range lines {
		game := Game{}
		game.Parse(line)
		fmt.Printf("%#v\n", game)

		if game.IsPossible(possibleRed, possibleGreen, possibleBlue) {
			possibleSum += game.ID
			fmt.Printf("  IS possible\n")
		} else {
			fmt.Printf("  NOT possible\n")
		}
	}

	fmt.Println("Possible sum is", possibleSum)

	return nil
}

func (d *Day2) Part2(filename string) error {

	lines := helpers.ReadFileToLines(filename)

	powerSum := 0

	for _, line := range lines {
		game := Game{}
		game.Parse(line)
		fmt.Printf("game %#v\n", game)

		minSet := game.GetMinColorSet()
		fmt.Printf("  minset %#v\n", minSet)

		power := minSet.Red * minSet.Blue * minSet.Green
		fmt.Printf("  power %d\n", power)

		powerSum += power
	}

	fmt.Println("Power sum is", powerSum)

	return nil
}
