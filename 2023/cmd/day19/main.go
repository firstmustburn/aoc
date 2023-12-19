package main

import (
	h "aoc2023/internal/helpers"
	"fmt"
	"log/slog"
	"maps"
	"os"
	"regexp"
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

	// f, err := os.Create("day19.prof")
	// if err != nil {
	// 	panic(err)
	// }
	// pprof.StartCPUProfile(f)
	// defer pprof.StopCPUProfile()

	d := &Day19{}

	err = h.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

type Day19 struct {
	lines     []string
	workflows map[string]Workflow //workflows by name
	parts     []Part
}

func (d *Day19) Setup(filename string) {
	fmt.Println("Setup")
	d.lines = h.ReadFileToLines(filename)

	d.workflows = make(map[string]Workflow, 0)
	makeWorkflows := true
	for _, line := range d.lines {
		if line == "" {
			makeWorkflows = false
			continue
		}

		if makeWorkflows {
			workflow := MakeWorkflow(line)
			d.workflows[workflow.Name] = workflow
		} else {
			d.parts = append(d.parts, MakePart(line))
		}
	}
}

func (d *Day19) Part1() {
	fmt.Println("Part 1")
	// for _, workflow := range d.workflows {
	// 	fmt.Println(workflow.Name)
	// 	for _, rule := range workflow.Rules {
	// 		fmt.Printf("%#v\n", rule)
	// 	}
	// }
	// fmt.Println("------------------------")
	// for _, part := range d.parts {
	// 	fmt.Printf("%#v\n", part)
	// }
	// fmt.Println("------------------------")

	acceptedParts := []Part{}
	rejectedParts := []Part{}
	for _, part := range d.parts {
		workflow := d.workflows["in"]
		outcome := ""

		for {
			outcome = workflow.Apply(part)
			if outcome == ACCEPT {
				acceptedParts = append(acceptedParts, part)
				break
			} else if outcome == REJECT {
				rejectedParts = append(rejectedParts, part)
				break
			} else {
				var ok bool
				workflow, ok = d.workflows[outcome]
				h.Assert(ok, "no workflow found for "+outcome)
			}
		}
	}

	fmt.Printf("Accepted %d parts and rejected %d parts", len(acceptedParts), len(rejectedParts))
	total := 0
	for _, part := range acceptedParts {
		fmt.Println(part)
		for _, value := range part.Properties {
			total += value
		}
	}

	fmt.Println("total score is", total)

}

func (d *Day19) Part2() {
	fmt.Println("Part 2")

	acceptedPartRanges := []PartRange{}
	rejectedPartRanges := []PartRange{}

	var recurseWorkflows func(w Workflow, pr PartRange, depth string)
	recurseWorkflows = func(w Workflow, pr PartRange, depth string) {
		results := w.ApplyToRange(pr)
		fmt.Printf("%sApplying %s to %s with results:\n", depth, w.originalValue, pr.String())
		for _, result := range results {
			fmt.Printf("%s %s->%s\n", depth, result.partRange.String(), result.outcome)
			if result.outcome == ACCEPT {
				acceptedPartRanges = append(acceptedPartRanges, result.partRange)
			} else if result.outcome == REJECT {
				rejectedPartRanges = append(rejectedPartRanges, result.partRange)
			} else {
				nextWorkflow, ok := d.workflows[result.outcome]
				h.Assert(ok, "no workflow found for "+result.outcome)

				recurseWorkflows(nextWorkflow, result.partRange, depth+"  ")
			}
		}
	}

	startRange := MakePartRange()
	startWorkflow := d.workflows["in"]

	recurseWorkflows(startWorkflow, startRange, "")

	outcomes := 0
	for _, pr := range acceptedPartRanges {
		prOutcomes := 1
		for _, propRange := range pr.Properties {
			prOutcomes *= (propRange.Maxval - propRange.Minval + 1)
		}
		outcomes += prOutcomes
	}
	fmt.Println("Possible outcomes:", outcomes)

}

const ACCEPT = "A"
const REJECT = "R"

type Workflow struct {
	Name          string
	Rules         []Rule
	originalValue string
}

func (w Workflow) Apply(p Part) string {
	for _, rule := range w.Rules {
		outcome := rule.Apply(p)
		if outcome != "" {
			return outcome
		}
	}
	panic("unreachable")
}

type WorkflowResult struct {
	outcome   string
	partRange PartRange
}

// ApplyToRange returns a map of the rule, ACCEPT, or REJECT to the applicable part subrange
func (w Workflow) ApplyToRange(pr PartRange) []WorkflowResult {

	remainder := pr.Clone()
	results := make([]WorkflowResult, 0, len(w.Rules))

	for _, rule := range w.Rules {
		var rangeToOutcome *PartRange
		var outcome string

		rangeToOutcome, outcome, remainder = rule.ApplyToRange(*remainder)
		if rangeToOutcome != nil {
			results = append(results, WorkflowResult{outcome, *rangeToOutcome})
		}
		if remainder == nil {
			break
		}
	}
	h.Assert(remainder == nil, "remainder not nil")
	return results
}

var workflowRe = regexp.MustCompile(`^([a-z]+)\{([^}]+)\}$`)

func MakeWorkflow(input string) Workflow {

	match := workflowRe.FindStringSubmatch(input)
	h.Assert(match != nil, "no match")

	ruleTokens := strings.Split(match[2], ",")
	rules := make([]Rule, 0, len(ruleTokens))
	for _, ruleToken := range ruleTokens {
		rules = append(rules, MakeRule(ruleToken))
	}
	return Workflow{
		Name:          match[1],
		Rules:         rules,
		originalValue: input,
	}
}

type Rule struct {
	PropToCheck   string
	Operator      string
	ExpectedValue int
	Outcome       string
}

func (r Rule) Apply(p Part) string {
	value := p.Properties[r.PropToCheck]
	var condition bool
	if r.Operator == "" {
		condition = true
	} else if r.Operator == "<" {
		condition = (value < r.ExpectedValue)
	} else if r.Operator == ">" {
		condition = (value > r.ExpectedValue)
	} else {
		panic("unreachable")
	}
	if condition {
		return r.Outcome
	} else {
		return ""
	}
}

// applies the rule to the range and returns
// the subrange that gets applied to a new outcome
// the applicable outcome (rule, ACCEPT, REJECT)
// the remainder subrange
func (r Rule) ApplyToRange(pr PartRange) (*PartRange, string, *PartRange) {
	if r.Operator == "" {
		//no condition to check, so all of the range goes to the outcome
		return pr.Clone(), r.Outcome, nil
	} else if r.Operator == "<" {
		//for less, we want the left range to go to expectedValue-1
		leftRange, rightRange := pr.Split(r.PropToCheck, r.ExpectedValue-1)
		//left range goes to the outcome, right range is the remainder
		return leftRange, r.Outcome, rightRange
	} else if r.Operator == ">" {
		//for greater, we want the right range to start at expectedValue+1
		leftRange, rightRange := pr.Split(r.PropToCheck, r.ExpectedValue)
		//right range goes to the outcome, left range is the remainder
		return rightRange, r.Outcome, leftRange
	} else {
		panic("unreachable")
	}
}

var ruleRe = regexp.MustCompile(`^([a-z]+)([<>]{1})(\d+):([a-zA-Z]+)$`)

func MakeRule(input string) Rule {

	if strings.Contains(input, ":") {
		match := ruleRe.FindStringSubmatch(input)
		h.Assert(match != nil, "no match for "+input)
		return Rule{
			PropToCheck:   match[1],
			Operator:      match[2],
			ExpectedValue: h.StrToInt(match[3]),
			Outcome:       match[4],
		}
	} else {
		//unconditional rule
		return Rule{
			PropToCheck:   "",
			Operator:      "",
			ExpectedValue: 0,
			Outcome:       input,
		}
	}
}

type Part struct {
	Properties map[string]int
}

var partRe = regexp.MustCompile(`^\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}$`)

func MakePart(input string) Part {
	match := partRe.FindStringSubmatch(input)
	h.Assert(match != nil, "no match")

	return Part{
		Properties: map[string]int{
			"x": h.StrToInt(match[1]),
			"m": h.StrToInt(match[2]),
			"a": h.StrToInt(match[3]),
			"s": h.StrToInt(match[4]),
		},
	}
}

type Range struct {
	Minval int
	Maxval int
}

func (r Range) Split(splitAfter int) (*Range, *Range) {
	if splitAfter < r.Minval {
		return nil, &Range{r.Minval, r.Maxval}
	} else if splitAfter >= r.Minval && splitAfter < r.Maxval {
		return &Range{r.Minval, splitAfter}, &Range{splitAfter + 1, r.Maxval}
	} else if splitAfter >= r.Maxval {
		return &Range{r.Minval, r.Maxval}, nil
	} else {
		panic("unreachable")
	}
}

type PartRange struct {
	Properties map[string]Range
}

func (pr PartRange) String() string {
	output := "{"
	for k, v := range pr.Properties {
		output += fmt.Sprintf("%s[%d->%d] ", k, v.Minval, v.Maxval)
	}
	return output + "}"
}

func (pr PartRange) Clone() *PartRange {
	return &PartRange{maps.Clone(pr.Properties)}
}

func (pr PartRange) Split(property string, splitAfter int) (*PartRange, *PartRange) {
	leftRange, rightRange := pr.Properties[property].Split(splitAfter)
	if leftRange == nil {
		return nil, pr.Clone()
	} else if rightRange == nil {
		return pr.Clone(), nil
	} else {
		left := pr.Clone()
		right := pr.Clone()
		left.Properties[property] = *leftRange
		right.Properties[property] = *rightRange
		return left, right
	}
}

func MakePartRange() PartRange {
	return PartRange{
		Properties: map[string]Range{
			"x": {1, 4000},
			"m": {1, 4000},
			"a": {1, 4000},
			"s": {1, 4000},
		},
	}
}
