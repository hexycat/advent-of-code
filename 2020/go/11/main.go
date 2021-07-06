package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strconv"
	"strings"
)

type waitingRoom [][]string
type seats []string

const (
	Empty    = "L"
	Occupied = "#"
	Floor    = "."
)

func main() {
	file := getFilePath()
	input := loadInput(file)

	for _, part := range []int{1, 2} {
		wr := newWaitingRoomFromFile(input)
		wr.simulate(part)
		fmt.Println("Total number of occupied seats", wr.nOccupied())
	}
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

func initWaitingRoom(h int, w int) waitingRoom {
	wr := make([][]string, h)
	for i := range wr {
		wr[i] = make([]string, w)
	}
	return wr
}

func newWaitingRoomFromFile(input []string) waitingRoom {
	wr := initWaitingRoom(len(input), len(input[0]))
	for i, s := range input {
		wr[i] = strings.Split(s, "")
	}
	return wr
}

func cloneWaitingRoom(src waitingRoom) waitingRoom {
	wr := initWaitingRoom(len(src), len(src[0]))
	for i, row := range src {
		for j, s := range row {
			wr[i][j] = s
		}
	}
	return wr
}

func (wr waitingRoom) getAdjacentSeatsPart1(i int, j int) seats {
	s := seats{}
	n, m := len(wr), len(wr[0])
	for _, r := range []int{i - 1, i, i + 1} {
		if (r < 0) || (r >= n) {
			continue
		}
		for _, c := range []int{j - 1, j, j + 1} {
			if (c < 0) || (c >= m) || ((c == j) && (r == i)) {
				continue
			}
			s = append(s, wr[r][c])
		}
	}
	return s
}

func (wr waitingRoom) getAdjacentSeatsPart2(i int, j int) seats {
	s := seats{}
	n, m := len(wr), len(wr[0])
	directions := [8][2]int{
		{0, -1},  // left
		{0, 1},   //right
		{1, 0},   // up
		{-1, 0},  // down
		{1, -1},  // upper-left
		{1, 1},   // upper-right
		{-1, 1},  // lower-right
		{-1, -1}, // lower-left
	}
	for d := 0; d < len(directions); d++ {
		delta_r, delta_c := directions[d][0], directions[d][1]
		r, c := i+delta_r, j+delta_c
		for (r >= 0) && (r < n) && (c >= 0) && (c < m) {
			if wr[r][c] != Floor {
				s = append(s, wr[r][c])
				break
			}
			r, c = r+delta_r, c+delta_c
		}
	}
	return s
}

func (s seats) nOccupied() int {
	return strings.Count(strings.Join(s, ""), Occupied)
}

func (wr waitingRoom) nOccupied() int {
	s := seats{}
	for i := 0; i < len(wr); i++ {
		s = append(s, strings.Join(wr[i], ""))
	}
	return strings.Count(strings.Join(s, ""), Occupied)
}

func newSeatStatePart1(s string, as seats) string {
	if (s == Empty) && (as.nOccupied() == 0) {
		return Occupied
	}
	if (s == Occupied) && (as.nOccupied() >= 4) {
		return Empty
	}
	return s
}

func newSeatStatePart2(s string, as seats) string {
	if (s == Empty) && (as.nOccupied() == 0) {
		return Occupied
	}
	if (s == Occupied) && (as.nOccupied() >= 5) {
		return Empty
	}
	return s
}

func (wr waitingRoom) playRound(part int) int {
	nChanges := 0
	src := cloneWaitingRoom(wr)
	for i, row := range src {
		for j, s := range row {
			switch part {
			case 2:
				wr[i][j] = newSeatStatePart2(s, src.getAdjacentSeatsPart2(i, j))
			default:
				wr[i][j] = newSeatStatePart1(s, src.getAdjacentSeatsPart1(i, j))
			}

			if wr[i][j] != s {
				nChanges += 1
			}
		}
	}
	return nChanges
}

func (wr waitingRoom) saveToFile(round int) {
	s := []string{}
	for _, r := range wr {
		s = append(s, strings.Join(r, ""))
	}
	d := strings.Join(s, "\n")
	ioutil.WriteFile(strconv.Itoa(round), []byte(d), 0777)
}

func (wr waitingRoom) simulate(part int) {
	fmt.Println("\nPart", part, "simulation starts")
	round := 0
	nChanges := 1
	for nChanges > 0 {
		nChanges = wr.playRound(part)
		round += 1
		fmt.Println("Round", round, "completed with", nChanges, "changes")
	}
}
