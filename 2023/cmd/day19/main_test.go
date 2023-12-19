package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestWorkflow(t *testing.T) {

	workflow := MakeWorkflow("qqz{s>2770:qs,m<1801:hdj,R}")
	inRange := MakePartRange()
	results := workflow.ApplyToRange(inRange)
	assert.Len(t, results, 3)
	assert.Equal(t, "qs", results[0].outcome)
	assert.Equal(t,
		PartRange{
			Properties: map[string]Range{
				"x": {1, 4000},
				"m": {1, 4000},
				"a": {1, 4000},
				"s": {2771, 4000},
			},
		},
		results[0].partRange)
	assert.Equal(t, "hdj", results[1].outcome)
	assert.Equal(t,
		PartRange{
			Properties: map[string]Range{
				"x": {1, 4000},
				"m": {1, 1800},
				"a": {1, 4000},
				"s": {1, 2770},
			},
		},
		results[1].partRange)
	assert.Equal(t, "R", results[2].outcome)
	assert.Equal(t,
		PartRange{
			Properties: map[string]Range{
				"x": {1, 4000},
				"m": {1801, 4000},
				"a": {1, 4000},
				"s": {1, 2770},
			},
		},
		results[2].partRange)
}

func TestRule(t *testing.T) {

	type TestCase struct {
		input        PartRange
		ruleStr      string
		outcomeRange *PartRange
		outcome      string
		remainder    *PartRange
	}
	testCases := []TestCase{
		{
			input: PartRange{
				Properties: map[string]Range{
					"x": {1337, 2905},
					"m": {0, 4000},
					"a": {0, 4000},
					"s": {0, 4000},
				},
			},
			ruleStr: "s>2770:qs",
			outcomeRange: &PartRange{
				Properties: map[string]Range{
					"x": {1337, 2905},
					"m": {0, 4000},
					"a": {0, 4000},
					"s": {2771, 4000},
				},
			},
			outcome: "qs",
			remainder: &PartRange{
				Properties: map[string]Range{
					"x": {1337, 2905},
					"m": {0, 4000},
					"a": {0, 4000},
					"s": {0, 2770},
				},
			},
		},
		{
			input: PartRange{
				Properties: map[string]Range{
					"x": {1337, 2905},
					"m": {0, 4000},
					"a": {0, 4000},
					"s": {3000, 4000},
				},
			},
			ruleStr: "s>2770:qs",
			outcomeRange: &PartRange{
				Properties: map[string]Range{
					"x": {1337, 2905},
					"m": {0, 4000},
					"a": {0, 4000},
					"s": {3000, 4000},
				},
			},
			outcome:   "qs",
			remainder: nil,
		},
		{
			input: PartRange{
				Properties: map[string]Range{
					"x": {1337, 2905},
					"m": {0, 4000},
					"a": {0, 4000},
					"s": {0, 2000},
				},
			},
			ruleStr:      "s>2770:qs",
			outcomeRange: nil,
			outcome:      "qs",
			remainder: &PartRange{
				Properties: map[string]Range{
					"x": {1337, 2905},
					"m": {0, 4000},
					"a": {0, 4000},
					"s": {0, 2000},
				},
			},
		},
	}

	for _, tc := range testCases {
		rule := MakeRule(tc.ruleStr)

		outcomeRange, outcome, remainder := rule.ApplyToRange(tc.input)

		assert.Equal(t, tc.outcome, outcome)
		assert.Equal(t, tc.outcomeRange, outcomeRange)
		assert.Equal(t, tc.remainder, remainder)
	}

}

func TestPartRangeSplit(t *testing.T) {

	type TestCase struct {
		splitProp string
		splitVal  int
		out1      *PartRange
		out2      *PartRange
	}
	testCases := []TestCase{
		{
			"x", 2000,
			&PartRange{Properties: map[string]Range{
				"x": {0, 2000},
				"m": {0, 4000},
				"a": {0, 4000},
				"s": {0, 4000},
			}},
			&PartRange{Properties: map[string]Range{
				"x": {2001, 4000},
				"m": {0, 4000},
				"a": {0, 4000},
				"s": {0, 4000},
			}},
		},
		{
			"m", 500,
			&PartRange{Properties: map[string]Range{
				"x": {0, 4000},
				"m": {0, 500},
				"a": {0, 4000},
				"s": {0, 4000},
			}},
			&PartRange{Properties: map[string]Range{
				"x": {0, 4000},
				"m": {501, 4000},
				"a": {0, 4000},
				"s": {0, 4000},
			}},
		},
		{
			"a", -3,
			nil,
			&PartRange{Properties: map[string]Range{
				"x": {0, 4000},
				"m": {0, 4000},
				"a": {0, 4000},
				"s": {0, 4000},
			}},
		},
		{
			"s", 5000,
			&PartRange{Properties: map[string]Range{
				"x": {0, 4000},
				"m": {0, 4000},
				"a": {0, 4000},
				"s": {0, 4000},
			}},
			nil,
		},
	}

	for _, tc := range testCases {
		partRange := MakePartRange()
		out1, out2 := partRange.Split(tc.splitProp, tc.splitVal)
		assert.Equal(t, tc.out1, out1)
		assert.Equal(t, tc.out2, out2)
	}
}

func TestRangeSplit(t *testing.T) {

	type TestCase struct {
		input    Range
		splitVal int
		out1     *Range
		out2     *Range
	}
	testCases := []TestCase{
		// [1000,3000] @ 500 => [], [1000, 3000]
		{
			input:    Range{1000, 3000},
			splitVal: 500,
			out1:     nil,
			out2:     &Range{1000, 3000},
		},
		// [1000,3000] @ 999 => [], [1000, 3000]
		{
			input:    Range{1000, 3000},
			splitVal: 999,
			out1:     nil,
			out2:     &Range{1000, 3000},
		},
		// [1000,3000] @ 1000 => [1000, 1000], [1001, 3000]
		{
			input:    Range{1000, 3000},
			splitVal: 1000,
			out1:     &Range{1000, 1000},
			out2:     &Range{1001, 3000},
		},
		// [1000,3000] @ 1001 => [1000, 1001], [1002, 3000]
		{
			input:    Range{1000, 3000},
			splitVal: 1001,
			out1:     &Range{1000, 1001},
			out2:     &Range{1002, 3000},
		},
		// [1000,3000] @ 2000 => [1000,2000], [2001, 3000]
		{
			input:    Range{1000, 3000},
			splitVal: 2000,
			out1:     &Range{1000, 2000},
			out2:     &Range{2001, 3000},
		},
		// [1000,3000] @ 2999 => [1000,2999], [3000, 3000]
		{
			input:    Range{1000, 3000},
			splitVal: 2999,
			out1:     &Range{1000, 2999},
			out2:     &Range{3000, 3000},
		},
		// [1000,3000] @ 3000 => [1000,3000], []
		{
			input:    Range{1000, 3000},
			splitVal: 3000,
			out1:     &Range{1000, 3000},
			out2:     nil,
		},
		// [1000,3000] @ 3001 => [1000,3000], []
		{
			input:    Range{1000, 3000},
			splitVal: 3001,
			out1:     &Range{1000, 3000},
			out2:     nil,
		},
		// [1000,3000] @ 3500 => [1000,3000], []
		{
			input:    Range{1000, 3000},
			splitVal: 3500,
			out1:     &Range{1000, 3000},
			out2:     nil,
		},
	}

	for _, tc := range testCases {
		out1, out2 := tc.input.Split(tc.splitVal)
		assert.Equal(t, out1, tc.out1)
		assert.Equal(t, out2, tc.out2)
	}
}
