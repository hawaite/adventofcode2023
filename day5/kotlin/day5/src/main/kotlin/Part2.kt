object Part2 {
    data class AlmanacMap(val mapType:String, val mapRanges: List<AlmanacMapRange>)
    data class AlmanacMapRange(val sourceRangeStart: Long, val destRangeStart: Long, val rangeLength: Long)

    private fun numberIsInRange(number:Long, almanacMapRange: AlmanacMapRange): Boolean {
        return number in almanacMapRange.sourceRangeStart..almanacMapRange.sourceRangeStart+almanacMapRange.rangeLength
    }

    private fun parseAlmanac(rowList: List<String>): Map<String, AlmanacMap>{
        val numberRowRegex = Regex("""^(\d+) (\d+) (\d+)$""")
        val mapLabelRegex = Regex("""^([a-z]+-to-[a-z]+) map:$""")

        var currentMapLabel = ""
        var currentMapsRanges = mutableListOf<AlmanacMapRange>()
        val almanacMaps = mutableMapOf<String, AlmanacMap>()

        for (row in rowList){
            if( mapLabelRegex.matches(row)){
                currentMapLabel = mapLabelRegex.find(row)!!.groupValues[1]
            }
            else if( numberRowRegex.matches(row) ){
                val rowNumbers = numberRowRegex.findAll(row).toList()
                val destRangeStart = rowNumbers[0].groupValues[1]
                val sourceRangeStart = rowNumbers[0].groupValues[2]
                val rangeLen = rowNumbers[0].groupValues[3]

                currentMapsRanges.add(AlmanacMapRange(sourceRangeStart.toLong(), destRangeStart.toLong(), rangeLen.toLong()))
            }
            else if ( row == "" ){
                // end of map definition
                almanacMaps[currentMapLabel] = AlmanacMap(currentMapLabel, currentMapsRanges)
                currentMapsRanges = mutableListOf()
            }
        }

        return almanacMaps
    }

    private fun performTransform(map: AlmanacMap, input: String ):String{
        var foundMappedVal = ""
        for ( range in map.mapRanges ){
            if (numberIsInRange(input.toLong(), range)){
                // need to get the difference between input value and the start of the source range
                val diff = input.toLong() - range.sourceRangeStart
                val mapped = range.destRangeStart + diff
                foundMappedVal = mapped.toString()
                // then add that value to the destination range
                // then return that value
                break
            }
        }
        if(foundMappedVal == "")
            foundMappedVal = input
        return foundMappedVal
    }

    private fun parseSeedRow(seedRow: String): List<LongRange> {
        val seedLst = seedRow.split(" ").drop(1)
        val rangeList = mutableListOf<LongRange>()
        for ( i in 0..<seedLst.count() step 2){
            rangeList.add(LongRange(seedLst[i].toLong(), seedLst[i].toLong() + seedLst[i+1].toLong() - 1))
        }

        return rangeList
    }

    fun solve(rowList: List<String>){

        val seedList = parseSeedRow(rowList[0])
        println(seedList)
        val almanacMaps = parseAlmanac(rowList.slice(2..<rowList.count()))

        val startTime = System.currentTimeMillis()
        val locationList =
            seedList[0]
                .asSequence()
                .map { performTransform(almanacMaps["seed-to-soil"]!!, it.toString()) }
                .map { performTransform(almanacMaps["soil-to-fertilizer"]!!, it) }
                .map { performTransform(almanacMaps["fertilizer-to-water"]!!, it) }
                .map { performTransform(almanacMaps["water-to-light"]!!, it) }
                .map { performTransform(almanacMaps["light-to-temperature"]!!, it) }
                .map { performTransform(almanacMaps["temperature-to-humidity"]!!, it) }
                .map { performTransform(almanacMaps["humidity-to-location"]!!, it) }
                .toList()
        println("transformation performed in : ${System.currentTimeMillis() - startTime} ms")

        println(locationList)
        println(locationList.minOfOrNull { it.toLong() })
    }
}