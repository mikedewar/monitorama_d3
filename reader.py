import requests
import json

# open the connection to the bitly stream
r = requests.get('http://developer.usa.gov/1usagov', stream=True)

# deal with each line as it comes in
for line in r.iter_lines(chunk_size=1):
    # reject empty strings should they show up
    if not line.strip():
        continue
    # we are only interested in strings that can be parsed into JSON
    try:
        data = json.loads(line)
    except ValueError:
        continue
    # we don't want json blobs with lats and lons
    if 'll' in data:
        # when we come across a blob we want, send it to tornado
        print line
        requests.post('http://127.0.0.1:8888/put',data=line)
