package main

import (
	h "aoc2023/internal/helpers"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

func main() {

	d := &Day7{}

	err := h.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

type Day7 struct {
	lines []string
	hands []Hand
}

func (d *Day7) Setup(filename string) {
	fmt.Println("Setup")
	d.lines = h.ReadFileToLines(filename)
	for _, line := range d.lines {
		tokens := strings.Split(line, " ")
		bid, err := strconv.Atoi(tokens[1])
		h.Assert(err == nil, "")
		newHand := Hand{
			Cards: tokens[0],
			Bid:   bid,
		}
		d.hands = append(d.hands, newHand)
	}
}

type Hand struct {
	Cards    string
	Bid      int
	HType    HandType
	CardInts []int
}

func (hand *Hand) P1Process() {
	hand.CardInts = make([]int, 0, 5)
	for _, c := range hand.Cards {
		hand.CardInts = append(hand.CardInts, P1CardCharToInt(byte(c)))
	}
	hand.HType = P1ComputeHandType(hand.CardInts)
}

type HandType int

const (
	FIVE_KIND  HandType = 7
	FOUR_KIND  HandType = 6
	FULL_HOUSE HandType = 5
	THREE_KIND HandType = 4
	TWO_PAIR   HandType = 3
	ONE_PAIR   HandType = 2
	HIGH_CARD  HandType = 1
)

func P1CardCharToInt(card byte) int {
	if card == 'A' {
		return 14
	}
	if card == 'K' {
		return 13
	}
	if card == 'Q' {
		return 12
	}
	if card == 'J' {
		return 11
	}
	if card == 'T' {
		return 10
	}
	numCard, err := strconv.Atoi(string(card))
	h.Assert(err == nil, "")
	return numCard
}

func P1ComputeHandType(cardInts []int) HandType {
	groups := make([]int, 15)
	for _, ci := range cardInts {
		groups[ci] += 1
	}
	//sort the groups
	sort.Slice(groups, func(i, j int) bool {
		return groups[i] >= groups[j]
	})
	if groups[0] == 5 {
		return FIVE_KIND
	}
	if groups[0] == 4 {
		return FOUR_KIND
	}
	if groups[0] == 3 && groups[1] == 2 {
		return FULL_HOUSE
	}
	if groups[0] == 3 {
		return THREE_KIND
	}
	if groups[0] == 2 && groups[1] == 2 {
		return TWO_PAIR
	}
	if groups[0] == 2 {
		return ONE_PAIR
	}
	if groups[0] == 1 {
		return HIGH_CARD
	}
	panic(fmt.Errorf("unhandled case for cards %v with groups %v", cardInts, groups))
}

func (d *Day7) SortHands() {
	sort.Slice(d.hands, func(i, j int) bool {
		hi := d.hands[i]
		hj := d.hands[j]
		if hi.HType != hj.HType {
			return hi.HType < hj.HType
		}
		for cardInd := range hi.CardInts {
			if hi.CardInts[cardInd] != hj.CardInts[cardInd] {
				return hi.CardInts[cardInd] < hj.CardInts[cardInd]
			}
		}
		return false
	})
}

func (d *Day7) ComputeWinnings() {
	winnings := 0
	for index, hand := range d.hands {
		fmt.Println(hand)
		winnings += (index + 1) * hand.Bid
	}
	fmt.Println("Winnings", winnings)
}

func (d *Day7) Part1() {
	fmt.Println("Part 1")
	for index := range d.hands {
		d.hands[index].P1Process()
	}
	d.SortHands()
	d.ComputeWinnings()
}

//**************************************************************************************************
//**************************************************************************************************
//** Part 2 ****************************************************************************************
//**************************************************************************************************
//**************************************************************************************************

func (hand *Hand) P2Process() {
	hand.CardInts = make([]int, 0, 5)
	for _, c := range hand.Cards {
		hand.CardInts = append(hand.CardInts, P2CardCharToInt(byte(c)))
	}
	hand.HType = P2ComputeHandType(hand.CardInts)
}

func P2CardCharToInt(card byte) int {
	if card == 'A' {
		return 14
	}
	if card == 'K' {
		return 13
	}
	if card == 'Q' {
		return 12
	}
	if card == 'J' {
		return 1 //Jokers now the lowest
	}
	if card == 'T' {
		return 10
	}
	numCard, err := strconv.Atoi(string(card))
	h.Assert(err == nil, "")
	return numCard
}

// These are the cases for groups with jokers, showing that to get the best hand you always add the
// jokers to the first group

// # 1 joker
// 40000 -> 5
// 31  -> 41
// 22 -> 32
// 211 -> 311
// 1111 -> 2111

// # 2 joker
// 3 -> 5
// 21 -> 41
// 111 -> 31

// # 3 joker
// 2 -> 5
// 11 -> 4

// # 4 joker
// 1 -> 5

// # 5 joker
//   -> 5

func P2ComputeHandType(cardInts []int) HandType {
	groups := make([]int, 15)
	jokers := 0

	//break things into groups
	for _, ci := range cardInts {
		if ci == 1 { //this is the new int value we assigned to jokers
			jokers += 1
		} else {
			groups[ci] += 1
		}
	}

	//sort the groups
	sort.Slice(groups, func(i, j int) bool {
		return groups[i] >= groups[j]
	})

	//add the jokers to the first group
	groups[0] += jokers

	if groups[0] == 5 {
		return FIVE_KIND
	}
	if groups[0] == 4 {
		return FOUR_KIND
	}
	if groups[0] == 3 && groups[1] == 2 {
		return FULL_HOUSE
	}
	if groups[0] == 3 {
		return THREE_KIND
	}
	if groups[0] == 2 && groups[1] == 2 {
		return TWO_PAIR
	}
	if groups[0] == 2 {
		return ONE_PAIR
	}
	if groups[0] == 1 {
		return HIGH_CARD
	}
	panic(fmt.Errorf("unhandled case for cards %v with groups %v", cardInts, groups))
}

func (d *Day7) Part2() {
	for index := range d.hands {
		d.hands[index].P2Process()
	}
	d.SortHands()
	d.ComputeWinnings()
}
