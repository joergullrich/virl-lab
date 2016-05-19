{
	'cisco':{
		'hosts': ['al-switch1','al-switch2','l2-l3-1','l2-l3-2','provider','provider-bu','internet'],
		'vars':{
			'ansible_connection': 'local',
			'hostname': '1.2.3.4',
			'password': 'cisco',
			'username': 'cisco'
		}
	},
	'local':{
		'hosts': ['localhost'],
		'vars': {'ansible_connection': 'local'}
	}
}
