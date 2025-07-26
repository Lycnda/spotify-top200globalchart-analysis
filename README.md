# spotify-top200globalchart-analysis

There are folders with the weekly spotify data for the Global, South Africa, South Korea, India, Nigeria, Great Britain and Australia Top 200 Weekly Charts from the start of each chart to the most recent week. 

There are Notebooks for Clustering, Data Analysis and PowerBI Data Visualisations of the Top 200 weekly Chart data contained herein. There are updated csv files which contain a List of Girl Groups, a List of Boy Groups and a List of Mixed Groups files. 

How to Run:
1. Run the python script named ChartsAnalysisALL.py which is in the folder main folder
2. It will run all 7 locales "kr", "za", "global", "gb", "ng", "au", "in" which can be selected/de-selected in the configs/chartsanalysisparams.yml file
3. The resulting output csv files are named all_files_krv1, all_files_zav1, all_files_globalv1, all_files_gbv1, all_files_NGv1, all_files_auv1, and all_files_inv1 are in the Classification folder.
4. The output has 26 columns namely, trackAppearanceCount, artistAppearanceCount,	artist_names,	track_name,	rank,	uri,	source,	peak_rank,	previous_rank,	weeks_on_chart,	streams,	End Date,	Week,	Year,	End Date Dt,	Seconds since Epoch,	End Date Aggregated,	ArtistCount,	main_artist,	isTopTen,	Artist and Track,	rank, difference,	Position over Time,	IsGirlGroup,	IsBoyGroup,	IsMixedGroup.

