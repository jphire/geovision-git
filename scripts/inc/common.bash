# Add utility scripts as well as locally installed programs to path.
PATH=.:./inc/:$HOME/.local/bin/:$HOME/.local/sbin/:$PATH
PATH=$PATH:/usr/local/pgsql/bin/:/usr/lib/postgresql/8.4/bin/

source `dirname $0`/conf/defaults.conf
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
