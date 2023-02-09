from fake_headers import Headers




class HeaderGen:
    _header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="win",  # Generate ony Windows platform
        headers=True  # generate misc headers
    )

    def get_header(self):
        return self._header.generate()
Footer