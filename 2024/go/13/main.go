package main

import (
	"fmt"
	"log"
	"math"
	"os"
	"strings"
)

type Arcade struct {
	ButtonA [2]int
	ButtonB [2]int
	Prize   [2]int
}

func (arcade *Arcade) Play() (pushA, pushB int) {
	PX := arcade.Prize[0]
	PY := arcade.Prize[1]
	AX := arcade.ButtonA[0]
	AY := arcade.ButtonA[1]
	BX := arcade.ButtonB[0]
	BY := arcade.ButtonB[1]

	b := float64(PY*AX-PX*AY) / float64(BY*AX-AY*BX)
	if math.Mod(b, 1) != 0 || b < 0 {
		return 0, 0
	}
	pushB = int(b)

	a := float64(PX-pushB*BX) / float64(AX)
	if math.Mod(a, 1) != 0 || a < 0 {
		return 0, 0
	}
	pushA = int(a)

	return pushA, pushB
}

func loadInput(filePath string) []Arcade {
	input, err := os.ReadFile(filePath)
	if err != nil {
		log.Fatalln("Failed to read input file:", err)
	}

	arcades := []Arcade{}
	for line := range strings.SplitSeq(string(input), "\n") {
		if line == "" {
			continue
		}

		if strings.HasPrefix(line, "Button A:") {
			arcades = append(arcades, Arcade{})
		}

		arcade := &arcades[len(arcades)-1]

		if strings.HasPrefix(line, "Button A:") {
			_, err := fmt.Sscanf(line, "Button A: X+%d, Y+%d", &arcade.ButtonA[0], &arcade.ButtonA[1])
			if err != nil {
				log.Fatalln("Failed to parse Button A coordinates:", err)
			}
			continue
		}

		if strings.HasPrefix(line, "Button B:") {
			_, err := fmt.Sscanf(line, "Button B: X+%d, Y+%d", &arcade.ButtonB[0], &arcade.ButtonB[1])
			if err != nil {
				log.Fatalln("Failed to parse Button B coordinates:", err)
			}
			continue
		}

		if strings.HasPrefix(line, "Prize:") {
			_, err := fmt.Sscanf(line, "Prize: X=%d, Y=%d", &arcade.Prize[0], &arcade.Prize[1])
			if err != nil {
				log.Fatalln("Failed to parse Prize coordinates:", err)
			}
		}
	}

	return arcades
}

func calculateTotalCosts(arcades []Arcade) int {
	cost := 0
	for _, arcade := range arcades {
		pushA, pushB := arcade.Play()
		cost += 3*pushA + pushB
	}
	return cost
}

func correctArcades(arcades []Arcade) []Arcade {
	correctedArcades := make([]Arcade, 0, len(arcades))
	for _, arcade := range arcades {
		arcade.Prize[0] += 10000000000000
		arcade.Prize[1] += 10000000000000
		correctedArcades = append(correctedArcades, arcade)
	}
	return correctedArcades
}

func main() {
	arcades := loadInput("input")

	totalCost := calculateTotalCosts(arcades)
	fmt.Println("Total cost to win all prizes:", totalCost)

	correctedArcades := correctArcades(arcades)
	totalCostCorrected := calculateTotalCosts(correctedArcades)
	fmt.Println("Total cost to win all prizes after arcades correction:", totalCostCorrected)
}
