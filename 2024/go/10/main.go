package main

import (
	"fmt"
	"log"
	"os"
	"slices"
	"strconv"
	"strings"
)

type Position [2]int

type ScoreFunc func(trails [][]Position) int

var Directions = []Position{
	{0, 1},  // right
	{1, 0},  // down
	{0, -1}, // left
	{-1, 0}, // up
}

func loadInput(filePath string) [][]int {
	input, err := os.ReadFile(filePath)
	if err != nil {
		log.Fatalln("Error reading the file", filePath)
	}

	topoMap := [][]int{}
	for row := range strings.SplitSeq(string(input), "\n") {
		if row == "" {
			continue
		}
		topoMapLine := []int{}
		if len(topoMap) > 0 {
			topoMapLine = make([]int, 0, len(topoMap[0]))
		}
		for char := range strings.SplitSeq(row, "") {
			height, err := strconv.Atoi(char)
			if err != nil {
				log.Fatalln("Error converting character", char, "to integer")
			}
			topoMapLine = append(topoMapLine, height)
		}
		topoMap = append(topoMap, topoMapLine)
	}
	return topoMap
}

func isOutOfBounds(mapSize [2]int, pos Position) bool {
	return pos[0] < 0 || pos[0] >= mapSize[0] || pos[1] < 0 || pos[1] >= mapSize[1]
}

func expandTrail(topoMap *[][]int, topoMapSize [2]int, trail []Position, trails *[][]Position) *[][]Position {
	currentPos := trail[len(trail)-1]
	currentHeight := (*topoMap)[currentPos[0]][currentPos[1]]

	for _, direrction := range Directions {
		newPos := Position{currentPos[0] + direrction[0], currentPos[1] + direrction[1]}
		if isOutOfBounds(topoMapSize, newPos) || slices.Contains(trail, newPos) {
			continue
		}

		newHeight := (*topoMap)[newPos[0]][newPos[1]]
		if newHeight-currentHeight != 1 {
			continue
		}

		expandedTrail := make([]Position, len(trail)+1)
		copy(expandedTrail, trail)
		expandedTrail[len(trail)] = newPos

		if newHeight == 9 {
			*trails = append(*trails, expandedTrail)
			continue
		}

		expandTrail(topoMap, topoMapSize, expandedTrail, trails)
	}
	return trails
}

func uniquePeaksScore(trails [][]Position) int {
	peaks := map[Position]bool{}
	for _, trail := range trails {
		peak := trail[len(trail)-1]
		peaks[peak] = true
	}
	return len(peaks)
}

func uniqueTrailsScore(trails [][]Position) int {
	return len(trails)
}

func calculateMapScore(topoMap *[][]int, scoreFunc ScoreFunc) int {
	topoMapSize := [2]int{len(*topoMap), len((*topoMap)[0])}
	sum := 0
	for rowIdx, line := range *topoMap {
		for colIdx, height := range line {
			if height != 0 {
				continue
			}
			trails := &[][]Position{}
			trail := []Position{{rowIdx, colIdx}}
			trails = expandTrail(topoMap, topoMapSize, trail, trails)
			sum += scoreFunc(*trails)
		}
	}

	return sum
}

func main() {
	topoMap := loadInput("input")

	peaksScore := calculateMapScore(&topoMap, uniquePeaksScore)
	fmt.Println("Total score using unique peaks rating:", peaksScore)

	trailsScore := calculateMapScore(&topoMap, uniqueTrailsScore)
	fmt.Println("Total score using unique trails rating:", trailsScore)
}
