package main

import (
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"
)

func loadInput(filePath string) []string {
	input, err := os.ReadFile(filePath)
	if err != nil {
		log.Fatalln("Error on reading input file", err)
	}
	return strings.Split(string(input), "\n")
}

func parseInput(input []string) ([]int, []int) {
	left := make([]int, 0, len(input))
	right := make([]int, 0, len(input))

	for _, row := range input {
		if row == "" {
			continue
		}
		parts := strings.Split(row, "   ")
		if len(parts) != 2 {
			log.Fatalln("Unexpected row format:", row)
		}

		leftNumber, err := strconv.Atoi(parts[0])
		if err != nil {
			log.Fatalln("Error converting left part to int:", parts[0])
		}
		left = append(left, leftNumber)

		rightNumber, err := strconv.Atoi(parts[1])
		if err != nil {
			log.Fatalln("Error converting right part to int:", parts[1])
		}
		right = append(right, rightNumber)
	}
	return left, right
}

// Part One
func calculateDistance(left, right []int) int {
	if len(left) != len(right) {
		log.Fatalln("Left and right slices must have the same length")
	}
	distance := 0
	for i := range left {
		diff := left[i] - right[i]
		if diff < 0 {
			diff = -diff
		}
		distance += diff
	}
	return distance
}

// Part Two
func countFrequencies(arr []int) map[int]int {
	frequency := make(map[int]int)
	for _, num := range arr {
		frequency[num]++
	}
	return frequency
}

func calculateSimilarityScore(arr []int, frequencies map[int]int) int {
	score := 0
	for _, num := range arr {
		if count, exists := frequencies[num]; exists {
			score += num * count
		}
	}
	return score
}

func main() {
	filePath := "input"
	if len(os.Args) > 1 {
		filePath = os.Args[1]
	}

	input := loadInput(filePath)
	left, right := parseInput(input)
	sort.Ints(left)
	sort.Ints(right)

	// Part One
	distance := calculateDistance(left, right)
	fmt.Printf("Total distance: %d\n", distance)

	// Part Two
	rightFrequencies := countFrequencies(right)
	similarityScore := calculateSimilarityScore(left, rightFrequencies)
	fmt.Printf("Similarity score: %d\n", similarityScore)
}
