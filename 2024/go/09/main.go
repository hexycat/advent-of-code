package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

const FreeSpace = -1

type Archive struct {
	pointers []int
	files    []int
}

func (Archive) New(size int) Archive {
	archive := Archive{
		pointers: make([]int, size),
		files:    make([]int, size),
	}
	for idx := range size {
		archive.files[idx] = FreeSpace
	}
	return archive
}

func (archive *Archive) CheckSum() int {
	sum := 0
	pos := 0
	for idx := range len(archive.pointers) {
		for _ = range archive.pointers[idx] {
			sum += max(archive.files[idx], 0) * pos
			pos++
		}
	}
	return sum
}

func (archive *Archive) movePart(fromIdx, toIdx int) bool {
	if archive.files[fromIdx] == FreeSpace || archive.files[toIdx] != FreeSpace {
		return false
	}

	partSize := min(archive.pointers[fromIdx], archive.pointers[toIdx])
	leftSpace := archive.pointers[toIdx] - partSize

	archive.pointers[toIdx] = partSize
	archive.files[toIdx] = archive.files[fromIdx]

	archive.pointers[fromIdx] -= partSize
	if archive.pointers[fromIdx] == 0 {
		archive.files[fromIdx] = FreeSpace
	}

	if leftSpace > 0 {
		copy(archive.pointers[toIdx+1:fromIdx+1], archive.pointers[toIdx:fromIdx])
		copy(archive.files[toIdx+1:fromIdx+1], archive.files[toIdx:fromIdx])
		archive.pointers[toIdx+1] = leftSpace
		archive.files[toIdx+1] = FreeSpace
	}

	return true
}

func (archive *Archive) moveEntireFile(fromIdx, toIdx int) bool {
	fileSize := archive.pointers[fromIdx]
	freeSpace := archive.pointers[toIdx]

	if fileSize > freeSpace {
		return false
	}

	if fileSize == freeSpace {
		archive.files[toIdx] = archive.files[fromIdx]
		archive.files[fromIdx] = FreeSpace
		return true
	}

	newArchive := archive.New(len(archive.pointers) + 1)
	copy(newArchive.pointers[:toIdx], archive.pointers[:toIdx])
	copy(newArchive.files[:toIdx], archive.files[:toIdx])
	// Move file to the free space
	newArchive.pointers[toIdx] = fileSize
	newArchive.files[toIdx] = archive.files[fromIdx]
	// Update the free space next to the moved file
	newArchive.pointers[toIdx+1] = freeSpace - fileSize
	newArchive.files[toIdx+1] = FreeSpace
	// Copy the rest of the archive
	copy(newArchive.pointers[toIdx+2:], archive.pointers[toIdx+1:])
	copy(newArchive.files[toIdx+2:], archive.files[toIdx+1:])
	// Mark the original file position as free space
	newArchive.pointers[fromIdx+1] = fileSize
	newArchive.files[fromIdx+1] = FreeSpace

	*archive = newArchive
	return true
}

func (archive *Archive) Compress() {
	fileIdx := len(archive.files) - 1
	freeSpaceIdx := 0

	for fileIdx > freeSpaceIdx {
		if archive.files[freeSpaceIdx] != FreeSpace {
			freeSpaceIdx++
			continue
		}
		if archive.files[fileIdx] == FreeSpace {
			fileIdx--
			continue
		}
		archive.movePart(fileIdx, freeSpaceIdx)
	}
}

func (archive *Archive) Compress2() {
	for fileIdx := len(archive.pointers) - 1; fileIdx >= 0; fileIdx-- {
		if archive.files[fileIdx] == FreeSpace {
			continue
		}

		for freeSpaceIdx := 0; freeSpaceIdx < fileIdx; freeSpaceIdx++ {
			if archive.files[freeSpaceIdx] != FreeSpace {
				continue
			}
			if archive.moveEntireFile(fileIdx, freeSpaceIdx) {
				break
			}
		}
	}
}

func loadInput(filePath string) []int {
	input, err := os.ReadFile(filePath)
	if err != nil {
		log.Fatalln("Error reading the file", filePath)
	}

	diskMap := []int{}
	for idx, char := range strings.Split(strings.TrimRight(string(input), "\n"), "") {
		number, err := strconv.Atoi(char)
		if err != nil {
			log.Fatalln("Error converting character", char, "to integer at index", idx)
		}
		diskMap = append(diskMap, number)
	}
	return diskMap
}

func createArchiveFromDiskMap(diskMap []int) Archive {
	archive := Archive{}.New(len(diskMap))
	copy(archive.pointers, diskMap)
	for idx := range len(diskMap) {
		if idx%2 == 0 {
			archive.files[idx] = idx / 2
		}
	}
	return archive
}

func main() {
	diskMap := loadInput("input")

	archive := createArchiveFromDiskMap(diskMap)
	archive.Compress()
	fmt.Println("Checksum after compression 1:", archive.CheckSum())

	archive = createArchiveFromDiskMap(diskMap)
	archive.Compress2()
	fmt.Println("Checksum after compression 2:", archive.CheckSum())
}
