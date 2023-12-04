package main

import (
	"aoc2023/internal/helpers"
	"fmt"
	"os"
)

func main() {

	d := &Day4{}

	err := helpers.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

type Day4 struct {
}

func (d *Day4) Setup(filename string) {
	fmt.Println("Setup")
}


func (d *Day4) Part1() {
    fmt.Println("Part 1")
}

func (d *Day4) Part2() {
    fmt.Println("Part 2")
}
