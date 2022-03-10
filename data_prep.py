import pandas as pd
import json
state_abbreviation_to_name = {
	"AL": "Alabama",
	"AK": "Alaska",
	"AZ": "Arizona",
	"AR": "Arkansas",
	"CA": "California",
	"CO": "Colorado",
	"CT": "Connecticut",
	"DE": "Delaware",
	"DC": "District of Columbia",
	"FL": "Florida",
	"GA": "Georgia",
	"GU": "Guam",
	"HI": "Hawaii",
	"ID": "Idaho",
	"IL": "Illinois",
	"IN": "Indiana",
	"IA": "Iowa",
	"KS": "Kansas",
	"KY": "Kentucky",
	"LA": "Louisiana",
	"ME": "Maine",
	"MD": "Maryland",
	"MA": "Massachusetts",
	"MI": "Michigan",
	"MN": "Minnesota",
	"MS": "Mississippi",
	"MO": "Missouri",
	"MT": "Montana",
	"NE": "Nebraska",
	"NV": "Nevada",
	"NH": "New Hampshire",
	"NJ": "New Jersey",
	"NM": "New Mexico",
	"NY": "New York",
	"NC": "North Carolina",
	"ND": "North Dakota",
	"OH": "Ohio",
	"OK": "Oklahoma",
	"OR": "Oregon",
	"PA": "Pennsylvania",
	"RI": "Rhode Island",
	"SC": "South Carolina",
	"SD": "South Dakota",
	"TN": "Tennessee",
	"TX": "Texas",
	"UT": "Utah",
	"VT": "Vermont",
	"VI": "Virgin Islands",
	"VA": "Virginia",
	"WA": "Washington",
	"WV": "West Virginia",
	"WI": "Wisconsin",
	"WY": "Wyoming",
}

fips_code_to_name = {
	"01": "Alabama",
	"02": "Alaska",
	"04": "Arizona",
	"05": "Arkansas",
	"06": "California",
	"08": "Colorado",
	"09": "Connecticut",
	"10": "Delaware",
	"11": "District of Columbia",
	"12": "Florida",
	"13": "Georgia",
	"15": "Hawaii",
	"16": "Idaho",
	"17": "Illinois",
	"18": "Indiana",
	"19": "Iowa",
	"20": "Kansas",
	"21": "Kentucky",
	"22": "Louisiana",
	"23": "Maine",
	"24": "Maryland",
	"25": "Massachusetts",
	"26": "Michigan",
	"27": "Minnesota",
	"28": "Mississippi",
	"29": "Missouri",
	"30": "Montana",
	"31": "Nebraska",
	"32": "Nevada",
	"33": "New Hampshire",
	"34": "New Jersey",
	"35": "New Mexico",
	"36": "New York",
	"37": "North Carolina",
	"38": "North Dakota",
	"39": "Ohio",
	"40": "Oklahoma",
	"41": "Oregon",
	"42": "Pennsylvania",
	"44": "Rhode Island",
	"45": "South Carolina",
	"46": "South Dakota",
	"47": "Tennessee",
	"48": "Texas",
	"49": "Utah",
	"50": "Vermont",
	"51": "Virginia",
	"53": "Washington",
	"54": "West Virginia",
	"55": "Wisconsin",
	"56": "Wyoming",
	"60": "American Samoa",
	"66": "Guam",
	"69": "Northern Mariana Islands",
	"72": "Puerto Rico",
	"78": "Virgin Islands",
}



def get_data():
    """Generates dataframe with all data including shape of counties
    """
    data=pd.read_csv("counties.csv")
    #changes name from code to actual name of state
    data=data.replace({"state":state_abbreviation_to_name})
    geodata=pd.read_json("geojson_counties.json")

    #opens up geodata into a more accessible dataframe
    geodata=geodata.features.apply(pd.Series)
    geodata=pd.concat([geodata,geodata.properties.apply(pd.Series)],axis=1)
    geodata.drop(columns=["properties"],inplace=True)

    #creates new column with name in same format as in "data"
    geodata["County name"]=geodata.NAME+" "+geodata.LSAD
    geodata["County name"]=geodata["County name"].str.lower()

    #changes from fips code to name of state
    geodata=geodata.replace({"STATE":fips_code_to_name})
    print(geodata.shape)
    #merges data and geodata
    merging=pd.merge(geodata[["County name","STATE","COUNTY"]],data,how="inner",left_on="County name",right_on="name")

    #filters so that only counties with the same name in the same state are matched
    merging=merging[merging.STATE==merging.state]

    
    print(merging.shape)
    #TODO: something off about the shape changing? Are we losing some counties??

    
    return merging

