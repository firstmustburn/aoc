package main

import (
	h "aoc2023/internal/helpers"
	"fmt"
	"os"
	"slices"
	"strings"
)

func main() {

	d := &Day4{}

	err := h.Dispatch(os.Args, d)
	if err != nil {
		fmt.Println("Error:", err)
		os.Exit(1)
	}

}

type Day4 struct {
	lines []string
	cards []Card
}

type Card struct {
	ID      int
	Copies  int
	Winners []int
	Numbers []int
}

func (d *Day4) Setup(filename string) {
	fmt.Println("Setup")
	d.lines = h.ReadFileToLines(filename)

	for _, line := range d.lines {
		cardTokens := strings.Split(line, ":")
		h.Assert(len(cardTokens) == 2, "card_tokens not len 2")

		card := Card{}

		card.ID, _ = h.ParseLabeledValue(cardTokens[0], false)
		numberListTokens := strings.Split(cardTokens[1], "|")
		h.Assert(len(numberListTokens) == 2, "numberListTokens not len 2")
		card.Winners = h.ParseIntList(strings.TrimSpace(numberListTokens[0]), " ")
		card.Numbers = h.ParseIntList(strings.TrimSpace(numberListTokens[1]), " ")
		card.Copies = 1

		d.cards = append(d.cards, card)
	}

}

func (d *Day4) Part1() {
	fmt.Println("Part 1")

	score := 0

	for _, card := range d.cards {
		fmt.Printf("%#v\n", card)
		cardScore := 0

		for _, winner := range card.Winners {
			if slices.Contains(card.Numbers, winner) {
				//found a match
				if cardScore == 0 {
					cardScore = 1
				} else {
					cardScore = cardScore * 2
				}
			}
		}

		fmt.Println("  score=", cardScore)

		score += cardScore
	}
	fmt.Println("Total score: ", score)
}

func (d *Day4) Part2() {
	fmt.Println("Part 1")

	for cardIndex, card := range d.cards {
		fmt.Printf("%#v\n", card)

		matchCount := 0
		for _, winner := range card.Winners {
			if slices.Contains(card.Numbers, winner) {
				//found a match
				matchCount += 1
			}
		}

		//incre``ment the copies for successive cards, depenting on matchs
		for matchOffset := 1; matchOffset <= matchCount; matchOffset++ {
			//we add a copy for successive cards for every copy of the current card
			d.cards[cardIndex+matchOffset].Copies += card.Copies
		}

		fmt.Println("  matches=", matchCount)
	}

	//count the total number of cards
	cardCount := 0
	for _, card := range d.cards {
		cardCount += card.Copies
	}

	fmt.Println("Total card count: ", cardCount)
}
