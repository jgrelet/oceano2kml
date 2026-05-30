# Configuration Reference

`oceano2kml` uses TOML files to define cruise metadata, NetCDF variable names, and instrument-specific settings.

## Global Keys (Required)

| Key | Type | Description | Example |
|-----|------|-------------|---------|
| `cruise` | string | Cruise identifier. Used for output KML filename (lowercased). | `"PIRATA-FR31"` |
| `time` | string | NetCDF variable name for time dimension. | `"TIME"` |
| `latitude` | string | NetCDF variable name for latitude. | `"LATITUDE"` |
| `longitude` | string | NetCDF variable name for longitude. | `"LONGITUDE"` |
| `profile` | string | NetCDF variable name for profile IDs. | `"PROFILE"` |

## Global Keys (Optional)

| Key | Type | Description | Example |
|-----|------|-------------|---------|
| `ship` | string | Ship name (unused in current version). | `"ANTEA"` |
| `size_plots` | integer | Plot width in pixels (unused in current version). | `700` |
| `station_number` | boolean | Enable station numbering (unused in current version). | `true` |

## Instrument Sections

Each instrument section (`[ctd]`, `[ladcp]`, `[xbt]`, `[tsg]`) is **optional**. Set `file = "none"` to disable an instrument.

### Profile Instruments: `[ctd]`, `[ladcp]`, `[xbt]`

**All profile instruments share the same keys:**

| Key | Type | Required | Description | Example |
|-----|------|----------|-------------|---------|
| `file` | string | Yes | Path to NetCDF file. Use `"none"` to disable. | `"data/amazomix/OS_AMAZOMIX_CTD.nc"` |
| `name` | string | Yes | Prefix for point names. | `"St"` |
| `name_format` | integer | Yes | Field width for profile number formatting. | `5` |
| `plots` | string | Yes | URL template for profile plots. `{:05d}` is replaced by the profile number. | `"http://example.org/plot-{:05d}.png"` |

**Example:**
```toml
[ctd]
file = "data/fr31/OS_PIRATA-FR31_CTD.nc"
name = "St"
name_format = 3
plots = "http://www.brest.ird.fr/us191/cruises/pirata-fr31/CTD/PIRATA-FR31-{:03d}_CTD.png"
```

> **Note:** LADCP data can be read from ADCP NetCDF files as a fallback. For example, `amazomix.toml` uses `OS_AMAZOMIX_ADCP.nc` for its `[ladcp]` section.

---

### Trajectory Instrument: `[tsg]`

| Key | Type | Required | Description | Example |
|-----|------|----------|-------------|---------|
| `file` | string | Yes | Path to NetCDF file. Use `"none"` to disable. | `"data/amazomix/OS_AMAZOMIX_TSG.nc"` |
| `params` | string | Yes | TSG parameters (unused in KML generation, but included in KML description). | `"SSPS,SSTP"` |
| `plots` | string | Yes | URL for TSG scatter plot. | `"http://example.org/tsg_plot.png"` |

**Example:**
```toml
[tsg]
file = "data/amazomix/OS_AMAZOMIX_TSG.nc"
params = "SSPS,SSTP"
plots = "http://www.brest.ird.fr/us191/cruises/amazomix/TSG/AMAZOMIX_TSG_COLCOR_SCATTER.png"
```

---

## Full Example: `amazomix.toml`

```toml
cruise = "AMAZOMIX"
ship = "ANTEA"
size_plots = 700
station_number = true
file = "netcdf"
time = 'TIME'
latitude = 'LATITUDE'
longitude = 'LONGITUDE'
profile = 'PROFILE'

[ctd]
file = 'data/amazomix/OS_AMAZOMIX_CTD.nc'
name = 'St'
name_format = 5
plots = "http://www.brest.ird.fr/us191/cruises/amazomix/CTD/AMAZOMIX-{:05d}_CTD.png"

[ladcp]
file = 'data/amazomix/OS_AMAZOMIX_ADCP.nc'
name = 'St'
name_format = 5
plots = "http://www.brest.ird.fr/us191/cruises/amazomix/LADCP/AMAZOMIX-{:05d}_ADCP.png"

[xbt]
file = 'data/amazomix/OS_AMAZOMIX_XBT.nc'
name = 'Xbt'
name_format = 2
plots = "http://www.brest.ird.fr/us191/cruises/amazomix/XBT/AMAZOMIX-{:05d}_XBT.png"

[tsg]
file = "data/amazomix/OS_AMAZOMIX_TSG.nc"
params = 'SSPS,SSTP'
plots = "http://www.brest.ird.fr/us191/cruises/amazomix/TSG/AMAZOMIX_TSG_COLCOR_SCATTER.png"
```
