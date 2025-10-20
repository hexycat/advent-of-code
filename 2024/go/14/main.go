package main

import (
	"fmt"
	"log"
	"os"
	"strings"
)

const (
	SpaceWidth  = 101
	SpaceHeight = 103
)

type Robot struct {
	Position [2]int
	Velocity [2]int
}

func (robot *Robot) MoveFor(seconds int) {
	robot.Position[0] = (robot.Position[0] + robot.Velocity[0]*seconds) % SpaceWidth
	if robot.Position[0] < 0 {
		robot.Position[0] += SpaceWidth
	}

	robot.Position[1] = (robot.Position[1] + robot.Velocity[1]*seconds) % SpaceHeight
	if robot.Position[1] < 0 {
		robot.Position[1] += SpaceHeight
	}
}

func loadInput(filePath string) []Robot {
	input, err := os.ReadFile(filePath)
	if err != nil {
		log.Fatalln("Failed to read input file:", err)
	}

	robots := []Robot{}
	for line := range strings.SplitSeq(string(input), "\n") {
		if line == "" {
			continue
		}

		robot := &Robot{}
		_, err := fmt.Sscanf(line, "p=%d,%d v=%d,%d",
			&robot.Position[0], &robot.Position[1], &robot.Velocity[0], &robot.Velocity[1])
		if err != nil {
			log.Fatalln("Failed to parse line:", err)
		}
		robots = append(robots, *robot)
	}

	return robots
}

func moveRobotsFor(robots *[]Robot, seconds int) {
	for i := range *robots {
		(*robots)[i].MoveFor(seconds)
	}
}

func countRobotsInQuadrants(robots *[]Robot) [4]int {
	counts := [4]int{}

	for _, robot := range *robots {
		x, y := robot.Position[0], robot.Position[1]
		if x < SpaceWidth/2 && y < SpaceHeight/2 {
			counts[0]++
		} else if x > SpaceWidth/2 && y < SpaceHeight/2 {
			counts[1]++
		} else if x < SpaceWidth/2 && y > SpaceHeight/2 {
			counts[2]++
		} else if x > SpaceWidth/2 && y > SpaceHeight/2 {
			counts[3]++
		}
	}

	return counts
}

func calculateSafetyScore(robots *[]Robot) int {
	score := 1
	robotsInQuadrants := countRobotsInQuadrants(robots)
	for _, count := range robotsInQuadrants {
		score *= max(1, count)
	}
	return score
}

func printEntireSpace(robots *[]Robot) {
	space := make([][]rune, SpaceHeight)
	for i := range space {
		space[i] = make([]rune, SpaceWidth)
		for j := range SpaceWidth {
			space[i][j] = '.'
		}
	}

	for _, robot := range *robots {
		x, y := robot.Position[0], robot.Position[1]
		space[y][x] = '#'
	}

	for _, row := range space {
		fmt.Println(string(row))
	}
}

func isPossibleTree(robots *[]Robot, minRobotsInARow int) bool {
	// Looking for at least 'minRobotsSeq' robots in a row horizontally
	takenPositions := make(map[[2]int]bool)
	for _, robot := range *robots {
		takenPositions[robot.Position] = true
	}

	for _, robot := range *robots {
		robotsInARow := 1
		x, y := robot.Position[0], robot.Position[1]

		for true {
			x += 1
			if _, exists := takenPositions[[2]int{x, y}]; !exists {
				break
			}

			robotsInARow++
			if robotsInARow == minRobotsInARow {
				return true
			}
		}
	}

	return false
}

func searchForTreePattern(robots *[]Robot, minRobotsInARow int) int {
	possibleTree := false
	seconds := 0

	for !possibleTree {
		seconds++
		moveRobotsFor(robots, 1)
		possibleTree = isPossibleTree(robots, minRobotsInARow)
	}

	return seconds
}

func main() {
	robots := loadInput("input")

	moveRobotsFor(&robots, 100)
	safetyScore := calculateSafetyScore(&robots)
	fmt.Println("Safety Score after 100 seconds:", safetyScore)

	robots = loadInput("input")
	secondsToTreePattern := searchForTreePattern(&robots, 10)
	fmt.Println("Seconds elapsed to form tree pattern:", secondsToTreePattern)
	printEntireSpace(&robots)
}
