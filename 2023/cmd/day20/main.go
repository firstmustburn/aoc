package main

import (
	h "aoc2023/internal/helpers"
	"encoding/csv"
	"fmt"
	"log/slog"
	"os"
	"slices"
	"strings"
)

var verbose bool = false

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

	// f, err := os.Create("day20.prof")
	// if err != nil {
	// 	panic(err)
	// }
	// pprof.StartCPUProfile(f)
	// defer pprof.StopCPUProfile()

	d := &Day20{}

	err = h.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

type Day20 struct {
	lines   []string
	modules map[string]*Module
}

func (d *Day20) Setup(filename string) {
	fmt.Println("Setup")
	d.lines = h.ReadFileToLines(filename)

	for _, line := range d.lines {
		MakeModule(line)
	}

	//make all the modules and put them in the module map
	d.modules = make(map[string]*Module, len(d.lines))
	inputMap := make(map[string][]string) //map of module name to to its inputs

	//process the input lines into modules
	for _, line := range d.lines {
		module := MakeModule(line)
		d.modules[module.Name] = module
		//build inputMap from outputs
		//this module is an input for all its outputs
		for _, outputName := range module.Outputs {
			inputMap[outputName] = append(inputMap[outputName], module.Name)
		}
	}
	//now setup all the modules with their inputs
	for moduleName, module := range d.modules {
		module.Setup(inputMap[moduleName])
	}

}

const MARKER_FLIPFLOP = '%'
const MARKER_CONJUNCTION = '&'
const MARKER_BROADCASTER_STR = "broadcaster"

type ModuleType int

const MODULE_UNKNOWN ModuleType = 0
const MODULE_FLIPFLOP ModuleType = 1
const MODULE_CONJUNCTION ModuleType = 2
const MODULE_BROADCAST ModuleType = 3

var MODULE_TYPE_STR = map[ModuleType]string{
	MODULE_UNKNOWN:     "UNKNOWN",
	MODULE_FLIPFLOP:    "FLIPFLOP",
	MODULE_CONJUNCTION: "CONJUNCTION",
	MODULE_BROADCAST:   "BROADCAST",
}

type Module struct {
	Name         string
	MType        ModuleType
	Inputs       []string
	Outputs      []string
	ConfigString string

	//internal state
	FFIsOn      bool
	InputStates []bool //true if the last pulse received was high
}

type Pulse struct {
	State  bool //high if true
	Source string
	Dest   string
}

func (p Pulse) String() string {
	strval := "low"
	if p.State {
		strval = "high"
	}
	return fmt.Sprintf("%s: %s -> %s", strval, p.Source, p.Dest)
}

func (m *Module) Setup(inputs []string) {
	m.Inputs = inputs
	m.Reset()
}

func (m *Module) Reset() {
	//initialize state
	if m.MType == MODULE_FLIPFLOP {
		m.FFIsOn = false
	} else if m.MType == MODULE_CONJUNCTION {
		m.InputStates = make([]bool, len(m.Inputs))
	} //else no state for broadcast
}

func (m Module) makeAllOutputs(pulseState bool) []Pulse {
	pulseOut := []Pulse{}
	for _, output := range m.Outputs {
		pulseOut = append(pulseOut, Pulse{State: pulseState, Source: m.Name, Dest: output})
	}
	return pulseOut
}

func (m *Module) Recieve(pulse Pulse) []Pulse {

	if m.MType == MODULE_FLIPFLOP {
		// Flip-flop modules (prefix %) are either on or off; they are initially off.
		// If a flip-flop module receives a high pulse, it is ignored and nothing
		// happens. However, if a flip-flop module receives a low pulse, it flips
		// between on and off. If it was off, it turns on and sends a high pulse.
		// If it was on, it turns off and sends a low pulse.
		if pulse.State {
			//high pulse
			//do nothing
			return []Pulse{}
		} else {
			//low pulse
			m.FFIsOn = !m.FFIsOn
			return m.makeAllOutputs(m.FFIsOn)
		}
		//end of FLIPFLOP
	} else if m.MType == MODULE_CONJUNCTION {
		//Conjunction modules (prefix &) remember the type of the most recent pulse received from
		//each of their connected input modules; they initially default to remembering a low pulse
		//for each input. When a pulse is received, the conjunction module first updates its memory
		//for that input. Then, if it remembers high pulses for all inputs, it sends a low pulse;
		//otherwise, it sends a high pulse.
		index := slices.Index(m.Inputs, pulse.Source)
		m.InputStates[index] = pulse.State
		return m.makeAllOutputs(!h.All(m.InputStates))
	} else if m.MType == MODULE_BROADCAST {
		// There is a single broadcast module (named broadcaster). When it receives a pulse, it
		// sends the same pulse to all of its destination modules.
		return m.makeAllOutputs(pulse.State)
	}
	panic("unhandled type")
}

func MakeModule(input string) *Module {
	tokens := strings.Split(input, " -> ")
	h.Assert(len(tokens) == 2, "bad line")

	var mType ModuleType
	var name string
	if tokens[0][0] == MARKER_CONJUNCTION {
		mType = MODULE_CONJUNCTION
		name = tokens[0][1:]
	} else if tokens[0][0] == MARKER_FLIPFLOP {
		mType = MODULE_FLIPFLOP
		name = tokens[0][1:]
	} else if tokens[0] == MARKER_BROADCASTER_STR {
		mType = MODULE_BROADCAST
		name = tokens[0]
	} else {
		panic("unhandled case")
	}
	outputs := []string{}
	for _, output := range strings.Split(tokens[1], ",") {
		outputs = append(outputs, strings.TrimSpace(output))
	}
	return &Module{
		ConfigString: input,
		Name:         name,
		MType:        mType,
		Outputs:      outputs,
	}
}

// ProcessPulses initiates a button input and runs the modules until they are quiescent
// Returns the number of high and low pulses sent
func (d *Day20) ProcessPulses(callback func([]Pulse)) (int, int) {

	highPulseCount := 0
	lowPulseCount := 0

	//initialise with low pulse for the button press
	pendingPulses := []Pulse{
		{State: false, Source: "button", Dest: MARKER_BROADCASTER_STR},
	}
	if callback != nil {
		callback(pendingPulses)
	}
	lowPulseCount += 1

	for len(pendingPulses) > 0 {
		//pop the next pulse
		nextPulse := pendingPulses[0]
		pendingPulses = pendingPulses[1:]

		targetModule, ok := d.modules[nextPulse.Dest]
		if !ok {
			//we hit an output or rx node, so do not propagate them
			if nextPulse.Dest != "output" && nextPulse.Dest != "rx" {
				panic("no module named " + nextPulse.Dest)
			}
			continue
		}

		//send the pulse to the target module
		outPulses := targetModule.Recieve(nextPulse)

		if callback != nil {
			callback(outPulses)
		}

		for _, outPulse := range outPulses {
			if outPulse.State {
				highPulseCount += 1
			} else {
				lowPulseCount += 1
			}
		}
		//save the outputs to process them later, in order
		pendingPulses = append(pendingPulses, outPulses...)
	}
	return highPulseCount, lowPulseCount
}

func (d *Day20) Part1() {
	fmt.Println("Part 1")
	// for _, m := range d.modules {
	// 	fmt.Printf("%#v\n", m)
	// }
	highTotal := 0
	lowTotal := 0
	for i := 0; i < 1000; i++ {
		h, l := d.ProcessPulses(nil)
		highTotal += h
		lowTotal += l
	}
	fmt.Printf("Total High: %d Total Low %d Product %d\n", highTotal, lowTotal, highTotal*lowTotal)
}

func (d *Day20) ToDot(filename string) {

	f, err := os.Create(filename)
	h.Assert(err == nil, "could not open dot file")

	defer f.Close()

	node := func(module *Module) {
		//label node
		fmt.Fprintf(f, "%s [ label = \"%s %s\" ]\n",
			module.Name, MODULE_TYPE_STR[module.MType], module.Name)
	}
	edges := func(module *Module) {
		//make edges
		for _, output := range module.Outputs {
			fmt.Fprintf(f, "%s -> %s;\n", module.Name, output)
		}
	}

	fmt.Fprintln(f, "digraph day20 {")

	for _, module := range d.modules {
		//make all the edges
		node(module)
		edges(module)
	}
	fmt.Fprintln(f, "}")

}

func (d *Day20) RecordPresses(numPresses int, filename string) {
	f, err := os.Create(filename)
	h.Assert(err == nil, "could not open csv file")

	defer f.Close()

	w := csv.NewWriter(f)

	heading := []string{"Press", "broadcaster", "rp", "fh", "jn", "tn", "rn", "pm", "tt", "xg", "xm", "xn", "mv", "pp", "bc"}
	sep := make([]string, len(heading))
	for i := range sep {
		sep[i] = "-"
	}

	w.Write(heading)

	pressCount := 0

	callback := func(pulses []Pulse) {
		if len(pulses) == 0 {
			return
		}
		sourceInd := slices.Index(heading, pulses[0].Source)
		if sourceInd == -1 {
			return
		}

		row := make([]string, len(heading))
		row[0] = fmt.Sprintf("%d", pressCount)
		if pulses[0].State {
			row[sourceInd] = "H"
		} else {
			row[sourceInd] = "L"
		}
		for _, pulse := range pulses {
			destInd := slices.Index(heading, pulse.Dest)
			if destInd != -1 {
				row[destInd] = "X"
			}
		}
		w.Write(row)
	}

	for {
		d.ProcessPulses(callback)

		w.Write(sep)

		pressCount += 1
		if pressCount == numPresses {
			break
		}
	}

}

func (d *Day20) Reset() {
	for _, module := range d.modules {
		module.Reset()
	}
}

func (d *Day20) FindLowCycleLength(modName string) (int, int) {

	pressCount := 0
	lowSeen := false
	callback := func(pulses []Pulse) {
		for _, p := range pulses {
			if p.Source == modName && p.State == false {
				lowSeen = true
			}
		}
	}

	//go to the first low
	for !lowSeen {
		pressCount += 1
		d.ProcessPulses(callback)
	}
	firstPress := pressCount

	lowSeen = false
	//go to the second low
	for !lowSeen {
		pressCount += 1
		d.ProcessPulses(callback)
	}
	secondPress := pressCount

	lowSeen = false
	//go to the third low
	for !lowSeen {
		pressCount += 1
		d.ProcessPulses(callback)
	}
	thirdPress := pressCount
	h.Assert(thirdPress-secondPress == secondPress-firstPress, "not a consistent cycle")

	return firstPress, secondPress - firstPress
}

func (d *Day20) Part2() {

	d.ToDot("inputs/day20/input.dot")
	// the overall structure is a set of four LFSR-like counters whose output is a conjuntion.
	// each counter's output goes through an inverter to the final conjunction for that ouputs
	// to rx.  When the counter conjunctions all pulse low in the same button cycle, the rx
	// output will pulse low.

	// d.RecordPresses(20000, "day20_output.csv")
	// from the CSV output, we see that the cycle time for a low output on `bc` is 3911 presses

	// this list is obtained by inspection from the DOT graph
	conMods := []string{"hl", "ql", "hq", "bc"}
	cycleLens := make([]uint64, 0, len(conMods))
	for _, conMod := range conMods {
		d.Reset()
		first, second := d.FindLowCycleLength(conMod)
		h.Assert(first == second, "cycles don't start at the beginning")
		fmt.Println("Cycles", conMod, first, second)
		cycleLens = append(cycleLens, uint64(first))
	}
	totalLen := h.LCM(cycleLens...)
	fmt.Println("Total length to output is ", totalLen)
}
