. ./virtualenv.sh

apps=($(git ls-files | awk -F/ '$0 ~ "/tests.py$" {print $(NF - 1)}'))

langs=($(ls -d */locale/??/ 2>/dev/null | cut -d/ -f3 | sort -u))

msg() {
    echo "* $@"
}

errmsg() {
    echo ERROR: $@
}
