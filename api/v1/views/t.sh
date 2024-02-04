# Add the pyformat function
# Add the pyformat function
pyformat() {
	if [ -z "$1" ]; then
		echo "Usage: autopep8file <file_name.py>"
		return 1
	fi
    echo "a7a"
	python3 -m autopep8 --in-place "$1"
}