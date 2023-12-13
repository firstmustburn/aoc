package helpers

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestIncrementCounter(t *testing.T) {
	counter := []int{0, 0, 0}

	expectedValues := [][]int{
		{1, 0, 0},
		{2, 0, 0},
		{0, 1, 0},
		{1, 1, 0},
		{2, 1, 0},
		{0, 2, 0},
		{1, 2, 0},
		{2, 2, 0},
		{0, 0, 1},
		{1, 0, 1},
		{2, 0, 1},
		{0, 1, 1},
		{1, 1, 1},
		{2, 1, 1},
		{0, 2, 1},
		{1, 2, 1},
		{2, 2, 1},
		{0, 0, 2},
		{1, 0, 2},
		{2, 0, 2},
		{0, 1, 2},
		{1, 1, 2},
		{2, 1, 2},
		{0, 2, 2},
		{1, 2, 2},
		{2, 2, 2},
		{0, 0, 0},
	}

	for index, expected := range expectedValues {
		counter, carryOut := IncrementCounter(counter, 3)
		assert.Equal(t, expected, counter)
		if index < len(expectedValues)-1 {
			assert.False(t, carryOut)
		} else {
			assert.True(t, carryOut)
		}
	}
}
