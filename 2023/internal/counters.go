package helpers

// IncrementCounter increments each entry of counter, wrapping them at limit and carying over
// to the next counter.
// Returns the updated counters and true if there is a carry out from the last entry, otherwise false
func IncrementCounter(counter []int, limit int) ([]int, bool) {
	carry := 1
	for index := range counter {
		counter[index] += carry
		if counter[index] < limit {
			carry = 0
			break
		} else {
			counter[index] = 0
			carry = 1
		}
	}
	return counter, carry == 1
}

func CountersAtPos(counter []int, position int) int {
	atPos := 0
	for _, cVal := range counter {
		if cVal == position {
			atPos += 1
		}
	}
	return atPos
}
