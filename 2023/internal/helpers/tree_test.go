package helpers

import (
	"fmt"
	"slices"
	"testing"

	"github.com/stretchr/testify/assert"
)

type MyData struct {
	value int
}

func makeTreeDown() *Node[MyData] {
	//root
	n1 := MakeNodeBare[MyData](&MyData{1})

	//second level
	n11 := MakeNodeLeaf[MyData](n1, &MyData{11})
	n12 := MakeNodeLeaf[MyData](n1, &MyData{12})
	n13 := MakeNodeLeaf[MyData](n1, &MyData{13})

	//third level
	MakeNodeLeaf(n11, &MyData{111})
	MakeNodeLeaf(n11, &MyData{112})
	MakeNodeLeaf(n11, &MyData{113})

	MakeNodeLeaf(n12, &MyData{121})
	MakeNodeLeaf(n12, &MyData{122})
	MakeNodeLeaf(n12, &MyData{123})

	MakeNodeLeaf(n13, &MyData{131})
	MakeNodeLeaf(n13, &MyData{132})
	MakeNodeLeaf(n13, &MyData{133})

	return n1
}

func makeTreeUp() *Node[MyData] {
	//third level
	n111 := MakeNodeBare(&MyData{111})
	n112 := MakeNodeBare(&MyData{112})
	n113 := MakeNodeBare(&MyData{113})

	n121 := MakeNodeBare(&MyData{121})
	n122 := MakeNodeBare(&MyData{122})
	n123 := MakeNodeBare(&MyData{123})

	n131 := MakeNodeBare(&MyData{131})
	n132 := MakeNodeBare(&MyData{132})
	n133 := MakeNodeBare(&MyData{133})

	//second level
	n11 := MakeNodeRoot[MyData]([]*Node[MyData]{n111, n112, n113}, &MyData{11})
	n12 := MakeNodeRoot[MyData]([]*Node[MyData]{n121, n122, n123}, &MyData{12})
	n13 := MakeNodeRoot[MyData]([]*Node[MyData]{n131, n132, n133}, &MyData{13})

	//root
	n1 := MakeNodeRoot[MyData]([]*Node[MyData]{n11, n12, n13}, &MyData{1})

	return n1
}

func TestTreeIds(t *testing.T) {
	seenIDs := []NodeID{}

	for i := 0; i < 100; i++ {
		//make a node
		node := MakeNodeBare[MyData](&MyData{i})
		assert.False(t, slices.Contains(seenIDs, node.GetID()))
		seenIDs = append(seenIDs, node.GetID())
	}
}

func TestTreeSetParent(t *testing.T) {

	n1 := MakeNodeBare[MyData](&MyData{1})
	n2 := MakeNodeBare[MyData](&MyData{2})

	n2.setParent(n1)

	//check the parent was set
	assert.True(t, n2.GetParent().Is(n1))
	//set parent doesn't modify children of the parent
	assert.False(t, n1.HasChild(n2))

}

func TestTreeSetData(t *testing.T) {

	n1 := MakeNodeBare[MyData](&MyData{1})

	assert.Equal(t, 1, n1.data.value)

	n1.SetData(&MyData{100})

	assert.Equal(t, 100, n1.data.value)

}

func TestTreeModifications(t *testing.T) {

	loneNode := MakeNodeBare[MyData](&MyData{0})

	trees := []*Node[MyData]{
		makeTreeDown(),
		makeTreeUp(),
	}
	for treeIndex, tree := range trees {
		fmt.Println("Tree index", treeIndex)

		{
			n12 := tree.GetChildren()[1]
			assert.Equal(t, 12, n12.data.value)
			//remove with RemoveChild
			n122 := n12.GetChildren()[1]
			assert.Equal(t, 122, n122.data.value)

			//remove n122, should return true
			assert.True(t, n12.RemoveChild(n122))

			//check the properties of n122
			assert.Nil(t, n122.GetParent())

			//check the properties of n12 after the removal
			assert.Len(t, n12.GetChildren(), 2)
			assert.Equal(t, 121, n12.GetChildren()[0].data.value)
			assert.Equal(t, 123, n12.GetChildren()[1].data.value)

			//spurious removal should not do anything and return false
			assert.False(t, n12.RemoveChild(loneNode))

			//check the properties of n12 after the failed attempt -- should be the same
			assert.Len(t, n12.GetChildren(), 2)
			assert.Equal(t, 121, n12.GetChildren()[0].data.value)
			assert.Equal(t, 123, n12.GetChildren()[1].data.value)
		}
		{
			n13 := tree.GetChildren()[2]
			assert.Equal(t, 13, n13.data.value)
			//remove with RemoveChildByID
			n132 := n13.GetChildren()[1]
			assert.Equal(t, 132, n132.data.value)

			//remove n132
			removedNode := n13.RemoveChildByID(n132.GetID())
			assert.True(t, removedNode.Is(n132))

			//check the properties of n132
			assert.Nil(t, n132.GetParent())

			//check the properties of n13 after the removal
			assert.Len(t, n13.GetChildren(), 2)
			assert.Equal(t, 131, n13.GetChildren()[0].data.value)
			assert.Equal(t, 133, n13.GetChildren()[1].data.value)

			//supurious removal should not do anything and should return nil
			assert.Nil(t, n13.RemoveChildByID(loneNode.GetID()))

			//check the properties of n13 after the removal
			assert.Len(t, n13.GetChildren(), 2)
			assert.Equal(t, 131, n13.GetChildren()[0].data.value)
			assert.Equal(t, 133, n13.GetChildren()[1].data.value)
		}
		{
			//make a new node
			newNode := MakeNodeBare[MyData](&MyData{999})

			//add it to the root
			tree.AddChild(newNode)

			//check the newNode after
			assert.True(t, newNode.GetParent().Is(tree))

			//check the parent node after
			assert.True(t, tree.HasChild(newNode))
			assert.True(t, tree.HasChildByID(newNode.GetID()))
			assert.Len(t, tree.GetChildren(), 4)
			assert.True(t, tree.GetChildren()[3].Is(newNode))

			//panic if we add the node again
			assert.Panics(t, func() {
				tree.AddChild(newNode)
			})
			//no change to node after failed add
			assert.Len(t, tree.GetChildren(), 4)

			//panic if we add the node to a different node
			assert.Panics(t, func() {
				loneNode.AddChild(newNode)
			})
			//no change to node after failed add
			assert.Len(t, loneNode.GetChildren(), 0)
		}
	}
}

func TestTreeWalkOrder(t *testing.T) {

	trees := []*Node[MyData]{
		makeTreeDown(),
		makeTreeUp(),
	}

	expectedBreadthFirst := []int{
		1,
		11, 12, 13,
		111, 112, 113, 121, 122, 123, 131, 132, 133,
	}
	expectedDepthFirst := []int{
		1,
		11, 111, 112, 113,
		12, 121, 122, 123,
		13, 131, 132, 133,
	}

	for treeIndex, tree := range trees {
		{
			//breadth first
			record := []int{}
			callback := func(n *Node[MyData]) bool {
				record = append(record, n.data.value)
				return true
			}
			tree.WalkDepthFirst(callback)
			assert.Equal(t, expectedDepthFirst, record, "test index %d", treeIndex)
		}
		{
			//depth first
			record := []int{}
			callback := func(n *Node[MyData]) bool {
				record = append(record, n.data.value)
				return true
			}
			tree.WalkBreadthFirst(callback)
			assert.Equal(t, expectedBreadthFirst, record, "test index %d", treeIndex)
		}
	}
}

func TestTreeWalkHalt(t *testing.T) {

	trees := []*Node[MyData]{
		makeTreeDown(),
		makeTreeUp(),
	}

	expectedBreadthFirst := []int{
		1,
		11, 12, 13,
		111, 112, 113,
		// these are never reached due to halt at 113
		// 121, 122, 123, 131, 132, 133,
	}
	expectedDepthFirst := []int{
		1,
		11, 111, 112, 113,
		// these are never reached due to halt at 113
		// 12, 121, 122, 123,
		// 13, 131, 132, 133,
	}

	for treeIndex, tree := range trees {
		{
			//breadth first
			record := []int{}
			callback := func(n *Node[MyData]) bool {
				record = append(record, n.data.value)
				return n.data.value != 113
			}
			tree.WalkDepthFirst(callback)
			assert.Equal(t, expectedDepthFirst, record, "test index %d", treeIndex)
		}
		{
			//depth first
			record := []int{}
			callback := func(n *Node[MyData]) bool {
				record = append(record, n.data.value)
				return n.data.value != 113
			}
			tree.WalkBreadthFirst(callback)
			assert.Equal(t, expectedBreadthFirst, record, "test index %d", treeIndex)
		}
	}
}

func TestTreeStructure(t *testing.T) {

	loneNode := MakeNodeBare[MyData](&MyData{0})

	trees := []*Node[MyData]{
		makeTreeDown(),
		makeTreeUp(),
	}

	l1Expected := 1
	l2Expected := []int{11, 12, 13}
	l3Expected := [][]int{
		{111, 112, 113},
		{121, 122, 123},
		{131, 132, 133},
	}

	for treeIndex, tree := range trees {
		//check data on the root node
		assert.Equal(t, l1Expected, tree.data.value)
		assert.True(t, tree.IsRoot(), "test index %d", treeIndex)
		assert.False(t, tree.IsLeaf(), "test index %d", treeIndex)
		assert.Nil(t, tree.GetParent(), "test index %d", treeIndex)
		//check has child for nonexistent nodes
		assert.False(t, tree.HasChild(loneNode), "test index %d", treeIndex)
		assert.False(t, tree.HasChildByID(loneNode.GetID()), "test index %d", treeIndex)
		//check path
		assert.Equal(t, []*Node[MyData]{tree}, tree.GetPath(), "test index %d", treeIndex)

		l2Actual := tree.GetChildren()
		assert.Len(t, l2Actual, 3, "test index %d", treeIndex)
		//check level 2 children
		for l2Ind, child2 := range l2Actual {
			//check expected data
			assert.Equal(t, l2Expected[l2Ind], child2.data.value, "test %d child [%d]", treeIndex, l2Ind)
			//check hasChild for l1
			assert.True(t, tree.HasChild(child2))
			assert.True(t, tree.HasChildByID(child2.GetID()))
			//check hasChild for l2 nonexistent nodes
			assert.False(t, child2.HasChild(loneNode), "test %d child [%d]", treeIndex, l2Ind)
			assert.False(t, child2.HasChildByID(loneNode.GetID()), "test %d child [%d]", treeIndex, l2Ind)
			//check getparent
			assert.Equal(t, tree.GetID(), child2.GetParent().GetID(), "test %d child [%d]", treeIndex, l2Ind)
			assert.True(t, tree.Is(child2.GetParent()), "test %d child [%d]", treeIndex, l2Ind)
			//check path
			assert.Equal(t, []*Node[MyData]{tree, child2}, child2.GetPath(), "test %d child [%d]", treeIndex, l2Ind)

			//check l3 children
			l3Actual := child2.GetChildren()
			for l3Ind, child3 := range l3Actual {
				//check expected data
				assert.Equal(t, l3Expected[l2Ind][l3Ind], child3.data.value, "test %d child [%d][%d]", treeIndex, l2Ind, l3Ind)
				//check getParent
				assert.True(t, child3.GetParent().Is(child2), "test %d child [%d][%d]", treeIndex, l2Ind, l3Ind)
				assert.Equal(t, child2.GetID(), child3.GetParent().GetID(), "test %d child [%d][%d]", treeIndex, l2Ind, l3Ind)
				assert.True(t, tree.Is(child2.GetParent()))
				//check hasChild for l2
				assert.True(t, child2.HasChild(child3), "test %d child [%d][%d]", treeIndex, l2Ind, l3Ind)
				assert.True(t, child2.HasChildByID(child3.GetID()), "test %d child [%d][%d]", treeIndex, l2Ind, l3Ind)

				//check root and leaf
				assert.False(t, child3.IsRoot(), "test %d child [%d][%d]", treeIndex, l2Ind, l3Ind)
				assert.True(t, child3.IsLeaf(), "test %d child [%d][%d]", treeIndex, l2Ind, l3Ind)

				//check hasChild for l3
				assert.False(t, child3.HasChild(loneNode), "test %d child [%d][%d]", treeIndex, l2Ind, l3Ind)
				assert.False(t, child3.HasChildByID(loneNode.GetID()), "test %d child [%d][%d]", treeIndex, l2Ind, l3Ind)

				//check no children for leaf nodes
				assert.Len(t, child3.GetChildren(), 0, "test %d child [%d][%d]", treeIndex, l2Ind, l3Ind)

				//check path
				assert.Equal(t, []*Node[MyData]{tree, child2, child3}, child3.GetPath(), "test %d child [%d][%d]", treeIndex, l2Ind, l3Ind)
			}
		}
	}
}
