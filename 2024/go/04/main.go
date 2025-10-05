package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

type Position [2]int // row, col

func loadInput(filePath string) [][]rune {
	file, err := os.Open(filePath)
	if err != nil {
		log.Fatalln("Error on opening input file", err)
	}
	defer file.Close()

	grid := [][]rune{}
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := scanner.Text()
		row := []rune(line)
		grid = append(grid, row)
	}

	if err := scanner.Err(); err != nil {
		log.Fatalln("Error reading input file", err)
	}

	return grid
}

func locatePhraseInDiretion(grid [][]rune, start Position, direction [2]int, phrase []rune) ([]Position, bool) {
	phraseLocation := make([]Position, 0, len(phrase))
	row := start[0]
	col := start[1]

	for _, rune := range phrase {
		if col < 0 || col >= len(grid[0]) || row < 0 || row >= len(grid) {
			return []Position{}, false
		}
		if rune != grid[row][col] {
			return []Position{}, false
		}
		phraseLocation = append(phraseLocation, Position{row, col})
		row += direction[0]
		col += direction[1]
	}
	return phraseLocation, true
}

func locatePhrases(grid [][]rune, phrase []rune, directions [][2]int) [][]Position {
	if len(phrase) == 0 {
		return [][]Position{}
	}

	locations := [][]Position{}
	for rowNum, row := range grid {
		for colNum, rune := range row {
			if rune != phrase[0] {
				continue
			}
			for _, direction := range directions {
				location, found := locatePhraseInDiretion(grid, Position{rowNum, colNum}, direction, phrase)
				if found {
					locations = append(locations, location)
				}
			}
		}
	}
	return locations
}

func countXShapedLocations(locations [][]Position) int {
	count := 0
	centerIndex := len(locations[0]) / 2
	visitedCenterPositions := make(map[Position]bool)

	for _, location := range locations {
		center := location[centerIndex]
		if visitedCenterPositions[center] {
			count++
		} else {
			visitedCenterPositions[center] = true
		}
	}

	return count
}

func countPhrasePartOne(grid [][]rune, phrase []rune) int {
	directions := [][2]int{
		{0, 1},   // right
		{1, 0},   // down
		{1, 1},   // down-right
		{0, -1},  // left
		{-1, 0},  // up
		{-1, -1}, // up-left
		{1, -1},  // down-left
		{-1, 1},  // up-right
	}
	locations := locatePhrases(grid, phrase, directions)
	return len(locations)
}

func countPhrasePartTwo(grid [][]rune, phrase []rune) int {
	directions := [][2]int{
		{1, 1},   // down-right
		{1, -1},  // down-left
		{-1, -1}, // up-left
		{-1, 1},  // up-right
	}
	locations := locatePhrases(grid, phrase, directions)
	return countXShapedLocations(locations)
}

func main() {
	grid := loadInput("input")

	phrasePartOne := "XMAS"
	countPartOne := countPhrasePartOne(grid, []rune(phrasePartOne))
	fmt.Println(phrasePartOne, "found", countPartOne, "times")

	phrasePartTwo := "MAS"
	countPartTwo := countPhrasePartTwo(grid, []rune(phrasePartTwo))
	fmt.Println(phrasePartTwo, "forming X shapes found", countPartTwo, "times")
}
