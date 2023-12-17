package main

import (
	h "aoc2023/internal/helpers"
	"fmt"
	"log/slog"
	"math"
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

	// f, err := os.Create("day17.prof")
	// if err != nil {
	// 	panic(err)
	// }
	// pprof.StartCPUProfile(f)
	// defer pprof.StopCPUProfile()

	d := &Day17{}

	err = h.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

func (d *Day17) DumpGridValue() {
	walker := func(r int, c int, v GridData) {
		if c == 0 {
			fmt.Println("")
		}
		fmt.Printf("%d", v.HeatLoss)
	}
	d.grid.WalkRCV(walker)
	fmt.Println("")
}

type Day17 struct {
	lines     []string
	grid      *h.Grid[GridData]
	nullCoord h.Coord
	isPart1   bool
}

func (d *Day17) Setup(filename string) {
	fmt.Println("Setup")
	d.lines = h.ReadFileToLines(filename)

	rows := len(d.lines)
	cols := len(d.lines[0])
	d.grid = h.CreateGrid[GridData](rows, cols)

	//fill the grid
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			d.grid.SetRC(
				r,
				c,
				MakeGridData(h.StrToInt(string(d.lines[r][c]))),
			)
		}
	}

	//the nullCoord is outside the grid
	d.nullCoord = h.Coord{Row: rows * 2, Col: cols * 2}

}

type VisitState struct {
	Direction      h.Direction
	StraightLength int
}

type GridData struct {
	HeatLoss int
	Costs    map[VisitState]int
	Visited  map[VisitState]bool
}

// UpdateCosts returns True if the data changed
func (gd *GridData) UpdateCosts(newWeight int, visitState VisitState) bool {
	currentWeight, ok := gd.Costs[visitState]
	if ok {
		//compare the current weight to the new weight and use the smaller
		if newWeight < currentWeight {
			gd.Costs[visitState] = newWeight
			return true
		} else {
			return false
		}
	} else {
		//no entry, so treat the current value as MAX and assign the new weight
		gd.Costs[visitState] = newWeight
		return true
	}
}
func (gd GridData) IsVisited(visitState VisitState) bool {
	isVisited, ok := gd.Visited[visitState]
	if ok {
		return isVisited
	}
	return false
}
func (gd *GridData) SetVisited(visitState VisitState) {
	gd.Visited[visitState] = true
}

func MakeGridData(heatLoss int) GridData {
	return GridData{
		HeatLoss: heatLoss,
		Costs:    make(map[VisitState]int),
		Visited:  make(map[VisitState]bool),
	}
}

func (d *Day17) UnvisitedNeighborsP1(node h.Coord, visitState VisitState) ([]h.Coord, []VisitState) {
	neighborCoords := make([]h.Coord, 0, 3)
	visitStates := make([]VisitState, 0, 3)
	{
		//add the left turn if it is in the grid and the neighbor is unvisited
		neighborCoord := node.Dir(visitState.Direction.Left())
		if d.grid.ContainsCoord(neighborCoord) {
			newVisitState := VisitState{
				Direction:      visitState.Direction.Left(),
				StraightLength: 1,
			}
			if !d.grid.Get(neighborCoord).IsVisited(newVisitState) {
				neighborCoords = append(neighborCoords, neighborCoord)
				visitStates = append(visitStates, newVisitState)
			}
		}
	}

	// add goint straight if we have less then 3 in our current dirction, it is in the grid and
	// the neighbor is unvisited
	if visitState.StraightLength < 3 {
		neighborCoord := node.Dir(visitState.Direction)
		if d.grid.ContainsCoord(neighborCoord) {
			newVisitState := VisitState{
				Direction:      visitState.Direction,
				StraightLength: visitState.StraightLength + 1,
			}
			if !d.grid.Get(neighborCoord).IsVisited(newVisitState) {
				neighborCoords = append(neighborCoords, neighborCoord)
				visitStates = append(visitStates, newVisitState)
			}
		}
	}
	{
		//add the right turn if it is in the grid and the neighbor is unvisited
		neighborCoord := node.Dir(visitState.Direction.Right())
		if d.grid.ContainsCoord(neighborCoord) {
			newVisitState := VisitState{
				Direction:      visitState.Direction.Right(),
				StraightLength: 1,
			}
			if !d.grid.Get(neighborCoord).IsVisited(newVisitState) {
				neighborCoords = append(neighborCoords, neighborCoord)
				visitStates = append(visitStates, newVisitState)
			}
		}
	}
	return neighborCoords, visitStates
}

func (d *Day17) VisitNode(nodeCoord h.Coord, visitState VisitState) {
	// if nodeCoord.Row == 4 && nodeCoord.Col == 7 {
	// 	fmt.Println("break")
	// }
	node := d.grid.GetPtr(nodeCoord)
	nodeCost, ok := node.Costs[visitState]
	h.Assert(ok, "no previously assigned cost for the node")

	var neighborCoords []h.Coord
	var neighborVisitStates []VisitState
	if d.isPart1 {
		neighborCoords, neighborVisitStates = d.UnvisitedNeighborsP1(nodeCoord, visitState)
	} else {
		neighborCoords, neighborVisitStates = d.UnvisitedNeighborsP2(nodeCoord, visitState)
	}
	for nInd := range neighborCoords {
		neighborNode := d.grid.GetPtr(neighborCoords[nInd])
		neighborNode.UpdateCosts(nodeCost+node.HeatLoss, neighborVisitStates[nInd])
	}
	//mark this node as visited
	node.SetVisited(visitState)
}

// Dijkstra's algorithm considering the VisitState we enter the node as a different graph node
func (d *Day17) FindMinPath() {
	startCoord := h.Coord{Row: 0, Col: 0}
	endCoord := h.Coord{Row: d.grid.Rows() - 1, Col: d.grid.Cols() - 1}

	//seed the algorithm by setting 0 weights on the points adjacent to the start point
	startDirs := []h.Direction{h.EAST, h.SOUTH}
	//first set up the cost in this direction on the node
	for _, startDir := range startDirs {
		coord := startCoord.Dir(startDir)
		visitState := VisitState{startDir, 1}
		d.grid.GetPtr(coord).UpdateCosts(0, visitState)
	}

	visitCount := 0
	for {
		minCost := math.MaxInt
		minCoord := d.nullCoord
		minVisitState := VisitState{}
		found := false
		//find the smallest unvisited node and visit it
		walker := func(coord h.Coord, data GridData) {
			for visitState, visitCost := range data.Costs {
				if visitCost < minCost && !data.IsVisited(visitState) {
					minCost = visitCost
					minCoord = coord
					minVisitState = visitState
					found = true
				}
			}
		}
		d.grid.WalkV(walker)
		h.Assert(found, "no path to end node")

		//check for end state
		if d.isPart1 {
			//the end state is any time we reach the endCoord
			if minCoord == endCoord {
				fmt.Printf("Reached the end coordinate %v via visitState %v with cost %d\n",
					minCoord, minVisitState, minCost+d.grid.Get(endCoord).HeatLoss)
				break
			}
		} else {
			//the end state is any time we reach the endCoord with a visitState length of >=4
			if minCoord == endCoord && minVisitState.StraightLength >= 4 {
				fmt.Printf("Reached the end coordinate %v via visitState %v with cost %d\n",
					minCoord, minVisitState, minCost+d.grid.Get(endCoord).HeatLoss)
				break
			}

		}

		d.VisitNode(minCoord, minVisitState)
		visitCount += 1
		if visitCount%10000 == 0 {
			fmt.Println("Visits: ", visitCount)
			fmt.Printf("Visited %#v at %#v with cost %d\n", minCoord, minVisitState, d.grid.Get(minCoord).Costs[minVisitState])
		}
	}
}

func (d *Day17) Part1() {
	d.isPart1 = true
	fmt.Println("Part 1")
	// d.DumpGridValue()
	d.FindMinPath()
}

func (d *Day17) UnvisitedNeighborsP2(node h.Coord, visitState VisitState) ([]h.Coord, []VisitState) {
	neighborCoords := make([]h.Coord, 0, 3)
	visitStates := make([]VisitState, 0, 3)

	// add goint straight if we have less then 10 in our current direction, it is in the grid and
	// the neighbor is unvisited
	if visitState.StraightLength < 10 {
		neighborCoord := node.Dir(visitState.Direction)
		if d.grid.ContainsCoord(neighborCoord) {
			newVisitState := VisitState{
				Direction:      visitState.Direction,
				StraightLength: visitState.StraightLength + 1,
			}
			if !d.grid.Get(neighborCoord).IsVisited(newVisitState) {
				neighborCoords = append(neighborCoords, neighborCoord)
				visitStates = append(visitStates, newVisitState)
			}
		}
	}

	//add turns if we've traveled at least 4
	if visitState.StraightLength >= 4 {
		{
			//add the left turn if it is in the grid and the neighbor is unvisited
			neighborCoord := node.Dir(visitState.Direction.Left())
			if d.grid.ContainsCoord(neighborCoord) {
				newVisitState := VisitState{
					Direction:      visitState.Direction.Left(),
					StraightLength: 1,
				}
				if !d.grid.Get(neighborCoord).IsVisited(newVisitState) {
					neighborCoords = append(neighborCoords, neighborCoord)
					visitStates = append(visitStates, newVisitState)
				}
			}
		}

		{
			//add the right turn if it is in the grid and the neighbor is unvisited
			neighborCoord := node.Dir(visitState.Direction.Right())
			if d.grid.ContainsCoord(neighborCoord) {
				newVisitState := VisitState{
					Direction:      visitState.Direction.Right(),
					StraightLength: 1,
				}
				if !d.grid.Get(neighborCoord).IsVisited(newVisitState) {
					neighborCoords = append(neighborCoords, neighborCoord)
					visitStates = append(visitStates, newVisitState)
				}
			}
		}
	}

	return neighborCoords, visitStates
}

func (d *Day17) Part2() {
	d.isPart1 = false
	fmt.Println("Part 2")

	d.FindMinPath()
}
