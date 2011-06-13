var json_data = {
id: "DB1",
name: "DB1",
data: [{R001:"R001"}, {R002:"R002"}, ],
children: [	{
	id: "R001",
	name: "R001",
	data: [{parent: "DB1"}, {DB2:"DB2"},{DB3:"DB3"}],
	children: [	{
	id: "DB2",
	name: "DB2",
	data: [{parent: "R001"}, {"1.1.2.22":"1.1.2.22"},{"1.1.2.24":"1.1.2.24"}],
	children: [	{
	id: "1.1.2.22",
	name: "1.1.2.22",
	data: [{parent: "DB2"}, {DB6:"DB6"}],
	children: [	{
	id: "DB6",
	name: "DB6",
	data: [{parent: "1.1.2.22"}, {R004:"R004"}],
	children: [	{
	id: "R004",
	name: "R004",
	data: [{parent: "DB6"},],
	children: []},
]},
]},
	{
	id: "1.1.2.24",
	name: "1.1.2.24",
	data: [{parent: "DB2"}, {DB5:"DB5"},{DB4:"DB4"}],
	children: [	{
	id: "DB5",
	name: "DB5",
	data: [{parent: "1.1.2.24"}, {R002:"R002"}],
	children: [	{
	id: "R002",
	name: "R002",
	data: [{parent: "DB5"}, {DB4:"DB4"}],
	children: [	{
	id: "DB4",
	name: "DB4",
	data: [{parent: "R002"},],
	children: []},
]},
]},
	{
	id: "DB4",
	name: "DB4",
	data: [{parent: "1.1.2.24"}, {R005:"R005"}],
	children: [	{
	id: "R005",
	name: "R005",
	data: [{parent: "DB4"},],
	children: []},
]},
]},
]},
	{
	id: "DB3",
	name: "DB3",
	data: [{parent: "R001"}, {"1.1.2.23":"1.1.2.23"}],
	children: [	{
	id: "1.1.2.23",
	name: "1.1.2.23",
	data: [{parent: "DB3"},],
	children: []},
]},
]},
	{
	id: "R002",
	name: "R002",
	data: [{parent: "DB1"},],
	children: []},
]
};