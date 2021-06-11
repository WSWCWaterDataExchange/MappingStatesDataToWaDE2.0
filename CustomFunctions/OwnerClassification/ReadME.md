# WaDE Owner Classification Type Project Overview
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to categorizing water right's owners into easily distinguishable groups for the purpose of data filtering and dashboard visualizations.


## Summary of Data Prep
The WaDE **OwnerClassificationTypeCV** field was assigned by utilizing a keyword search algorithm using the state provided water right owner (e.g., **AllocationOwner** field in WaDE) information.  The keyword search starts with a generic term search, but then is overridden with a more term specific search (e.g. a water right owner listed as *AZ USBR* would at first be labeled as an Arizona type owner, but then replaced with a more specific Bureau Reclamation type owner).  Water right records can possess multiple owners.  Records within WaDE with multiple **AllocationOwner** entries were given a single best fist term for **OwnerClassificationTypeCV**, as WaDE only allows for a single entry (at this time 06/11/2021).  Terms not found in the keyword search were given the default value of 'In Review', for further review by the WSWC staff and state agencies.



## Keyword Search Lists
This listed provided below are used to determine WaDE **OwnerClassificationTypeCV** field.  Lists are not concrete, and will be updated as more / better water right owner information is provided.  

**OwnerClassificationTypeCV** types include the following:
- Generic
- Government
- Military
- Natural Resources


***
### Generic Keywords
- **Unspecified**. unList = ["unspecified", "unknown"]
- **Native American**. nalist = ["apace tribe","apache nation","arapaho tribes","arapahoe tribes","blackfeet tribe","cheyenne tribe","indian reservation","kalispel tribe","kootenai tribe","kootenai tribes","muckleshoot indian tribe","navajo nation","navajo tribe","otoe missouria tribe","paiute tribe","peoria tribe","puyallup tribe","quapaw tribe","quileute tribe","quinault indian nation","seneca cayuga tribe","shawnee tribe","shoshone paiute tribes","shoshone tri","shoshone tribe","shoshone tribes","sioux tribe","spirit lake tribe","spokane tribe","stillaquamish indian tribe","ute indian tribe","ute mountain ute tribe","wyandotte tribe","yomba shoshone tribe","yurok tribe","zuni indian tribe","zuni tribe","apache indians","quechan tribe","navajo & hopi indian","pautte tribe","cocopah indain tribe"]


***
### Government Keywords
- **Bureau of Indian Affairs (USBIA)**. bialist = ["bureau of indian aff", "indian affairs", "usbia"]
- **Department of Housing and Urban Development (USHUD)**. ushudlist = ["housing and urban development", "housing & urban development", "ushud"]
- **Federal Aviation Administration (USFAA)**. usfaalist = ["usfaa", "federal aviation administration"]
- **General Services Administration (USGSA)**. usgsalist = ["usgsa", "general services administration"]


***
### Military Keywords
- **Army (USA)**. usaalist = ["us army", "u s army", "usarmy", "usa army", "national guard", "corps of engineer", "corps of engineers", "army corp", "army corps", "army corp of", "usa department of the army"]
- **Customs and Border Patrol (USCBP)**. uscbplist = ["uscbp", "border patrol", "border protection", "customs service ", "customs office"]
- **Department of Defense (USDOD)**. usdodlist = ["department of defense", "dept of defense"]
- **Department of Homeland Security (USDHS)**. usdhslist = ["dhs", "homeland security"]
- **Marine Corps (USMC)**. usmarinelist = ["marine corps"]
- **United States Air Force (USAF)**. usaflist = [ "usaf", "usafb", "afb", "air force", "airforce", "aire force", "air national guard"]


***
### Natural Resources Keywords
- **Bureau of Land Management (USBLM)**. usblmlist = ["usblm", "blm", "bureau of land mgmt", "bureau of land management", "bureau of land mgmnt", "bureau of land mgt", "bureau of land managment", "bureau of land managenemt"]
- **Bureau Reclamation (USBR)**. usbrlist = ["usbr", "bureau of reclam", "bureau of reclamation", "bureau reclamation"]
- **Department of Agriculture (USDA)**. usdalist = ["u s  dept of agriculture", "u s agriculture", "us agriculture dept", "us department agriculture", "us dept of agriculture", "usa  department of agriculture", "usa  dept of agriculture", "usda"]
- **Department of Energy (USDOE)**. usdoelist = ["department of energy", "u s department of energy", "u s dept  of energy lanl", "u s  department of energy", "u s  department of energy", "u s department of energy", "united states department of energy", "us department energy", "us department of energy", "us doe", "usa department of energy"]
- **Environmental Protection Agency (USEPA)**. epalist = ["environmental protection agency", "epa", "e p a"]
- **Fish and Wildlife Service (USFWS)**. fwlist = ["u s department of the interior fish and wildlife service","u s dept of fish & wildlife","u s dept of the interior fish and wildlife","u s fish & wildlife","u s fish and wildlife","united states fish and wildlife","united states of america fish and wildlife","us department fish & wildlife","us department of fish & wildlife","us dept of interior fish and wildlife","us dept of the interior fish and wildlif","us fish & wild life","us fish & wildlife","us fish and wildlife","us interior dept fish & wildlife","usa department of interior fish and wildlife","usa dept of interior fish & wildlife","usa fish & wildlife","usa fish and wildlife","usdi fish & wildlife","usdi fish and wildlife","usdoi fish & wildlife","usfws"]
- **Forest Service (USFS)**. usfslist = ["forest service united states","forest service usda","u s d a forest service","u s forest service","u s forest","united states forest service","us forest service","usa forest service","usda forest service","usfs"]
- **Geological Survey (USGS)**. usgslist = ["u s geological survey","us geological survey","usa geological survey"]
- **National Park Service (USNPS)**. usnplist = ["national park", "natl park serv", "national forest", "nat forest", "natl forest"]