package main

import (
	h "aoc2023/internal/helpers"
	"fmt"
	"os"
)

func main() {

	d := &Day9{}

	err := h.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

type Day9 struct {
	lines     []string
	sequences [][]int
}

func (d *Day9) Setup(filename string) {
	fmt.Println("Setup")
	d.lines = h.ReadFileToLines(filename)

	for _, line := range d.lines {
		d.sequences = append(d.sequences, h.ParseIntList(line, " "))
	}
}

func IsZero(seq []int) bool {
	for _, s := range seq {
		if s != 0 {
			return false
		}
	}
	return true
}

func ExtrapNext(seq []int) int {
	if IsZero(seq) {
		return 0
	}
	differences := make([]int, 0, len(seq)-1)
	for index := 0; index < len(seq)-1; index++ {
		difference := seq[index+1] - seq[index]
		differences = append(differences, difference)
	}
	//extraplolate the differences
	nextDifference := ExtrapNext(differences)
	return seq[len(seq)-1] + nextDifference
}

func (d *Day9) Part1() {
	fmt.Println("Part 1")
	// fmt.Println(d.sequences)
	seqSum := 0
	for _, seq := range d.sequences {
		nextVal := ExtrapNext(seq)
		fmt.Println("nextVal", nextVal)
		seqSum += nextVal
	}
	fmt.Println("Sequence sum is", seqSum)
}

func ExtrapPrev(seq []int) int {
	if IsZero(seq) {
		return 0
	}
	differences := make([]int, 0, len(seq)-1)
	for index := 0; index < len(seq)-1; index++ {
		difference := seq[index+1] - seq[index]
		differences = append(differences, difference)
	}
	//extraplolate the differences
	nextDifference := ExtrapPrev(differences)
	return seq[0] - nextDifference
}

func (d *Day9) Part2() {
	fmt.Println("Part 2")
	// fmt.Println(d.sequences)
	seqSum := 0
	for _, seq := range d.sequences {
		nextVal := ExtrapPrev(seq)
		fmt.Println("nextVal", nextVal)
		seqSum += nextVal
	}
	fmt.Println("Sequence sum is", seqSum)
}
