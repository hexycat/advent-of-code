package main

import (
	"fmt"
	"log"
	"maps"
	"os"
	"strings"
)

const (
	GuardChar    = "^"
	EmptyChar    = "."
	VisitedChar  = "X"
	ObstacleChar = "#"
)

type CellStatus int

const (
	NewCell CellStatus = iota
	VisitedCell
	OutOfBoundsCell
	ObstacleCell
)

type Position struct {
	row       int
	col       int
	direction int
}

func (position Position) turn() Position {
	position.direction = (position.direction + 1) % 4
	return position
}

func (position Position) next() Position {
	directions := [4][2]int{{-1, 0}, {0, 1}, {1, 0}, {0, -1}}
	step := directions[position.direction]
	position.row += step[0]
	position.col += step[1]
	return position
}

func LoadInput(filePath string) (grid [][]string, guardPosition Position) {
	input, err := os.ReadFile(filePath)
	if err != nil {
		log.Fatalln("Error reading input file")
	}

	grid = [][]string{}
	guardPosition = Position{-1, -1, -1}
	guardFound := false
	for inputLine := range strings.SplitSeq(string(input), "\n") {
		if inputLine == "" {
			continue
		}
		gridLine := strings.Split(inputLine, "")
		if !guardFound {
			for i, char := range gridLine {
				if char == GuardChar {
					guardPosition = Position{len(grid), i, 0}
					gridLine[i] = VisitedChar
					guardFound = true
					break
				}
			}
		}
		grid = append(grid, gridLine)
	}

	if !guardFound {
		log.Fatalln("Guard not found on the grid")
	}
	return grid, guardPosition
}

func isOutOfBounds(grid [][]string, position Position) bool {
	return position.row < 0 || position.row >= len(grid) || position.col < 0 || position.col >= len(grid[0])
}

func moveToNextCell(grid [][]string, position Position, placeVisitedChar bool) (Position, CellStatus) {
	nextPosition := position.next()

	if !isOutOfBounds(grid, nextPosition) {
		switch grid[nextPosition.row][nextPosition.col] {

		case EmptyChar:
			if placeVisitedChar {
				grid[nextPosition.row][nextPosition.col] = VisitedChar
			}
			return nextPosition, NewCell

		case VisitedChar:
			return nextPosition, VisitedCell

		case ObstacleChar:
			return position.turn(), ObstacleCell

		default:
			log.Fatalln("Unknown character on the grid:", grid[nextPosition.row][nextPosition.col])
		}
	}

	return position, OutOfBoundsCell
}

func TrackGuardAndCountVisitedPlaces(grid [][]string, position Position) int {
	cellStatus := NewCell
	nVisitedPlaces := 1

	for cellStatus != OutOfBoundsCell {
		position, cellStatus = moveToNextCell(grid, position, true)
		if cellStatus == NewCell {
			nVisitedPlaces++
		}
	}

	return nVisitedPlaces
}

func getNewObstaclePosition(grid [][]string, position Position) (Position, bool) {
	obstaclePosition, status := moveToNextCell(grid, position, false)
	if status == ObstacleCell || status == OutOfBoundsCell || status == VisitedCell {
		return Position{}, false
	}
	return obstaclePosition, true
}

func containsCycle(grid [][]string, position Position, visitedPositions map[Position]bool) bool {
	localyVisitedPositions := make(map[Position]bool)
	maps.Copy(localyVisitedPositions, visitedPositions)

	cellStatus := NewCell
	for cellStatus != OutOfBoundsCell {
		if localyVisitedPositions[position] {
			return true
		}
		localyVisitedPositions[position] = true
		position, cellStatus = moveToNextCell(grid, position, false)
	}

	return false
}

func TrackGuardAndCountCreatedCycles(grid [][]string, position Position) int {
	nCycles := 0
	cellStatus := NewCell
	visitedPlaces := map[Position]bool{position: true}

	for cellStatus != OutOfBoundsCell {
		if obstaclePosition, ok := getNewObstaclePosition(grid, position); ok {
			grid[obstaclePosition.row][obstaclePosition.col] = ObstacleChar
			if containsCycle(grid, position.turn(), visitedPlaces) {
				nCycles++
			}
			grid[obstaclePosition.row][obstaclePosition.col] = EmptyChar
		}

		position, cellStatus = moveToNextCell(grid, position, true)
		visitedPlaces[position] = true
	}
	return nCycles
}

func main() {
	grid, guardPosition := LoadInput("input")
	nVisitedPlaces := TrackGuardAndCountVisitedPlaces(grid, guardPosition)
	fmt.Println("Number of visited places:", nVisitedPlaces)

	grid, guardPosition = LoadInput("input")
	nCreatedCycles := TrackGuardAndCountCreatedCycles(grid, guardPosition)
	fmt.Println("Number of created cycles:", nCreatedCycles)
}
