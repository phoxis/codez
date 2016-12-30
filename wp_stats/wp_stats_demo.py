#!/bin/python3

# Sample code to utilise the wordpress.com stats API .

#####################################
#
# NOTE: Please run the script in python3 interpreter, and change the first #! line accordingly
#       OR run like   /path/to/python3
#       
#       Commandline arguments
#       --id <apikey>     : Specifies the API Key
#       --blog <blogurl>  : Specifies the blog URL
#       --noplot          : If this switch is present, on-screen plots will not be shown
#       --noget           : If this switch is present, the files will not be downloaded from web API.
#       
#       # NOTE: Please run the script without any commandline arguments for *default behaviour*
#       # Default behaviour will display the blog information http://phoxis.org
#       # Download information from the blog and also plot on screen.
#       
######################################
# # 
# # KNOWN ISSUES: 
# # Fetching searchterms will fail.
# # All exceptions are not properly handled.
# # Negative testcases are not used for testing.
# #  
# # TO IMPLEMENT:
# # Postwise stats is not implemented. [INPROGRESS]
# # Weekly stats not implemented.
# # Flexible selection of filenames and other configurables needs to be done.
# # 
# # 
# # 


# TODO: [1] Error checking, and throw exceptions. [2] A little bit beautiful code maybe? 
#       [3] Try remove hardcoded things. [4] Verbose option to print, show progresss? [5] More useful stats?
#       [6] We need to put the impute the values inside the functions and not in the generic function, such that
#           they can impute as per required. This needs change in other functions as well. Take out the impute
#           function from the generic and get it inside the specific functions.
#       [7] Useful postwise stats.
#       [8] Re-factor code, Pandas time series would be a better optoin.

# Check for proper version then run
import sys
if sys.version_info < (3, 0):
  print ("[Please use python3]");
  print ("[*] Change the #! statement at the begining of this file and make sure it points to a python3 interpreter " + \
         "\nOR \n[*] Run like /path/to/python3 <file_name>.py");
  print ("Script terminating")
  sys.exit (0);
  
  
  
  
import urllib.request
import re
import pandas as pd
import matplotlib.pyplot as plt
import urllib.parse
import math
import argparse

# TODO: Make proper exception handling
class ArgError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs);
        
class FileIOError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs);
        
class URLFetchError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs);
        
class JSONParseError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs);
        
class WPStatsFetchError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs);
    
class UnknownError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs);


class ImputeError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs);

code_to_month = {  
                   "01": "January",
                   "02": "February",
                   "03": "March",
                   "04": "April",
                   "05": "May",
                   "06": "June",
                   "07": "July",
                   "08": "August",
                   "09": "September",
                   "10": "October",
                   "11": "November",
                   "12": "December"
                };

### Makes a wordpress com api call url
### TODO: This can be extended to a proper api with defined argument and return protocols, as 
### no proper API exists for this site. Will be interesting.
def make_wp_url (api_key, blog_id_uri = None, table = None, post_id = None, end = None, days = None, period = None, limit = None, summarize = None, form = None):
  
  blog_uri = None;
  blog_id  = None;
  
  if api_key is None:
    raise ArgError ("Argument \"api_key\" is mandatory", e);
    return (-1);
  
  if blog_id_uri is not None:
    if isinstance (blog_id_uri, str):
      blog_uri = blog_id_uri;
    elif isinstance (blog_id_uri, int):
      blog_id = blog_id_uri;
    else:
      raise ArgError ("Argument passed in \"blog_id_uri\" is not a string or a number", e);
  else:
    raise ArgError ("Argument \"blog_id_uri\" must be provided", e);
    return (-2);
  
  req_url = "http://stats.wordpress.com/csv.php";
  args = "";
  
  # API Key
  args += "?api_key=" + api_key;
  # Blog ID takes precedence if both are provided
  if blog_id:
    args += "&blog_id=" + blog_id;
  else:
    args += "&blog_uri=" + blog_uri;
    
  if table:
    valid_table_args = ["views", "postviews", "referrers", "referrers_grouped", "searchterms", "clicks", "videoplays"];
    if table not in valid_table_args:
      raise ArgError ("Argument \"table\" can have only values in [" + ','.join (valid_table_args) + "]", e);
      return (-3);
    else:
      args += "&table=" + table;
    
  if post_id:
    try:
      for this_post_id in post_id.split (','):
        int (this_post_id);
        
    except ValueError as e:
      raise ArgError ("Argument \"post_id\" should have a comma seperated list of post ids. First encountered malformed value was \"" + this_post_id + "\"", e);
      return (-4);
      
    args += "&post_id=" + post_id;
  
  if end:
    m = re.search ("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", end);
    if m:
      [yyyy, mm, dd]  = m.group(0).split ("-");
      # NOTE: Lazy validation. Full validation is not done.
      if not (int(yyyy) > 1970 and (int(mm) >= 1 and int (mm) <= 12) and (int (dd) >= 1 and int (dd) <= 31)):
        raise ArgError ("Argument \"end\" has got malformed value for \"yyyy-mm-dd\". Value found was " + end + "\nNote: Year should be > 1970", e);
    else:
      raise ArgError ("Argument \"end\" should be in a \"yyyy-mm-dd\" format, value found was " + end, e);
      
    args += "&end=" + end;
    
  if days:
    args += "&days=" + str (days);
    
  if period:
    # NOTE: This is to work with table and days. But, as even if these parameters are None, the server will assume default. Anyways, we don't do any detailed validation.
    valid_period_args = ["week", "month", "days"];
    if period not in valid_period_args:
      raise ArgError ("Argument \"period\" can have only values in [" + ','.join (valid_period_args) + "]", e);
      return (-4);
    else:
      args += "&period=" + period;
    
  if limit:
    args += "&limit=" + str (limit);
    
  if summarize:
    # NOTE: This is a flag.
    args += "&summarize";
    
  if form:
    valid_format_args = ["csv", "xml", "json"];
    if form not in valid_format_args:
      raise ArgError ("Argument \"form\" can have only values in [" + ','.join (valid_format_args) + "] value found \"" + form + "\"", e);
    else:
      args += "&format=" + form;
    

  return req_url + args;




# Makes wp.com api url, fetches it and saves to a file
def wp_stats_fetch (wp_api_args, file_save):
  
  wp_url = None;
  
  try:
    
    wp_url = make_wp_url (wp_api_args["api_key"], 
                          wp_api_args["blog_id_uri"], 
                          wp_api_args["table"], 
                          wp_api_args["post_id"], 
                          wp_api_args["end"], 
                          wp_api_args["days"], 
                          wp_api_args["period"], 
                          wp_api_args["limit"], 
                          wp_api_args["summarize"], 
                          wp_api_args["form"]
                          );
    
    # DEBUG PRINT
    #print (wp_url);
    
    response = urllib.request.urlopen (wp_url);
    
    file_ext = None;
    if wp_api_args["form"]:
      file_ext = "." + wp_api_args["form"];
    else:
      file_ext = ".csv";
      
    text = response.read().decode("utf-8");
    m = re.search ("Error:", text);
    if m:
      raise WPStatsFetchError ("Incorrect url arguments, Error returned");
      return (-1);
    
    fp = open (file_save + file_ext, "w");
    fp.write (text);
    fp.close ();
    
  except ArgError as e:
    print (e);
    return (wp_url);
  
  except Exception as e:
    print (e);
    return (wp_url);
  
  return 0;



###
# params
#   df : A Pandas dataframe
#   
# return
#   -1     : Argument invalid
#   Success: returns a list of attribute names with missing values.
# 
# throws
#   ArgError
#   
# summary: 
###
def attrs_with_na (df):
    # Find missing value
    # Convert boolean dataframe indicating if the ij^th value is missing or not.
    # Make column-wise set for each attribute. Now the result will contain the 
    # Possible boolean values which are present in each column. Next check if there
    # is a True in any of the columns in the aggregated info check_na. If yes, then
    # this is one columns with atleast a missing value in it.
    if df is None:
        raise ArgError ("Dataframe missing");
        return (-1);
    # TODO: check pandas dataframe
    
    missing_attrs = list ([]);
    check_na = pd.isnull(df).apply(set, 0);
    for row_name in check_na.index:
        if True in check_na[row_name]:
            missing_attrs.append (row_name);
    return (missing_attrs);
  

###
# params
#   df                      : A Pandas dataframe
#   missing_attrs (optional): A list of attributes with missing values to be imputed
#   cont_method   (optional): Imputation method for continuous variables. Possible values in ["mean", "median"]
#   cat_method    (optional): Imputation method for categorical variables. Possible values in ["mode"]
#   
# return
#   -1     : Argument invalid
#   -2     : Invalid value for cont_method
#   -3     : Invalid value for cat_method
#   Success: returns 0
# throws
#   ArgError, ImputeError
#   
# summary: 
###
# TODO: Implement removal of rows with missing values
def impute_missing (df, missing_attrs = None, cont_method = "median", cat_method = "mode", remove_row = False):
    
    if df is None:
        raise ArgError ("Dataframe missing");
        return (-1);
    #TODO: validate Pandas dataframe
    
    # If missing attributes are not provided, then call
    # attrs_with_na () to get the list first and then process
    if not missing_attrs:
        missing_attrs = attrs_with_na (df);
        
    # Filling missing values with median
    for this_missing_attr in missing_attrs:
        if df.dtypes[this_missing_attr] not in ["object"]:
            if cont_method is "median":
                df[this_missing_attr] = df[this_missing_attr].fillna(df[this_missing_attr].median());
                
            elif cont_method is "mean":
                df[this_missing_attr] = df[this_missing_attr].fillna(df[this_missing_attr].mean());
                
            else:
                raise ImputeError ("Invalid continuous variable imputation method: \"%s\"" % (cont_method));
                return (-2);

        else:
            if cat_method in ["mode"]:
                df[this_missing_attr] = df[this_missing_attr].fillna(df[this_missing_attr].mode());
                
            else:
                raise ImputeError ("Invalid categorical variable imputation method: \"%s\"" % (cat_method));
                return (-3);
            
    return df;


###
# params
#   df    : A Pandas dataframe
#   field : A string indicating the column having the date in yyyy-mm-dd, to be shattered.
#   
# return
#   -1     : Argument invalid
#   Success: returns the given dataframe with the date field removed and the shattered data fields added with 
#            the new columns yyyy, mm and dd
# 
# throws
#   ArgError
#   
# summary: Breaks down the date field to yyyy, mm, dd fields
###
def shatter_date (df, field):
  
  if df is None:
    raise ArgError ("Dataframe missing");
    return (-1);
  #TODO: validate Pandas dataframe

  date_flds = df[field].str.split ('-').apply (pd.Series, 1);
  date_flds.columns = ["yyyy", "mm", "dd"];
  del df[field];
  df = date_flds.join (df);
  del date_flds;
  return df;


# TODO: Make a frame which will make a weekly dataframe, maybe need to refer the calender
def make_weekly_visits (df):
  #TODO: validate Pandas dataframe
  pass;


###
# params
#   stat_type : The type of stats for the wordpress.com blog. Should be in 
#               ["views", "clicks", "referrers"] for now.
#   datafile  : A string indicating the path of the datafile to be loaded
#   
# return
#   -1     : Argument invalid
#   -2     : File input-output error
#   Success: returns the given stats structure returned by the called function, depending on the stat_type value
# 
# throws
#   ArgError, FileIOError
#   
# summary: Depending on the requested stat_type, calls the required functions. This will work as a generic interface.
#          TODO: Should be able to handle csv, json, xml in future in transparent way.
###
def analyse_stats (stat_type, datafile):
  
  valid_stat_types =  ["views", "clicks", "referrers", "postviews"];
  if (stat_type not in valid_stat_types):
    raise ArgError ("Stat type should be one of " + ','.join (valid_stat_types));
    return (-1);
  
  retval = None;
  
  try:
    
    data = pd.read_csv (datafile);
    na_attrs = attrs_with_na(data);
    
    if len (na_attrs) > 0:
      data = impute_missing (data, na_attrs);
        
      
    data = shatter_date (data, "date");
      
    if stat_type   == "views":
      retval = analyse_stats_views (data);
    elif stat_type == "clicks":
      retval = analyse_stats_clicks (data);
    elif stat_type == "referrers":
      retval = analyse_stats_referrs (data);
    elif stat_type == "postviews":
      retval = analyse_stats_postviews (data);
    else:
      raise UnknownError ("Something went wrong internally");
      return (-2);
  
  except IOError as e:
    raise FileIOError ("Error with file \"" + datafile + "\". Make sure the file name and path is correct. Else to re-download stats files from webAPI, use \"fetch_data = True\" in function \"initialize\"", e);
    return (-3);
           
  except Exception as e:
    print ("Unhandled exception caught: " + str (e));

  return (retval);


# TODO: We need to group the missing values to one row.
# TODO: WORK ON PROGRESS on BYPOST STATS
def analyse_stats_postviews (data):
  
  if data is None:
    raise ArgError ("Dataframe missing");
    return (-1);
  
  postview_stats = pd.Series ();
  
  #missing_index = pd.isnull(data).any(1).nonzero()[0];
  
  overall_post_count = data.groupby (["post_id", "post_title"]).sum ().sort_values (by="views", ascending=False);
  total_views = overall_post_count["views"].sum ();
  percent_view = (overall_post_count / total_views) * 100;
  overall_post_count = pd.concat ([overall_post_count, pd.DataFrame ({'percent_view': percent_view["views"]}, index=overall_post_count.index)], axis = 1);
  
  postview_stats['overall_postviews'] = overall_post_count;
  
  fig, axes = plt.subplots (nrows=2, ncols=2);
  overall_post_count["percent_view"].plot (kind="bar", fontsize=6, axes=axes[0,0]);
  axes[0,0].set_title ("Postviews by percent barplot");
  
  st = fig.suptitle ("Overall postviews", fontsize="large");
  st.set_y (0.99);
  
  dft = df.groupby (["post_id","post_title", "mm","yyyy"]).sum ().reset_index ();

  
  return (postview_stats);


###
# params
#   data   : A Pandas dataframe.
#   
# return
#   -1     : Argument invalid
#   Success: Statistics about clicks
# 
# throws
#   ArgError
#   
# summary: Performs analysis with clicks data and generates plots, saves stats in a json file. 
#          Returns click stats data. This function will assume
#            [1] All missing data has been imputed using 'impute_missing' function (or by other means). 
#            [2] Date field should be shattered using 'shatter_date' function.
###
def analyse_stats_clicks (data):
  
  if data is None:
      raise ArgError ("Dataframe missing");
      return (-1);
      
  click_stat = pd.Series ();
  precent_threshold = 1.0;
  
  # Clean urls and get the root of the URL, sort by highest to lowest clicks
  data["click"] = data.apply (lambda x: urllib.parse.urlparse(x["click"]).netloc,1);
  click_group = data.groupby(["click"]).sum().sort_values(by="views", ascending=0);
  #print ("clicks_sorted = \n" + str (click_group));
  
  click_stat['unique_sites']   = click_group.shape[0];
  click_stat['total_clicks']   = click_group["views"].sum();
  
  # Add percentage information to click_groups
  percent_view = click_group["views"] / click_group["views"].sum() * 100;
  click_group = pd.concat ([click_group, pd.DataFrame ({'percent_view': percent_view}, index=click_group.index)], axis = 1); 
  
  click_stat['click_table']    = click_group;
  
  # Compute a new dataframe with links with visits less than `percent_threshold' grouped together
  idx_lt = pd.DataFrame (click_group[click_group["percent_view"] < precent_threshold].sum ()).transpose ();
  idx_lt.index = ["others"];
  new_click_group = click_group[click_group["percent_view"] >= precent_threshold];
  new_click_group = new_click_group.append (idx_lt);
  
  fig, axes = plt.subplots (nrows=1, ncols=2);
  
  new_click_group["percent_view"].plot.pie(autopct="%1.2f",shadow=True, ax=axes[0]);
  axes[0].set_title ("Overall clicks piechart");
  
  new_click_group["percent_view"].plot (kind="bar", rot=90, alpha=0.75, fontsize=6, ax=axes[1]);
  axes[1].set_title ("Overall clicks barchart");
  
  st = fig.suptitle ("Overall clicks", fontsize="large");
  st.set_y (0.99);

  # TODO: These features can be made flexible and controlled by parameters in future

  # Save the plots in pdf files.
  fig.set_size_inches (17.7,10);
  #fig.tight_layout ();
  
  plot1_name = "plot_clicks_01.pdf";
  print ("\tSaving click analysis plot" + plot1_name);
  fig.savefig(plot1_name, dpi=100);
  
  json_file_name = "click_stats.json";
  print ("\tSaving click stats summary json" + json_file_name);
  click_stat.to_json (json_file_name);
  
  return (click_stat);
  


###
# params
#   data   : A Pandas dataframe.
#   
# return
#   -1     : Argument invalid
#   Success: Statistics about referrers
# 
# throws
#   ArgError
#   
# summary: Performs analysis with referrers data and generates plots, saves stats in a json file. 
#          Returns referrers stats data. This function will assume
#            [1] All missing data has been imputed using 'impute_missing' function (or by other means). 
#            [2] Date field should be shattered using 'shatter_date' function.
###
def analyse_stats_referrs (data):
  
  if data is None:
      raise ArgError ("Dataframe missing");
      return (-1);
      
  referrer_stat = pd.Series ();
  precent_threshold = 0.5;
  
  # Clean urls and get the root of the URL, sort by highest to lowest referrers
  data["referrer"] = data.apply (lambda x: urllib.parse.urlparse(x["referrer"]).netloc,1);
  referrer_group = data.groupby (["referrer"]).sum().sort_values(by="views", ascending=0);
  old_index = pd.Series(referrer_group.index);
  old_index[old_index == ""] = "(unknown)";
  referrer_group.index = old_index;
  #print ("referrers_sorted = \n" + str (referrer_group));
  
  referrer_stat['unique_referrer']   = referrer_group.shape[0];
  referrer_stat['total_referrer']   = referrer_group["views"].sum();
  
  # Add percentage information to referrer_groups
  percent_view = referrer_group["views"] / referrer_group["views"].sum() * 100;
  referrer_group = pd.concat ([referrer_group, pd.DataFrame ({'percent_view': percent_view}, index=referrer_group.index)], axis = 1); 
  
  referrer_stat['referrer_table']    = referrer_group;
  
  # Compute a new dataframe with links with visits less than `percent_threshold' grouped together
  idx_lt = pd.DataFrame (referrer_group[referrer_group["percent_view"] < precent_threshold].sum ()).transpose ();
  idx_lt.index = ["others"];
  new_referrer_group = referrer_group[referrer_group["percent_view"] >= precent_threshold];
  new_referrer_group = new_referrer_group.append (idx_lt);
  
  fig, axes = plt.subplots (nrows=1, ncols=2);
  
  new_referrer_group["percent_view"].plot.pie(autopct="%1.2f",shadow=True, ax=axes[0]);
  axes[0].set_title ("Overall referrers piechart");
  
  new_referrer_group["percent_view"].plot (kind="bar", rot=45, alpha=0.75, fontsize=10, ax=axes[1]);
  axes[1].set_title ("Overall referrers barchart");
  
  st = fig.suptitle ("Overall referrers", fontsize="large");
  st.set_y (0.99);

  # Save the plots in pdf files.
  fig.set_size_inches (17.7,10);
  #fig.tight_layout ();
  
  
  # TODO: These features can be made flexible and controlled by parameters in future
  
  plot1_name = "plot_referrer_01.pdf";
  print ("\tSaving referrer analysis plot " + plot1_name);
  fig.savefig(plot1_name, dpi=100);
  
 
  # Save json file.
  json_file_name = "referrer_stats.json";
  print ("\tSaving referrer stats summary json" + json_file_name);
  referrer_stat.to_json (json_file_name);
  
  return (referrer_stat);


###
# params
#   data   : A Pandas dataframe.
#   
# return
#   -1     : Argument invalid
#   Success: Statistics about views
# 
# throws
#   ArgError
#   
# summary: Performs analysis with views data and generates plots, saves stats in a json file. 
#          Returns views stats data. This function will assume
#            [1] All missing data has been imputed using 'impute_missing' function (or by other means). 
#            [2] Date field should be shattered using 'shatter_date' function.
###
def analyse_stats_views (data):
    
    if data is None:
        raise ArgError ("Dataframe missing");
        return (-1);
      
    view_stats = pd.Series ();
    
    # Get the subplots for figure 1, (2x2)
    fig1, axes = plt.subplots (nrows=2,ncols=2);
    
    
    view_stats['total_days'] = data.shape[0];
    # TODO: Store the plot objects to var, and feed them to the plot, which is fed to the figure
    data.groupby(["yyyy"]).sum ().plot (kind="bar", alpha=0.75, ax=axes[0,0]); # Views per year
    axes[0,0].set_title  ("Total visits per year");
    axes[0,0].set_xlabel ("Years");
    axes[0,0].set_ylabel ("Views");
    
    # Daily visits by year
    data.boxplot (column="views", by="yyyy", ax=axes[0,1]); 
    axes[0,1].set_title  ("Daily visits per year Boxplot");
    axes[0,1].set_xlabel ("Years");
    axes[0,1].set_ylabel ("Views");
    
    # Aggregated views per month of each year
    data.groupby(["mm"]).sum ().plot (kind="bar", alpha=0.75, ax=axes[1,0]);
    axes[1,0].set_title  ("Total monthly visits total over years");
    axes[1,0].set_xlabel ("Months");
    axes[1,0].set_ylabel ("Views");
    
    # Daily visits by month
    data.boxplot (column="views", by="mm", ax=axes[1,1]);
    axes[1,1].set_title  ("Daily visits by months over the years");
    axes[1,1].set_xlabel ("Months");
    axes[1,1].set_ylabel ("Views");
    
    # Subplot container outerplot title and adjustments to avoid overlap.
    st1 = fig1.suptitle ("Daily stats over Years and Months", fontsize = "large");
    st1.set_y (0.99);
    
    # Setting image size to be saved. 16:9 ratio maintained.
    fig1.set_size_inches (17.7,10);
    fig1.tight_layout ();

    fig2, axes = plt.subplots (nrows=2, ncols=2);
    
    # All months monthly visits
    data.groupby(["yyyy", "mm"]).sum().reset_index().plot (kind="line", ax=axes[0,0]);
    axes[0,0].set_title ("Monthly visit trend over the years");
    axes[0,0].set_xlabel ("Months");
    axes[0,0].set_ylabel ("Views");
    
    # Aggregated monthly visits throughout the months of the year
    data.groupby(["yyyy", "mm"]).sum().reset_index().boxplot (column="views", by="yyyy", ax=axes[0,1]); 
    axes[0,1].set_title ("Monthly visits over the years");
    axes[0,1].set_xlabel ("Years");
    axes[0,1].set_ylabel ("Views");
    
    # Stacked plots
    # First extract the unique years, and make an empty index labeled by the month numbers.
    # Next for each year, filter out the months and the visits.
    # Then reset the index of the above extrated frame to the month and assign the views to
    #     a new column with the current year "yy" as a column label. Reseting the index to
    #     the month column matches up the months across years. This solves the problem when some month
    #     is missing. This can happen like, for example the visit information starts from, say, July
    #     then the filtered out dataframe will contain views from July only.
    dft = data.groupby(["yyyy", "mm"]).sum().reset_index();
    years = dft["yyyy"].unique ();
    tmp_df = pd.DataFrame(index=["01","02","03","04","05","06","07","08","09","10","11","12"]);
    for yy in years:
      tmp_yy = dft[dft["yyyy"]==yy];
      tmp_df[yy] = tmp_yy.set_index ("mm")["views"];
    
    # This data frame has year-wise columns containing the views for its months.
    # This data frame is now used to create a stacked lineplot easily.
    tmp_df.plot(kind="area", stacked=True, ax=axes[1,0], alpha=0.5);
    axes[1,0].set_title  ("Monthly visits stacked by year");
    axes[1,0].set_xlabel ("Months");
    axes[1,0].set_ylabel ("Relative visits");
    #print(tmp_df);
    #tmpdf[tmpdf["yyyy"]=="2010"].plot(stacked=True, ax=axes[1,0]);
    #tmpdf[tmpdf["yyyy"]=="2011"].plot(stacked=True, ax=axes[1,0]);
    

    # Aggregated per month visits throughout the year
    data.groupby(["yyyy", "mm"]).sum().reset_index().boxplot (column="views", by="mm", ax=axes[1,1]);
    axes[1,1].set_title ("Yearly visit variations throughout the months");
    axes[1,1].set_xlabel ("Months");
    axes[1,1].set_ylabel ("Views");
    
    # Subplot container outerplot title and adjustments to avoid overlap.
    st2 = fig2.suptitle ("Monthly Stats over Years", fontsize="large");
    st2.set_y (0.99);
    
    # Setting image size to be saved. 16:9 ratio maintained.
    fig2.set_size_inches (17.7,10);
    fig2.tight_layout ();
    
    
    # Fill in the stats.
    
    # Total views overall, mean and median
    view_stats['total_visits']        = sum (data["views"]);
    view_stats['total_mean_visits']   = data["views"].mean ();
    view_stats['total_median_visits'] = data["views"].median();
    
    # Overall daily max visits and the date
    tmp_didx = data.set_index(["yyyy", "mm", "dd"]).idxmax();
    view_stats['day_max_hit']      = {'yyyy'  : tmp_didx[0][0],
                                      'mm'    : tmp_didx[0][1],
                                      'dd'    : tmp_didx[0][2],
                                      'views' : data.set_index(["yyyy","mm", "dd"]).max()['views']
                                     };
    
    # Overall daily min visits and the date
    tmp_didx = data.set_index(["yyyy", "mm", "dd"]).idxmin();
    view_stats['day_min_hit']      = {'yyyy'  : tmp_didx[0][0],
                                      'mm'    : tmp_didx[0][1],
                                      'dd'    : tmp_didx[0][2],
                                      'views' : data.set_index(["yyyy","mm", "dd"]).min()['views']
                                     };
    
    # Overall monthly max views and the year and month which had the max monthly visits
    tmp_didx = data.groupby(["yyyy", "mm"]).sum().idxmax();
    view_stats['month_max_hit']    = {'yyyy'  : tmp_didx[0][0],
                                      'mm'    : tmp_didx[0][1],
                                      'views' : data.groupby(["yyyy","mm"]).sum().max()['views']
                                     };
    
    # Overall monthly min views and the year and month which had the min monthly visits
    tmp_didx = data.groupby(["yyyy", "mm"]).sum().idxmin();
    view_stats['month_min_hit']    = {'yyyy'  : tmp_didx[0][0],
                                      'mm'    : tmp_didx[0][1],
                                      'views' : data.groupby(["yyyy", "mm"]).sum().min()['views']
                                     };

    
    # Yearwise monthly max visits
    #view_stats['max_month_per_year_idx'] = data.groupby(["yyyy","mm"]).sum().reset_index().groupby(["yyyy"]).idxmax();
    #view_stats['max_month_per_year_val'] = data.groupby(["yyyy","mm"]).sum().reset_index().groupby(["yyyy"]).max();
    
    # Yearwise monthly min visits
    #view_stats['min_month_per_year_idx'] = data.groupby(["yyyy","mm"]).sum().reset_index().groupby(["yyyy"]).idxmin();
    #view_stats['min_month_per_year_val'] = data.groupby(["yyyy","mm"]).sum().reset_index().groupby(["yyyy"]).min();
    
    month_min_by_year = data.groupby(["yyyy","mm"]).sum().reset_index().groupby(["yyyy"]).min();
    month_min_by_year.columns = ["mm", "min_views"];
    #month_min_by_year.rename ("Minimum visits months per year");
                                            
    month_max_by_year = data.groupby(["yyyy","mm"]).sum().reset_index().groupby(["yyyy"]).max();
    month_max_by_year.columns = ["mm", "max_views"];
    #month_min_by_year.rename ("maximum visits months per year");
    
    view_stats['month_minmax_by_year'] = {'min': month_min_by_year,
                                          'max': month_max_by_year
                                         };
    
    
    # DEBUG lines
    #plt.show ();
    #print ("total_visits           = " + str (view_stats['total_visits']));
    #print ("day_max_hit_id         = " + str (view_stats['day_max_hit_id']));
    #print ("day_max_hit_val        = " + str (view_stats['day_max_hit_val']));
    #print ("day_min_hit_id         = " + str (view_stats['day_min_hit_id']));
    #print ("day_min_hit_val        = " + str (view_stats['day_min_hit_val']));
    #print ("month_max_hit_id       = " + str (view_stats['month_max_hit_id']));
    #print ("month_max_hit_val      = " + str (view_stats['month_max_hit_val']));
    #print ("month_min_hit_id       = " + str (view_stats['month_min_hit_id']));
    #print ("month_min_hit_val      = " + str (view_stats['month_min_hit_val']));
    #print ("max_month_per_year_idx = " + str (view_stats['max_month_per_year_idx']));
    #print ("max_month_per_year_val = " + str (view_stats['max_month_per_year_val']));
    #print ("min_month_per_year_idx = " + str (view_stats['min_month_per_year_idx']));
    #print ("min_month_per_year_val = " + str (view_stats['min_month_per_year_val']));
  
  
    # TODO: These features can be made flexible and controlled by parameters in future
    # Save the plots in pdf files.
    plot1_name = "plot_views_01.pdf";
    plot2_name = "plot_views_02.pdf";
    
    print ("\tSaving view analysis plot " + plot1_name);
    fig1.savefig(plot1_name, dpi=100);
    print ("\tSaving view analysis plot " + plot2_name);
    fig2.savefig(plot2_name, dpi=100);
    
    # Save json file.
    json_file_name = "view_stats.json";
    print ("\tSaving view stats summary json " + json_file_name);
    view_stats.to_json (json_file_name);
    
    # Return stats structure for some other function to use and print.
    return (view_stats);
  
  


###
# params
#   my_api     : API Key
#   my_blog    : Blog URL
#   fetch_data : True, if to fetch data from the web API. 
#                False, if we don't want to fetch from the web API and try to use the local copy.
#   
# return
#   -1     : Argument invalid
#   Success: Returns True
# 
# throws
#   ArgError
#   
# summary: This function will download the data from the web API and save in csv using the  
#          functions written above. Also, this function is responsible to initialize global
#          variables and other structures which will be needed throughout the lifetime of
#          the script. (Right now it does not do much).
###
def initialize (my_api, my_blog, fetch_data = False):
  
  if (my_api is None) or (my_blog is None):
    raise ArgError ("An API key and a blog URL is mandatory");
    return (-1);
 
  table_list = ["views", "postviews", "referrers", "searchterms", "clicks"];
  post_id    = None;
  end        = None;
  days       = -1;
  period     = None;
  limit      = -1;
  summarize  = None;
  form       = "csv";


  req_url    = None;
  fileprefix = "stats_";

  if fetch_data is True:
    print ("\tDownloading data from web API. Overwriting local (if any)");
    try:
      wp_api_args = {
                      "api_key"     : my_api,
                      "blog_id_uri" : my_blog,
                      "table"       : None,
                      "post_id"     : post_id,
                      "end"         : end,
                      "days"        : days,
                      "period"      : period,
                      "limit"       : limit,
                      "summarize"   : summarize,
                      "form"        : form
                    };
      
      feedback_str = "";
      for table in table_list:
        feedback_str = "Fetching " + table + " stats";
        wp_api_args["table"] = table;
        sys.stdout.write (feedback_str),
        sys.stdout.flush ();
        retval = wp_stats_fetch (wp_api_args, fileprefix + table);
        
        if retval == 0:
          #feedback_str += " [SUCCESS]";
          print (" [SUCCESS]");
        else:
          #feedback_str += " [FAILED]";
          print (" [FAILED]");
          
        sys.stdout.flush ();
        
        #print (feedback_str);
        

    except Exception as e:
      print ("Exception: " + str (e));
      
  else:
    print ("\tNot fetching data from web API. Using local");
      
  return (True);



###
# params
#   data    : View stats structure
#   
# return
#   -1      : Argument invalid
#   Success : True
# throws
#   ArgError
#   
# summary: Prints the stats in a pretty format using human redable natural language.
###
# TODO: Make a class for stats, so we can distinguish between different stat types.
def print_view_stats_to_text (stats):
  
  if stats is None:
        raise ArgError ("Statistics in argument missing. Cannot pretty print.");
        return (-1);
  
  print ("[------ VISIT STATS ------]");
  # WARNING: Lazy days to year convert. Fix later.
  years = math.floor (stats['total_days'] / 365);
  rem_days = stats['total_days'] % 365
  mm       = math.floor (rem_days/ 30);
  rem_days = rem_days % 30;
  dd    = rem_days;
  
  print ("[*] The blog had overall %d views in %d years,  %d months, %d days" % (stats['total_visits'], years, mm, dd));
  print ("[*] Overall mean and median visits throughout the entire period was %d and %d respectively" % (stats['total_mean_visits'], stats['total_median_visits']));
  print ("[*] The overall busiest %s.%s.%s which had %d views" % (stats['day_max_hit']['dd'], stats['day_max_hit']['mm'], stats['day_max_hit']['yyyy'], stats['day_max_hit']['views']));
  print ("[*] The overall saddest day was on %s.%s.%s which had %d views" % (stats['day_min_hit']['dd'], stats['day_min_hit']['mm'], stats['day_min_hit']['yyyy'], stats['day_min_hit']['views']));
  print ("[*] The month of %s of the year %s was the busiest with total monthly views of %d" % (code_to_month[stats['month_max_hit']['mm']], stats['month_max_hit']['yyyy'], stats['month_max_hit']['views']));
  print ("[*] The month of %s of the year %s had the lowest monthly visits of total monthly views of %d" % (code_to_month[stats['month_min_hit']['mm']], stats['month_min_hit']['yyyy'], stats['month_min_hit']['views']));
  
  print ("[*] The below table shows a yearwise minimum monthly visits");
  print (str(stats['month_minmax_by_year']['min']));
  
  print ("[*] The below table shows a yearwise maximum monthly visits");
  print (str(stats['month_minmax_by_year']['max']));
  
  print ("------ ------ ------");
  
  return (True);



###
# params
#   data    : Click stats structure
#   
# return
#   -1      : Argument invalid
#   Success : True
# throws
#   ArgError
#   
# summary: Prints the stats in a pretty format using human redable natural language.
###
def print_click_stats_to_text (stats):
  
  if stats is None:
        raise ArgError ("Statistics in argument missing. Cannot pretty print.");
        return (-1);
      
  top_site_count = 10;
  print ("[------ CLICK STATS ------]");
  print ("[*] Overall, a total of %d links were clicked, with pointed to %d unique websites" % (stats['total_clicks'], stats['unique_sites']));
  print ("[*] The below table shows the top %d unique links and the number of times they were clicked" % (top_site_count));
  print (str(stats['click_table'].iloc[0:top_site_count]));
  
  print ("------ ------ ------");
  
  return (True);
  



###
# params
#   data    : Referrers stats structure
#   
# return
#   -1      : Argument invalid
#   Success : True
# throws
#   ArgError
#   
# summary: Prints the stats in a pretty format using human redable natural language.
###
def print_referrer_stats_to_text (stats):
  
  if stats is None:
        raise ArgError ("Statistics in argument missing. Cannot pretty print.");
        return (-1);
  
  # TODO: Referrer percentage of total views
  top_referrer_count = 10;
  print ("[------ REFERRER STATS ------]");
  print ("[*] Overall, a total of %d referrers brought traffic to the blog, with a sum of %d unique referrers" % (stats['total_referrer'], stats['unique_referrer']));
  print ("[*] The below table shows the top %d unique links and the number of times they were clicked" % (top_referrer_count));
  print (str(stats['referrer_table'].iloc[0:top_referrer_count]));
   
  print ("------ ------ ------");

  return (True);

######################
### MAIN PROGRAM #####
######################


#TODO: Add commandline arguments for [1] blogname, [2] apikey, [3] reload data or not (default is don't load) [4] Plot on screen or not. If nothing is given, assume defaults
#COMMENT CODE and function.

# Defaults
my_api          = None;
my_blog         = None;
plot_show_flag  = True;
fetch_data_flag = True;
datafile_path = "./";

view_stats      = None;
click_stats     = None;
referrer_stats  = None;


# Parse arguments.
parser = argparse.ArgumentParser ();
parser.add_argument ("--id", help="API Key");
parser.add_argument ("--blog", help="Blog URL");
parser.add_argument ("--noget", help="Download from web. If not set, use local", action="store_false");
parser.add_argument ("--noplot", help="Plot on screen", action="store_false");
parser.add_argument ("--datapath", help="Path of the datafiles");
args = parser.parse_args ();

if ((args.id is not None) and (args.blog is None) or
    (args.id is None)     and (args.blog is not None)):
  print ("Both the \"--id\" and \"--blog\" needs to be given");
  sys.exit (0);
  
if args.id is not None:
  my_api = args.id;
  
if args.blog is not None:
  my_blog = args.blog;

fetch_data_flag = args.noget;
plot_show_flag  = args.noplot;

if args.datapath is not None:
  datafile_path = args.datapath;

init_status = True;

try:
  print ("[Initializing]");
  initialize (my_api, my_blog, fetch_data = fetch_data_flag);
  
except Exception as e:
  init_status = False;
  print (e);
  
if (init_status == True):
  try:
    print ("[Analysing Views Stats]");
    view_stats = analyse_stats ("views", datafile_path + "stats_views.csv");
    
  except Exception as e:
    print (e);
    
  try:
    print ("[Analysing Click Stats]");
    click_stats = analyse_stats ("clicks", datafile_path + "stats_clicks.csv");
    
  except Exception as e:
    print (e);
    
  try:
    print ("[Analysing Referrers Stats]");
    referrer_stats = analyse_stats ("referrers", datafile_path + "stats_referrers.csv");
    
  except Exception as e:
    print (e);

  print ("\n\n[INFO: Check the saved plots and the json files in the current directory]");


  print ("\n\n\n\n[Printing pretty statistics of blog \"%s\"]" % (my_blog));
  try:
    print_view_stats_to_text (view_stats);
    
  except Exception as e:
    print (e);

  try:
    print_click_stats_to_text (click_stats);
    
  except Exception as e:
    print (e);
    
  try:
    print_referrer_stats_to_text (referrer_stats);

  except Exception as e:
    print (e);


  # Display the plots
  if plot_show_flag is True:
    print ("\n\n[Plotting on screen]");
    plt.show ();

