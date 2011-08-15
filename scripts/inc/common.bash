# Add utility scripts as well as locally installed programs to path.
PATH=.:$HOME/.local/bin/:$PATH
statusecho() { echo -e "\033[1;32m>>>>>" "$@" "\033[0m" }
errorecho() { echo -e "\033[1;31m*****" "$@" "\033[0m" }
