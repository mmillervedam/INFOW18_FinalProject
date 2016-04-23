"""
Data cleaning functions for
 INFOW18 Final Project (NYC Crime)
"""

# TODO: Add tally columns to vadir final data set
# TODO: Re-order columns - is this needed?
# TODO: Create function to clean other data

# imports
import numpy as np
import pandas as pd
from pandas import DataFrame, Series


##############################################################
# Helper functions for VADIR cleaning
def vadir_column_data_row(df):
	"""
	Helper function to determine where the column index starts
	INPUT: DataFrame
	OUTPUT: Row location - integer
	"""

	columns = df.columns
	c = [c for c in columns if str(c[:7]).lower() == 'unnamed'][0]  # first unnamed column
	irow = df[c].first_valid_index()
	return irow

def vadir_clean_cnames(df, row_num, replace_dict = {}):
    """
    Helper function to clean up column names for VARDIS files.
    INPUT: dataframe, index of the row that contains the names,
           and an optional dictionary of column names that need
           to be replaced as keys and the values as the new
           columns names
    OUTPUT: list of column names
    """
    names = list(df.iloc[row_num])
    newnames = [replace_dict.get(cname, cname) for cname in names]
    for idx in range(len(newnames)):
        if str(newnames[idx]) == 'nan' and str(newnames[idx-1][:6]).lower() != 'weapon':
            newnames[idx] = newnames[idx-1] + '_nw' # 'no weapon'
            newnames[idx-1] += '_ww' # 'with weapon'
        elif str(newnames[idx]) == 'nan' and str(newnames[idx-1][:6]).lower() == 'weapon':
            newnames[idx] = newnames[idx-1] + '_ts' # 'through screening'
            newnames[idx-1] += '_oc' # 'other circumstances'
    return newnames

def vadir_get_cnames_replace(df_list, df_to_use):
    """
    This function determines the column differecnes between each
    of the excel files passed in.
    INPUT: list of excel files to import and the file with the
           right column names to use to compare against
    OUTPUT: dictionary of excel files as keys and list of unmatched
            columns as values of the dictionary
    """
    columns_to_use = []
    other_columns = {}
    unmatched_c = {}
    for df in df_list:
        if df == df_to_use:
            df_import = pd.read_excel(df)
            c_row = vadir_column_data_row(df_import)
            columns_to_use = vadir_clean_cnames(df_import, c_row)
            unmatched_c[df] = columns_to_use
        else:
            df_import = pd.read_excel(df)
            c_row = vadir_column_data_row(df_import)
            other_columns[df] = vadir_clean_cnames(df_import, c_row)
    for df, columns in other_columns.items():
        unmatched_c[df] = [c for c in columns if c not in columns_to_use]
    return unmatched_c


##############################################################
# Helper functions for loading/merging VADIR data
def vadir_concat_dfs(df_dict, replace_dict):
    """
    This function concatenates the specified dataframes into one,
    appends a school year column for each of the different year files,
    and replaces the right columns in order to be able conctenate and
    have the same columns across all dataframes in the list.
    INPUT: dictionary of years as keys and the excel file related to
           to that year to concatenate, and a dictionary of column names that need
           to be replaced as keys and the values as the new
           columns names
    OUTPUT: cancatenated dataframe with all years
    """
    concat_df = pd.DataFrame()
    for year, f in df_dict.items():
        df = pd.read_excel(f)
        c_row = vadir_column_data_row(df)
        row_start = c_row + 2
        columns_to_use = vadir_clean_cnames(df, c_row, replace_dict)
        df.columns = columns_to_use
        df = df[row_start:]
        df['School Year'] = [year] * len(df)
        concat_df = pd.concat([concat_df, df], ignore_index = True)
        print ('... data from {} appended. Added {} rows for a total of {}.'.format(f, len(df), len(concat_df)))
    return concat_df

def vadir_reorder_columns(df, beginner_columns):
    """
    This function re-orders columns and returns a new data DataFrame
    INPUT: dataframe and columns that need to go in the beginning of the data DataFrame
    OUPUT: new datarame with re-ordered columns
    """
    df_columns = beginner_columns + [c for c in df.columns.tolist() if c not in beginner_columns]
    new_df = df[df_columns]
    return new_df

def vadir_create_tallies(df, tally_columns):
    df[tally_columns] = df[tally_columns].apply(lambda x: pd.to_numeric(x))
    df['Total Incidents'] = df[tally_columns].sum(axis=1)

    weapon_cols = [x for x in tally_columns if x[-3:] == '_ww']
    df['Incidents w/ Weapons'] = df[weapon_cols].sum(axis=1)

    no_weapon_cols = [x for x in tally_columns if x[-3:] == '_nw']
    df['Incidents w/o Weapons'] = df[no_weapon_cols].sum(axis=1)
    return df

def vadir_clean_concat_df(concat_df):
    """
    This function is very customized to the VADIR data set and cleans
    data we know is dirty
    INPUT: the concatenated DataFrame
    OUTPUT: clean DataFrame
    """
    #remove commentary data - this is where the unique school identifier is null
    index_remove = concat_df[concat_df['BEDS Code'].isnull()].index.values.tolist()
    concat_df.drop(index_remove, axis=0, inplace=True)
    concat_df.reindex()

    #clean up county values - some are capitalized differently, spelled differently, etc
    #others are duplicated (i.e Kings should be Brooklyn)
    concat_df['County']= concat_df['County'].apply(lambda x: x.title() if type(x) == type('s') else x)
    cleancounty = {'Bronx': 'Bronx', 'Queens': 'Queens', 'Brooklyn': 'Brooklyn', 'Kings': 'Brooklyn', 'New York': 'New York',
               'Manhattan': 'Manhattan', 'Richmond': 'Staten Island', 'Nyc Central Office': 'Nyc Central Office',
               'Manhatten': 'Manhattan', 'Nassau': 'Nassau', 'nan': 'nan'}
    concat_df['County'] = concat_df['County'].apply(cleancounty.get)

    #replace 'Charter School' with 'Charter' to remove dupes
    indices = concat_df[concat_df['School Type'] == 'Charter School'].index.tolist()
    concat_df.loc[indices, 'School Type'] = 'Charter'

    # Adjust 'School Name' values to all have the same capitalization
    concat_df['School Name']= concat_df['School Name'].apply(lambda x: x.title() if type(x) == type('s') else x)
    return concat_df

##############################################################
# Main function for loading and cleaning VADIR data

def load_and_clean_VADIR():
    """
    Function to load, join and clean VADIR (performs a series
    of functions from the cleandata module). Returns school
    dataframe ready for analysis.
    """
    # Raw data for each year
    RAW_DATA_DICT = {2006: 'VADIR_2006.xls', 2007: 'VADIR_2007.xls',
                     2008: 'VADIR_2008.xls', 2009: 'VADIR_2009.xls',
                     2010: 'VADIR_2010.xls', 2011: 'VADIR_2011.xls',
                     2012: 'VADIR_2012.xls', 2013: 'VADIR_2013.xls',
                     2014: 'VADIR_2014.xls'}

    # Duplicate name columns in raw files (and their replacements)
    DUP_COLS = {'County Name':'County',
                'District Name': 'District',
                'BEDS CODE': 'BEDS Code',
                'False Alarm':'Bomb Threat False Alarm',
                'Other Sex offenses': 'Other Sex Offenses',
                'Use Possession or Sale of Drugs': 'Drug Possession',
                'Use Possession or Sale of Alcohol': 'Alcohol Possession',
                'Other Disruptive Incidents': 'Other Disruptive Incidents',
                'Drug Possesion': 'Drug Possession',
                'Alcohol Possesion': 'Alcohol Possession',
                'Other Disruptive': 'Other Disruptive Incidents'}

    # Read in raw data and correct duplicate columns
    vadir_df = vadir_concat_dfs(RAW_DATA_DICT, DUP_COLS)

    # Reorder columns putting demographic information first.
    DEMO_COLS = ['School Name', 'School Type', 'School Year', 'BEDS Code',
                 'County', 'District', 'Enrollment', 'Grade Organization',
                 'Need/Resource Category']
    vadir_df = vadir_reorder_columns(vadir_df, DEMO_COLS)

    # Create Columns for  tot incidents and w/ and w/o weapons
    COLUMNS = vadir_df.columns.tolist()
    INCIDENT_COLS = [c for c in COLUMNS if c not in DEMO_COLS]
    vadir_df = vadir_create_tallies(vadir_df, INCIDENT_COLS)

    # fix name capitalization, remove comment rows and duplicate names/counties
    school_df = vadir_clean_concat_df(vadir_df)

    return school_df


##############################################################
# Main function for cleaning NYPD data

def load_and_clean_NYPD():
    """
    Function to cleanup NYPD felony data inclding, reset index,
    create shorthand columns for dates, remove data from before 2006.
    INPUT: dataframe loaded from 'NYPD_7_Major_Felony_Incidents.csv'
    OUTPUT: cleaned dataframe
    """
    felony_df = pd.read_csv('NYPD_7_Major_Felony_Incidents.csv',
                            index_col = False)
    # reset index
    felony_df.set_index('OBJECTID', inplace = True)

    #creating a new column to strip off Time from Occurrence Date
    cname = 'Short Occurrence Date'
    felony_df[cname]= pd.to_datetime(felony_df['Occurrence Date'])
    felony_df[cname] = [d.strftime('%Y-%m-%d') if not pd.isnull(d) else '' for d in felony_df['Short Occurrence Date']]

    #removing data prior to 2006 (by occurence date b/c year has issues)
    rows_to_drop = felony_df[felony_df["Short Occurrence Date"] <= '2005-12-31']
    felony_df.drop(rows_to_drop.index, inplace=True)

    # Fixing Occurrence year incase some are still mislabeled
    felony_df['Occurrence Year'] = felony_df["Short Occurrence Date"
                                             ].apply(lambda x: x[:4])

    # Create column for month order
    month_order = {'Jan':'01(Jan)', 'Feb': '02(Feb)', 'Mar': '03(Mar)',
                   'Apr': '04(Apr)', 'May': '05(May)', 'Jun': '06(Jun)',
                   'Jul': '07(Jul)', 'Aug': '08(Aug)', 'Sep': '09(Sep)',
                   'Oct': '10(Oct)', 'Nov': '11(Nov)', 'Dec': '12(Dec)'}
    cname2 = 'Occurrence Month Ordered'
    felony_df[cname2] = felony_df['Occurrence Month'].map(month_order)

    # Create column for day order
    day_order = {'Monday': '1 (Mon)', 'Tuesday': '2 (Tues)',
                 'Wednesday': '3 (Wed)', 'Thursday': '4 (Thur)',
                 'Friday': '5 (Fri)', 'Saturday': '6 (Sat)',
                 'Sunday': '7 (Sun)'}
    cname3 = 'Day of Week Ordered'
    felony_df[cname3] = felony_df['Day of Week'].map(day_order)

    # Create column for school year
    felony_df['Occurrence Year'] = felony_df['Occurrence Year'].astype(np.int64)
    felony_df['School Year'] =  felony_df['Occurrence Year'] - (felony_df['Occurrence Month Ordered'] < '08')

    print('... loaded NYPD felony data: {} observations'.format(len(felony_df)))
    return felony_df
