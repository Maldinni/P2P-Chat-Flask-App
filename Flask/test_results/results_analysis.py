import pandas as pd
import matplotlib.pyplot as plt
import os

#This line creates a variable that receives the right directory, returning to the parent directory and searching for the file named 'test_results'
CSV_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'test_results'))

#Creates the directory 'graphs', in case that it doesn't exists
graphs_directory = os.path.join(os.path.dirname(__file__), 'graphs')
os.makedirs(graphs_directory, exist_ok=True)

#Defined list to armazenate the data of all CSV files
execution_times = [] #Stores execution times of all tests.
test_names = [] #Stores the names of all tests.

#Function to read CSV and process data from CSV
def process_csv(csv_file):
    #Load the CSV file into a Pandas Dataframe
    df = pd.read_csv(csv_file)

    #Prints on console to verify if the code is running
    print(f"Processing file: {csv_file}")
    print(df.head())

    #Casting the execution time to numeric
    df['Execution Time (seconds)'] = pd.to_numeric(df['Execution Time (seconds)'], errors='coerce')

    #Loop to save data for the graphs
    for test_name, execution_time, status in zip(df['Test Name'], df['Execution Time (seconds)'], df['Status']):
        execution_times.append(execution_time)
        test_names.append(test_name)

    df['csv_file_names'] = os.path.basename(csv_file)

    return df

#Process all CSV files in the directory with a loop, simple logic that read the files in the root as a list and if it's a '.csv' takes the file path, process the data with the function and saves at the array 'all_dataframes'
all_dataframes = []
for csv_file in os.listdir(CSV_DIRECTORY):
    if csv_file.endswith('.csv'):
        full_csv_path = os.path.join(CSV_DIRECTORY, csv_file)
        df = process_csv(full_csv_path)
        all_dataframes.append(df)

#That variables takes all dataframes and concatenates them into a single one
all_data = pd.concat(all_dataframes, ignore_index=True)

best_execution_time_csv = all_data.groupby('Test Name')['Execution Time (seconds)'].min().idxmin()#The code was supposed to save the file name of the CSV with best results(shortest execution) but this functionality isn't working for now and it will be refactored in the future

#Comparative graph with all execution times of the tests of all CSV
plt.figure(figsize=(12, 6))
plt.scatter(test_names, execution_times, color='blue', label='Execution Time')
plt.xlabel('Test Name')
plt.ylabel('Execution Time (seconds)')
plt.title('Comparative Execution Time for All Tests')

plt.text(0.5, max(execution_times), f"Best file: {best_execution_time_csv}", horizontalalignment='center', fontsize=12, color='red')#Same problem, isn't working

plt.xticks(rotation=90)
plt.tight_layout()

#Saves the final result in 'graphs'
execution_time_graph_path = os.path.join(graphs_directory, 'comparative_execution_time.png')
plt.savefig(execution_time_graph_path)

#Display the graph
plt.show()
