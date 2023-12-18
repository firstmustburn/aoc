package helpers

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestPQBasic(t *testing.T) {

	type QD struct {
		Value int
	}

	pq := MakePriorityQueue[QD]()

	pq.Dump()

	pq.Push(QD{0}, 10)
	pq.Push(QD{1}, 5)
	pq.Push(QD{2}, 1)
	pq.Push(QD{3}, 3)
	pq.Push(QD{4}, 11)

	pq.Dump()

	recordQD := []QD{}
	recordPriority := []PriorityValue{}

	for pq.Len() > 0 {
		qd, p := pq.Pop()
		recordQD = append(recordQD, qd)
		recordPriority = append(recordPriority, p)
	}

	//expected
	expectedQD := []QD{{2}, {3}, {1}, {0}, {4}}
	expectedPriority := []PriorityValue{1, 3, 5, 10, 11}

	assert.Equal(t, expectedQD, recordQD)
	assert.Equal(t, expectedPriority, recordPriority)

	// assert.True(t, false)

}
