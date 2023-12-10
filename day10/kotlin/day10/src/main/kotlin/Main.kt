import java.lang.StringBuilder

data class Coordinate(val row: Int, val col:Int, val value:Char)

data class Neighbours(
    val here:Coordinate,
    val up:Coordinate?,
    val down:Coordinate?,
    val left:Coordinate?,
    val right:Coordinate?,
)

enum class Direction{
    LEFT,
    RIGHT,
    UP,
    DOWN
}

fun allowedDirectionsByNodeValue(value:Char): List<Direction>{
    return when (value){
        '-'  -> listOf(Direction.LEFT, Direction.RIGHT)
        '|'  -> listOf(Direction.UP, Direction.DOWN)
        'L'  -> listOf(Direction.UP, Direction.RIGHT)
        'J'  -> listOf(Direction.UP, Direction.LEFT)
        '7'  -> listOf(Direction.LEFT, Direction.DOWN)
        'F'  -> listOf(Direction.DOWN, Direction.RIGHT)
        'S'  -> listOf(Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT)
        else -> listOf()
    }
}

fun getOppositeDirection(direction:Direction): Direction =
    when (direction){
        Direction.DOWN -> Direction.UP
        Direction.UP -> Direction.DOWN
        Direction.LEFT -> Direction.RIGHT
        Direction.RIGHT -> Direction.LEFT
    }

fun canMoveFromSourceToDestination(source:Coordinate, destination:Coordinate, direction:Direction) : Boolean{
    val allowedMovesFromSource = allowedDirectionsByNodeValue(source.value)
    // moves in to a destination are just flipped outbound moves for that symbol
    val allowedMovesToDestination = allowedDirectionsByNodeValue(destination.value).map{ getOppositeDirection(it) }

    // you can traverse from one symbol to the next
    // if one of the allowed outgoing moves from the source symbol exists in input moves of the destination symbol
    return direction in allowedMovesFromSource && direction in allowedMovesToDestination
}

fun getNeighbours(gameMap:List<String>, currentNode:Coordinate) : Neighbours{
    val row = currentNode.row
    val col = currentNode.col
    val boardHeight = gameMap.count()
    val boardWidth = gameMap[0].count()

    var up:Coordinate? = null
    var down:Coordinate? = null
    var left:Coordinate? = null
    var right:Coordinate? = null

    if(row > 0){
        up = Coordinate(row - 1, col, gameMap[row - 1][col])
    }
    if(row < boardHeight - 1){
        down = Coordinate(row + 1, col, gameMap[row + 1][col])
    }
    if(col > 0){
        left = Coordinate(row, col - 1, gameMap[row][col - 1])
    }
    if(col < boardWidth - 1){
        right = Coordinate(row, col + 1, gameMap[row][col + 1])
    }

    return Neighbours(here = currentNode, up, down, left, right)
}

fun translateCharForRendering(char:Char):Char =
    when(char){
        '-' -> '─'
        '|' -> '│'
        'F' -> '┌'
        'J' -> '┘'
        'L' -> '└'
        '7' -> '┐'
        else -> '#'
    }

fun main() {
    val rowList = object {}.javaClass.getResourceAsStream("input.txt")?.bufferedReader()?.readLines()
        ?: throw Error("row list was null")

    var startingRow = 0
    var startingCol = 0

    for (i in 0..<rowList.count()){
        if ('S' in rowList[i]){
            startingCol = rowList[i].indexOf('S')
            startingRow = i
            break
        }
    }
    val startingCoordinate = Coordinate(startingRow, startingCol, 'S')

    var currentCoordinate = startingCoordinate
    val visitedList = mutableListOf(startingCoordinate)
    var pathLength = 0


    // traverse until we arrive at a node with no available moves
    // this will be the last node in the circular path
    while(true){

        val neighbours = getNeighbours(rowList, currentCoordinate)
        if(neighbours.up != null){
            val canMoveUp = canMoveFromSourceToDestination(currentCoordinate, neighbours.up, Direction.UP)
            if(canMoveUp && neighbours.up !in visitedList){
                currentCoordinate = neighbours.up
                visitedList.add(currentCoordinate)
                pathLength += 1
                continue
            }
        }

        if(neighbours.down != null){
            val canMoveDown = canMoveFromSourceToDestination(currentCoordinate, neighbours.down, Direction.DOWN)
            if(canMoveDown && neighbours.down !in visitedList){
                currentCoordinate = neighbours.down
                visitedList.add(currentCoordinate)
                pathLength += 1
                continue
            }
        }

        if(neighbours.left != null){
            val canMoveLeft = canMoveFromSourceToDestination(currentCoordinate, neighbours.left, Direction.LEFT)
            if(canMoveLeft && neighbours.left !in visitedList){
                currentCoordinate = neighbours.left
                visitedList.add(currentCoordinate)
                pathLength += 1
                continue
            }
        }

        if(neighbours.right != null){
            val canMoveRight = canMoveFromSourceToDestination(currentCoordinate, neighbours.right, Direction.RIGHT)
            if(canMoveRight && neighbours.right !in visitedList){
                currentCoordinate = neighbours.right
                visitedList.add(currentCoordinate)
                pathLength += 1
                continue
            }
        }

        // hit a node with no move. Can assume we are done as we are explicitly told it is a looped path
        pathLength += 1
        break
    }

    println("Path Length = $pathLength")
    println("half Path Length = ${pathLength/2}")

    // for part 2, lets plog the thing with nice unicode box drawing characters
    // then pull the whole thing in to mspaint in order to solve

    val blankGameBoard = mutableListOf<String>()
    for (row in rowList){
        blankGameBoard.add("".padStart(row.length, '#'))
    }

    for( visited in visitedList ){
        val sb = StringBuilder(blankGameBoard[visited.row])
        sb.setCharAt(visited.col, visited.value)
        blankGameBoard[visited.row] = sb.toString()
    }

    val rendered = blankGameBoard.map{ row -> row.map { translateCharForRendering(it) }.joinToString(separator = "")}

    for ( row in rendered){
        println(row)
    }
}