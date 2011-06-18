var json_data = {
id: "1.1.2.22",
name: "1.1.2.22",
data: { adjancies:"DB6:</br>DB6</br>DB2:</br>DB2</br>DB1:</br>DB1</br>"},
children: [	{
	id: "DB6",
	name: "DB6",
	data: [{parent: "1.1.2.22"}, {R4:"R4"}],
	children: [	{
	id: "R4",
	name: "R4",
	data: [{parent: "DB6"},],
	children: []},
]},
	{
	id: "DB2",
	name: "DB2",
	data: [{parent: "1.1.2.22"}, {R1:"R1"},{"1.1.2.24":"1.1.2.24"}],
	children: [	{
	id: "R1",
	name: "R1",
	data: [{parent: "DB2"}, {DB3:"DB3"},{DB4:"DB4"}],
	children: [	{
	id: "DB3",
	name: "DB3",
	data: [{parent: "R1"}, {"1.1.2.23":"1.1.2.23"}],
	children: [	{
	id: "1.1.2.23",
	name: "1.1.2.23",
	data: [{parent: "DB3"},],
	children: []},
]},
	{
	id: "DB4",
	name: "DB4",
	data: [{parent: "R1"}, {R5:"R5"},{"1.1.2.24":"1.1.2.24"}],
	children: [	{
	id: "R5",
	name: "R5",
	data: [{parent: "DB4"},],
	children: []},
	{
	id: "1.1.2.24",
	name: "1.1.2.24",
	data: [{parent: "DB4"}, {DB5:"DB5"}],
	children: [	{
	id: "DB5",
	name: "DB5",
	data: [{parent: "1.1.2.24"}, {R2:"R2"}],
	children: []
	},]},
]},
]},
	{
	id: "1.1.2.24",
	name: "1.1.2.24",
	data: [{parent: "DB2"},],
	children: []},
]},
	{
	id: "DB1",
	name: "DB1",
	data: [{parent: "1.1.2.22"}, {R2:"R2"}],
	children: [	{
	id: "R2",
	name: "R2",
	data: [{parent: "DB1"},],
	children: []},
]},
]
};