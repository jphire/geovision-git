var json_data = {
id: "1.1.2.22",
name: "1.1.2.22",
data: [{DB1:"DB1"}, {DB1:"DB1"}, {DB2:"DB2"}, {DB4:"DB4"}, {DB6:"DB6"}, ],
children: [	{
	id: "DB1",
	name: "DB1",
	data: [{parent: "1.1.2.22"}, {R001:"R001"},{R002:"R002"}],
	children: [	{
	id: "R001",
	name: "R001",
	data: {
		parent: "DB1"
	},
	children: []
	},
	{
	id: "R002",
	name: "R002",
	data: {
		parent: "DB1"
	},
	children: []
	},
]},
	{
	id: "DB1",
	name: "DB1",
	data: [{parent: "1.1.2.22"}, {R001:"R001"},{R002:"R002"}],
	children: [	{
	id: "R001",
	name: "R001",
	data: {
		parent: "DB1"
	},
	children: []
	},
	{
	id: "R002",
	name: "R002",
	data: {
		parent: "DB1"
	},
	children: []
	},
]},
	{
	id: "DB2",
	name: "DB2",
	data: [{parent: "1.1.2.22"}, {R003:"R003"}],
	children: [	{
	id: "R003",
	name: "R003",
	data: {
		parent: "DB2"
	},
	children: []
	},
]},
	{
	id: "DB4",
	name: "DB4",
	data: [{parent: "1.1.2.22"}, {R005:"R005"}],
	children: [	{
	id: "R005",
	name: "R005",
	data: {
		parent: "DB4"
	},
	children: []
	},
]},
	{
	id: "DB6",
	name: "DB6",
	data: [{parent: "1.1.2.22"}, {R004:"R004"}],
	children: [	{
	id: "R004",
	name: "R004",
	data: {
		parent: "DB6"
	},
	children: []
	},
]},
]
};