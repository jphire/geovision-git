# Add utility scripts as well as locally installed programs to path.
PATH=.:./inc/:$HOME/.local/bin/:$HOME/.local/sbin/:$PATH
PATH=$PATH:/usr/local/pgsql/bin/:/usr/lib/postgresql/8.4/bin/

source conf/defaults.conf
statusecho() {
	echo -e "\033[1;32m>>>>>" "$@" "\033[0m"
}
errorecho() {
	echo -e "\033[1;31m*****" "$@" "\033[0m"
}
die() {
	errorecho "$@"
	exit 2
}
warn-cacheinvalidate() {
	echo "You have run a command that invalidates the blast-ecs-cache."
	echo "After you are done with your data importing session, please run the rebuild-cache scripts or your enzyme queries may report incorrect results!"
}
