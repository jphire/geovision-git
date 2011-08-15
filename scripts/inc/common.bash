# Add utility scripts as well as locally installed programs to path.
PATH=.:$HOME/.local/bin/:$PATH
PATH=$PATH:/usr/local/pgsql/bin/:/usr/lib/postgresql/8.4/bin/
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
