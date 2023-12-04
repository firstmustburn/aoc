package helpers

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCoord(t *testing.T) {
	c := Coord{10, 15}

	assert.Equal(t, c.NW(), Coord{9, 14})
	assert.Equal(t, c.N(), Coord{9, 15})
	assert.Equal(t, c.NE(), Coord{9, 16})
	assert.Equal(t, c.E(), Coord{10, 16})
	assert.Equal(t, c.SE(), Coord{11, 16})
	assert.Equal(t, c.S(), Coord{11, 15})
	assert.Equal(t, c.SW(), Coord{11, 14})
	assert.Equal(t, c.W(), Coord{10, 14})

	assert.Equal(t, c.Top(), []Coord{{9, 14}, {9, 15}, {9, 16}})
	assert.Equal(t, c.Right(), []Coord{{9, 16}, {10, 16}, {11, 16}})
	assert.Equal(t, c.Bottom(), []Coord{{11, 16}, {11, 15}, {11, 14}})
	assert.Equal(t, c.Left(), []Coord{{11, 14}, {10, 14}, {9, 14}})

	assert.Equal(t, c.Adjacent(true), []Coord{
		{9, 14},
		{9, 15},
		{9, 16},
		{10, 16},
		{11, 16},
		{11, 15},
		{11, 14},
		{10, 14},
	})

	assert.Equal(t, c.Adjacent(false), []Coord{
		{9, 15},
		{10, 16},
		{11, 15},
		{10, 14},
	})

}

func TestRegionBasic(t *testing.T) {

	r := CreateRegion(Coord{1, 2}, Coord{10, 9})

	assert.Equal(t, 8, r.Width())
	assert.Equal(t, 10, r.Height())
	assert.Equal(t, Coord{1, 2}, r.UpperLeft())
	assert.Equal(t, Coord{1, 9}, r.UpperRight())
	assert.Equal(t, Coord{10, 2}, r.LowerLeft())
	assert.Equal(t, Coord{10, 9}, r.LowerRight())

	assert.True(t, r.ContainsCoord(Coord{5, 5}))
	assert.False(t, r.ContainsCoord(Coord{0, 5}))

	assert.True(t, r.ContainsRegion(CreateRegion(Coord{4, 4}, Coord{6, 6})))
	//disjoint region
	assert.False(t, r.ContainsRegion(CreateRegion(Coord{11, 11}, Coord{13, 13})))
	//overlapping region
	assert.False(t, r.ContainsRegion(CreateRegion(Coord{0, 0}, Coord{5, 5})))

	{
		recording := []Coord{}

		walker := func(c Coord) {
			recording = append(recording, c)
		}
		r.Walk(walker)

		expected := []Coord{
			{1, 2}, {1, 3}, {1, 4}, {1, 5}, {1, 6}, {1, 7}, {1, 8}, {1, 9},
			{2, 2}, {2, 3}, {2, 4}, {2, 5}, {2, 6}, {2, 7}, {2, 8}, {2, 9},
			{3, 2}, {3, 3}, {3, 4}, {3, 5}, {3, 6}, {3, 7}, {3, 8}, {3, 9},
			{4, 2}, {4, 3}, {4, 4}, {4, 5}, {4, 6}, {4, 7}, {4, 8}, {4, 9},
			{5, 2}, {5, 3}, {5, 4}, {5, 5}, {5, 6}, {5, 7}, {5, 8}, {5, 9},
			{6, 2}, {6, 3}, {6, 4}, {6, 5}, {6, 6}, {6, 7}, {6, 8}, {6, 9},
			{7, 2}, {7, 3}, {7, 4}, {7, 5}, {7, 6}, {7, 7}, {7, 8}, {7, 9},
			{8, 2}, {8, 3}, {8, 4}, {8, 5}, {8, 6}, {8, 7}, {8, 8}, {8, 9},
			{9, 2}, {9, 3}, {9, 4}, {9, 5}, {9, 6}, {9, 7}, {9, 8}, {9, 9},
			{10, 2}, {10, 3}, {10, 4}, {10, 5}, {10, 6}, {10, 7}, {10, 8}, {10, 9},
		}

		assert.Equal(t, expected, recording)
	}

	{
		expected := []Coord{
			{0, 1}, {0, 2}, {0, 3}, {0, 4}, {0, 5}, {0, 6}, {0, 7}, {0, 8}, {0, 9},
			{0, 10}, {1, 10}, {2, 10}, {3, 10}, {4, 10}, {5, 10}, {6, 10}, {7, 10}, {8, 10}, {9, 10}, {10, 10},
			{11, 10}, {11, 9}, {11, 8}, {11, 7}, {11, 6}, {11, 5}, {11, 4}, {11, 3}, {11, 2},
			{11, 1}, {10, 1}, {9, 1}, {8, 1}, {7, 1}, {6, 1}, {5, 1}, {4, 1}, {3, 1}, {2, 1}, {1, 1},
		}

		assert.Equal(t, expected, r.Adjacent(true))
	}

	{
		expected := []Coord{
			{0, 2}, {0, 3}, {0, 4}, {0, 5}, {0, 6}, {0, 7}, {0, 8}, {0, 9},
			{1, 10}, {2, 10}, {3, 10}, {4, 10}, {5, 10}, {6, 10}, {7, 10}, {8, 10}, {9, 10}, {10, 10},
			{11, 9}, {11, 8}, {11, 7}, {11, 6}, {11, 5}, {11, 4}, {11, 3}, {11, 2},
			{10, 1}, {9, 1}, {8, 1}, {7, 1}, {6, 1}, {5, 1}, {4, 1}, {3, 1}, {2, 1}, {1, 1},
		}

		assert.Equal(t, expected, r.Adjacent(false))
	}

}

func TestRegionCreate(t *testing.T) {

	//all of these regions shold be the same
	r1 := CreateRegion(Coord{1, 2}, Coord{8, 9})
	r2 := CreateRegion(Coord{8, 9}, Coord{1, 2})
	r3 := CreateRegion(Coord{1, 9}, Coord{8, 2})
	r4 := CreateRegion(Coord{8, 2}, Coord{1, 9})
	assert.Equal(t, r1, r2)
	assert.Equal(t, r1, r3)
	assert.Equal(t, r1, r4)

}

func TestRegionIntersect(t *testing.T) {

	r1 := CreateRegion(Coord{11, 12}, Coord{18, 19})
	{
		//no overlap
		r2 := CreateRegion(Coord{5, 5}, Coord{7, 7})
		assert.False(t, r1.IntersectsRegion(r2))
		assert.False(t, r2.IntersectsRegion(r1))
	}
	{
		// northwest corner overlap
		r2 := CreateRegion(Coord{5, 5}, Coord{13, 13})
		assert.True(t, r1.IntersectsRegion(r2))
		assert.True(t, r2.IntersectsRegion(r1))
	}
	{
		// northeast corner overlap
		r2 := CreateRegion(Coord{5, 22}, Coord{13, 13})
		assert.True(t, r1.IntersectsRegion(r2))
		assert.True(t, r2.IntersectsRegion(r1))
	}
	{
		// southeast corner overlap
		r2 := CreateRegion(Coord{22, 22}, Coord{13, 13})
		assert.True(t, r1.IntersectsRegion(r2))
		assert.True(t, r2.IntersectsRegion(r1))
	}
	{
		// southwest corner overlap
		r2 := CreateRegion(Coord{22, 5}, Coord{13, 13})
		assert.True(t, r1.IntersectsRegion(r2))
		assert.True(t, r2.IntersectsRegion(r1))
	}
	{
		// r2 contained
		r2 := CreateRegion(Coord{17, 17}, Coord{13, 13})
		assert.True(t, r1.IntersectsRegion(r2))
		assert.True(t, r2.IntersectsRegion(r1))
	}
	{
		// r2 contains
		r2 := CreateRegion(Coord{5, 5}, Coord{22, 22})
		assert.True(t, r1.IntersectsRegion(r2))
		assert.True(t, r2.IntersectsRegion(r1))
	}
	{
		// overlapping but corners are disjoint
		r2 := CreateRegion(Coord{14, 0}, Coord{16, 22})
		assert.True(t, r1.IntersectsRegion(r2))
		assert.True(t, r2.IntersectsRegion(r1))
	}

}

func TestGridBasic(t *testing.T) {

	grid := CreateGrid[int](10, 9)

	assert.Equal(t, 10, grid.Rows())
	assert.Equal(t, 9, grid.Cols())

	assert.True(t, grid.ContainsCoord(Coord{0, 0}))
	assert.True(t, grid.ContainsCoord(Coord{5, 5}))
	assert.True(t, grid.ContainsCoord(Coord{9, 8}))
	assert.True(t, grid.ContainsCoord(Coord{0, 8}))
	assert.True(t, grid.ContainsCoord(Coord{9, 0}))
	assert.False(t, grid.ContainsCoord(Coord{-1, 0}))
	assert.False(t, grid.ContainsCoord(Coord{0, -1}))
	assert.False(t, grid.ContainsCoord(Coord{10, 8}))
	assert.False(t, grid.ContainsCoord(Coord{9, 9}))

	gRegion := grid.AsRegion()
	assert.Equal(t, Coord{0, 0}, gRegion.UpperLeft())
	assert.Equal(t, Coord{9, 8}, gRegion.LowerRight())

	for r := 0; r < 10; r++ {
		for c := 0; c < 9; c++ {
			assert.Equal(t, 0, grid.Get(Coord{r, c}))
			assert.Equal(t, 0, grid.GetRC(r, c))
			//fill the grid with values
			grid.Set(Coord{r, c}, r+c)
			assert.Equal(t, r+c, grid.Get(Coord{r, c}))
			//fill the grid with values
			grid.SetRC(r, c, r*c)
			assert.Equal(t, r*c, grid.GetRC(r, c))
		}
	}
}

func TestGridCoordAdjacent(t *testing.T) {

	grid := CreateGrid[int](10, 9)

	//test one at the center
	{
		expected := []Coord{
			{4, 4}, {4, 5},
			{4, 6}, {5, 6},
			{6, 6}, {6, 5},
			{6, 4}, {5, 4},
		}

		assert.Equal(t, expected, grid.AdjacentToCoord(Coord{5, 5}, true))
	}
	{
		expected := []Coord{
			{4, 5},
			{5, 6},
			{6, 5},
			{5, 4},
		}

		assert.Equal(t, expected, grid.AdjacentToCoord(Coord{5, 5}, false))
	}
	//test one at a corner
	{
		expected := []Coord{
			{0, 1},
			{1, 1}, {1, 0},
		}

		assert.Equal(t, expected, grid.AdjacentToCoord(Coord{0, 0}, true))
	}
	{
		expected := []Coord{
			{0, 1},
			{1, 0},
		}

		assert.Equal(t, expected, grid.AdjacentToCoord(Coord{0, 0}, false))
	}

	//test one in the middle of a side
	{
		expected := []Coord{
			{4, 7}, {4, 8},
			{6, 8},
			{6, 7}, {5, 7},
		}

		assert.Equal(t, expected, grid.AdjacentToCoord(Coord{5, 8}, true))
	}
	{
		expected := []Coord{
			{4, 8},
			{6, 8},
			{5, 7},
		}

		assert.Equal(t, expected, grid.AdjacentToCoord(Coord{5, 8}, false))
	}

}

func TestGridRegionAdjacent(t *testing.T) {

	grid := CreateGrid[int](10, 10)

	//test one at the center
	{
		expected := []Coord{
			{3, 3}, {3, 4}, {3, 5},
			{3, 6}, {4, 6}, {5, 6},
			{6, 6}, {6, 5}, {6, 4},
			{6, 3}, {5, 3}, {4, 3},
		}

		assert.Equal(t, expected, grid.AdjacentToRegion(
			CreateRegion(Coord{4, 4}, Coord{5, 5}), true))
	}
	{
		expected := []Coord{
			{3, 4}, {3, 5},
			{4, 6}, {5, 6},
			{6, 5}, {6, 4},
			{5, 3}, {4, 3},
		}

		assert.Equal(t, expected, grid.AdjacentToRegion(
			CreateRegion(Coord{4, 4}, Coord{5, 5}), false))
	}
	//test one that is disjoint
	{
		expected := []Coord{}

		assert.Equal(t, expected, grid.AdjacentToRegion(
			CreateRegion(Coord{11, 11}, Coord{20, 20}), true))
	}
	{
		expected := []Coord{}

		assert.Equal(t, expected, grid.AdjacentToRegion(
			CreateRegion(Coord{11, 11}, Coord{20, 20}), false))
	}
	//test one that is partially overlapping
	{
		expected := []Coord{
			{3, 0}, {3, 1}, {3, 2},
			{3, 3}, {4, 3}, {5, 3}, {6, 3},
			{7, 3}, {7, 2}, {7, 1}, {7, 0},
		}

		assert.Equal(t, expected, grid.AdjacentToRegion(
			CreateRegion(Coord{4, -2}, Coord{6, 2}), true))
	}
	{
		expected := []Coord{
			{3, 0}, {3, 1}, {3, 2},
			{4, 3}, {5, 3}, {6, 3},
			{7, 2}, {7, 1}, {7, 0},
		}

		assert.Equal(t, expected, grid.AdjacentToRegion(
			CreateRegion(Coord{4, -2}, Coord{6, 2}), false))
	}

}

func TestGridWalker(t *testing.T) {

	grid := CreateGrid[int](3, 4)

	for r := 0; r < 3; r++ {
		for c := 0; c < 4; c++ {
			grid.SetRC(r, c, r*c)
		}
	}

	{
		recording := []Coord{}

		walker := func(row int, col int) {
			recording = append(recording, Coord{row, col})
		}

		grid.WalkRC(walker)

		expected := []Coord{
			{0, 0}, {0, 1}, {0, 2}, {0, 3},
			{1, 0}, {1, 1}, {1, 2}, {1, 3},
			{2, 0}, {2, 1}, {2, 2}, {2, 3},
		}

		assert.Equal(t, expected, recording)
	}
	{
		recordingC := []Coord{}
		recordingV := []int{}

		walker := func(row int, col int, value int) {
			recordingC = append(recordingC, Coord{row, col})
			recordingV = append(recordingV, value)
		}

		grid.WalkRCV(walker)

		expectedC := []Coord{
			{0, 0}, {0, 1}, {0, 2}, {0, 3},
			{1, 0}, {1, 1}, {1, 2}, {1, 3},
			{2, 0}, {2, 1}, {2, 2}, {2, 3},
		}
		expectedV := []int{
			0, 0, 0, 0,
			0, 1, 2, 3,
			0, 2, 4, 6,
		}

		assert.Equal(t, expectedC, recordingC)
		assert.Equal(t, expectedV, recordingV)
	}

}
