package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func loadInput(filePath string) map[int]int {
	input, err := os.ReadFile(filePath)
	if err != nil {
		log.Fatalln("Error reading the file", filePath)
	}

	stones := map[int]int{}
	for stoneStr := range strings.SplitSeq(strings.Trim(string(input), "\n"), " ") {
		stone, err := strconv.Atoi(stoneStr)
		if err != nil {
			log.Fatalln("Error converting stone", stoneStr, "to integer")
		}
		stones[stone]++
	}
	return stones
}

func splitStoneStr(stoneStr string) (int, int) {
	leftStone, _ := strconv.Atoi(stoneStr[:len(stoneStr)/2])
	rightStone, _ := strconv.Atoi(stoneStr[len(stoneStr)/2:])
	return leftStone, rightStone
}

func blink(stones map[int]int) map[int]int {
	changes := map[int]int{}
	for stone, times := range stones {
		if stone == 0 {
			changes[1] += times
			continue
		}

		stoneStr := strconv.Itoa(stone)
		if len(stoneStr)%2 == 0 {
			left, right := splitStoneStr(stoneStr)
			changes[left] += times
			changes[right] += times
			continue
		}

		changes[stone*2024] += times
	}
	return changes
}

func blinkNTimes(stones map[int]int, times int) map[int]int {
	for range times {
		stones = blink(stones)
	}
	return stones
}

func numberOfStones(stones map[int]int) int {
	count := 0
	for _, times := range stones {
		count += times
	}
	return count
}

func main() {
	stones := loadInput("input")

	fmt.Println("Number of stones after 25 blinks:", numberOfStones(blinkNTimes(stones, 25)))
	fmt.Println("Number of stones after 75 blinks:", numberOfStones(blinkNTimes(stones, 75)))
}
