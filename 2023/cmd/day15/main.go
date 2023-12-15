package main

import (
	h "aoc2023/internal/helpers"
	"fmt"
	"log/slog"
	"os"
	"regexp"
	"slices"
	"strconv"
	"strings"
)

func main() {

	var programLevel = new(slog.LevelVar) // Info by default
	handler := &slog.HandlerOptions{
		Level: programLevel,
		ReplaceAttr: func(groups []string, a slog.Attr) slog.Attr {
			// Remove time from the output for predictable test output.
			if a.Key == slog.TimeKey {
				return slog.Attr{}
			}
			// Remove the level output
			if a.Key == slog.LevelKey {
				return slog.Attr{}
			}

			return a
		},
	}
	logger := slog.New(slog.NewTextHandler(os.Stdout, handler))
	slog.SetDefault(logger)
	// programLevel.Set(slog.LevelInfo)
	programLevel.Set(slog.LevelWarn)

	var err error

	// f, err := os.Create("day15.prof")
	// if err != nil {
	// 	panic(err)
	// }
	// pprof.StartCPUProfile(f)
	// defer pprof.StopCPUProfile()

	d := &Day15{}

	err = h.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

type Day15 struct {
	lines []string
}

func hash(input string) int {
	value := 0
	for _, c := range input {
		value += int(c)
		value = value * 17
		value = value % 256
	}
	return value
}

func (d *Day15) Setup(filename string) {
	fmt.Println("Setup")
	d.lines = h.ReadFileToLines(filename)
}

func (d *Day15) Part1() {
	fmt.Println("Part 1")
	fmt.Println("hash(HASH)=", hash("HASH"))

	tokens := strings.Split(d.lines[0], ",")
	hashSum := 0
	for _, token := range tokens {
		h := hash(token)
		fmt.Printf("hash(%s)=%d\n", token, h)
		hashSum += h
	}
	fmt.Println("hash Sum", hashSum)

}

type Lens struct {
	Label       string
	FocalLength int
}

type Box struct {
	Lenses []Lens
}

func (b *Box) AddLens(newLens Lens) {
	currentInd := slices.IndexFunc(b.Lenses, func(l Lens) bool { return l.Label == newLens.Label })
	if currentInd == -1 {
		//add to the end
		b.Lenses = append(b.Lenses, newLens)
	} else {
		b.Lenses[currentInd] = newLens
	}
}

func (b *Box) RemoveLens(lensLabel string) {
	currentInd := slices.IndexFunc(b.Lenses, func(l Lens) bool { return l.Label == lensLabel })
	if currentInd == -1 {
		//do nothing
	} else {
		//collapse the slice
		b.Lenses = append(b.Lenses[:currentInd], b.Lenses[currentInd+1:]...)
	}
}

func DumpBoxes(boxes []Box) {
	for index, box := range boxes {
		if len(box.Lenses) == 0 {
			continue
		}
		fmt.Printf("Box %d: %v\n", index, box.Lenses)
	}
}

func (d *Day15) Part2() {
	fmt.Println("Part 2")

	//initialize the boxes
	boxes := make([]Box, 256)

	re := regexp.MustCompile(`([a-z]+)(=|-)([0-9]?)`)

	for _, token := range strings.Split(d.lines[0], ",") {
		// fmt.Printf("'%s', %v\n", token, re.FindStringSubmatch(token))
		matches := re.FindStringSubmatch(token)
		label := matches[1]
		boxIndex := hash(matches[1])
		if matches[2] == "=" {
			//add the lens
			focalLength, err := strconv.Atoi(matches[3])
			h.Assert(err == nil, "focal length conversion error")
			newLens := Lens{label, focalLength}
			boxes[boxIndex].AddLens(newLens)
		} else if matches[2] == "-" {
			//remove the lense
			boxes[boxIndex].RemoveLens(label)
		} else {
			panic("unhandled")
		}
		// fmt.Println("token", token)
		// DumpBoxes(boxes)
		// fmt.Println("-----------------")
	}

	// To confirm that all of the lenses are installed correctly, add up the focusing power of all
	// of the lenses. The focusing power of a single lens is the result of multiplying together:

	// One plus the box number of the lens in question.
	// The slot number of the lens within the box: 1 for the first lens, 2 for the second lens, and
	// so on.
	// The focal length of the lens.
	totalPower := 0
	for boxIndex, box := range boxes {
		for lensIndex, lens := range box.Lenses {
			power := (boxIndex + 1) * (lensIndex + 1) * lens.FocalLength
			totalPower += power
		}
	}
	fmt.Println("Total power", totalPower)

}
