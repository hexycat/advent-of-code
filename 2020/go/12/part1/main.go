package main

import (
	"fmt"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

const (
	East    = "E"
	West    = "W"
	North   = "N"
	South   = "S"
	Forward = "F"
	Left    = "L"
	Right   = "R"
)

type position [2]int
type rotationMap map[string]string

type Ship struct {
	face string
	p    position
}

var rotationCommands = []string{Left, Right}
var movementCommands = []string{Forward, East, West, North, South}

var rightRotation = rotationMap{
	North: East,
	East:  South,
	South: West,
	West:  North,
}

var leftRotation = rotationMap{
	North: West,
	West:  South,
	South: East,
	East:  North,
}

var rMap = map[string]rotationMap{
	Right: rightRotation,
	Left:  leftRotation,
}

var directionMap = map[string]int{
	North: 1,
	South: 1,
	East:  0,
	West:  0,
}

func (p *position) change(direction string, value int) {
	switch direction {
	case East:
		(*p)[0] += value
	case West:
		(*p)[0] -= value
	case North:
		(*p)[1] += value
	case South:
		(*p)[1] -= value
	}
}

func main() {

	input := loadInput(getFilePath())
	ship := Ship{face: East}
	for _, s := range input {
		direction, value := readCommand(s)
		if contains(rotationCommands, direction) {
			ship.rotate(direction, value)
		} else if contains(movementCommands, direction) {
			ship.move(direction, value)
		}
	}
	fmt.Println("Manhattan distance of the ship is", ship.p.manhattan())
}

func (sh *Ship) rotate(direction string, degrees int) {
	for i := 0; i < int(degrees/90); i++ {
		(*sh).face = rMap[direction][(*sh).face]
	}
	fmt.Println("Rotate", direction, degrees, "facing", (*sh).face)

}

func (sh *Ship) move(direction string, steps int) {
	if direction == Forward {
		direction = (*sh).face
	}
	(*sh).p.change(direction, steps)
	fmt.Println("Move", direction, steps, "position", (*sh).p)
}

func (p position) manhattan() int {
	return int(math.Abs(float64(p[0])) + math.Abs(float64(p[1])))
}

func getFilePath() string {
	if len(os.Args) < 2 {
		return "input"
	} else {
		return os.Args[1]
	}
}

func loadInput(file string) []string {
	input, err := os.ReadFile(file)
	if err != nil {
		log.Fatalln("Error on reading input file", err)
	}
	return strings.Split(string(input), "\n")
}

func readCommand(s string) (string, int) {
	splits := strings.Split(s, "")
	value, _ := strconv.Atoi(strings.Join(splits[1:], ""))
	return splits[0], value
}

func contains(s []string, e string) bool {
	for _, a := range s {
		if a == e {
			return true
		}
	}
	return false
}
