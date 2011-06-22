var json_data = {
id: "1.1.2.22",
name: "1.1.2.22",
data: { node_type: "ec", description: "<b>1.1.2.22:</b></br></br></br>", adjacencies: "<b>Adjacent nodes: </b></br>DB entries: </br>'DB6'</br>'DB2'</br>'DB1'</br>"},
children: [	{
	id: "DB6",
	name: "DB6",
	data: {description: "<b>DB6:</b></br>quux</br></br>", adjacencies: "<b>Adjacent nodes:</b></br>Reads: </br>'R4', bitscore: 780.0</br></br>Enzymes: </br>'1.1.2.22'<br>"},
	children: [	{
	id: "R4",
	name: "R4",
	data: {description: "<b>R4:</b></br>baz</br></br>", adjacencies: "<b>Adjacent nodes:</b></br>DB entries: </br>'DB6', bitscore: 780.0</br>"},
	children: []},
]},
	{
	id: "DB2",
	name: "DB2",
	data: {description: "<b>DB2:</b></br>quux</br></br>", adjacencies: "<b>Adjacent nodes:</b></br>Reads: </br>'R1', bitscore: 70.0</br>'R3', bitscore: 50.0</br></br>Enzymes: </br>'1.1.2.22'<br>'1.1.2.24'<br>"},
	children: [	{
	id: "R1",
	name: "R1",
	data: {description: "<b>R1:</b></br>baz</br></br>", adjacencies: "<b>Adjacent nodes:</b></br>DB entries: </br>'DB3', bitscore: 100.0</br>'DB2', bitscore: 70.0</br>'DB4', bitscore: 55.0</br>'DB1', bitscore: 50.0</br>"},
	children: [	{
	id: "DB3",
	name: "DB3",
	data: {description: "<b>DB3:</b></br>quux</br></br>", adjacencies: "<b>Adjacent nodes:</b></br>Reads: </br>'R1', bitscore: 100.0</br></br>Enzymes: </br>'1.1.2.23'<br>"},
	children: [	{
	id: "1.1.2.23",
	name: "1.1.2.23",
	data: {description: "<b>1.1.2.23:</b></br></br></br>", adjacencies: "<b>Adjacent nodes:</b></br>DB entries: </br>'DB3'</br>"},
	children: []},
]},
	{
	id: "DB4",
	name: "DB4",
	data: {description: "<b>DB4:</b></br>quux</br></br>", adjacencies: "<b>Adjacent nodes:</b></br>Reads: </br>'R1', bitscore: 55.0</br>'R5', bitscore: 30.0</br></br>Enzymes: </br>'1.1.2.24'<br>"},
	children: [	{
	id: "R5",
	name: "R5",
	data: {description: "<b>R5:</b></br>baz</br></br>", adjacencies: "<b>Adjacent nodes:</b></br>DB entries: </br>'DB4', bitscore: 30.0</br>"},
	children: []},
	{
	id: "1.1.2.24",
	name: "1.1.2.24",
	data: {description: "<b>1.1.2.24:</b></br></br></br>", adjacencies: "<b>Adjacent nodes:</b></br>DB entries: </br>'DB5'</br>'DB4'</br>'DB2'</br>"},
	children: [	{
	id: "DB5",
	name: "DB5",
	data: {description: "<b>DB5:</b></br>quux</br></br>", adjacencies: "<b>Adjacent nodes:</b></br>Reads: </br>'R2', bitscore: 90.0</br></br>Enzymes: </br>'1.1.2.24'<br>"},
	children: [	{
	id: "R2",
	name: "R2",
	data: {description: "<b>R2:</b></br>baz</br></br>", adjacencies: "<b>Adjacent nodes:</b></br>DB entries: </br>'DB5', bitscore: 90.0</br>'DB1', bitscore: 30.0</br>"},
	children: [	{
	id: "DB1",
	name: "DB1",
	data: {description: "<b>DB1:</b></br>quux</br></br>", adjacencies: "<b>Adjacent nodes:</b></br>Reads: </br>'R1', bitscore: 50.0</br>'R2', bitscore: 30.0</br></br>Enzymes: </br>'1.1.2.22'<br>"},
	children: []},
]},
]},
]},
]},
	{
	id: "DB1",
	name: "DB1",
	data: {description: "<b>DB1:</b></br>quux</br></br>", adjacencies: "<b>Adjacent nodes:</b></br>Reads: </br>'R1', bitscore: 50.0</br>'R2', bitscore: 30.0</br></br>Enzymes: </br>'1.1.2.22'<br>"},
	children: []},
]},
	{
	id: "R3",
	name: "R3",
	data: {description: "<b>R3:</b></br>baz</br></br>", adjacencies: "<b>Adjacent nodes:</b></br>DB entries: </br>'DB2', bitscore: 50.0</br>"},
	children: []},
	{
	id: "1.1.2.24",
	name: "1.1.2.24",
	data: {description: "<b>1.1.2.24:</b></br></br></br>", adjacencies: "<b>Adjacent nodes:</b></br>DB entries: </br>'DB5'</br>'DB4'</br>'DB2'</br>"},
	children: []},
]},
	{
	id: "DB1",
	name: "DB1",
	data: {description: "<b>DB1:</b></br>quux</br></br>", adjacencies: "<b>Adjacent nodes:</b></br>Reads: </br>'R1', bitscore: 50.0</br>'R2', bitscore: 30.0</br></br>Enzymes: </br>'1.1.2.22'<br>"},
	children: []},
]
};