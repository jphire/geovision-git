var json_data = {
id: "1.1.2.22",
name: "1.1.2.22",
data: [{DB1:"DB1"}, {DB2:"DB2"}, ],
children: [	{
	id: "DB1",
	name: "DB1",
	data: [{parent: "1.1.2.22"}, {R001:"R001"},{R002:"R002"}],
	children: [	{
	id: "R001",
	name: "R001",
	data: [{parent: "DB1"}, {DB1:"DB1"}],
	children: [	{
	id: "DB1",
	name: "DB1",
	data: [{parent: "R001"}, {R001:"R001"},{R002:"R002"}],
	children: [	{
	id: "R001",
	name: "R001",
	data: [{parent: "DB1"}, {DB1:"DB1"}],
	children: []
	},	{
	id: "R002",
	name: "R002",
	data: [{parent: "DB1"}, {DB1:"DB1"}],
	children: []
	},]},
]},
	{
	id: "R002",
	name: "R002",
	data: [{parent: "DB1"}, {DB1:"DB1"}],
	children: [	{
	id: "DB1",
	name: "DB1",
	data: [{parent: "R002"}, {R001:"R001"},{R002:"R002"}],
	children: [	{
	id: "R001",
	name: "R001",
	data: [{parent: "DB1"}, {DB1:"DB1"}],
	children: []
	},	{
	id: "R002",
	name: "R002",
	data: [{parent: "DB1"}, {DB1:"DB1"}],
	children: []
	},]},
]},
]},
	{
	id: "DB2",
	name: "DB2",
	data: [{parent: "1.1.2.22"}, {R003:"R003"}],
	children: [	{
	id: "R003",
	name: "R003",
	data: [{parent: "DB2"}, {DB2:"DB2"}],
	children: [	{
	id: "DB2",
	name: "DB2",
	data: [{parent: "R003"}, {R003:"R003"}],
	children: [	{
	id: "R003",
	name: "R003",
	data: [{parent: "DB2"}, {DB2:"DB2"}],
	children: []
	},]},
]},
]},
]
};