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

var rotationCommands = []string{Left, Right}
var movementCommands = []string{East, West, North, South}

type rotationMap map[string]string

type position struct {
	coords [2]int
	cp     [2]string
}

type Waypoint struct {
	p position
}

type Ship struct {
	face string
	p    position
}

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

var oppositeDirection = map[string]string{
	East:  West,
	West:  East,
	North: South,
	South: North,
}

func main() {

	input := loadInput(getFilePath())
	waypoint := Waypoint{p: position{
		coords: [2]int{10, 1},
		cp:     [2]string{East, North},
	}}
	ship := Ship{
		face: East,
		p:    position{cp: [2]string{East, North}},
	}
	for _, s := range input {
		direction, value := readCommand(s)
		if contains(rotationCommands, direction) {
			waypoint.rotate(direction, value)
		} else if contains(movementCommands, direction) {
			waypoint.move(direction, value)
		} else {
			ship.move(waypoint, value)
		}
	}
	fmt.Println("Manhattan distance of the ship is", ship.p.manhattan())
}

func (p *position) rotate(direction string, degrees int) {
	for i := 0; i < int(degrees/90); i++ {
		(*p).cp[0] = rMap[direction][(*p).cp[0]]
		(*p).cp[1] = rMap[direction][(*p).cp[1]]
	}
	fmt.Println("Rotate position", direction, degrees, "facing", (*p).cp)
}

func (p *position) move(direction string, steps int) {
	for i := range []int{0, 1} {
		cardinal_point := (*p).cp[i]
		if direction == cardinal_point {
			(*p).coords[i] += steps
		} else if oppositeDirection[direction] == cardinal_point {
			(*p).coords[i] -= steps
		}
	}
}

func (wp *Waypoint) move(direction string, steps int) {
	wp.p.move(direction, steps)
}

func (wp *Waypoint) rotate(direction string, value int) {
	wp.p.rotate(direction, value)
}

func (sh *Ship) move(wp Waypoint, steps int) {
	for i := range []int{0, 1} {
		(*sh).p.move(wp.p.cp[i], steps*wp.p.coords[i])
	}
	fmt.Println("Moving ship to position", (*sh).p)
}

func (p position) manhattan() int {
	return int(math.Abs(float64(p.coords[0])) + math.Abs(float64(p.coords[1])))
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
