-- projects table
CREATE TABLE IF NOT EXISTS Cards (
	Id INTEGER PRIMARY KEY,
	Name TEXT NOT NULL,
	Japanese TEXT,
	Star INTEGER,
	Cost INTEGER,
	Class TEXT,
	Type INTEGER,
	ATK TEXT,
	HP TEXT,
	GrailATKLV100 INTEGER,
	GrailATKLV120 INTEGER,
	GrailHPLV100 INTEGER,
	GrailHPLV120 INTEGER,
	AKA TEXT,
	Alignments TEXT,
    Growth TEXT,
	Attribute TEXT,
	Gender TEXT,
	Traits TEXT
);