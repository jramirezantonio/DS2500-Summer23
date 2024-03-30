"""
running_log.py: A running logger for runners
DS2501: Lab for Intermediate Programming with Data
Josue Antonio 6/6/23
running_log.py
"""

import matplotlib.pyplot as plt

class RunningLog:

    def __init__(self, *runs):
        """ The running log constructor
            runs will be a list of (run_number, hms, dist_km) tuples
        """
        self.runs = list(runs)

    def add_run(self, hms, dist_km):
        """ Record a run.  The time is given as 'hh:mm:ss' and the distance is in kilometers """
        self.runs.append((self.num_runs() + 1, hms, dist_km))

    def num_runs(self):
        """ How many run records are in the database? """
        return len(self.runs)

    def plot(self):
        """ Generate a line plot showing the average pace (minutes per kilometer) for
        run1, run2, .... run N. The x-axis is the run number, and the y-axis is the average
        pace for that run. """
        avg_paces = []
        runs = [i for i in range(1, self.num_runs() + 1)]
        for run in self.runs:
            minutes = run[1].split(":")
            minutes = (float(minutes[0]) * 60) + float(minutes[1]) + (float(minutes[2]) / 60)
            avg_pace = minutes / float(run[2])
            avg_paces.append(avg_pace)

        plt.figure(dpi=200)
        plt.plot(runs, avg_paces, color='navy', linestyle='dashed')
        plt.title("Average Paces for all Runs", color='navy')

        # Hide top and right axes
        plt.gca().spines[['top', 'right']].set_visible(False)
        plt.xticks(runs, color='navy')
        plt.yticks(color='navy')
        plt.xlabel("Run", color='navy')
        plt.ylabel("Average Pace", color='navy')
        plt.show()

    def save(self, filename):
        """ OPTIONAL: Save the data to a file. """
        # Wrote this code with help from ChatGPT

        # Open the file in write mode
        file = open(filename, "w")

        # Iterate over the runs list and write each run to a new line in the file
        for run in self.runs:
            file.write(str(run) + "\n")

        # Close the file
        file.close()

    def load(self, filename):
        """ OPTIONAL: Load the data from a file """
        my_runs = []
        with open(filename, "r") as infile:
            for line in infile:
                my_runs.append(line.strip())
        return my_runs

def main():

    # Instantiate a new running log
    logger = RunningLog()

    # This is optional
    my_runs = logger.load("running_log_testdata.txt")
    # print(my_runs)

    # Here are 10 sample running events
    logger.add_run("00:32:14", 5.1)
    logger.add_run("00:34:59", 5.5)
    logger.add_run("00:29:01", 4.9)
    logger.add_run("00:30:00", 5.0)
    logger.add_run("00:15:25", 3)
    logger.add_run("00:50:02", 7.2)
    logger.add_run("00:43:35", 5.0)
    logger.add_run("01:00:00", 9)
    logger.add_run("02:30:00", 20)
    logger.add_run("01:10:30", 10)

    # Output some data
    print(f"There are {logger.num_runs()} runs in the database")
    logger.plot()

    # This is also optional
    logger.save("running.log")


if __name__ == '__main__':
    main()

