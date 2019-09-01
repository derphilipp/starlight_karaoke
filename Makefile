all: download extract convert

download:
	wget http://starlight.bplaced.net/songliste.pdf
extract:
	pdftotext -layout songliste.pdf - | sort -f -u > songlist.txt
convert:
	python3 filter_and_convert.py songlist.txt  > docs/songlist.json
