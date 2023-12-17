package helpers

import (
	"container/heap"
	"fmt"
)

type PriorityValue int

// An Item is something we manage in a priority queue.
type item[T any] struct {
	value    T             // The value of the item; arbitrary.
	priority PriorityValue // the priority of the item
	// The index is needed by update and is maintained by the heap.Interface methods.
	index int // The index of the item in the heap.
}

type PriorityQueue[T comparable] struct {
	pqi         pqInner[T]
	valueToItem map[T]*item[T]
}

func MakePriorityQueue[T comparable]() *PriorityQueue[T] {
	pq := &PriorityQueue[T]{}
	heap.Init(&pq.pqi)
	pq.valueToItem = make(map[T]*item[T])
	return pq
}

func (pq PriorityQueue[T]) Dump() {
	fmt.Println("---------------------")
	for ind, item := range pq.pqi {
		fmt.Printf("%d: p=%d, i=%d, v=%v\n", ind, item.priority, item.index, item.value)
	}
	fmt.Println("---------------------")
}

func (pq PriorityQueue[T]) Len() int {
	return len(pq.pqi)
}

func (pq *PriorityQueue[T]) Push(value T, priority PriorityValue) {
	_, ok := pq.valueToItem[value]
	if ok {
		pq.Update(value, priority)
	} else {
		newItem := &item[T]{
			value:    value,
			priority: priority,
		}
		pq.valueToItem[value] = newItem
		heap.Push(&pq.pqi, newItem)
	}
}

func (pq *PriorityQueue[T]) Peek(value T) PriorityValue {
	item, ok := pq.valueToItem[value]
	if ok {
		return item.priority
	}
	panic(fmt.Errorf("called Peek with non-existent value %v", value))
}

func (pq *PriorityQueue[T]) Pop() (T, PriorityValue) {
	if len(pq.pqi) == 0 {
		panic(fmt.Errorf("called pop on empty queue"))
	}
	item := heap.Pop(&pq.pqi).(*item[T])
	delete(pq.valueToItem, item.value)
	return item.value, item.priority
}

// call when the priority of T has changed, returns true if the newPriority is different than the
// existing priority
func (pq *PriorityQueue[T]) Update(value T, newPriority PriorityValue) bool {
	//look up the item from the value
	item, ok := pq.valueToItem[value]
	if !ok {
		panic(fmt.Errorf("value %v does not exist in the queue", value))
	}
	if newPriority != item.priority {
		item.priority = newPriority
		heap.Fix(&pq.pqi, item.index)
		return true
	}
	return false
}

// A pqInner[T] implements heap.Interface and holds Items.
type pqInner[T any] []*item[T]

func (pqi pqInner[T]) Len() int { return len(pqi) }

func (pqi pqInner[T]) Less(i, j int) bool {
	return pqi[i].priority < pqi[j].priority
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
