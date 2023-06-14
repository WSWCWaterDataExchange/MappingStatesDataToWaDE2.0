To download this file, click [here](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/raw/master/1_DataTableTemplatesAndMetadata/Site_Specific_Data/template_site_specific_data_WaDE.xlsx) 




**Feasibility of importing stream or reservoir data**
The feasibility of retrieving site-specific reservoir and observation site (SSRO) time series data depends on the following information, which lists the minimum requirements to fit the data into the Water Data Exchange (WaDE) database. 


**Minimum Site Information & Related Metadata.**

* Site Type: A high-level description of the site type categorization recognized by the data provider (e.g., well, spring, reservoir, river, ditch, etc.). Provided site type should be unique per site.
* Water Source Type: A high-level description of the water source type categorization. Simple water type classification of either surface water, groundwater, or reuse is preferred. 
* Latitude and Longitude location information per site in decimal degrees format. In numeric format. Preference is a six-significant digit number in World Geodetic System (WGS) (WGS) 1984.
* Unique identifier code / ID used by the data provider to distinguish the data site in the source data set. Code / ID should be unique enough such that it separates out sites from one another. Site identifiers should be unique to the data provider, and care should be taken to prevent mix-ups in site IDs if another data provider is using a similar code / ID style. Site ID should be used to retrieve and tie time-series information to the site.  


**Minimum Time Series Information & Related Metadata**

* The reported time of the measurement is related to the timestep, used to separate other measurements made at different times. Preferably in a YYYY-MM-DD-MM format, timestep dependent.
* Known timestep of the time series data (e.g., daily, monthly, annual, etc.).
* The measured values are in a numeric format.
* The unit of the measured value (e.g., CFS, AF, etc.). If the unit of measurement is not either in a CFS or AF value, data providers should provide means of converting the given unit to CFS or AF.
* Unique identifier code / ID used by the data provider to distinguish the data site in the source data set. Code / ID should be unique enough to separate out sites. Site identifiers should be unique to the data provider, and care should be taken to prevent mix-ups in site IDs if another data provider is using a similar code / ID style. Site ID should be used to retrieve and tie time series information to the site.
* Purpose of measurement (i.e., variable terminology): high-level description used by the data provider on the use of the time series data (e.g., withdrawal flow, discharge flow, reservoir volume, reservoir height, stream gage height, well depth, well withdrawal flow, etc.).


**Site and Timeseries Data Retrieval (machine-readable format availability)**

* **Site Data Retrieval**
* Data should be publicly accessible/downloadable anytime and not require administrative approval or email correspondence to retrieve.
* Data should be accessible on a state-hosted website or service.
* Site data should be available in a tabular format (shapefile, CSV, etc.) so that the WaDE staff can easily access and process the data.
* Metadata should be provided / accessible for this site information. The meaning of the unique entry should be provided. Any abbreviated code and its meanings should be provided.

* **Time-series Data Retrieval**
* Data should be publicly accessible/downloadable at any time and not require administrative approval or email correspondence to retrieve.
* Data should be accessible on a state-hosted website or service.
* Time series data retrieval should come in machine readable tabular format, mass accessed either through an API using provided unique site identification ID or available in a single CSV download where it can be tied to site information using a unique site identification ID. If API data retrieval is available, the data should be accessible in a CSV tabular-friendly format.
* Metadata should be provided / accessible for this site information. The meaning of the unique entry should be provided. Any abbreviated code and its meanings should be provided
