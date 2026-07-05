package main

import (
	"fmt"
	"os"
	"slices"
	"strings"
)

const (
	Wall         = '#'
	Empty        = '.'
	Robot        = '@'
	Box          = 'O'
	Left         = '<'
	Right        = '>'
	Up           = '^'
	Down         = 'v'
	WideBoxLeft  = '['
	WideBoxRight = ']'
)

type Direction [2]int

func (d Direction) Reverse() Direction {
	return Direction{-d[0], -d[1]}
}

func (d Direction) IsVertical() bool {
	return d[0] != 0
}

type Position [2]int

func (p Position) Next(direction Direction) Position {
	return Position{p[0] + direction[0], p[1] + direction[1]}
}

func (p *Position) Move(direction Direction) {
	p[0] += direction[0]
	p[1] += direction[1]
}

type Warehouse [][]rune

func (w Warehouse) get(position Position) rune {
	return w[position[0]][position[1]]
}

func (w Warehouse) set(position Position, value rune) {
	w[position[0]][position[1]] = value
}

func (w Warehouse) moveBox(from Position, to Position) {
	if w.get(to) != Empty {
		return
	}

	char := w.get(from)
	if char == Empty || char == Wall {
		return
	}

	w.set(to, char)
	w.set(from, Empty)
}

type charExpansion map[rune][]rune

type boxMover func(warehouse *Warehouse, position Position, direction Direction) (boxMoved bool)

type GameEngine struct {
	tileMap   charExpansion
	moveBox   boxMover
	scoreChar rune
}

func (ge *GameEngine) deserializeInput(input []byte) (warehouse Warehouse, moves []rune, position Position) {
	movesSegment := false
	lines := strings.Split(string(input), "\n")

	for row := range lines {
		if lines[row] == "" && !movesSegment {
			movesSegment = true
			continue
		}

		if movesSegment {
			for _, char := range lines[row] {
				moves = append(moves, char)
			}
			continue
		}

		// Warehouse mapping segment
		line := []rune{}
		for _, char := range lines[row] {
			if char == Robot {
				position = Position{row, len(line)}
			}
			line = append(line, ge.tileMap[char]...)
		}
		warehouse = append(warehouse, line)

	}

	return warehouse, moves, position
}

func (ge *GameEngine) score(warehouse Warehouse) int {
	sum := 0
	for row := range warehouse {
		for col := range warehouse[row] {
			if warehouse[row][col] == ge.scoreChar {
				sum += 100*row + col
			}
		}
	}
	return sum
}

func (ge *GameEngine) simulate(warehouse *Warehouse, position *Position, moves []rune) {
	for _, move := range moves {

		direction := moveToDirection[move]
		nextPosition := position.Next(direction)

		switch warehouse.get(nextPosition) {
		case Empty:
			*position = nextPosition
		case Box, WideBoxLeft, WideBoxRight:
			if ge.moveBox(warehouse, nextPosition, direction) {
				*position = nextPosition
			}
		}
	}
}

var (
	slimExpansion = charExpansion{
		Wall:  {Wall},
		Empty: {Empty},
		Box:   {Box},
		Robot: {Empty},
	}

	wideExpansion = charExpansion{
		Wall:  {Wall, Wall},
		Empty: {Empty, Empty},
		Box:   {WideBoxLeft, WideBoxRight},
		Robot: {Empty, Empty},
	}

	moveToDirection = map[rune]Direction{
		Left:  {0, -1},
		Right: {0, 1},
		Up:    {-1, 0},
		Down:  {1, 0},
	}
)

func Must[T any](x T, err error) T {
	if err != nil {
		panic(err)
	}
	return x
}

func moveSlimBox(warehouse *Warehouse, position Position, direction Direction) (boxMoved bool) {
	startPosition := position
	reverseDirection := direction.Reverse()

	// Check if the box can be moved in the given direction.
	for {
		if warehouse.get(position) == Empty {
			break
		} else if warehouse.get(position) == Wall {
			return false
		}
		position.Move(direction)
	}

	// Move the box to the empty space, moving all boxes in the way.
	for position != startPosition {
		previousPosition := position.Next(reverseDirection)
		warehouse.moveBox(previousPosition, position)
		position = previousPosition
	}

	warehouse.set(startPosition, Empty)
	return true
}

// When working with wide boxes, it's easier to track only the left side of the box.
// Given that right side of the box is always to the right of the left side,
// we can calculate its position as needed.
func moveWideBoxVertical(warehouse *Warehouse, position Position, direction Direction) (boxMoved bool) {
	if warehouse.get(position) == WideBoxRight {
		position = position.Next(Direction{0, -1})
	}

	boxesToMove := []Position{position}
	boxesToCheck := []Position{position}

	// Collect information about all boxes that need to be moved, and check if the move is valid.
	for {
		newBoxesToMove := []Position{}
		for _, box := range boxesToCheck {
			nextLeft := box.Next(direction)
			nextRight := nextLeft.Next(Direction{0, 1})

			switch warehouse.get(nextLeft) {
			case WideBoxLeft:
				newBoxesToMove = append(newBoxesToMove, nextLeft)
			case WideBoxRight:
				newBoxesToMove = append(newBoxesToMove, nextLeft.Next(Direction{0, -1}))
			case Wall:
				return false
			}

			switch warehouse.get(nextRight) {
			case WideBoxLeft:
				newBoxesToMove = append(newBoxesToMove, nextRight)
			case Wall:
				return false
			}
		}

		if len(newBoxesToMove) == 0 {
			break
		}

		boxesToMove = append(boxesToMove, newBoxesToMove...)
		boxesToCheck = newBoxesToMove
	}

	// Move all boxes in reverse order to avoid overwriting boxes that haven't been moved yet.
	for _, left := range slices.Backward(boxesToMove) {
		right := left.Next(Direction{0, 1})

		warehouse.moveBox(left, left.Next(direction))
		warehouse.moveBox(right, right.Next(direction))
	}

	return true
}

func moveWideBox(warehouse *Warehouse, position Position, direction Direction) (boxMoved bool) {
	if direction.IsVertical() {
		return moveWideBoxVertical(warehouse, position, direction)
	}
	return moveSlimBox(warehouse, position, direction)
}

func main() {
	input := Must(os.ReadFile("input"))

	partOneEngine := GameEngine{
		tileMap:   slimExpansion,
		moveBox:   moveSlimBox,
		scoreChar: Box,
	}

	warehouse, moves, robotPosition := partOneEngine.deserializeInput(input)
	partOneEngine.simulate(&warehouse, &robotPosition, moves)
	fmt.Println("Part 1: Sum of boxes GPS coordinates after robot movements -", partOneEngine.score(warehouse))

	partTwoEngine := GameEngine{
		tileMap:   wideExpansion,
		moveBox:   moveWideBox,
		scoreChar: WideBoxLeft,
	}

	wideWarehouse, moves, robotPosition := partTwoEngine.deserializeInput(input)
	partTwoEngine.simulate(&wideWarehouse, &robotPosition, moves)
	fmt.Println("Part 2: Sum of boxes GPS coordinates after robot movements -", partTwoEngine.score(wideWarehouse))
}
