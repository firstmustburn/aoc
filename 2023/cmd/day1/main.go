package main

import (
	"aoc2023/internal/helpers"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {

	d := &Day1{}

	err := helpers.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

type Day1 struct {
}

func (d *Day1) Part1(filename string) error {

	lines := helpers.ReadFileToLines(filename)

	calibrations := make([]int, 0, len(lines))

	for _, line := range lines {
		calibration := ""

		for _, c := range line {
			if c >= '0' && c <= '9' {
				calibration += string(c)
				break
			}
		}
		for index := len(line) - 1; index >= 0; index-- {
			if line[index] >= '0' && line[index] <= '9' {
				calibration += string(line[index])
				break
			}
		}

		calibrationInt, err := strconv.Atoi(calibration)
		if err != nil {
			return fmt.Errorf("String conversion failed for %s: %w", calibration, err)
		}

		calibrations = append(calibrations, calibrationInt)
	}

	sum := 0

	fmt.Println("Calibrations")
	for index, calibration := range calibrations {
		fmt.Printf("%s -> %d\n", lines[index], calibration)
		sum += calibration
	}

	fmt.Println("Sum of calibrations is", sum)
	return nil
}

var numberStrings = []string{
	"one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
}

// peelNumber finds the first numeric or text string match in the string and returns that as an int
// along with the remainder of the string
func peelNumber(sin string) (string, int) {
	if len(sin) == 0 {
		//halting condition for recursion -- we didn't find any match after consuming the string
		return "", 0
	}

	if sin[0] >= '1' && sin[0] <= '9' {
		//found a number match
		numStr := string(sin[0])
		numVal, err := strconv.Atoi(numStr)
		if err != nil {
			panic(fmt.Sprintf("String conversion failed for %s: %s", numStr, err))
		}
		return sin[1:], numVal
	}
	for index, numStr := range numberStrings {
		if strings.HasPrefix(sin, numStr) {
			//found a number string match
			numVal := index + 1
			//still only peel the first character off in case the others are used in a number?
			return sin[1:], numVal
		}
	}
	//the first character is not part of a number string and is not a number, so just discard it
	//this recursive call is lazy but the strings are not that long
	return peelNumber(sin[1:])
}

func peelNumbers(sin string) []int {
	numbers := make([]int, 0)
	remaining := sin
	for len(remaining) > 0 {
		var numVal int
		remaining, numVal = peelNumber(remaining)
		if numVal > 0 {
			numbers = append(numbers, numVal)
		}
	}
	return numbers
}

func (d *Day1) Part2(filename string) error {
	lines := helpers.ReadFileToLines(filename)

	sum := 0
	for _, line := range lines {

		numbers := peelNumbers(line)
		calibration := numbers[0]*10 + numbers[len(numbers)-1]
		fmt.Printf("%s -> %d\n", line, calibration)
		sum += calibration
		fmt.Printf("running sum: %d", sum)
	}

	fmt.Println("Sum of calibrations is", sum)
	return nil
}
