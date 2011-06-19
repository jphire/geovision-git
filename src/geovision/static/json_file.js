var json_data = {
id: "DB1",
name: "DB1",
data: { adjacencies:"Read: 'R1', bitscore: 50.0</br>Read: 'R2', bitscore: 30.0</br>Enzyme: '1.1.2.22'</br>"},
children: [	{
	id: "R1",
	name: "R1",
	data: {parent: "DB enntry: 'DB1'</br>", dbentrys: "DB entry: 'DB2'</br>DB entry: 'DB3'</br>DB entry: 'DB4'</br>"},
	children: [	{
	id: "DB2",
	name: "DB2",
	data: {parent: "Read: 'R1'</br>", reads: "Read: 'R3'</br>", enzymes: "Enzyme: '1.1.2.22'<br>Enzyme: '1.1.2.24'<br>"},
	children: [	{
	id: "R3",
	name: "R3",
	data: {parent: "DB entry: 'DB2'</br>", dbentrys: ""},
	children: []},
	{
	id: "1.1.2.22",
	name: "1.1.2.22",
	data: {parent: "DB entry: 'DB2'</br>", dbentrys: "DB entry: 'DB6'</br>"},
	children: [	{
	id: "DB6",
	name: "DB6",
	data: {parent: "Enzyme: '1.1.2.22'</br>", reads: "Read: 'R4'</br>", enzymes: ""},
	children: [	{
	id: "R4",
	name: "R4",
	data: {parent: "DB entry: 'DB6'</br>", dbentrys: ""},
	children: []},
]},
]},
	{
	id: "1.1.2.24",
	name: "1.1.2.24",
	data: {parent: "DB entry: 'DB2'</br>", dbentrys: "DB entry: 'DB5'</br>DB entry: 'DB4'</br>"},
	children: [	{
	id: "DB5",
	name: "DB5",
	data: {parent: "Enzyme: '1.1.2.24'</br>", reads: "Read: 'R2'</br>", enzymes: ""},
	children: [	{
	id: "R2",
	name: "R2",
	data: {parent: "DB entry: 'DB5'</br>", dbentrys: ""},
	children: []},
]},
	{
	id: "DB4",
	name: "DB4",
	data: {parent: "Enzyme: '1.1.2.24'</br>", reads: "Read: 'R5'</br>", enzymes: ""},
	children: [	{
	id: "R5",
	name: "R5",
	data: {parent: "DB entry: 'DB4'</br>", dbentrys: ""},
	children: []},
]},
]},
]},
	{
	id: "DB3",
	name: "DB3",
	data: {parent: "Read: 'R1'</br>", reads: "", enzymes: "Enzyme: '1.1.2.23'<br>"},
	children: [	{
	id: "1.1.2.23",
	name: "1.1.2.23",
	data: {parent: "DB entry: 'DB3'</br>", dbentrys: ""},
	children: []},
]},
	{
	id: "DB4",
	name: "DB4",
	data: {parent: "Read: 'R1'</br>", reads: "", enzymes: ""},
	children: []},
]},
	{
	id: "R2",
	name: "R2",
	data: {parent: "DB entry: 'DB1'</br>", dbentrys: ""},
	children: []},
	{
	id: "1.1.2.22",
	name: "1.1.2.22",
	data: {parent: "DB entry: 'DB1'</br>", dbentrys: ""},
	children: []},
]
};