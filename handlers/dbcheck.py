import numpy as np
import pandas as pd
import warnings

from .log import Logger
from .messages import write_warning

pd.set_option('display.max_rows', 20)
warnings.filterwarnings("ignore")


def compCollar(bhid, ocname, ncname, encoding="ISO-8859-1"):

    # Collar Import
    log = Logger(name='compCollar')

    ocollar = pd.read_csv(ocname, encoding=encoding)
    log.info('***** OLD COLLAR INFO*****')
    print('# of collars:', len(ocollar))
    print('# of columns:', len(ocollar.columns))
    print('Columns are:\n', list(ocollar.columns))
    # display(ocollar.head(2))

    #############################################################

    ncollar = pd.read_csv(ncname, encoding=encoding)
    print('\n***** NEW COLLAR INFO*****')
    print('# of collars:', len(ncollar))
    print('# of columns:', len(ncollar.columns))
    print('Columns are:\n', list(ncollar.columns))
    # display(ncollar.head(2))

    # Columns Names

    print('\n***** COLUMNS NAMES *****')
    col_only_o = list(set(ocollar.columns)-set(ncollar.columns))
    col_only_n = list(set(ncollar.columns)-set(ocollar.columns))
    if not col_only_o and not col_only_n:
        print('\nAll columns names match!')
    else:
        print('\nDifferent column names were found!')
        if col_only_o:
            print('The column:', col_only_o, 'appears only on the old.')
        if col_only_n:
            print('The column:', col_only_n, 'appears only on the new.\n')

    # Additional Collars

    print('\n***** DIFFERENT COLLARS *****')
    #     bhid='BHID'
    merge_all = pd.merge(ocollar, ncollar, how='outer',
                         on=bhid, indicator=True, copy=False)
    df_add = merge_all.loc[merge_all['_merge'] != 'both', (bhid, '_merge')]
    df_add.reset_index(inplace=True, drop=True)
    df_add.replace('left_only', 'old', inplace=True)
    df_add.replace('right_only', 'new', inplace=True)
    df_add.columns = [bhid, 'DB']

    for i in merge_all.columns:
        if merge_all[i].isnull().values.any():
            merge_all[i].fillna(0, inplace=True)

    nameadd = 'different_collars.csv'
    df_add.to_csv(nameadd, index=False)
    print('There are', len(df_add), 'different collars found.')
    print(f'The list of additional collars was saved as: "{nameadd}"')

    # Differences in Data

    # merge_int is intersection, only where BHID is present on both
    merge_int = pd.merge(ocollar, ncollar, how='inner',
                         on=bhid, indicator=True, copy=False)

    for i in merge_int.columns:
        if merge_int[i].isnull().values.any():
            merge_int[i].fillna(0, inplace=True)

    cols_o = []
    cols_n = []
    for i in merge_int.columns:
        if i.endswith('_x'):
            cols_o.append(i)
        elif i.endswith('_y'):
            cols_n.append(i)

    df_diff = pd.DataFrame()
    df_diff[bhid] = merge_int[bhid]

    for i in range(len(cols_o)):
        if merge_int[cols_o[i]].dtype != merge_int[cols_o[i]].dtype:
            print('\nYou have different types of data for:',
                  cols_o[i], 'and', cols_n[i])
            print(cols_o[i], '=', merge_int[cols_o[i]].dtype)
            print(cols_n[i], '=', merge_int[cols_n[i]].dtype)
            df_diff[(cols_o[i][:-2])] = 'ERROR'
        else:
            if merge_int[cols_o[i]].dtype == 'object':
                cond = (merge_int[cols_o[i]] != merge_int[cols_n[i]])
                df_diff[(cols_o[i][:-2])] = cond*1
                df_diff.loc[cond, (cols_o[i][:-2]+'_old')
                            ] = merge_int.loc[cond, cols_o[i]]
                df_diff.loc[cond, (cols_o[i][:-2]+'_new')
                            ] = merge_int.loc[cond, cols_n[i]]
            else:
                cond = (np.abs(merge_int[cols_o[i]] -
                               merge_int[cols_n[i]]) > 0.001)
                df_diff[(cols_o[i][:-2])] = cond * 1
                df_diff.loc[cond, (cols_o[i][:-2]+'_old')
                            ] = merge_int.loc[cond, cols_o[i]]
                df_diff.loc[cond, (cols_o[i][:-2]+'_new')
                            ] = merge_int.loc[cond, cols_n[i]]

    print(f'\nThe total of matching collars is:, {len(merge_int)}')

    print('\nNumber of different records per column:')
    for i in df_diff.columns:
        if (i != bhid) and not (i.endswith('_old')) and not (i.endswith('_new')):
            print(i, '=', sum(df_diff[i]))

    namedif = 'different_data.csv'
    df_diff.to_csv(namedif, index=False)

    print(f'\nA csv table was saved as:, "{namedif}"')
    print('The table contains all collars that are matching in both old/new '
          'files with the respective fields.')
    print('It is in binary code, being 0 no difference, and 1 presence of '
          'difference.')
    print('Whenever a difference exists, both old/new values are shown.')


def compSurvey(bhid, at, ocname, ncname, encoding="ISO-8859-1"):

    # Survey Import

    osurvey = pd.read_csv(ocname, encoding=encoding)
    print('\n***** OLD SURVEY INFO*****')
    print('# of surveys:', len(osurvey))
    print('# of columns:', len(osurvey.columns))
    print('Columns are:\n', list(osurvey.columns))
    # display(osurvey.head(2))

    nsurvey = pd.read_csv(ncname, encoding=encoding)
    print('\n***** NEW SURVEY INFO*****')
    print('# of surveys:', len(nsurvey))
    print('# of columns:', len(nsurvey.columns))
    print('Columns are:\n', list(nsurvey.columns))
    # display(nsurvey.head(2))

    # Columns Names

    print('\n***** COLUMNS NAMES *****')
    col_only_o = list(set(osurvey.columns)-set(nsurvey.columns))
    col_only_n = list(set(nsurvey.columns)-set(osurvey.columns))
    if not col_only_o and not col_only_n:
        print('\nAll columns names match!')
    else:
        print('\nDifferent column names were found!')
        if col_only_o:
            print('The column:', col_only_o, 'appears only on the old.')
        if col_only_n:
            print('The column:', col_only_n, 'appears only on the new.\n')

    # Additional Surveys

    print('\n***** DIFFERENT SURVEYS *****')
    # outer option means all values will be merged (common ones and different ones)
    merge_all = pd.merge(osurvey, nsurvey, how='outer', on=[
                         bhid, at], indicator=True, copy=False)
    # extract only different values
    df_add = merge_all.loc[merge_all['_merge'] != 'both', (bhid, at, '_merge')]
    #recreate index from 0
    df_add.reset_index(inplace=True, drop=True)
    #left only and right only are default names from merge function.
    df_add.replace('left_only', 'old', inplace=True)
    df_add.replace('right_only', 'new', inplace=True)
    df_add.columns = [bhid, at, 'DB']
    #loop over all colums
    for i in merge_all.columns:
        #if value is nan (null)
        if merge_all[i].isnull().values.any():
            # fill it with 0, so formulas can work later on
            merge_all[i].fillna(0, inplace=True)
    nameadd = 'additional_surveys.csv'
    #save to .csv
    df_add.to_csv(nameadd, index=False)
    print('There are', len(df_add), 'additional surveys found.')
    print('The list of additional surveys was saved as:', '"' + nameadd + '"')

    # Differences in Data

    # merge_int is intersection, only where BHID and AT is present on both (inner option)
    merge_int = pd.merge(osurvey, nsurvey, how='inner', on=[
                         bhid, at], indicator=True, copy=False)

    for i in merge_int.columns:
        if merge_int[i].isnull().values.any():
            merge_int[i].fillna(0, inplace=True)
    #merge_int.index = ['BHID','AT']
    cols_o = []
    cols_n = []
    #fills cols_o with old file columns, and fills colls_n with new file columns
    for i in merge_int.columns:
        if i.endswith('_x'):
            cols_o.append(i)
        elif i.endswith('_y'):
            cols_n.append(i)
    #create list of common BHID and AT values
    df_diff = pd.DataFrame()
    df_diff[bhid] = merge_int[bhid]
    df_diff[at] = merge_int[at]

    #This loop will find for different values on each column. If value is the same, the returns 0.
    #If values are different, returns 1, and display the old and the new information.
    #the df_diff will contain all different values.
    for i in range(len(cols_o)):
        # if data format is different, show it.
        if merge_int[cols_o[i]].dtype != merge_int[cols_o[i]].dtype:
            print('\nYou have different types of data for:',
                  cols_o[i], 'and', cols_n[i])
            print(cols_o[i], '=', merge_int[cols_o[i]].dtype)
            print(cols_n[i], '=', merge_int[cols_n[i]].dtype)
            df_diff[(cols_o[i][:-2])] = 'ERROR'
        else:
            # if data format is the same, check if dtype is not nomeric, or object.
            if merge_int[cols_o[i]].dtype == 'object':
                # True if same value, False if values are different
                cond = (merge_int[cols_o[i]] != merge_int[cols_n[i]])
                #Transform 'True' and 'False' into '0' and '1'
                df_diff[(cols_o[i][:-2])] = cond*1
                #replace '_x' and '_y' by '_old' and '_new' and print the different value.
                df_diff.loc[cond, (cols_o[i][:-2]+'_old')
                            ] = merge_int.loc[cond, cols_o[i]]
                df_diff.loc[cond, (cols_o[i][:-2]+'_new')
                            ] = merge_int.loc[cond, cols_n[i]]
            else:
                #do the same, but for numeric vlaues
                cond = (np.abs(merge_int[cols_o[i]] -
                               merge_int[cols_n[i]]) > 0.001)
                df_diff[(cols_o[i][:-2])] = cond * 1
                df_diff.loc[cond, (cols_o[i][:-2]+'_old')
                            ] = merge_int.loc[cond, cols_o[i]]
                df_diff.loc[cond, (cols_o[i][:-2]+'_new')
                            ] = merge_int.loc[cond, cols_n[i]]

    print('\nThe total of matching surveys is:', len(merge_int))
    print('\nNumber of different records per column:')
    for i in df_diff.columns:
        if (i != bhid) and (i != at) and not (i.endswith('_old')) and not (i.endswith('_new')):
            print(i, '=', sum(df_diff[i]))

    namedif = 'different_data_survey.csv'
    df_diff.to_csv(namedif, index=False)

    print('\nA csv table was saved as:', '"'+namedif+'"')
    print('The table contains all surveys that are matching in both old/new files with the respective fields.')
    print('It is in binary code, being 0 no difference, and 1 presence of difference.')
    print('Whenever a difference exists, both old/new values are shown.')


def compAssay(bhid, from_i, to_i, ocname, ncname, encoding="ISO-8859-1"):


    #Assay Import
    oassay = pd.read_csv(ocname, encoding=encoding)
    print('\n***** OLD ASSAY INFO*****')
    print('# of assays:', len(oassay))
    print('# of columns:', len(oassay.columns))
    print('Columns are:\n', list(oassay.columns))
    # display(oassay.head(2))

    nassay = pd.read_csv(ncname, encoding=encoding)
    print('\n***** NEW ASSAY INFO*****')
    print('# of assays:', len(nassay))
    print('# of columns:', len(nassay.columns))
    print('Columns are:\n', list(nassay.columns))
    # display(nassay.head(2))

    # Columns Names

    print('\n***** COLUMNS NAMES *****')
    col_only_o = list(set(oassay.columns)-set(nassay.columns))
    col_only_n = list(set(nassay.columns)-set(oassay.columns))
    if not col_only_o and not col_only_n:
        print('\nAll columns names match!')
    else:
        print('\nDifferent column names were found!')
        if col_only_o:
            print('The column:', col_only_o, 'appears only on the old.')
        if col_only_n:
            print('The column:', col_only_n, 'appears only on the new.\n')

    # Additional Assays

    print('\n***** DIFFERENT ASSAYS *****')

    '''
    outer option means all values will be merged
    (common ones and different ones)
    '''
    merge_all = pd.merge(oassay, nassay, how='outer', on=[
                         bhid, from_i, to_i], indicator=True, copy=False)
    # extract only different values
    df_add = merge_all.loc[merge_all['_merge'] !=
                           'both', (bhid, from_i, to_i, '_merge')]
    # recreate index from 0
    df_add.reset_index(inplace=True, drop=True)

    # left only and right only are default names from merge function.
    df_add.replace('left_only', 'old', inplace=True)
    df_add.replace('right_only', 'new', inplace=True)
    df_add.columns = [bhid, from_i, to_i, 'DB']

    #loop over all colums
    for i in merge_all.columns:
        #if value is nan (null)
        if merge_all[i].isnull().values.any():
            # fill it with 0, so formulas can work later on
            merge_all[i].fillna(0, inplace=True)

    nameadd = 'additional_assays.csv'
    df_add.to_csv(nameadd, index=False)

    print(f'There are, {len(df_add)}, additional assays found.')
    print(f'The list of additional assays was saved as: "{nameadd}"')

    # Differences in Data

    '''
    merge_int is intersection, only where BHID, FROM, TO is present on
    both (inner option)'''
    merge_int = pd.merge(oassay, nassay, how='inner', on=[
                         bhid, from_i, to_i], indicator=True, copy=False)

    for i in merge_int.columns:
        if merge_int[i].isnull().values.any():
            merge_int[i].fillna(0, inplace=True)
    cols_o = []
    cols_n = []
    '''
    fills cols_o with old file columns, and fills colls_n with new file columns
    '''
    for i in merge_int.columns:
        if i.endswith('_x'):
            cols_o.append(i)
        elif i.endswith('_y'):
            cols_n.append(i)
    # create list of common BHID and AT values
    df_diff = pd.DataFrame()
    df_diff[bhid] = merge_int[bhid]
    df_diff[from_i] = merge_int[from_i]
    df_diff[to_i] = merge_int[to_i]
    '''
    This loop will find for different values on each column. If value is the
    same, the returns 0. If values are different, returns 1, and display the
    old and the new information. the df_diff will contain all different values.
    '''
    for i in range(len(cols_o)):
        # if data format is different, show it.
        if merge_int[cols_o[i]].dtype != merge_int[cols_o[i]].dtype:
            print('\nYou have different types of data for:',
                  cols_o[i], 'and', cols_n[i])
            print(cols_o[i], '=', merge_int[cols_o[i]].dtype)
            print(cols_n[i], '=', merge_int[cols_n[i]].dtype)
            df_diff[(cols_o[i][:-2])] = 'ERROR'
        else:
            # if data format is the same, check if dtype is not nomeric, or object.
            if merge_int[cols_o[i]].dtype == 'object':
                # True if same value, False if values are different
                cond = (merge_int[cols_o[i]] != merge_int[cols_n[i]])
                # Transform 'True' and 'False' into '0' and '1'
                df_diff[(cols_o[i][:-2])] = cond*1
                # replace '_x' and '_y' by '_old' and '_new' and print the different value.
                df_diff.loc[cond, (cols_o[i][:-2]+'_old')
                            ] = merge_int.loc[cond, cols_o[i]]
                df_diff.loc[cond, (cols_o[i][:-2]+'_new')
                            ] = merge_int.loc[cond, cols_n[i]]
            else:
                #do the same, but for numeric vlaues
                cond = (np.abs(merge_int[cols_o[i]] -
                               merge_int[cols_n[i]]) > 0.001)
                df_diff[(cols_o[i][:-2])] = cond * 1
                df_diff.loc[cond, (cols_o[i][:-2]+'_old')
                            ] = merge_int.loc[cond, cols_o[i]]
                df_diff.loc[cond, (cols_o[i][:-2]+'_new')
                            ] = merge_int.loc[cond, cols_n[i]]

    print('\nThe total of matching assays are:', len(merge_int))
    print('\nNumber of different records per column:')

    for i in df_diff.columns:
        if (i != bhid) and (i != from_i) and (i != to_i) and not (i.endswith('_old')) and not (i.endswith('_new')):
            print(i, '=', sum(df_diff[i]))

    namedif = 'different_data_assay.csv'
    df_diff.to_csv(namedif, index=False)

    print(f'\nA csv table was saved as:, "{namedif}"')
    print('The table contains all assays that are matching in both old/new'
          'files with the respective fields.')
    print('It is in binary code, being 0 no difference, and 1 presence of'
          'difference.')
    print('Whenever a difference exists, both old/new values are shown.')


def validSurvey(bhid, at, brg, dip, filen, encoding="ISO-8859-1"):
    # Survey Import

    print('\n############################################################')
    print('Starting Survey Validation')

    survey = pd.read_csv(filen, encoding=encoding)
    errordf = pd.DataFrame()
    error_l = np.array([])
    fields = [bhid, at, brg, dip]
    survey = survey[fields]
    cond_inv = survey[(survey[dip] > 90) | (survey[dip] < -90)
                      | (survey[brg] > 360) | (survey[brg] < -360)]
    print('\nValidation 1 - There are', len(cond_inv),
          'invalid Dip and azimuth values')
    if (len(cond_inv) > 0):
        errordf = errordf.append(cond_inv, ignore_index=True)
        error_l = np.append(error_l, len(cond_inv)*['Invalid Dip/Azimuth'])

    cond_nul = survey.isnull().sum().sum()
    print('\nValidation 2 - There are', cond_nul, 'null values')
    if cond_nul > 0:
        for v in fields:
            cond = survey.loc[survey[v].isnull()]
            if len(cond) > 0:
                errordf = errordf.append(cond, ignore_index=True)
                error_l = np.append(error_l, ['Null Values'])

    fields_dup = [at, brg, dip]
    cond_dup = survey[fields_dup]
    cond_dup = cond_dup[cond_dup.duplicated()]
    print('\nValidation 3 - There are', len(cond_dup), 'duplicated values')
    if (len(cond_dup) > 0):
        errordf = errordf.append(
            survey.loc[cond_dup.index.values], ignore_index=True)
        error_l = np.append(error_l, len(cond_dup)*['Duplicated Values'])

    errordf['TYPE'] = error_l
    errordf.sort_values([bhid, at], ignore_index=True, inplace=True)
    errordf.to_csv('error_survey.csv', index=False)
    print('\nErrors exported to "error_survey.csv"')
    print('############################################################\n')


def validCollar(bhid, xcol, ycol, zcol, dataframe, encoding="ISO-8859-1"):

    print('\n############################################################')

    write_warning('Starting Collar Validation')
    # Collar Import
    ncollar = dataframe
    collar = pd.DataFrame()
    cols = [bhid, xcol, ycol, zcol]
    collar = ncollar[cols]

    errordf = pd.DataFrame()
    error_l = np.array([])

    cond_1 = collar[(collar[xcol] == 0) | (
        collar[ycol] == 0) | (collar[zcol] == 0)]
    write_warning(f'\nValidation 1 - There are {len(cond_1)}, '
                  'ZERO value on Collar coordinates')
    if (len(cond_1) > 0):
        errordf = errordf.append(
            collar.loc[cond_1.index.values], ignore_index=True)
        error_l = np.append(error_l, len(cond_1)*['Zero Coordinate'])

    cond_2 = collar[(collar[xcol] % 1 == 0) | (
        collar[ycol] % 1 == 0) | (collar[zcol] % 1 == 0)]
    write_warning(f'\nValidation 2 - There are {len(cond_2)} '
                  'rounded collar coordinates')
    if (len(cond_2) > 0):
        errordf = errordf.append(
            collar.loc[cond_2.index.values], ignore_index=True)
        error_l = np.append(error_l, len(cond_2)*['Rounded Coordinate'])

    cols = [bhid]
    cond_3 = ncollar[cols]
    cond_3 = cond_3[cond_3.duplicated()]
    write_warning(f'\nValidation 3 - There are {len(cond_3)} '
                  'duplicated Hole ID')

    if (len(cond_3) > 0):
        errordf = errordf.append(
            collar.loc[cond_3.index.values], ignore_index=True)
        error_l = np.append(error_l, len(cond_3)*['Duplicate Hole ID'])

    cols = [xcol, ycol, zcol]
    cond_4 = ncollar[cols]
    cond_4 = cond_4[(cond_4.duplicated())]
    write_warning(f'\nValidation 4 - There are {len(cond_4)} '
                  'duplicate coordinates')

    if (len(cond_4) > 0):
        errordf = errordf.append(
            collar.loc[cond_4.index.values], ignore_index=True)
        error_l = np.append(error_l, len(cond_4)*['Duplicate Coordinates'])

    cond_5 = collar[
        (collar[xcol] > (
            collar[ycol].mean()-collar[ycol].std())) &
        (collar[xcol] < (
            collar[ycol].mean()+collar[ycol].std())) &
        (collar[ycol] > (
            collar[xcol].mean()-collar[xcol].std())) &
        (collar[ycol] < (
            collar[xcol].mean()+collar[xcol].std()))
        ]

    write_warning(f'\nValidation 5 - There are {len(cond_5)} '
                  'inverted X and Y')
    if (len(cond_5) > 0):
        errordf = errordf.append(
            collar.loc[cond_5.index.values], ignore_index=True)
        error_l = np.append(error_l, len(cond_5)*['Inverted X and Y'])

    errordf['TYPE'] = error_l
    return errordf


def validAssay(bhid, from_i, to_i, fields, filen, encoding="ISO-8859-1"):
    #Assay Import

    print('\n############################################################')
    print('Starting Assay Validation')

    errordf = pd.DataFrame()

    assay = pd.read_csv(filen, encoding=encoding)
    cols = [bhid, from_i, to_i] + fields
    assay = assay[cols]
    cond_neg = np.sum(np.sum(assay[fields] <= 0))
    print('\nValidation 1- There are', cond_neg, 'negative/zero values')
    if cond_neg > 0:
        for v in fields:
            cond = assay.loc[assay[v] <= 0]
            if len(cond) > 0:
                errordf = errordf.append(cond, ignore_index=True)

    errordf['TYPE'] = 'negative/zero'
    errordf.sort_values([from_i, to_i], ignore_index=True, inplace=True)
    errordf.to_csv('error_assay.csv', index=False)
    print('\nErrors exported to "error_assay.csv"')
    print('############################################################\n')
