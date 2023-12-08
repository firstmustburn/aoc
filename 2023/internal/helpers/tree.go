package helpers

import "fmt"

type NodeID uint64

var nextNodeID NodeID = 0

type Node[V any] struct {
	id       NodeID
	parent   *Node[V]
	children []*Node[V]
	data     *V
}

// Create a new node with the specified parent and children and data.  Child nodes will have
// their parent set as the new node automatically.
func MakeNodeGeneral[V any](parent *Node[V], children []*Node[V], data *V) *Node[V] {
	thisId := nextNodeID
	nextNodeID += 1
	newNode := &Node[V]{
		id:       thisId,
		parent:   parent,
		children: []*Node[V]{}, //no children
		data:     data,
	}
	for _, c := range children {
		newNode.AddChild(c)
	}
	return newNode
}

// Create a new node with the specified parent and data.  The new node will be added as a child
// of the parent
func MakeNodeLeaf[V any](parent *Node[V], data *V) *Node[V] {
	thisId := nextNodeID
	nextNodeID += 1
	newNode := &Node[V]{
		id:       thisId,
		parent:   nil,
		children: []*Node[V]{}, //no children
		data:     data,
	}
	parent.AddChild(newNode) //this will set the parent in newNode
	return newNode
}

// Create a new node with the specified children and data.  Child nodes will have
// their parent set as the new node automatically.
func MakeNodeRoot[V any](children []*Node[V], data *V) *Node[V] {
	thisId := nextNodeID
	nextNodeID += 1
	newNode := &Node[V]{
		id:       thisId,
		parent:   nil,
		children: []*Node[V]{}, //no children
		data:     data,
	}
	for _, c := range children {
		newNode.AddChild(c)
	}
	return newNode
}

// Create a new node without any relationships and the specified data.
func MakeNodeBare[V any](data *V) *Node[V] {
	thisId := nextNodeID
	nextNodeID += 1
	return &Node[V]{
		id:       thisId,
		parent:   nil,          //no parent
		children: []*Node[V]{}, //no children
		data:     data,
	}
}

func (n *Node[V]) GetID() NodeID {
	return n.id
}

func (n *Node[V]) Is(other *Node[V]) bool {
	return n.id == other.id
}

func (n *Node[V]) GetRoot() *Node[V] {
	return n.parent
}

func (n *Node[V]) GetParent() *Node[V] {
	return n.parent
}

func (n *Node[V]) GetChildren() []*Node[V] {
	return n.children
}

func (n *Node[V]) GetSiblings() []*Node[V] {
	if n.parent == nil {
		return []*Node[V]{}
	}
	siblings := make([]*Node[V], 0, len(n.parent.children)-1)
	for _, sib := range n.parent.children {
		if !sib.Is(n) {
			siblings = append(siblings, sib)
		}
	}
	return siblings
}

func (n *Node[V]) GetData() *V {
	return n.data
}

func (n *Node[V]) IsRoot() bool {
	return n.parent == nil
}

func (n *Node[V]) IsLeaf() bool {
	return len(n.children) == 0
}

func (n *Node[V]) HasChild(child *Node[V]) bool {
	for _, c := range n.children {
		if c.Is(child) {
			return true
		}
	}
	return false
}

func (n *Node[V]) HasChildByID(childId NodeID) bool {
	for _, c := range n.children {
		if c.id == childId {
			return true
		}
	}
	return false
}

// GetPath returns a list of nodes representing the path from the root to the current node.
// The first element of the return value is the root, the last element will be this node.
// If the node is the root, slice is returned contains only the root node
func (n *Node[V]) GetPath() []*Node[V] {
	if n.IsRoot() {
		//just ourselves
		return []*Node[V]{n}
	}
	//add this node to the parent path - recursive call will get the whole path
	return append(n.parent.GetPath(), n)
}

// WalkDepthFirst iterates the tree below this node in a depth-first order beginning with this node.
// For each node encountered, callback(node) is called.  If the callback returns false, then
// the tree traversal is halted.  If the callback is true, then traversal continues.
// Returns true if the whole tree was walked, false if the walk was halted at some point.
func (n *Node[V]) WalkDepthFirst(callback func(*Node[V]) bool) bool {
	ret := callback(n)
	if !ret {
		//halt the traversal
		return false
	}
	for _, c := range n.children {
		ret = c.WalkDepthFirst(callback)
		if !ret {
			//halt traversal
			return false
		}
	}
	//traversal complete
	return true
}

// WalkBreadthFirst iterates the tree below this node in a breadth-first order beginning with this node.
// For each node encountered, callback(node) is called.  If the callback returns false, then
// the tree traversal is halted.  If the callback is true, then traversal continues.
// Returns true if the whole tree was walked, false if the walk was halted at some point.
func (n *Node[V]) WalkBreadthFirst(callback func(*Node[V]) bool) bool {
	nodesToTraverse := make([]*Node[V], 0, 1)
	nodesToTraverse = append(nodesToTraverse, n)

	//while there are any nodes in the queue
	for len(nodesToTraverse) > 0 {
		//remove the next node off the queue
		nextNode := nodesToTraverse[0]
		nodesToTraverse = nodesToTraverse[1:]
		//callback the node
		ret := callback(nextNode)
		if !ret {
			//halt traversal
			return false
		}
		//enqueue the nodes children, if any
		if !nextNode.IsLeaf() {
			nodesToTraverse = append(nodesToTraverse, nextNode.children...)
		}
	}
	//traversal complete
	return true
}

//**************************************************************************************************
// Set / modification methods

// SetData replaces the data on the node and returns the old value
func (n *Node[V]) SetData(newData *V) *V {
	old := n.data
	n.data = newData
	return old
}

// setParent replaces the parent on the node and returns the old parent node (or nil if there was
// no old parent)
// in general this is only used by Add and Remove child.  The preferred way of manipulating the tree
// is through these operations
func (n *Node[V]) setParent(newParent *Node[V]) *Node[V] {
	old := n.parent
	n.parent = newParent
	return old
}

// AddChild adds the child to the node
// panics if the child node already has a parent
func (n *Node[V]) AddChild(newChild *Node[V]) bool {
	if newChild.GetParent() != nil {
		panic(fmt.Errorf("not allowed to add a child that already has a parent"))
	}
	n.children = append(n.children, newChild)
	newChild.setParent(n)
	return true
}

// RemoveChild removes the child from the node if it is present. Othewise it has no effect.
// Returns true if the child was removed, false if it was not present
func (n *Node[V]) RemoveChild(childToRemove *Node[V]) bool {
	for i, c := range n.children {
		if c.Is(childToRemove) {
			n.children = append(n.children[:i], n.children[i+1:]...)
			childToRemove.setParent(nil) //clear the child node's parent
			return true
		}
	}
	return false
}

// RemoveChildByID removes the child from the node if a child with that ID is present. Othewise it has no effect.
// Returns the node that was removed, or nil if it was not present
func (n *Node[V]) RemoveChildByID(childIDToRemove NodeID) *Node[V] {
	for i, c := range n.children {
		if c.id == childIDToRemove {
			n.children = append(n.children[:i], n.children[i+1:]...)
			c.setParent(nil) //clear the child node's parent
			return c
		}
	}
	return nil
}
