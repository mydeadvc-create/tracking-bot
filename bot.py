#!/usr/bin/env python3
"""HTE Tracking Bot v3"""
import os, json, re, base64, urllib.request, time
from datetime import datetime

BOT_TOKEN   = os.environ.get("BOT_TOKEN",   "8327743942:AAGlZjo1bVwt3FvwF00zLYGiwIvLubY3S5s")
ADMIN_ID    = int(os.environ.get("ADMIN_ID", "1715716748"))
UPDATER_URL = os.environ.get("UPDATER_URL", "https://tracking.sdlg.online/updater.php")
UPDATER_KEY = os.environ.get("UPDATER_KEY", "hte_tracking_2026_Xk9mP3qR")
API         = f"https://api.telegram.org/bot{BOT_TOKEN}"

LOGO_SRC      = "data:image/png;base64,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"
CONTAINER_SVG = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 24 24\" fill=\"currentColor\"><rect x=\"2\" y=\"7\" width=\"20\" height=\"11\" rx=\"1.5\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.8\"/><line x1=\"7\" y1=\"7\" x2=\"7\" y2=\"18\" stroke=\"currentColor\" stroke-width=\"1.5\"/><line x1=\"12\" y1=\"7\" x2=\"12\" y2=\"18\" stroke=\"currentColor\" stroke-width=\"1.5\"/><line x1=\"17\" y1=\"7\" x2=\"17\" y2=\"18\" stroke=\"currentColor\" stroke-width=\"1.5\"/><rect x=\"6\" y=\"5\" width=\"12\" height=\"2.5\" rx=\"0.5\" fill=\"currentColor\"/><rect x=\"4\" y=\"18\" width=\"3\" height=\"2.5\" rx=\"0.5\" fill=\"currentColor\"/><rect x=\"17\" y=\"18\" width=\"3\" height=\"2.5\" rx=\"0.5\" fill=\"currentColor\"/></svg>"
MASTER_CSS    = base64.b64decode("LmxvZ28taW1ne3dpZHRoOjQ0cHg7aGVpZ2h0OjQ0cHg7b2JqZWN0LWZpdDpjb250YWlufSosKjo6YmVmb3JlLCo6OmFmdGVye2JveC1zaXppbmc6Ym9yZGVyLWJveDttYXJnaW46MDtwYWRkaW5nOjB9Cjpyb290ey0teWVsbG93OiNGRkM3MkM7LS1wYWdlLWJnOiNmMmYwZWF9CmJvZHl7Zm9udC1mYW1pbHk6J0ludGVyJywtYXBwbGUtc3lzdGVtLEJsaW5rTWFjU3lzdGVtRm9udCxzYW5zLXNlcmlmO2JhY2tncm91bmQ6dmFyKC0tcGFnZS1iZyk7Y29sb3I6IzBkMGQwZDttaW4taGVpZ2h0OjEwMHZoO2ZvbnQtc2l6ZToxM3B4fQpoZWFkZXJ7cGFkZGluZzowIDQ4cHg7ZGlzcGxheTpmbGV4O2FsaWduLWl0ZW1zOmNlbnRlcjtqdXN0aWZ5LWNvbnRlbnQ6c3BhY2UtYmV0d2VlbjtoZWlnaHQ6NjhweDtwb3NpdGlvbjpzdGlja3k7dG9wOjA7ei1pbmRleDoyMDA7YmFja2dyb3VuZDpyZ2JhKDUsMjAsNDAsMC42KTtiYWNrZHJvcC1maWx0ZXI6Ymx1cigxNHB4KTtib3JkZXItYm90dG9tOjFweCBzb2xpZCByZ2JhKDI1NSwyNTUsMjU1LDAuMDgpfQoubG9nb3tkaXNwbGF5OmZsZXg7YWxpZ24taXRlbXM6Y2VudGVyO2dhcDoxNHB4O3RleHQtZGVjb3JhdGlvbjpub25lfQoubG9nby1tYXJre3dpZHRoOjM4cHg7aGVpZ2h0OjM4cHg7YmFja2dyb3VuZDp2YXIoLS15ZWxsb3cpO2JvcmRlci1yYWRpdXM6OHB4O2Rpc3BsYXk6ZmxleDthbGlnbi1pdGVtczpjZW50ZXI7anVzdGlmeS1jb250ZW50OmNlbnRlcjtmb250LXdlaWdodDo4MDA7Zm9udC1zaXplOjEzcHg7Y29sb3I6IzBkMjA0MH0KLmxvZ28tdGV4dHtmb250LXdlaWdodDo3MDA7Zm9udC1zaXplOjE1cHg7Y29sb3I6I2ZmZn0ubG9nby1zdWJ7Zm9udC1zaXplOjEwcHg7Y29sb3I6cmdiYSgyNTUsMjU1LDI1NSwwLjQpO2xldHRlci1zcGFjaW5nOi4xZW07dGV4dC10cmFuc2Zvcm06dXBwZXJjYXNlfQoubGl2ZS1iYWRnZXtkaXNwbGF5OmZsZXg7YWxpZ24taXRlbXM6Y2VudGVyO2dhcDo4cHg7YmFja2dyb3VuZDpyZ2JhKDI1NSwyNTUsMjU1LDAuMSk7Ym9yZGVyOjFweCBzb2xpZCByZ2JhKDI1NSwyNTUsMjU1LDAuMTUpO2JhY2tkcm9wLWZpbHRlcjpibHVyKDhweCk7Ym9yZGVyLXJhZGl1czoyNHB4O3BhZGRpbmc6NnB4IDE2cHg7Zm9udC1zaXplOjExcHg7Y29sb3I6cmdiYSgyNTUsMjU1LDI1NSwwLjYpfQoubGl2ZS1kb3R7d2lkdGg6N3B4O2hlaWdodDo3cHg7Ym9yZGVyLXJhZGl1czo1MCU7YmFja2dyb3VuZDojNGNhZjUwO2JveC1zaGFkb3c6MCAwIDAgM3B4IHJnYmEoNzYsMTc1LDgwLDAuMyk7YW5pbWF0aW9uOnB1bHNlIDJzIGluZmluaXRlfQpAa2V5ZnJhbWVzIHB1bHNlezAlLDEwMCV7Ym94LXNoYWRvdzowIDAgMCAzcHggcmdiYSg3NiwxNzUsODAsMC4zKX01MCV7Ym94LXNoYWRvdzowIDAgMCA3cHggcmdiYSg3NiwxNzUsODAsMC4xKX19Ci5oZXJvLXNlY3Rpb257cG9zaXRpb246cmVsYXRpdmU7b3ZlcmZsb3c6aGlkZGVufQouaGVyby1iZ3twb3NpdGlvbjphYnNvbHV0ZTtpbnNldDowO2JhY2tncm91bmQtaW1hZ2U6dXJsKCdodHRwczovL2ltYWdlcy51bnNwbGFzaC5jb20vcGhvdG8tMTU3ODU3NTQzNzEzMC01MjdlZWQzYWJiZWM/dz0xNjAwJnE9ODAmYXV0bz1mb3JtYXQmZml0PWNyb3AnKTtiYWNrZ3JvdW5kLXNpemU6Y292ZXI7YmFja2dyb3VuZC1wb3NpdGlvbjpjZW50ZXIgNDAlO2ZpbHRlcjpicmlnaHRuZXNzKDAuNDUpIHNhdHVyYXRlKDAuOCl9Ci5oZXJvLW92ZXJsYXl7cG9zaXRpb246YWJzb2x1dGU7aW5zZXQ6MDtiYWNrZ3JvdW5kOmxpbmVhci1ncmFkaWVudCh0byBib3R0b20scmdiYSg1LDIwLDQwLDAuNikgMCUscmdiYSg1LDIwLDQwLDAuMykgNTAlLHJnYmEoNSwyMCw0MCwwLjg1KSAxMDAlKX0KLmhlcm97cG9zaXRpb246cmVsYXRpdmU7ei1pbmRleDoyO3BhZGRpbmc6NDhweCA0OHB4IDUycHh9Ci5oZXJvLWxhYmVse2ZvbnQtc2l6ZToxMXB4O2xldHRlci1zcGFjaW5nOi4yZW07dGV4dC10cmFuc2Zvcm06dXBwZXJjYXNlO2NvbG9yOnZhcigtLXllbGxvdyk7bWFyZ2luLWJvdHRvbToxNHB4O2ZvbnQtd2VpZ2h0OjUwMH0KLmhlcm8tdGl0bGV7Zm9udC1zaXplOmNsYW1wKDMycHgsNXZ3LDU4cHgpO2ZvbnQtd2VpZ2h0OjgwMDtjb2xvcjojZmZmO2xpbmUtaGVpZ2h0OjEuMDU7bGV0dGVyLXNwYWNpbmc6LS4wMmVtO21hcmdpbi1ib3R0b206OHB4fQouaGVyby10aXRsZSAueXtjb2xvcjp2YXIoLS15ZWxsb3cpfQouaGVyby1kZXNje2ZvbnQtc2l6ZToxM3B4O2NvbG9yOnJnYmEoMjU1LDI1NSwyNTUsMC40NSk7bWFyZ2luLWJvdHRvbTo0MHB4fQouc3RhdHN7ZGlzcGxheTpncmlkO2dyaWQtdGVtcGxhdGUtY29sdW1uczpyZXBlYXQoNCwxZnIpO2dhcDoycHg7bWF4LXdpZHRoOjcyMHB4O2JvcmRlci1yYWRpdXM6MTRweDtvdmVyZmxvdzpoaWRkZW47YmFja2dyb3VuZDpyZ2JhKDI1NSwyNTUsMjU1LDAuMDgpO2JvcmRlcjoxcHggc29saWQgcmdiYSgyNTUsMjU1LDI1NSwwLjEyKTtiYWNrZHJvcC1maWx0ZXI6Ymx1cigxNnB4KX0KLnN0YXQtY2FyZHtiYWNrZ3JvdW5kOnJnYmEoNSwyMCw0MCwwLjU1KTtwYWRkaW5nOjIwcHggMjRweH0KLnN0YXQtdmFse2ZvbnQtc2l6ZTo0MHB4O2ZvbnQtd2VpZ2h0OjgwMDtsaW5lLWhlaWdodDoxO21hcmdpbi1ib3R0b206NXB4O2NvbG9yOiNmZmZ9Ci5zdGF0LXZhbC55bHtjb2xvcjp2YXIoLS15ZWxsb3cpfQouc3RhdC1sYmx7Zm9udC1zaXplOjEwcHg7Y29sb3I6cmdiYSgyNTUsMjU1LDI1NSwwLjM1KTtsZXR0ZXItc3BhY2luZzouMWVtO3RleHQtdHJhbnNmb3JtOnVwcGVyY2FzZTtmb250LXdlaWdodDo1MDB9Ci50aW1lbGluZS13cmFwe2Rpc3BsYXk6Z3JpZDtncmlkLXRlbXBsYXRlLWNvbHVtbnM6MjAwcHggMWZyO21heC13aWR0aDoxMTAwcHg7bWFyZ2luOjAgYXV0bztwYWRkaW5nOjYwcHggNDhweCA4MHB4fQoubW9udGgtbmF2e3Bvc2l0aW9uOnN0aWNreTt0b3A6ODhweDthbGlnbi1zZWxmOnN0YXJ0O3BhZGRpbmctcmlnaHQ6MjhweDtwYWRkaW5nLXRvcDo0cHh9Ci5tb250aC1uYXYtdGl0bGV7Zm9udC1zaXplOjEwcHg7bGV0dGVyLXNwYWNpbmc6LjE1ZW07dGV4dC10cmFuc2Zvcm06dXBwZXJjYXNlO2NvbG9yOiM5OTk7bWFyZ2luLWJvdHRvbToxNnB4O2ZvbnQtd2VpZ2h0OjYwMH0KLm1vbnRoLWl0ZW17ZGlzcGxheTpmbGV4O2FsaWduLWl0ZW1zOmNlbnRlcjtnYXA6MTBweDtwYWRkaW5nOjdweCAwO3RleHQtZGVjb3JhdGlvbjpub25lO3RyYW5zaXRpb246b3BhY2l0eSAuMTVzfQoubW9udGgtaXRlbTpob3ZlcntvcGFjaXR5Oi42fQoubW9udGgtZG90e3dpZHRoOjEwcHg7aGVpZ2h0OjEwcHg7Ym9yZGVyLXJhZGl1czo1MCU7ZmxleC1zaHJpbms6MH0KLm1vbnRoLW5hbWV7Zm9udC1zaXplOjEzcHg7Zm9udC13ZWlnaHQ6NjAwO2NvbG9yOiMwZDBkMGR9Ci5tb250aC1jb3VudHtmb250LXNpemU6MTBweDtjb2xvcjojYWFhO21hcmdpbi1sZWZ0OmF1dG87Zm9udC13ZWlnaHQ6NTAwfQoubmF2LWxpbmV7d2lkdGg6MXB4O2hlaWdodDoxOHB4O2JhY2tncm91bmQ6I2RkZDttYXJnaW46MXB4IDAgMXB4IDRweH0KLm1vbnRoLXNlY3Rpb257bWFyZ2luLWJvdHRvbTo1MnB4O3Njcm9sbC1tYXJnaW4tdG9wOjEwMHB4fQoubW9udGgtaGVhZGVye2Rpc3BsYXk6ZmxleDthbGlnbi1pdGVtczpjZW50ZXI7cGFkZGluZzoyMHB4IDI0cHg7Ym9yZGVyLXJhZGl1czoxNHB4IDE0cHggMCAwO3Bvc2l0aW9uOnJlbGF0aXZlO292ZXJmbG93OmhpZGRlbn0KLm1vbnRoLWhlYWRlcjo6YWZ0ZXJ7Y29udGVudDonJztwb3NpdGlvbjphYnNvbHV0ZTtpbnNldDowO2JhY2tncm91bmQ6cmVwZWF0aW5nLWxpbmVhci1ncmFkaWVudCgtNDVkZWcsdHJhbnNwYXJlbnQsdHJhbnNwYXJlbnQgMTJweCxyZ2JhKDI1NSwyNTUsMjU1LDAuMDYpIDEycHgscmdiYSgyNTUsMjU1LDI1NSwwLjA2KSAxM3B4KX0KLm1oLWljb257Zm9udC1zaXplOjI2cHg7bWFyZ2luLXJpZ2h0OjE0cHg7cG9zaXRpb246cmVsYXRpdmU7ei1pbmRleDoxfQoubWgtaW5mb3twb3NpdGlvbjpyZWxhdGl2ZTt6LWluZGV4OjE7ZmxleDoxfQoubWgtYmlne2ZvbnQtc2l6ZToyMHB4O2ZvbnQtd2VpZ2h0OjgwMDtsaW5lLWhlaWdodDoxO21hcmdpbi1ib3R0b206M3B4fQoubWgtc21hbGx7Zm9udC1zaXplOjExcHg7b3BhY2l0eTouNjV9Ci5taC1waWxse3Bvc2l0aW9uOnJlbGF0aXZlO3otaW5kZXg6MTtmb250LXNpemU6MTBweDtmb250LXdlaWdodDo2MDA7cGFkZGluZzo1cHggMTJweDtib3JkZXItcmFkaXVzOjIwcHg7YmFja2dyb3VuZDpyZ2JhKDI1NSwyNTUsMjU1LDAuMjIpO3RleHQtdHJhbnNmb3JtOnVwcGVyY2FzZTtsZXR0ZXItc3BhY2luZzouMDZlbTt3aGl0ZS1zcGFjZTpub3dyYXB9Ci5jYXJkc3tkaXNwbGF5OmZsZXg7ZmxleC1kaXJlY3Rpb246Y29sdW1uO2dhcDoxMHB4O3BhZGRpbmctdG9wOjEwcHh9Ci5jYXJke2JhY2tncm91bmQ6I2ZmZjtib3JkZXItcmFkaXVzOjE0cHg7cGFkZGluZzoxOHB4IDIycHg7Ym9yZGVyOjEuNXB4IHNvbGlkIHRyYW5zcGFyZW50O3RyYW5zaXRpb246dHJhbnNmb3JtIC4xNXMsYm94LXNoYWRvdyAuMTVzLGJvcmRlci1jb2xvciAuMTVzO2FuaW1hdGlvbjpyaXNlIC40NXMgZWFzZSBib3RofQouY2FyZDpob3Zlcnt0cmFuc2Zvcm06dHJhbnNsYXRlWSgtMnB4KTtib3gtc2hhZG93OjAgOHB4IDI4cHggcmdiYSgwLDAsMCwwLjA3KX0KQGtleWZyYW1lcyByaXNle2Zyb217b3BhY2l0eTowO3RyYW5zZm9ybTp0cmFuc2xhdGVZKDhweCl9dG97b3BhY2l0eToxO3RyYW5zZm9ybTp0cmFuc2xhdGVZKDApfX0KLmNhcmQtaGVhZGVye2Rpc3BsYXk6ZmxleDthbGlnbi1pdGVtczpmbGV4LXN0YXJ0O2dhcDoxNHB4O21hcmdpbi1ib3R0b206MTJweH0KLm51bS1je3dpZHRoOjQwcHg7aGVpZ2h0OjQwcHg7Ym9yZGVyLXJhZGl1czo1MCU7ZGlzcGxheTpmbGV4O2FsaWduLWl0ZW1zOmNlbnRlcjtqdXN0aWZ5LWNvbnRlbnQ6Y2VudGVyO2ZvbnQtd2VpZ2h0OjgwMDtmb250LXNpemU6MTVweDtmbGV4LXNocmluazowO21hcmdpbi10b3A6MnB4fQouY2FyZC1oZWFkbGluZXtmbGV4OjF9Ci5jYXJkLXN0YXR1cy1yb3d7ZGlzcGxheTpmbGV4O2FsaWduLWl0ZW1zOmNlbnRlcjtqdXN0aWZ5LWNvbnRlbnQ6c3BhY2UtYmV0d2VlbjtmbGV4LXdyYXA6d3JhcDtnYXA6OHB4fQouY2FyZC1kYXRlLWJpZ3tmb250LXNpemU6MTZweDtmb250LXdlaWdodDo4MDA7bGluZS1oZWlnaHQ6MX0KLnBpbGx7ZGlzcGxheTppbmxpbmUtYmxvY2s7Zm9udC1zaXplOjEwcHg7Zm9udC13ZWlnaHQ6NjAwO3BhZGRpbmc6NHB4IDExcHg7Ym9yZGVyLXJhZGl1czoyMHB4O3RleHQtdHJhbnNmb3JtOnVwcGVyY2FzZTtsZXR0ZXItc3BhY2luZzouMDVlbTt3aGl0ZS1zcGFjZTpub3dyYXB9Ci5jYXJkLWRlc3R7Zm9udC1zaXplOjExcHg7Y29sb3I6Izg4ODttYXJnaW4tdG9wOjNweH0KLmVxLWxpc3R7ZGlzcGxheTpmbGV4O2ZsZXgtZGlyZWN0aW9uOmNvbHVtbjtnYXA6NnB4O2JvcmRlci10b3A6MXB4IHNvbGlkICNmMGVkZTY7cGFkZGluZy10b3A6MTJweH0KLmVxLWl0ZW17ZGlzcGxheTpmbGV4O2FsaWduLWl0ZW1zOmNlbnRlcjtnYXA6OHB4O3BhZGRpbmc6NnB4IDEwcHg7YmFja2dyb3VuZDojZmFmOWY2O2JvcmRlci1yYWRpdXM6OHB4fQouZXEtaWNvbntmb250LXNpemU6MThweDtmbGV4LXNocmluazowfQoKCi5lcS1sYWJlbHtmbGV4OjE7ZGlzcGxheTpmbGV4O2ZsZXgtZGlyZWN0aW9uOmNvbHVtbjtnYXA6MXB4fS5lcS1sYWJlbCAuZXEtdHlwZXtmb250LXNpemU6MTBweDtmb250LXdlaWdodDo1MDA7Y29sb3I6I2FhYTt0ZXh0LXRyYW5zZm9ybTp1cHBlcmNhc2U7bGV0dGVyLXNwYWNpbmc6LjA4ZW19LmVxLWxhYmVsIC5lcS1tb2RlbHtmb250LXNpemU6MTdweDtmb250LXdlaWdodDo4MDA7bGV0dGVyLXNwYWNpbmc6LS4wMmVtO2xpbmUtaGVpZ2h0OjEuMX0uZXEtcXR5e21hcmdpbi1sZWZ0OmF1dG87Zm9udC1zaXplOjEycHg7Zm9udC13ZWlnaHQ6NzAwO3BhZGRpbmc6MnB4IDEwcHg7Ym9yZGVyLXJhZGl1czoxMnB4O2JhY2tncm91bmQ6I2VlZTtjb2xvcjojNDQ0fQouY2FyZC1ub3Rle2ZvbnQtc2l6ZToxMXB4O2NvbG9yOiNlMDcwMDA7bWFyZ2luLXRvcDo4cHg7Zm9udC13ZWlnaHQ6NTAwO3BhZGRpbmc6NnB4IDEwcHg7YmFja2dyb3VuZDojZmZmOGVlO2JvcmRlci1yYWRpdXM6OHB4O2JvcmRlci1sZWZ0OjNweCBzb2xpZCAjZTA3MDAwfQouY2FyZC10ZWNoe2Rpc3BsYXk6ZmxleDtmbGV4LXdyYXA6d3JhcDtnYXA6NnB4O21hcmdpbi10b3A6OHB4fQoudGVjaC1waWxse2ZvbnQtc2l6ZToxMHB4O2NvbG9yOiNhYWE7YmFja2dyb3VuZDojZjVmM2VlO3BhZGRpbmc6MnB4IDhweDtib3JkZXItcmFkaXVzOjEwcHh9CgovKiBDT0xPUiBUSEVNRVMgKi8KLnQtMSAubW9udGgtaGVhZGVye2JhY2tncm91bmQ6bGluZWFyLWdyYWRpZW50KDEzMGRlZywjMWE0ZDJlLCMyZDhhNGEpO2NvbG9yOiNmZmZ9Ci50LTEgLmNhcmR7Ym9yZGVyLWNvbG9yOiNjNWVlZDV9LnQtMSAuY2FyZDpob3Zlcntib3JkZXItY29sb3I6IzRkYWE2ZH0KLnQtMSAubnVtLWN7YmFja2dyb3VuZDojZDRmMGRmO2NvbG9yOiMxYTRkMmV9LnQtMSAuY2FyZC1kYXRlLWJpZ3tjb2xvcjojMWE0ZDJlfS50LTEgLnBpbGx7YmFja2dyb3VuZDojZDRmMGRmO2NvbG9yOiMxYTRkMmV9LnQtMSAuZXEtbGFiZWx7ZmxleDoxO2Rpc3BsYXk6ZmxleDtmbGV4LWRpcmVjdGlvbjpjb2x1bW47Z2FwOjFweH0uZXEtbGFiZWwgLmVxLXR5cGV7Zm9udC1zaXplOjEwcHg7Zm9udC13ZWlnaHQ6NTAwO2NvbG9yOiNhYWE7dGV4dC10cmFuc2Zvcm06dXBwZXJjYXNlO2xldHRlci1zcGFjaW5nOi4wOGVtfS5lcS1sYWJlbCAuZXEtbW9kZWx7Zm9udC1zaXplOjE3cHg7Zm9udC13ZWlnaHQ6ODAwO2xldHRlci1zcGFjaW5nOi0uMDJlbTtsaW5lLWhlaWdodDoxLjF9LmVxLXF0eXtiYWNrZ3JvdW5kOiNkNGYwZGY7Y29sb3I6IzFhNGQyZX0KLnQtMiAubW9udGgtaGVhZGVye2JhY2tncm91bmQ6bGluZWFyLWdyYWRpZW50KDEzMGRlZywjMGQ0ODQ4LCMxYTgwODApO2NvbG9yOiNmZmZ9Ci50LTIgLmNhcmR7Ym9yZGVyLWNvbG9yOiNiZGU4ZTh9LnQtMiAuY2FyZDpob3Zlcntib3JkZXItY29sb3I6IzMwYWFhYX0KLnQtMiAubnVtLWN7YmFja2dyb3VuZDojYzhlY2VjO2NvbG9yOiMwZDQ4NDh9LnQtMiAuY2FyZC1kYXRlLWJpZ3tjb2xvcjojMGQ0ODQ4fS50LTIgLnBpbGx7YmFja2dyb3VuZDojYzhlY2VjO2NvbG9yOiMwZDQ4NDh9LnQtMiAuZXEtbGFiZWx7ZmxleDoxO2Rpc3BsYXk6ZmxleDtmbGV4LWRpcmVjdGlvbjpjb2x1bW47Z2FwOjFweH0uZXEtbGFiZWwgLmVxLXR5cGV7Zm9udC1zaXplOjEwcHg7Zm9udC13ZWlnaHQ6NTAwO2NvbG9yOiNhYWE7dGV4dC10cmFuc2Zvcm06dXBwZXJjYXNlO2xldHRlci1zcGFjaW5nOi4wOGVtfS5lcS1sYWJlbCAuZXEtbW9kZWx7Zm9udC1zaXplOjE3cHg7Zm9udC13ZWlnaHQ6ODAwO2xldHRlci1zcGFjaW5nOi0uMDJlbTtsaW5lLWhlaWdodDoxLjF9LmVxLXF0eXtiYWNrZ3JvdW5kOiNjOGVjZWM7Y29sb3I6IzBkNDg0OH0KLnQtMyAubW9udGgtaGVhZGVye2JhY2tncm91bmQ6bGluZWFyLWdyYWRpZW50KDEzMGRlZywjMGQyNDY4LCMxYTRmYTgpO2NvbG9yOiNmZmZ9Ci50LTMgLmNhcmR7Ym9yZGVyLWNvbG9yOiNjNGQ4Zjh9LnQtMyAuY2FyZDpob3Zlcntib3JkZXItY29sb3I6IzQwODBlMH0KLnQtMyAubnVtLWN7YmFja2dyb3VuZDojZDJlNGZhO2NvbG9yOiMwZDI0Njh9LnQtMyAuY2FyZC1kYXRlLWJpZ3tjb2xvcjojMGQyNDY4fS50LTMgLnBpbGx7YmFja2dyb3VuZDojZDJlNGZhO2NvbG9yOiMwZDI0Njh9LnQtMyAuZXEtbGFiZWx7ZmxleDoxO2Rpc3BsYXk6ZmxleDtmbGV4LWRpcmVjdGlvbjpjb2x1bW47Z2FwOjFweH0uZXEtbGFiZWwgLmVxLXR5cGV7Zm9udC1zaXplOjEwcHg7Zm9udC13ZWlnaHQ6NTAwO2NvbG9yOiNhYWE7dGV4dC10cmFuc2Zvcm06dXBwZXJjYXNlO2xldHRlci1zcGFjaW5nOi4wOGVtfS5lcS1sYWJlbCAuZXEtbW9kZWx7Zm9udC1zaXplOjE3cHg7Zm9udC13ZWlnaHQ6ODAwO2xldHRlci1zcGFjaW5nOi0uMDJlbTtsaW5lLWhlaWdodDoxLjF9LmVxLXF0eXtiYWNrZ3JvdW5kOiNkMmU0ZmE7Y29sb3I6IzBkMjQ2OH0KLnQtNCAubW9udGgtaGVhZGVye2JhY2tncm91bmQ6bGluZWFyLWdyYWRpZW50KDEzMGRlZywjMjIxNDY4LCM0YzM4YzgpO2NvbG9yOiNmZmZ9Ci50LTQgLmNhcmR7Ym9yZGVyLWNvbG9yOiNkOGQyZjh9LnQtNCAuY2FyZDpob3Zlcntib3JkZXItY29sb3I6IzcwNjBlMH0KLnQtNCAubnVtLWN7YmFja2dyb3VuZDojZTJkY2ZhO2NvbG9yOiMyMjE0Njh9LnQtNCAuY2FyZC1kYXRlLWJpZ3tjb2xvcjojMjIxNDY4fS50LTQgLnBpbGx7YmFja2dyb3VuZDojZTJkY2ZhO2NvbG9yOiMyMjE0Njh9LnQtNCAuZXEtbGFiZWx7ZmxleDoxO2Rpc3BsYXk6ZmxleDtmbGV4LWRpcmVjdGlvbjpjb2x1bW47Z2FwOjFweH0uZXEtbGFiZWwgLmVxLXR5cGV7Zm9udC1zaXplOjEwcHg7Zm9udC13ZWlnaHQ6NTAwO2NvbG9yOiNhYWE7dGV4dC10cmFuc2Zvcm06dXBwZXJjYXNlO2xldHRlci1zcGFjaW5nOi4wOGVtfS5lcS1sYWJlbCAuZXEtbW9kZWx7Zm9udC1zaXplOjE3cHg7Zm9udC13ZWlnaHQ6ODAwO2xldHRlci1zcGFjaW5nOi0uMDJlbTtsaW5lLWhlaWdodDoxLjF9LmVxLXF0eXtiYWNrZ3JvdW5kOiNlMmRjZmE7Y29sb3I6IzIyMTQ2OH0KLnQtNSAubW9udGgtaGVhZGVye2JhY2tncm91bmQ6bGluZWFyLWdyYWRpZW50KDEzMGRlZywjNDQxNDY4LCM4YTM4YjgpO2NvbG9yOiNmZmZ9Ci50LTUgLmNhcmR7Ym9yZGVyLWNvbG9yOiNlOGQyZjh9LnQtNSAuY2FyZDpob3Zlcntib3JkZXItY29sb3I6I2FhNjBkNH0KLnQtNSAubnVtLWN7YmFja2dyb3VuZDojZWVkY2ZhO2NvbG9yOiM0NDE0Njh9LnQtNSAuY2FyZC1kYXRlLWJpZ3tjb2xvcjojNDQxNDY4fS50LTUgLnBpbGx7YmFja2dyb3VuZDojZWVkY2ZhO2NvbG9yOiM0NDE0Njh9LnQtNSAuZXEtbGFiZWx7ZmxleDoxO2Rpc3BsYXk6ZmxleDtmbGV4LWRpcmVjdGlvbjpjb2x1bW47Z2FwOjFweH0uZXEtbGFiZWwgLmVxLXR5cGV7Zm9udC1zaXplOjEwcHg7Zm9udC13ZWlnaHQ6NTAwO2NvbG9yOiNhYWE7dGV4dC10cmFuc2Zvcm06dXBwZXJjYXNlO2xldHRlci1zcGFjaW5nOi4wOGVtfS5lcS1sYWJlbCAuZXEtbW9kZWx7Zm9udC1zaXplOjE3cHg7Zm9udC13ZWlnaHQ6ODAwO2xldHRlci1zcGFjaW5nOi0uMDJlbTtsaW5lLWhlaWdodDoxLjF9LmVxLXF0eXtiYWNrZ3JvdW5kOiNlZWRjZmE7Y29sb3I6IzQ0MTQ2OH0KLnQtNiAubW9udGgtaGVhZGVye2JhY2tncm91bmQ6bGluZWFyLWdyYWRpZW50KDEzMGRlZywjNjQxNDM4LCNjNDM4NjgpO2NvbG9yOiNmZmZ9Ci50LTYgLmNhcmR7Ym9yZGVyLWNvbG9yOiNmOGM0ZDh9LnQtNiAuY2FyZDpob3Zlcntib3JkZXItY29sb3I6I2UwNjA5MH0KLnQtNiAubnVtLWN7YmFja2dyb3VuZDojZmFkMmU0O2NvbG9yOiM2NDE0Mzh9LnQtNiAuY2FyZC1kYXRlLWJpZ3tjb2xvcjojNjQxNDM4fS50LTYgLnBpbGx7YmFja2dyb3VuZDojZmFkMmU0O2NvbG9yOiM2NDE0Mzh9LnQtNiAuZXEtbGFiZWx7ZmxleDoxO2Rpc3BsYXk6ZmxleDtmbGV4LWRpcmVjdGlvbjpjb2x1bW47Z2FwOjFweH0uZXEtbGFiZWwgLmVxLXR5cGV7Zm9udC1zaXplOjEwcHg7Zm9udC13ZWlnaHQ6NTAwO2NvbG9yOiNhYWE7dGV4dC10cmFuc2Zvcm06dXBwZXJjYXNlO2xldHRlci1zcGFjaW5nOi4wOGVtfS5lcS1sYWJlbCAuZXEtbW9kZWx7Zm9udC1zaXplOjE3cHg7Zm9udC13ZWlnaHQ6ODAwO2xldHRlci1zcGFjaW5nOi0uMDJlbTtsaW5lLWhlaWdodDoxLjF9LmVxLXF0eXtiYWNrZ3JvdW5kOiNmYWQyZTQ7Y29sb3I6IzY0MTQzOH0KLnQtNyAubW9udGgtaGVhZGVye2JhY2tncm91bmQ6bGluZWFyLWdyYWRpZW50KDEzMGRlZywjNTIyODAwLCNiMDU4MDApO2NvbG9yOiNmZmZ9Ci50LTcgLmNhcmR7Ym9yZGVyLWNvbG9yOiNmOGRlYmJ9LnQtNyAuY2FyZDpob3Zlcntib3JkZXItY29sb3I6I2UwODgzOH0KLnQtNyAubnVtLWN7YmFja2dyb3VuZDojZmFlOGNhO2NvbG9yOiM1MjI4MDB9LnQtNyAuY2FyZC1kYXRlLWJpZ3tjb2xvcjojNTIyODAwfS50LTcgLnBpbGx7YmFja2dyb3VuZDojZmFlOGNhO2NvbG9yOiM1MjI4MDB9LnQtNyAuZXEtbGFiZWx7ZmxleDoxO2Rpc3BsYXk6ZmxleDtmbGV4LWRpcmVjdGlvbjpjb2x1bW47Z2FwOjFweH0uZXEtbGFiZWwgLmVxLXR5cGV7Zm9udC1zaXplOjEwcHg7Zm9udC13ZWlnaHQ6NTAwO2NvbG9yOiNhYWE7dGV4dC10cmFuc2Zvcm06dXBwZXJjYXNlO2xldHRlci1zcGFjaW5nOi4wOGVtfS5lcS1sYWJlbCAuZXEtbW9kZWx7Zm9udC1zaXplOjE3cHg7Zm9udC13ZWlnaHQ6ODAwO2xldHRlci1zcGFjaW5nOi0uMDJlbTtsaW5lLWhlaWdodDoxLjF9LmVxLXF0eXtiYWNrZ3JvdW5kOiNmYWU4Y2E7Y29sb3I6IzUyMjgwMH0KLnQtc2FpbCAubW9udGgtaGVhZGVye2JhY2tncm91bmQ6bGluZWFyLWdyYWRpZW50KDEzMGRlZywjNjAzODAwLCNjNDcwMDApO2NvbG9yOiNmZmZ9Ci50LXNhaWwgLmNhcmR7Ym9yZGVyLWNvbG9yOiNmZmU0Yjh9LnQtc2FpbCAuY2FyZDpob3Zlcntib3JkZXItY29sb3I6I2YwYTAzMH0KLnQtc2FpbCAubnVtLWN7YmFja2dyb3VuZDojZmVlZWNlO2NvbG9yOiM2MDM4MDB9LnQtc2FpbCAuY2FyZC1kYXRlLWJpZ3tjb2xvcjojNjAzODAwfS50LXNhaWwgLnBpbGx7YmFja2dyb3VuZDojZmVlZWNlO2NvbG9yOiM2MDM4MDB9LnQtc2FpbCAuZXEtbGFiZWx7ZmxleDoxO2Rpc3BsYXk6ZmxleDtmbGV4LWRpcmVjdGlvbjpjb2x1bW47Z2FwOjFweH0uZXEtbGFiZWwgLmVxLXR5cGV7Zm9udC1zaXplOjEwcHg7Zm9udC13ZWlnaHQ6NTAwO2NvbG9yOiNhYWE7dGV4dC10cmFuc2Zvcm06dXBwZXJjYXNlO2xldHRlci1zcGFjaW5nOi4wOGVtfS5lcS1sYWJlbCAuZXEtbW9kZWx7Zm9udC1zaXplOjE3cHg7Zm9udC13ZWlnaHQ6ODAwO2xldHRlci1zcGFjaW5nOi0uMDJlbTtsaW5lLWhlaWdodDoxLjF9LmVxLXF0eXtiYWNrZ3JvdW5kOiNmZWVlY2U7Y29sb3I6IzYwMzgwMH0KLnQtcGVuZCAubW9udGgtaGVhZGVye2JhY2tncm91bmQ6bGluZWFyLWdyYWRpZW50KDEzMGRlZywjMjgyODI4LCM1NDU0NTQpO2NvbG9yOiNmZmZ9Ci50LXBlbmQgLmNhcmR7Ym9yZGVyLWNvbG9yOiNkZWRhZDJ9LnQtcGVuZCAuY2FyZDpob3Zlcntib3JkZXItY29sb3I6I2FhYX0KLnQtcGVuZCAubnVtLWN7YmFja2dyb3VuZDojZWFlNmRlO2NvbG9yOiM0NDR9LnQtcGVuZCAuY2FyZC1kYXRlLWJpZ3tjb2xvcjojNTU1fS50LXBlbmQgLnBpbGx7YmFja2dyb3VuZDojZWFlNmRlO2NvbG9yOiM1NTV9LnQtcGVuZCAuZXEtbGFiZWx7ZmxleDoxO2Rpc3BsYXk6ZmxleDtmbGV4LWRpcmVjdGlvbjpjb2x1bW47Z2FwOjFweH0uZXEtbGFiZWwgLmVxLXR5cGV7Zm9udC1zaXplOjEwcHg7Zm9udC13ZWlnaHQ6NTAwO2NvbG9yOiNhYWE7dGV4dC10cmFuc2Zvcm06dXBwZXJjYXNlO2xldHRlci1zcGFjaW5nOi4wOGVtfS5lcS1sYWJlbCAuZXEtbW9kZWx7Zm9udC1zaXplOjE3cHg7Zm9udC13ZWlnaHQ6ODAwO2xldHRlci1zcGFjaW5nOi0uMDJlbTtsaW5lLWhlaWdodDoxLjF9LmVxLXF0eXtiYWNrZ3JvdW5kOiNlYWU2ZGU7Y29sb3I6IzU1NX0KZm9vdGVye2JhY2tncm91bmQ6IzBkMjA0MDtwYWRkaW5nOjI4cHggNDhweDtkaXNwbGF5OmZsZXg7YWxpZ24taXRlbXM6Y2VudGVyO2p1c3RpZnktY29udGVudDpzcGFjZS1iZXR3ZWVuO2ZsZXgtd3JhcDp3cmFwO2dhcDoxNnB4fQouZnQtYnJhbmR7Zm9udC1zaXplOjEzcHg7Zm9udC13ZWlnaHQ6NjAwO2NvbG9yOnJnYmEoMjU1LDI1NSwyNTUsMC4zNSl9Ci5mdC1icmFuZCBzcGFue2NvbG9yOnZhcigtLXllbGxvdyl9Ci5mdC1saW5rc3tkaXNwbGF5OmZsZXg7Z2FwOjI0cHh9Ci5mdC1saW5rcyBhe2ZvbnQtc2l6ZToxMXB4O2NvbG9yOnJnYmEoMjU1LDI1NSwyNTUsMC4zNSk7dGV4dC1kZWNvcmF0aW9uOm5vbmU7dHJhbnNpdGlvbjpjb2xvciAuMTVzO2ZvbnQtd2VpZ2h0OjUwMH0KLmZ0LWxpbmtzIGE6aG92ZXJ7Y29sb3I6dmFyKC0teWVsbG93KX0KQG1lZGlhKG1heC13aWR0aDo4MDBweCl7aGVhZGVyLC5oZXJvLGZvb3RlcntwYWRkaW5nLWxlZnQ6MjBweDtwYWRkaW5nLXJpZ2h0OjIwcHh9LnRpbWVsaW5lLXdyYXB7Z3JpZC10ZW1wbGF0ZS1jb2x1bW5zOjFmcjtwYWRkaW5nOjI4cHggMjBweCA2MHB4fS5tb250aC1uYXZ7ZGlzcGxheTpub25lfS5zdGF0c3tncmlkLXRlbXBsYXRlLWNvbHVtbnM6cmVwZWF0KDIsMWZyKX0uY2FyZC1zdGF0dXMtcm93e2ZsZXgtZGlyZWN0aW9uOmNvbHVtbjthbGlnbi1pdGVtczpmbGV4LXN0YXJ0fX0=").decode()

STATUS_ICON = {'arriving':'🟢','transit':'🚢','sailing':'⚓','pending':'⏳'}
STATUS_PILL = {'arriving':'Прибывает','transit':'В пути','sailing':'Отплывает','pending':'Нет даты'}

MODELS = {
    'G9190H':  ('Автогрейдер',        'SDLG G9190H',  '🟡'),
    'G9165F':  ('Автогрейдер',        'SDLG G9165F',  '🟡'),
    'G9220H':  ('Автогрейдер',        'SDLG G9220H',  '🟡'),
    'E6255F':  ('Экскаватор',         'SDLG E6255F',  '⛏️'),
    'E6350H':  ('Экскаватор',         'SDLG E6350H',  '⛏️'),
    'E690F':   ('Экскаватор',         'SDLG E690F',   '⛏️'),
    'E7210H':  ('Экскаватор',         'SDLG E7210H',  '⛏️'),
    'L958F':   ('Фронтальный погрузчик','SDLG L958F', '🚜'),
    'L956FH':  ('Фронтальный погрузчик','SDLG L956FH','🚜'),
    'L956H':   ('Фронтальный погрузчик','SDLG L956H', '🚜'),
    'L933F':   ('Фронтальный погрузчик','SDLG L933F', '🚜'),
    'B877F':   ('Каток дорожный',     'SDLG B877F',   '🔵'),
    'SR900H':  ('Каток вибрационный', 'SDLG SR900H',  '🔵'),
    'SD26':    ('Бульдозер',          'SDLG SD26',    '🔨'),
    'D18H':    ('Бульдозер',          'SDLG D18H',    '🔨'),
}

SKIP_TOKENS = {'SKD','TDC','UST','ETD','ETA','BUS','SDLG','SRL','DOCS',
               'SHIPPING','SPARE','PARTS','FRET','CHINA','UST'}

def parse_equipment(raw):
    """
    Parse raw title string into list of dicts:
    [{'icon','type','model','qty','label'}, ...]
    """
    text = raw.upper()
    results = []
    found   = set()

    # Pattern: NxMODEL or MODEL+NxMODEL
    for m in re.finditer(r'(\d+)\s*[Xx]\s*([A-Z]\d+[A-Z0-9]*)', text):
        qty, model = m.group(1), m.group(2)
        if model in found: continue
        found.add(model)
        info = MODELS.get(model)
        if info:
            tp, mdl, icon = info
            results.append({'icon':icon,'type':tp,'model':mdl,'qty':int(qty)})
        else:
            results.append({'icon':'📦','type':'Техника','model':f'SDLG {model}','qty':int(qty)})

    # Standalone models (qty=1)
    for m in re.finditer(r'\b([A-Z]\d+[A-Z0-9]+)\b', text):
        model = m.group(1)
        if model in found or model in SKIP_TOKENS: continue
        info = MODELS.get(model)
        if not info: continue
        found.add(model)
        tp, mdl, icon = info
        results.append({'icon':icon,'type':tp,'model':mdl,'qty':1})

    # Buckets
    bm = re.search(r'(\d*)\s*[Xx]?\s*BUCKET', text)
    if bm or 'КОВШ' in text:
        qty = int(bm.group(1)) if bm and bm.group(1) else 1
        results.append({'icon':'🪣','type':'Ковш','model':'Навесное оборудование','qty':qty})

    # Forks
    fm = re.search(r'(\d*)\s*[Xx]?\s*FORK', text)
    if fm or 'ВИЛЫ' in text or 'ВИЛА' in text:
        qty = int(fm.group(1)) if fm and fm.group(1) else 1
        results.append({'icon':'🍴','type':'Вилы','model':'Навесное оборудование','qty':qty})

    # Yutong bus
    if 'YUTONG' in text and 'SPARE' not in text and 'PARTS' not in text:
        results.append({'icon':'🚌','type':'Автобус','model':'Yutong','qty':1})

    # Spare parts
    if 'SPARE' in text or 'ЗАП' in text:
        brand = 'SDLG' if 'SDLG' in text else ('Yutong' if 'YUTONG' in text else '')
        results.append({'icon':'🔧','type':'Запасные части','model':brand,'qty':0})

    # Robots AllyNav
    if 'ALLYNAV' in text or 'ALLYN' in text:
        results.append({'icon':'🤖','type':'Роботы','model':'AllyNav','qty':0})

    # Lonking forklift
    if 'LONKING' in text:
        results.append({'icon':'🏗️','type':'Погрузчик','model':'Lonking','qty':0})

    # Shandong Disam
    if 'DISAM' in text or 'SHANDONG' in text:
        results.append({'icon':'📦','type':'Техника','model':'Shandong Disam','qty':0})

    # Buldozer SD26 (text match)
    if 'BULDOZER' in text or 'БУЛЬДОЗЕР' in text:
        if not any(r['type']=='Бульдозер' for r in results):
            mdl_m = re.search(r'SD\d+', text)
            mdl = mdl_m.group(0) if mdl_m else 'SDLG'
            results.append({'icon':'🔨','type':'Бульдозер','model':f'SDLG {mdl}','qty':1})

    return results if results else [{'icon':'📦','type':'Груз','model':raw[:60],'qty':0}]


def build_card_items_html(equipment):
    """Build the equipment items list inside a card."""
    html = '<div class="eq-list">'
    for eq in equipment:
        qty_str = f'<span class="eq-qty">{eq["qty"]} ед.</span>' if eq['qty'] > 0 else ''
        model_str = f'<span class="eq-model">{eq["model"]}</span>' if eq['model'] else ''
        html += f'''<div class="eq-item">
  <span class="eq-type">{eq["type"]}</span>
  {model_str}
  {qty_str}
</div>'''
    html += '</div>'
    return html


# ── Parser ───────────────────────────────────────────────────────────────────

def parse_update_date(text):
    m = re.search(r'Обновление\s+(\d{1,2}/\d{1,2}/\d{4})', text)
    return m.group(1) if m else datetime.now().strftime("%d/%m/%Y")

def parse_shipments(text):
    shipments = []
    blocks = re.split(r'\n(?=\d+\))', text)
    for block in blocks:
        block = block.strip()
        if not block or not re.match(r'^\d+\)', block): continue
        s = {}
        num_m = re.match(r'^(\d+)\)', block)
        s['num'] = num_m.group(1) if num_m else '?'
        frets = re.findall(r'FRET\d+', block)
        s['fret'] = ' · '.join(frets) if frets else ''
        bls = re.findall(r'\b\d{9,}\b', block)
        bls += re.findall(r'[A-Z]{2,}\d{6,}-\d{6,}', block)
        s['bl'] = bls[0] if bls else ''
        ems = re.findall(r'EM\d{4}-\d+', block)
        s['em'] = ' + '.join(ems) if ems else ''
        containers = re.findall(r'SZYH\w+', block)
        rys = re.findall(r'RYS\w+', block)
        s['containers'] = ' · '.join(containers + rys)
        eta_m = re.search(r'ETA\s+Constanta\s+(\d{1,2}/\d{1,2}/\d{4})', block)
        etd_m = re.search(r'(\d{1,2}[-–]\d{1,2}/\d{2}/\d{4})', block)
        if eta_m:
            s['eta'] = eta_m.group(1)
            try:
                days = (datetime.strptime(s['eta'],"%d/%m/%Y") - datetime.now()).days
                s['status'] = 'arriving' if days <= 7 else 'transit'
            except:
                s['status'] = 'transit'
        elif 'Выплываем' in block or 'ETD' in block:
            s['status'] = 'sailing'
            s['eta'] = etd_m.group(1) if etd_m else 'уточняется'
        else:
            s['status'] = 'pending'
            s['eta'] = ''
        notes = []
        if re.search(r'Ждем|Ждём', block) and 'документ' in block.lower():
            notes.append('Ожидаем коммерческие документы от SDLG')
        if 'будет обновление' in block.lower():
            notes.append('Дата погрузки уточняется')
        s['note'] = ' · '.join(notes)
        # Extract raw title for equipment parsing
        raw = block
        raw = re.sub(r'^\d+\)\s*', '', raw)
        raw = re.sub(r'SHIPPING\s+DOCS[-–\s]*', '', raw)
        raw = re.sub(r'SPARE\s+PARTS\s+', 'SPARE PARTS ', raw)
        raw = re.sub(r'EM\d{4}-\d+\s*[+]?\s*', '', raw)
        raw = re.sub(r'[/\s]*FRET\d+[,\s]*', ' ', raw)
        raw = re.sub(r'\b\d{9,}\b', '', raw)
        raw = re.sub(r'[A-Z]{2,}\d{6,}-\d{6,}', '', raw)
        raw = re.sub(r'SZYH\w+[,\s]*', '', raw)
        raw = re.sub(r'RYS\w+[,\s]*', '', raw)
        raw = re.sub(r'ETA\s+Constanta\s+\S+', '', raw)
        raw = re.sub(r'ETD\s+China\s+\S+', '', raw)
        raw = re.sub(r'Прибытие|Выплываем|Ждем.*|Ждём.*|будет обновление.*', '', raw, flags=re.I)
        raw = re.sub(r'\s{2,}', ' ', raw).strip(' \n\t-–/')
        s['raw_title'] = raw
        s['equipment'] = parse_equipment(raw)
        shipments.append(s)
    return shipments


# ── HTML Generator ───────────────────────────────────────────────────────────

THEMES = [
    ('t-1','#2d8a4a','linear-gradient(130deg,#1a4d2e,#2d8a4a)'),
    ('t-2','#1a8080','linear-gradient(130deg,#0d4848,#1a8080)'),
    ('t-3','#1a4fa8','linear-gradient(130deg,#0d2468,#1a4fa8)'),
    ('t-4','#4c38c8','linear-gradient(130deg,#221468,#4c38c8)'),
    ('t-5','#8a38b8','linear-gradient(130deg,#441468,#8a38b8)'),
    ('t-6','#c43868','linear-gradient(130deg,#641438,#c43868)'),
    ('t-7','#b05800','linear-gradient(130deg,#522800,#b05800)'),
]



def parse_update_date(text):
    m = re.search(r'Обновление\s+(\d{1,2}/\d{1,2}/\d{4})', text)
    return m.group(1) if m else datetime.now().strftime("%d/%m/%Y")

def parse_shipments(text):
    shipments = []
    blocks = re.split(r'\n(?=\d+\))', text)
    for block in blocks:
        block = block.strip()
        if not block or not re.match(r'^\d+\)', block): continue
        s = {}
        num_m = re.match(r'^(\d+)\)', block)
        s['num'] = num_m.group(1) if num_m else '?'
        frets = re.findall(r'FRET\d+', block)
        s['fret'] = ' · '.join(frets) if frets else ''
        bls = re.findall(r'\b\d{9,}\b', block)
        bls += re.findall(r'[A-Z]{2,}\d{6,}-\d{6,}', block)
        s['bl'] = bls[0] if bls else ''
        ems = re.findall(r'EM\d{4}-\d+', block)
        s['em'] = ' + '.join(ems) if ems else ''
        containers = re.findall(r'SZYH\w+', block)
        rys = re.findall(r'RYS\w+', block)
        s['containers'] = ' · '.join(containers + rys)
        eta_m = re.search(r'ETA\s+Constanta\s+(\d{1,2}/\d{1,2}/\d{4})', block)
        etd_m = re.search(r'(\d{1,2}[-–]\d{1,2}/\d{2}/\d{4})', block)
        if eta_m:
            s['eta'] = eta_m.group(1)
            try:
                days = (datetime.strptime(s['eta'],"%d/%m/%Y") - datetime.now()).days
                s['status'] = 'arriving' if days <= 7 else 'transit'
            except:
                s['status'] = 'transit'
        elif 'Выплываем' in block or 'ETD' in block:
            s['status'] = 'sailing'
            s['eta'] = etd_m.group(1) if etd_m else 'уточняется'
        else:
            s['status'] = 'pending'
            s['eta'] = ''
        notes = []
        if re.search(r'Ждем|Ждём', block) and 'документ' in block.lower():
            notes.append('Ожидаем коммерческие документы от SDLG')
        if 'будет обновление' in block.lower():
            notes.append('Дата погрузки уточняется')
        s['note'] = ' · '.join(notes)
        # Extract raw title for equipment parsing
        raw = block
        raw = re.sub(r'^\d+\)\s*', '', raw)
        raw = re.sub(r'SHIPPING\s+DOCS[-–\s]*', '', raw)
        raw = re.sub(r'SPARE\s+PARTS\s+', 'SPARE PARTS ', raw)
        raw = re.sub(r'EM\d{4}-\d+\s*[+]?\s*', '', raw)
        raw = re.sub(r'[/\s]*FRET\d+[,\s]*', ' ', raw)
        raw = re.sub(r'\b\d{9,}\b', '', raw)
        raw = re.sub(r'[A-Z]{2,}\d{6,}-\d{6,}', '', raw)
        raw = re.sub(r'SZYH\w+[,\s]*', '', raw)
        raw = re.sub(r'RYS\w+[,\s]*', '', raw)
        raw = re.sub(r'ETA\s+Constanta\s+\S+', '', raw)
        raw = re.sub(r'ETD\s+China\s+\S+', '', raw)
        raw = re.sub(r'Прибытие|Выплываем|Ждем.*|Ждём.*|будет обновление.*', '', raw, flags=re.I)
        raw = re.sub(r'\s{2,}', ' ', raw).strip(' \n\t-–/')
        s['raw_title'] = raw
        s['equipment'] = parse_equipment(raw)
        shipments.append(s)
    return shipments


# ── HTML Generator ───────────────────────────────────────────────────────────

THEMES = [
    ('t-1','#2d8a4a','linear-gradient(130deg,#1a4d2e,#2d8a4a)'),
    ('t-2','#1a8080','linear-gradient(130deg,#0d4848,#1a8080)'),
    ('t-3','#1a4fa8','linear-gradient(130deg,#0d2468,#1a4fa8)'),
    ('t-4','#4c38c8','linear-gradient(130deg,#221468,#4c38c8)'),
    ('t-5','#8a38b8','linear-gradient(130deg,#441468,#8a38b8)'),
    ('t-6','#c43868','linear-gradient(130deg,#641438,#c43868)'),
    ('t-7','#b05800','linear-gradient(130deg,#522800,#b05800)'),
]

CSS = """*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--yellow:#FFC72C;--page-bg:#f2f0ea}
body{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;background:var(--page-bg);color:#0d0d0d;min-height:100vh;font-size:13px}
header{padding:0 48px;display:flex;align-items:center;justify-content:space-between;height:68px;position:sticky;top:0;z-index:200;background:rgba(5,20,40,0.6);backdrop-filter:blur(14px);border-bottom:1px solid rgba(255,255,255,0.08)}
.logo{display:flex;align-items:center;gap:14px;text-decoration:none}
.logo-mark{width:38px;height:38px;background:var(--yellow);border-radius:8px;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;color:#0d2040}
.logo-text{font-weight:700;font-size:15px;color:#fff}.logo-sub{font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:.1em;text-transform:uppercase}
.live-badge{display:flex;align-items:center;gap:8px;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.15);backdrop-filter:blur(8px);border-radius:24px;padding:6px 16px;font-size:11px;color:rgba(255,255,255,0.6)}
.live-dot{width:7px;height:7px;border-radius:50%;background:#4caf50;box-shadow:0 0 0 3px rgba(76,175,80,0.3);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{box-shadow:0 0 0 3px rgba(76,175,80,0.3)}50%{box-shadow:0 0 0 7px rgba(76,175,80,0.1)}}
.hero-section{position:relative;overflow:hidden}
.hero-bg{position:absolute;inset:0;background-image:url('https://images.unsplash.com/photo-1578575437130-527eed3abbec?w=1600&q=80&auto=format&fit=crop');background-size:cover;background-position:center 40%;filter:brightness(0.45) saturate(0.8)}
.hero-overlay{position:absolute;inset:0;background:linear-gradient(to bottom,rgba(5,20,40,0.6) 0%,rgba(5,20,40,0.3) 50%,rgba(5,20,40,0.85) 100%)}
.hero{position:relative;z-index:2;padding:48px 48px 52px}
.hero-label{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--yellow);margin-bottom:14px;font-weight:500}
.hero-title{font-size:clamp(32px,5vw,58px);font-weight:800;color:#fff;line-height:1.05;letter-spacing:-.02em;margin-bottom:8px}
.hero-title .y{color:var(--yellow)}
.hero-desc{font-size:13px;color:rgba(255,255,255,0.45);margin-bottom:40px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;max-width:720px;border-radius:14px;overflow:hidden;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.12);backdrop-filter:blur(16px)}
.stat-card{background:rgba(5,20,40,0.55);padding:20px 24px}
.stat-val{font-size:40px;font-weight:800;line-height:1;margin-bottom:5px;color:#fff}
.stat-val.yl{color:var(--yellow)}
.stat-lbl{font-size:10px;color:rgba(255,255,255,0.35);letter-spacing:.1em;text-transform:uppercase;font-weight:500}
.timeline-wrap{display:grid;grid-template-columns:200px 1fr;max-width:1100px;margin:0 auto;padding:60px 48px 80px}
.month-nav{position:sticky;top:88px;align-self:start;padding-right:28px;padding-top:4px}
.month-nav-title{font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#999;margin-bottom:16px;font-weight:600}
.month-item{display:flex;align-items:center;gap:10px;padding:7px 0;text-decoration:none;transition:opacity .15s}
.month-item:hover{opacity:.6}
.month-dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
.month-name{font-size:13px;font-weight:600;color:#0d0d0d}
.month-count{font-size:10px;color:#aaa;margin-left:auto;font-weight:500}
.nav-line{width:1px;height:18px;background:#ddd;margin:1px 0 1px 4px}
.month-section{margin-bottom:52px;scroll-margin-top:100px}
.month-header{display:flex;align-items:center;padding:20px 24px;border-radius:14px 14px 0 0;position:relative;overflow:hidden}
.month-header::after{content:'';position:absolute;inset:0;background:repeating-linear-gradient(-45deg,transparent,transparent 12px,rgba(255,255,255,0.06) 12px,rgba(255,255,255,0.06) 13px)}
.mh-icon{font-size:26px;margin-right:14px;position:relative;z-index:1}
.mh-info{position:relative;z-index:1;flex:1}
.mh-big{font-size:20px;font-weight:800;line-height:1;margin-bottom:3px}
.mh-small{font-size:11px;opacity:.65}
.mh-pill{position:relative;z-index:1;font-size:10px;font-weight:600;padding:5px 12px;border-radius:20px;background:rgba(255,255,255,0.22);text-transform:uppercase;letter-spacing:.06em;white-space:nowrap}
.cards{display:flex;flex-direction:column;gap:10px;padding-top:10px}
.card{background:#fff;border-radius:14px;padding:18px 22px;border:1.5px solid transparent;transition:transform .15s,box-shadow .15s,border-color .15s;animation:rise .45s ease both}
.card:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(0,0,0,0.07)}
@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.card-header{display:flex;align-items:flex-start;gap:14px;margin-bottom:12px}
.num-c{width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:15px;flex-shrink:0;margin-top:2px}
.card-headline{flex:1}
.card-status-row{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px}
.card-date-big{font-size:16px;font-weight:800;line-height:1}
.pill{display:inline-block;font-size:10px;font-weight:600;padding:4px 11px;border-radius:20px;text-transform:uppercase;letter-spacing:.05em;white-space:nowrap}
.card-dest{font-size:11px;color:#888;margin-top:3px}
.eq-list{display:flex;flex-direction:column;gap:6px;border-top:1px solid #f0ede6;padding-top:12px}
.eq-item{display:flex;align-items:center;gap:8px;padding:6px 10px;background:#faf9f6;border-radius:8px}
.eq-icon{display:none}
.eq-type{font-size:13px;font-weight:600;color:#0d0d0d}
.eq-model{font-size:12px;color:#888;margin-left:2px}
.eq-qty{margin-left:auto;font-size:12px;font-weight:700;padding:2px 10px;border-radius:12px;background:#eee;color:#444}
.card-note{font-size:11px;color:#e07000;margin-top:8px;font-weight:500;padding:6px 10px;background:#fff8ee;border-radius:8px;border-left:3px solid #e07000}
.card-tech{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.tech-pill{font-size:10px;color:#aaa;background:#f5f3ee;padding:2px 8px;border-radius:10px}

/* COLOR THEMES */
.t-1 .month-header{background:linear-gradient(130deg,#1a4d2e,#2d8a4a);color:#fff}
.t-1 .card{border-color:#c5eed5}.t-1 .card:hover{border-color:#4daa6d}
.t-1 .num-c{background:#d4f0df;color:#1a4d2e}.t-1 .card-date-big{color:#1a4d2e}.t-1 .pill{background:#d4f0df;color:#1a4d2e}.t-1 .eq-qty{background:#d4f0df;color:#1a4d2e}
.t-2 .month-header{background:linear-gradient(130deg,#0d4848,#1a8080);color:#fff}
.t-2 .card{border-color:#bde8e8}.t-2 .card:hover{border-color:#30aaaa}
.t-2 .num-c{background:#c8ecec;color:#0d4848}.t-2 .card-date-big{color:#0d4848}.t-2 .pill{background:#c8ecec;color:#0d4848}.t-2 .eq-qty{background:#c8ecec;color:#0d4848}
.t-3 .month-header{background:linear-gradient(130deg,#0d2468,#1a4fa8);color:#fff}
.t-3 .card{border-color:#c4d8f8}.t-3 .card:hover{border-color:#4080e0}
.t-3 .num-c{background:#d2e4fa;color:#0d2468}.t-3 .card-date-big{color:#0d2468}.t-3 .pill{background:#d2e4fa;color:#0d2468}.t-3 .eq-qty{background:#d2e4fa;color:#0d2468}
.t-4 .month-header{background:linear-gradient(130deg,#221468,#4c38c8);color:#fff}
.t-4 .card{border-color:#d8d2f8}.t-4 .card:hover{border-color:#7060e0}
.t-4 .num-c{background:#e2dcfa;color:#221468}.t-4 .card-date-big{color:#221468}.t-4 .pill{background:#e2dcfa;color:#221468}.t-4 .eq-qty{background:#e2dcfa;color:#221468}
.t-5 .month-header{background:linear-gradient(130deg,#441468,#8a38b8);color:#fff}
.t-5 .card{border-color:#e8d2f8}.t-5 .card:hover{border-color:#aa60d4}
.t-5 .num-c{background:#eedcfa;color:#441468}.t-5 .card-date-big{color:#441468}.t-5 .pill{background:#eedcfa;color:#441468}.t-5 .eq-qty{background:#eedcfa;color:#441468}
.t-6 .month-header{background:linear-gradient(130deg,#641438,#c43868);color:#fff}
.t-6 .card{border-color:#f8c4d8}.t-6 .card:hover{border-color:#e06090}
.t-6 .num-c{background:#fad2e4;color:#641438}.t-6 .card-date-big{color:#641438}.t-6 .pill{background:#fad2e4;color:#641438}.t-6 .eq-qty{background:#fad2e4;color:#641438}
.t-7 .month-header{background:linear-gradient(130deg,#522800,#b05800);color:#fff}
.t-7 .card{border-color:#f8debb}.t-7 .card:hover{border-color:#e08838}
.t-7 .num-c{background:#fae8ca;color:#522800}.t-7 .card-date-big{color:#522800}.t-7 .pill{background:#fae8ca;color:#522800}.t-7 .eq-qty{background:#fae8ca;color:#522800}
.t-sail .month-header{background:linear-gradient(130deg,#603800,#c47000);color:#fff}
.t-sail .card{border-color:#ffe4b8}.t-sail .card:hover{border-color:#f0a030}
.t-sail .num-c{background:#feeece;color:#603800}.t-sail .card-date-big{color:#603800}.t-sail .pill{background:#feeece;color:#603800}.t-sail .eq-qty{background:#feeece;color:#603800}
.t-pend .month-header{background:linear-gradient(130deg,#282828,#545454);color:#fff}
.t-pend .card{border-color:#dedad2}.t-pend .card:hover{border-color:#aaa}
.t-pend .num-c{background:#eae6de;color:#444}.t-pend .card-date-big{color:#555}.t-pend .pill{background:#eae6de;color:#555}.t-pend .eq-qty{background:#eae6de;color:#555}
footer{background:#0d2040;padding:28px 48px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px}
.ft-brand{font-size:13px;font-weight:600;color:rgba(255,255,255,0.35)}
.ft-brand span{color:var(--yellow)}
.ft-links{display:flex;gap:24px}
.ft-links a{font-size:11px;color:rgba(255,255,255,0.35);text-decoration:none;transition:color .15s;font-weight:500}
.ft-links a:hover{color:var(--yellow)}
@media(max-width:800px){header,.hero,footer{padding-left:20px;padding-right:20px}.timeline-wrap{grid-template-columns:1fr;padding:28px 20px 60px}.month-nav{display:none}.stats{grid-template-columns:repeat(2,1fr)}.card-status-row{flex-direction:column;align-items:flex-start}}"""

MONTHS_RU = ['','января','февраля','марта','апреля','мая','июня',
             'июля','августа','сентября','октября','ноября','декабря']
MONTHS_LONG = ['','Январь','Февраль','Март','Апрель','Май','Июнь',
               'Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь']

def date_nice(d):
    try:
        dt = datetime.strptime(d, "%d/%m/%Y")
        return f"{dt.day} {MONTHS_RU[dt.month]} {dt.year}"
    except:
        return d

def parse_date_dt(d):
    try: return datetime.strptime(d, "%d/%m/%Y")
    except: return datetime.max

def generate_html(shipments, update_date):
    # Group
    groups, sail, pend = {}, [], []
    for s in shipments:
        if s['status'] in ('arriving','transit'):
            groups.setdefault(s['eta'], []).append(s)
        elif s['status'] == 'sailing':
            sail.append(s)
        else:
            pend.append(s)

    sorted_dates = sorted(groups.keys(), key=parse_date_dt)

    total    = len(shipments)
    arriving = sum(1 for s in shipments if s['status']=='arriving')
    transit  = sum(1 for s in shipments if s['status'] in ('transit','sailing'))
    pending  = sum(1 for s in shipments if s['status']=='pending')

    all_dts = [parse_date_dt(d) for d in sorted_dates if parse_date_dt(d)!=datetime.max]
    if all_dts:
        period = f"{MONTHS_LONG[all_dts[0].month]} — {MONTHS_LONG[all_dts[-1].month]} {all_dts[-1].year}"
    else:
        period = str(datetime.now().year)

    nav_html = ''
    sections_html = ''
    ti = 0

    STATUS_ICON = {'arriving':'🟢','transit':'🚢','sailing':'⚓','pending':'⏳'}
    STATUS_PILL = {'arriving':'Прибывает','transit':'В пути','sailing':'Отплывает','pending':'Нет даты'}

    def make_card(s, delay):
        eq_html = ''
        for eq in s['equipment']:
            qty_str = f'<span class="eq-qty">{eq["qty"]} ед.</span>' if eq.get('qty',0)>0 else ''
            model_str = f'<span class="eq-model">{eq["model"]}</span>' if eq.get('model') else ''
            eq_html += f'<div class="eq-item"><div class="eq-label"><span class="eq-type">{eq["type"]}</span><span class="eq-model">{eq.get("model","")}</span></div>{qty_str}</div>'

        note_html = f'<div class="card-note">⚠️ {s["note"]}</div>' if s['note'] else ''

        # Tech pills (FRET, EM) — small, unobtrusive
        tech = []
        if s['fret']: tech.append(s['fret'])
        if s['em']:   tech.append(s['em'])
        tech_html = ''
        if tech:
            pills = ''.join(f'<span class="tech-pill">{t}</span>' for t in tech)
            tech_html = f'<div class="card-tech">{pills}</div>'

        date_display = date_nice(s['eta']) if s['eta'] else '—'
        pill_text    = STATUS_PILL.get(s['status'],'В пути')
        dest = 'Порт Констанца, Румыния' if s['status'] in ('arriving','transit') else ''
        dest_html = f'<div class="card-dest">📍 {dest}</div>' if dest else ''

        return f'''<div class="card" style="animation-delay:{delay:.2f}s">
  <div class="card-header">
    <div class="num-c">{s['num']}</div>
    <div class="card-headline">
      <div class="card-status-row">
        <div class="card-date-big">{date_display}</div>
        <span class="pill">{pill_text}</span>
      </div>
      {dest_html}
    </div>
  </div>
  <div class="eq-list">{eq_html}</div>
  {note_html}
  {tech_html}
</div>'''

    for date_key in sorted_dates:
        grp = groups[date_key]
        tc, dot_c, _ = THEMES[ti % len(THEMES)]
        ti += 1
        gid   = f'g{ti}'
        icon  = STATUS_ICON.get(grp[0]['status'],'🚢')
        pill  = STATUS_PILL.get(grp[0]['status'],'В пути')
        dn    = date_nice(date_key)
        cnt   = len(grp)

        nav_html += f'<a class="month-item" href="#{gid}"><div class="month-dot" style="background:{dot_c}"></div><div class="month-name">{dn}</div><div class="month-count">{cnt}</div></a><div class="nav-line"></div>\n'

        cards = ''.join(make_card(s, 0.05*(i+1)) for i,s in enumerate(grp))
        sections_html += f'''<div class="month-section {tc}" id="{gid}">
  <div class="month-header">
    <div class="mh-icon">{icon}</div>
    <div class="mh-info"><div class="mh-big">{dn}</div><div class="mh-small">Прибытие в Констанцу &nbsp;·&nbsp; {cnt} отправлений</div></div>
    <div class="mh-pill">{pill}</div>
  </div>
  <div class="cards">{cards}</div>
</div>\n'''

    if sail:
        nav_html += f'<a class="month-item" href="#g-sail"><div class="month-dot" style="background:#c47000"></div><div class="month-name">Отплывают</div><div class="month-count">{len(sail)}</div></a><div class="nav-line"></div>\n'
        cards = ''.join(make_card(s, 0.05*(i+1)) for i,s in enumerate(sail))
        sections_html += f'''<div class="month-section t-sail" id="g-sail">
  <div class="month-header"><div class="mh-icon">⚓</div><div class="mh-info"><div class="mh-big">Отплывают из Китая</div><div class="mh-small">{len(sail)} отправлений</div></div><div class="mh-pill">Отплывает</div></div>
  <div class="cards">{cards}</div>
</div>\n'''

    if pend:
        nav_html += f'<a class="month-item" href="#g-pend"><div class="month-dot" style="background:#888"></div><div class="month-name">Ожидают</div><div class="month-count">{len(pend)}</div></a>\n'
        cards = ''.join(make_card(s, 0.05*(i+1)) for i,s in enumerate(pend))
        sections_html += f'''<div class="month-section t-pend" id="g-pend">
  <div class="month-header"><div class="mh-icon">⏳</div><div class="mh-info"><div class="mh-big">Ожидают обновления</div><div class="mh-small">Дата уточняется &nbsp;·&nbsp; {len(pend)} отправлений</div></div><div class="mh-pill">Нет даты</div></div>
  <div class="cards">{cards}</div>
</div>\n'''

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Tracking — Hydro Tech Express</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<header>
  <a class="logo" href="https://sdlg.online" target="_blank">
    <div class="logo-mark">HTE</div>
    <div><div class="logo-text">Hydro Tech Express</div><div class="logo-sub">Официальный дилер SDLG</div></div>
  </a>
  <div class="live-badge"><div class="live-dot"></div>Обновлено {update_date}</div>
</header>
<div class="hero-section">
  <div class="hero-bg"></div><div class="hero-overlay"></div>
  <div class="hero">
    <div class="hero-label">Container Tracking · Hydro Tech Express SRL</div>
    <div class="hero-title">Мониторинг<br><span class="y">контейнеров</span></div>
    <div class="hero-desc">Китай → Констанца → Молдова &nbsp;·&nbsp; {period}</div>
    <div class="stats">
      <div class="stat-card"><div class="stat-val">{total}</div><div class="stat-lbl">Отправлений</div></div>
      <div class="stat-card"><div class="stat-val yl">{arriving}</div><div class="stat-lbl">Прибывают скоро</div></div>
      <div class="stat-card"><div class="stat-val">{transit}</div><div class="stat-lbl">В пути</div></div>
      <div class="stat-card"><div class="stat-val">{pending}</div><div class="stat-lbl">Ожидают данных</div></div>
    </div>
  </div>
</div>
<div class="timeline-wrap">
  <nav class="month-nav">
    <div class="month-nav-title">По датам прибытия</div>
    {nav_html}
  </nav>
  <div class="sections">{sections_html}</div>
</div>
<footer>
  <div class="ft-brand"><span>Hydro Tech Express SRL</span> — Официальный дилер SDLG в Молдове</div>
  <div class="ft-links">
    <a href="https://sdlg.online" target="_blank">sdlg.online</a>
    <a href="tel:+37360726262">+373 60 72 62 62</a>
  </div>
</footer>
</body></html>"""


def make_card(s, delay):
    eq_html = ""
    for eq in s["equipment"]:
        qty   = f'<span class="eq-qty">{eq["qty"]} ед.</span>' if eq.get("qty",0) > 0 else ""
        eq_html += (
            '<div class="eq-item">' +
            
            '<div class="eq-label">' +
            f'<span class="eq-type">{eq.get("type","")}</span>' +
            f'<span class="eq-model">{eq.get("model","")}</span>' +
            '</div>' + qty + '</div>'
        )
    note  = f'<div class="card-note">⚠️ {s["note"]}</div>' if s["note"] else ""
    tech  = [t for t in [s.get("fret",""), s.get("em","")] if t]
    tech_html = '<div class="card-tech">' + "".join(f'<span class="tech-pill">{t}</span>' for t in tech) + '</div>' if tech else ""
    date  = date_nice(s["eta"]) if s["eta"] else "—"
    pill  = STATUS_PILL.get(s["status"], "В пути")
    dest  = '<div class="card-dest">📍 Порт Констанца, Румыния</div>' if s["status"] in ("arriving","transit") else ""
    return (
        f'<div class="card" style="animation-delay:{delay:.2f}s">' +
        f'<div class="card-header"><div class="num-c">{s["num"]}</div>' +
        f'<div class="card-headline"><div class="card-status-row"><div class="card-date-big">{date}</div><span class="pill">{pill}</span></div>{dest}</div></div>' +
        f'<div class="eq-list">{eq_html}</div>{note}{tech_html}</div>'
    )

def generate_html(shipments, update_date):
    groups, sail, pend = {}, [], []
    for s in shipments:
        if s["status"] in ("arriving","transit"): groups.setdefault(s["eta"],[]).append(s)
        elif s["status"] == "sailing": sail.append(s)
        else: pend.append(s)
    dates    = sorted(groups.keys(), key=parse_date_dt)
    total    = len(shipments)
    arriving = sum(1 for s in shipments if s["status"]=="arriving")
    transit  = sum(1 for s in shipments if s["status"] in ("transit","sailing"))
    pending  = sum(1 for s in shipments if s["status"]=="pending")
    dts      = [parse_date_dt(d) for d in dates if parse_date_dt(d)!=datetime.max]
    period   = f"{MONTHS_LONG[dts[0].month]} — {MONTHS_LONG[dts[-1].month]} {dts[-1].year}" if dts else "2026"
    nav = ""
    secs = ""
    ti = 0
    for dk in dates:
        grp = groups[dk]; tc,dot,_ = THEMES[ti%len(THEMES)]; ti+=1
        gid=f"g{ti}"; icon=STATUS_ICON.get(grp[0]["status"],"🚢")
        pill=STATUS_PILL.get(grp[0]["status"],"В пути"); dn=date_nice(dk); cnt=len(grp)
        nav  += f'<a class="month-item" href="#{gid}"><div class="month-dot" style="background:{dot}"></div><div class="month-name">{dn}</div><div class="month-count">{cnt}</div></a><div class="nav-line"></div>\n'
        cards = "".join(make_card(s,0.05*(i+1)) for i,s in enumerate(grp))
        secs += f'<div class="month-section {tc}" id="{gid}"><div class="month-header"><div class="mh-icon">{icon}</div><div class="mh-info"><div class="mh-big">{dn}</div><div class="mh-small">Прибытие в Констанцу &nbsp;·&nbsp; {cnt} отправлений</div></div><div class="mh-pill">{pill}</div></div><div class="cards">{cards}</div></div>\n'
    if sail:
        nav  += f'<a class="month-item" href="#g-sail"><div class="month-dot" style="background:#c47000"></div><div class="month-name">Отплывают</div><div class="month-count">{len(sail)}</div></a><div class="nav-line"></div>\n'
        cards = "".join(make_card(s,0.05*(i+1)) for i,s in enumerate(sail))
        secs += f'<div class="month-section t-sail" id="g-sail"><div class="month-header"><div class="mh-icon">⚓</div><div class="mh-info"><div class="mh-big">Отплывают из Китая</div><div class="mh-small">{len(sail)} отправлений</div></div><div class="mh-pill">Отплывает</div></div><div class="cards">{cards}</div></div>\n'
    if pend:
        nav  += f'<a class="month-item" href="#g-pend"><div class="month-dot" style="background:#888"></div><div class="month-name">Ожидают</div><div class="month-count">{len(pend)}</div></a>\n'
        cards = "".join(make_card(s,0.05*(i+1)) for i,s in enumerate(pend))
        secs += f'<div class="month-section t-pend" id="g-pend"><div class="month-header"><div class="mh-icon">⏳</div><div class="mh-info"><div class="mh-big">Ожидают обновления</div><div class="mh-small">Дата уточняется &nbsp;·&nbsp; {len(pend)} отправлений</div></div><div class="mh-pill">Нет даты</div></div><div class="cards">{cards}</div></div>\n'
    logo = LOGO_SRC
    css  = MASTER_CSS
    return f"""<!DOCTYPE html>
<html lang="ru"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Tracking — Hydro Tech Express</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<header>
  <a class="logo" href="https://sdlg.online" target="_blank">
    <img class="logo-img" src="{logo}" alt="HTE">
    <div><div class="logo-text">Hydro Tech Express</div><div class="logo-sub">Официальный дилер SDLG</div></div>
  </a>
  <div class="live-badge"><div class="live-dot"></div>Обновлено {update_date}</div>
</header>
<div class="hero-section"><div class="hero-bg"></div><div class="hero-overlay"></div>
<div class="hero">
  <div class="hero-label">Container Tracking · Hydro Tech Express SRL</div>
  <div class="hero-title">Мониторинг<br><span class="y">контейнеров</span></div>
  <div class="hero-desc">Китай → Констанца → Молдова &nbsp;·&nbsp; {period}</div>
  <div class="stats">
    <div class="stat-card"><div class="stat-val">{total}</div><div class="stat-lbl">Отправлений</div></div>
    <div class="stat-card"><div class="stat-val yl">{arriving}</div><div class="stat-lbl">Прибывают скоро</div></div>
    <div class="stat-card"><div class="stat-val">{transit}</div><div class="stat-lbl">В пути</div></div>
    <div class="stat-card"><div class="stat-val">{pending}</div><div class="stat-lbl">Ожидают данных</div></div>
  </div>
</div></div>
<div class="timeline-wrap">
  <nav class="month-nav"><div class="month-nav-title">По датам прибытия</div>{nav}</nav>
  <div class="sections">{secs}</div>
</div>
<footer>
  <div class="ft-brand"><span>Hydro Tech Express SRL</span> — Официальный дилер SDLG в Молдове</div>
  <div class="ft-links"><a href="https://sdlg.online" target="_blank">sdlg.online</a><a href="tel:+37360726262">+373 60 72 62 62</a></div>
</footer></body></html>"""

def upload_html(html):
    body = json.dumps({"html": html}).encode()
    req  = urllib.request.Request(UPDATER_URL, data=body,
           headers={"X-Secret":UPDATER_KEY,"Content-Type":"application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def tg(method, **kwargs):
    body = json.dumps(kwargs).encode()
    req  = urllib.request.Request(f"{API}/{method}", data=body,
           headers={"Content-Type":"application/json"}, method="POST")
    with urllib.request.urlopen(req) as r:
        return json.load(r)

def send(chat_id, text):
    tg("sendMessage", chat_id=chat_id, text=text, parse_mode="HTML")

def typing(chat_id):
    tg("sendChatAction", chat_id=chat_id, action="typing")


def handle(msg):
    chat_id = msg["chat"]["id"]
    text    = msg.get("text","") or ""
    if chat_id != ADMIN_ID:
        send(chat_id,"⛔ Доступ запрещён."); return
    if text.startswith("/start") or text.startswith("/help"):
        send(chat_id,
            "👋 <b>HTE Tracking Bot v3</b>\n\n"
            "Перешли сюда текст от логиста — я обновлю "
            "<a href='https://tracking.sdlg.online'>tracking.sdlg.online</a> автоматически.")
        return
    if len(text) < 50:
        send(chat_id,"⚠️ Текст слишком короткий."); return
    typing(chat_id)
    try:
        update_date = parse_update_date(text)
        shipments   = parse_shipments(text)
        if not shipments:
            send(chat_id,"❌ Не удалось распарсить данные."); return
        typing(chat_id)
        html   = generate_html(shipments, update_date)
        result = upload_html(html)
        a = sum(1 for s in shipments if s["status"]=="arriving")
        t = sum(1 for s in shipments if s["status"] in ("transit","sailing"))
        p = sum(1 for s in shipments if s["status"]=="pending")
        send(chat_id,
            f"✅ <b>tracking.sdlg.online обновлён!</b>\n\n"
            f"📦 Всего: <b>{len(shipments)}</b>\n"
            f"🟢 Прибывают: <b>{a}</b>\n"
            f"🚢 В пути: <b>{t}</b>\n"
            f"⏳ Ожидают: <b>{p}</b>\n\n"
            f"🕐 {result.get('time','')}\n"
            f"🔗 <a href='https://tracking.sdlg.online'>tracking.sdlg.online</a>")
    except Exception as e:
        send(chat_id, f"❌ Ошибка: {e}")

if __name__ == "__main__":
    print("🤖 HTE Tracking Bot v3 — polling...")
    offset = 0
    while True:
        try:
            resp = tg("getUpdates", offset=offset, timeout=30)
            for upd in resp.get("result",[]):
                offset = upd["update_id"] + 1
                if "message" in upd:
                    handle(upd["message"])
        except Exception as e:
            print(f"Poll error: {e}")
            time.sleep(5)
