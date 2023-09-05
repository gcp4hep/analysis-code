import fsspec
import uproot

class FSSpecHttpSource(uproot.source.chunk.Source):
    def __init__(self, file_path, **options):
        self._file_path = file_path
        # will by default use aiohttp with TCPConnection pool of size 100
        # could also play with block_size and cache_type
        self._fs = fsspec.filesystem("http", block_size=0, cache_type="none")
        
    @property
    def closed(self):
        return False # we're opening all the time?
    
    def _make_chunk(self, start, stop, content):
        future = uproot.source.futures.TrivialFuture(content)
        return uproot.source.chunk.Chunk(self, start, stop, future)
    
    def chunk(self, start, stop):
        return self._make_chunk(start, stop, self._fs.cat_file(self._file_path, start, stop))
    
    def chunks(self, ranges, notifications):
        starts = []
        stops = []
        for start, stop in ranges:
            starts.append(start)
            stops.append(stop)
        contents = self._fs.cat_ranges(
            [self._file_path] * len(ranges), starts, stops
        )
        chunks = []
        for content, (start, stop) in zip(contents, ranges):
            chunk = self._make_chunk(start, stop, content)
            if notifications is not None:
                notifications.put(chunk)
            chunks.append(chunk)
        return chunks