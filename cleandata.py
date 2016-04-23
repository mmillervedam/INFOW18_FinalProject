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
# Main functions for loading/merging VADIR data
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
# Main function for cleaning NYPD data

def clean_NYPD(felony_df):
	"""
	Function to cleanup NYPD felony data inclding, reset index,
	create shorthand columns for dates, remove data from before 2006.
	INPUT: dataframe loaded from 'NYPD_7_Major_Felony_Incidents.csv'
	OUTPUT: cleaned dataframe
	"""
	# reset index
	felony_df.set_index('OBJECTID', inplace = True)

	#creating a new column to strip off Time from Occurrence Date
	cname = 'Short Occurrence Date'
	felony_df[cname]= pd.to_datetime(felony_df['Occurrence Date'])
	felony_df[cname] = [d.strftime('%Y-%m-%d') if not pd.isnull(d) else ''
						for d in felony_df['Short Occurrence Date']]

	#removing data prior to 2006 (by occurence date b/c year has issues)
    rows_to_drop = felony_df[felony_df["Short Occurrence Date"]<='2005-12-31'].index
    felony_df.drop(rows_to_drop, inplace=True)
    
	# Fixing Occurrence year incase some are still mislabeled
	felony_df['Occurrence Year'] = felony_df["Short Occurrence Date"].apply(lambda x: x[:4])

	# Create column for month order
	month_order = {'Jan':'01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
				   'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
				   'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
	cname2 = 'Occurrence Month Ordered'
	felony_df[cname2] = [month_order[m] + ' ' + m
						 for m in felony_df['Occurrence Month']]

	# Create column for day order
	day_order = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4,
                 'Friday': 5, 'Saturday': 6, 'Sunday': 7}
	cname3 = 'Day of Week Ordered'
	felony_df[cname3] = [str(day_order[d]) + ' ' + d
						 for d in felony_df['Day of Week']]
    
    # Create column for school year
    felony_df['Occurrence Year'] = felony_df['Occurrence Year'].astype(np.int64)
    school_year = felony_df['Occurrence Year'] - (felony_df['Occurrence Month Ordered'] < '08')
    felony_df['School Year'] =  school_year
    
	return felony_df_2006						  
