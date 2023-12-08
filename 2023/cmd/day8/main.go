package main

import (
	h "aoc2023/internal/helpers"
	"fmt"
	"os"
)

func main() {

	d := &Day8{}

	err := h.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

type Day8 struct {
	lines        []string
	instructions string
	nodes        map[string]*Node
}

type Node struct {
	Name      string
	Left      string
	Right     string
	LeftNode  *Node
	RightNode *Node
}

func (d *Day8) Setup(filename string) {
	fmt.Println("Setup")
	d.lines = h.ReadFileToLines(filename)

	d.instructions = d.lines[0]

	d.nodes = make(map[string]*Node)
	for _, line := range d.lines[2:] {
		name := line[0:3]
		left := line[7:10]
		right := line[12:15]
		d.nodes[name] = &Node{
			Name:  name,
			Left:  left,
			Right: right,
		}
	}

	//fill in the node pointers
	for _, node := range d.nodes {
		node.LeftNode = d.nodes[node.Left]
		node.RightNode = d.nodes[node.Right]
	}
}

func (d *Day8) numberOfSteps(startNode *Node, endCondition func(*Node) bool) uint64 {
	fmt.Println("Getting number of steps for ", startNode)
	stepCount := uint64(0)
	currentNode := startNode
	for !endCondition(currentNode) {
		for _, nextCommand := range d.instructions {
			if nextCommand == 'R' {
				currentNode = currentNode.RightNode
			} else if nextCommand == 'L' {
				currentNode = currentNode.LeftNode
			} else {
				panic(fmt.Errorf("unknown command character %s", string(nextCommand)))
			}
			stepCount += 1
			// fmt.Println("at", currentNode, "for", stepCount, "steps")
			if endCondition(currentNode) {
				break
			}
		}
	}
	fmt.Printf("Final step count for %v is %d\n", startNode, stepCount)
	return stepCount
}

func (d *Day8) Part1() {
	fmt.Println("Part 1")
	d.numberOfSteps(d.nodes["AAA"], func(n *Node) bool {
		return n.Name == "ZZZ"
	})
}

func GCD(n1, n2 uint64) uint64 {
	//Euclid's algorithm
	//repeate the loop of gcd(n1,n2) = gcd(n2, n1 % n2) until n1 % n2 = 0 which means n2 is the GCD
	for n2 != 0 {
		temp := n2
		n2 = n1 % n2
		n1 = temp
	}
	return n1
}

func LCM(values ...uint64) uint64 {
	//LCM = n1 * n2 / GCD(n1, n2)
	//start with the first pair and repeat until we have the LCM of all of them
	h.Assert(len(values) >= 2, "need at least two integer values")

	lcm := (values[0] * values[1]) / GCD(values[0], values[1])

	for _, value := range values[2:] {
		lcm = (lcm * value) / GCD(lcm, value)
	}
	return lcm
}

func (d *Day8) Part2() {
	fmt.Println("Part 2")
	stepCounts := []uint64{}
	for _, node := range d.nodes {
		if node.Name[2] == 'A' {
			stepCount := d.numberOfSteps(node, func(n *Node) bool {
				return n.Name[2] == 'Z'
			})
			stepCounts = append(stepCounts, stepCount)
		}
	}
	fullSteps := LCM(stepCounts...)
	fmt.Println("Full steps needed", fullSteps)
}
