package helpers

import (
	"container/heap"
	"fmt"
)

// An Item is something we manage in a priority queue.
type item[T any] struct {
	value T // The value of the item; arbitrary.
	// The index is needed by update and is maintained by the heap.Interface methods.
	index int // The index of the item in the heap.
}

type Prioritizable interface {
	GetPriority() int
	comparable
}

type PriorityQueue[T Prioritizable] struct {
	pqi         pqInner[T]
	valueToItem map[T]*item[T]
}

func MakePriorityQueue[T Prioritizable]() *PriorityQueue[T] {
	pq := &PriorityQueue[T]{}
	heap.Init(&pq.pqi)
	return pq
}

func (pq *PriorityQueue[T]) Push(value T) {
	//make sure we don't already have this value
	{
		oldItem, ok := pq.valueToItem[value]
		if ok {
			panic(fmt.Errorf("tried to push value %v but it aleady exists in the queue at %v", value, oldItem))
		}
	}
	newItem := &item[T]{
		value: value,
	}
	pq.valueToItem[value] = newItem
	heap.Push(&pq.pqi, newItem)
}

func (pq *PriorityQueue[T]) Pop() T {
	item := heap.Pop(&pq.pqi).(*item[T])
	delete(pq.valueToItem, item.value)
	return item.value
}

// call when the priority of T has changed
func (pq *PriorityQueue[T]) Update(value T) {
	//look up the item from the value
	item, ok := pq.valueToItem[value]
	if !ok {
		panic(fmt.Errorf("value %v does not exist in the queue", value))
	}
	heap.Fix(&pq.pqi, item.index)
}

// A pqInner[T] implements heap.Interface and holds Items.
type pqInner[T Prioritizable] []*item[T]

func (pqi pqInner[T]) Len() int { return len(pqi) }

func (pqi pqInner[T]) Less(i, j int) bool {
	// We want Pop to give us the highest, not lowest, priority so we use greater than here.
	return pqi[i].value.GetPriority() > pqi[j].value.GetPriority()
}

func (pqi pqInner[T]) Swap(i, j int) {
	pqi[i], pqi[j] = pqi[j], pqi[i]
	pqi[i].index = i
	pqi[j].index = j
}

func (pqi *pqInner[T]) Push(x any) {
	n := len(*pqi)
	item := x.(*item[T])
	item.index = n
	*pqi = append(*pqi, item)
}

func (pqi *pqInner[T]) Pop() any {
	old := *pqi
	n := len(old)
	item := old[n-1]
	old[n-1] = nil  // avoid memory leak
	item.index = -1 // for safety
	*pqi = old[0 : n-1]
	return item
}
