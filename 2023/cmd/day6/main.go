package main

import (
	h "aoc2023/internal/helpers"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {

	d := &Day6{}

	err := h.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

func RaceDistance(raceLength int, holdTime int) int {
	return holdTime * (raceLength - holdTime)
}

func WaysToWin(raceLength int, record int) int {
	winWays := 0
	for i := 0; i < raceLength; i++ {
		dist := RaceDistance(raceLength, i)
		if dist > record {
			winWays += 1
		}
	}
	return winWays
}

type Day6 struct {
	lines     []string
	times     []int
	distances []int
}

func (d *Day6) Setup(filename string) {
	fmt.Println("Setup")
	d.lines = h.ReadFileToLines(filename)

	d.times = h.ParseIntList(strings.Split(d.lines[0], ":")[1], " ")
	d.distances = h.ParseIntList(strings.Split(d.lines[1], ":")[1], " ")

	fmt.Println("Times:", d.times)
	fmt.Println("DIstances:", d.distances)
}

func (d *Day6) Part1() {
	fmt.Println("Part 1")
	waysProd := 1
	for index := 0; index < len(d.times); index++ {
		raceLength := d.times[index]
		record := d.distances[index]
		winWays := WaysToWin(raceLength, record)
		fmt.Println("WinWays", winWays)
		waysProd *= winWays
	}
	fmt.Println("WinWays product", waysProd)
}

func CombineVals(input string) int {
	output := ""
	for _, c := range input {
		if c >= '0' && c <= '9' {
			output += string(c)
		}
	}
	intVal, err := strconv.Atoi(output)
	h.Assert(err == nil, "error not nil")
	return intVal
}

func (d *Day6) Part2() {
	fmt.Println("Part 2")
	raceLength := CombineVals(d.lines[0])
	record := CombineVals(d.lines[1])
	fmt.Println("raceLength", raceLength)
	fmt.Println("record", record)

	winWays := WaysToWin(raceLength, record)
	fmt.Println("WinWays", winWays)
}
