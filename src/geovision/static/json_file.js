var json_data = {
id: "1.1.2.22",
name: "1.1.2.22",
data: { node_type: "ec", description: "<b>1.1.2.22:</b></br></br></br>", adjacencies: "<b>Adjacent nodes: </b></br>DB entries: </br>'DB2'</br>'DB6'</br>"},
children: [	{
	id: "DB2",
	name: "DB2",
	data: {description: "<b>DB2:</b></br>quux</br></br>", adjacencies: "<b>Adjacent nodes:</b></br>Reads: </br>'R1', bitscore: 1600.0</br>'R3', bitscore: 500.0</br>'R2', bitscore: 330.0</br></br>Enzymes: </br>'1.1.2.22'<br>'1.1.2.24'<br>"},
	children: [	{
	id: "R1",
	name: "R1",
	data: {description: "<b>R1:</b></br>baz</br></br>"},
	children: []
	},	{
	id: "R3",
	name: "R3",
	data: {description: "<b>R3:</b></br>baz</br></br>"},
	children: []
	},	{
	id: "R2",
	name: "R2",
	data: {description: "<b>R2:</b></br>baz</br></br>"},
	children: []
	},	{
	id: "1.1.2.24",
	name: "1.1.2.24",
	data: {description: "<b>1.1.2.24:</b></br></br></br>"},
	children: []
	},]},
	{
	id: "DB6",
	name: "DB6",
	data: {description: "<b>DB6:</b></br>quux</br></br>", adjacencies: "<b>Adjacent nodes:</b></br>Reads: </br>'R4', bitscore: 780.0</br></br>Enzymes: </br>'1.1.2.22'<br>"},
	children: [	{
	id: "R4",
	name: "R4",
	data: {description: "<b>R4:</b></br>baz</br></br>"},
	children: []
	},]},
]
};