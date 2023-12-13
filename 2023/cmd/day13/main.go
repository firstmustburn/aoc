package main

import (
	h "aoc2023/internal/helpers"
	"fmt"
	"log/slog"
	"os"
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

	// f, err := os.Create("day13.prof")
	// if err != nil {
	// 	panic(err)
	// }
	// pprof.StartCPUProfile(f)
	// defer pprof.StopCPUProfile()

	d := &Day13{}

	err = h.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

type Pattern struct {
	Data []string
}

func (p Pattern) Dump() {
	fmt.Println("-----------------")
	for _, d := range p.Data {
		fmt.Println(d)
	}
	fmt.Println("-----------------")
}

func (p Pattern) Rows() int {
	return len(p.Data)
}

func (p Pattern) Cols() int {
	return len(p.Data[0])
}

func (p Pattern) Transpose() Pattern {
	newData := make([]string, p.Cols())
	for row := 0; row < p.Rows(); row++ {
		for col := 0; col < p.Cols(); col++ {
			newData[col] += string(p.Data[row][col])
		}
	}
	return Pattern{newData}
}

func (p Pattern) CheckMirrorLine(index int) bool {
	checkCount := min(index+1, len(p.Data)-index-1)
	//skip 0 because we already checked it to get here
	for offset := 1; offset < checkCount; offset++ {
		if p.Data[index-offset] != p.Data[index+1+offset] {
			return false
		}
	}
	return true
}

func (p Pattern) GetMirrorLine() int {
	for index := 0; index < len(p.Data)-1; index++ {
		if p.Data[index] == p.Data[index+1] {
			isMirror := p.CheckMirrorLine(index)
			if isMirror {
				return index
			}
		}
	}
	return -1
}

func DiffCount(s1 string, s2 string) int {
	count := 0
	for i := range s1 {
		if s1[i] != s2[i] {
			count += 1
		}
	}
	return count
}

func (p Pattern) CheckSmudgeMirrorLine(index int) bool {
	checkCount := min(index+1, len(p.Data)-index-1)

	totalDiff := 0

	for offset := 0; offset < checkCount; offset++ {
		totalDiff += DiffCount(p.Data[index-offset], p.Data[index+1+offset])
	}
	return totalDiff == 1
}

func (p Pattern) GetSmudgeMirrorLine() int {
	for index := 0; index < len(p.Data)-1; index++ {
		diffCount := DiffCount(p.Data[index], p.Data[index+1])
		if diffCount == 0 || diffCount == 1 {
			isMirror := p.CheckSmudgeMirrorLine(index)
			if isMirror {
				return index
			}
		}
	}
	return -1
}

type Day13 struct {
	lines    []string
	patterns []Pattern
}

func (d *Day13) Setup(filename string) {
	fmt.Println("Setup")
	d.lines = h.ReadFileToLines(filename)

	currentPattern := Pattern{}
	for _, line := range d.lines {
		if len(line) == 0 {
			d.patterns = append(d.patterns, currentPattern)
			currentPattern = Pattern{}
		} else {
			currentPattern.Data = append(currentPattern.Data, line)
		}
	}
	d.patterns = append(d.patterns, currentPattern)

}

func (d *Day13) Part1() {
	fmt.Println("Part 1")
	rowSum := 0
	colSum := 0

	for _, pattern := range d.patterns {
		rowInd := pattern.GetMirrorLine()
		if rowInd != -1 {
			//found a mirror
			rowSum += rowInd + 1
		} else {
			//no row mirror so try column
			colPattern := pattern.Transpose()
			colPattern.Dump()
			colInd := colPattern.GetMirrorLine()
			if colInd == -1 {
				pattern.Dump()
				colPattern.Dump()
				panic("no row or column mirror found")
			}
			colSum += colInd + 1
		}
	}
	fmt.Println("rowSum", rowSum)
	fmt.Println("colSum", colSum)
	fmt.Println("result", rowSum*100+colSum)
}

func (d *Day13) Part2() {
	fmt.Println("Part 2")
	rowSum := 0
	colSum := 0

	for _, pattern := range d.patterns {
		rowInd := pattern.GetSmudgeMirrorLine()
		if rowInd != -1 {
			//found a mirror
			rowSum += rowInd + 1
		} else {
			//no row mirror so try column
			colPattern := pattern.Transpose()
			colPattern.Dump()
			colInd := colPattern.GetSmudgeMirrorLine()
			if colInd == -1 {
				pattern.Dump()
				colPattern.Dump()
				panic("no row or column mirror found")
			}
			colSum += colInd + 1
		}
	}
	fmt.Println("rowSum", rowSum)
	fmt.Println("colSum", colSum)
	fmt.Println("result", rowSum*100+colSum)
}
