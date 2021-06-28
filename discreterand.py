from decimal import Decimal as dml
from matplotlib import pyplot as plt
import tkinter as tk
import pyperclip as pyc

class App(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.inputFrame = tk.Frame(master=master)

        # Labels
        npl = self.newPropertyLabel
        self.titleLabel = npl("Chart title:", frame=self.inputFrame)
        self.xAxisLabel = npl("X axis title:", frame=self.inputFrame)
        self.yAxisLabel = npl("Y axis title:", frame=self.inputFrame)
        self.xValuesLabel = npl("X values:", frame=self.inputFrame)
        self.yValuesLabel = npl("Y values:", frame=self.inputFrame)

        # Entries
        self.titleEntry = tk.Entry(master=self.inputFrame)
        self.xAxisEntry = tk.Entry(master=self.inputFrame)
        self.yAxisEntry = tk.Entry(master=self.inputFrame)
        self.xValuesEntry = tk.Entry(master=self.inputFrame)
        self.yValuesEntry = tk.Entry(master=self.inputFrame)

        # Buttons
        ncb = self.newClearButton
        self.clearTitleButton = ncb(self.titleEntry, frame=self.inputFrame)
        self.clearXAxisButton = ncb(self.xAxisEntry, frame=self.inputFrame)
        self.clearYAxisButton = ncb(self.yAxisEntry, frame=self.inputFrame)
        self.clearXValuesButton = ncb(self.xValuesEntry, frame=self.inputFrame)
        self.clearYValuesButton = ncb(self.yValuesEntry, frame=self.inputFrame)

        self.submitButton = tk.Button(
            master=self.master,
            text="Calculate data",
            width=18,
            height=2,
            command=lambda:self.showCalculations(
                self.titleEntry.get(),
                self.xAxisEntry.get(),
                self.yAxisEntry.get(),
                list(map(dml, "".join([i for i in str(self.xValuesEntry.get()) if i != " "]).split(","))),
                list(map(dml, "".join([i for i in str(self.yValuesEntry.get()) if i != " "]).split(",")))
            ))

        # Grid formation
        grid = [
            [self.titleLabel, self.titleEntry, self.clearTitleButton],
            [self.xAxisLabel, self.xAxisEntry, self.clearXAxisButton],
            [self.yAxisLabel, self.yAxisEntry, self.clearYAxisButton],
            [self.xValuesLabel, self.xValuesEntry, self.clearXValuesButton],
            [self.yValuesLabel, self.yValuesEntry, self.clearYValuesButton]
        ]

        for i in range(len(grid)):
            for j, e in enumerate(grid[i]):
                e.grid(row=i, column=j, padx=4, pady=4)

        self.inputFrame.pack()
        self.submitButton.pack(padx=4, pady=4)
        

    def constructGraph(self, title="", x_label="Values", y_label="Probabilities", x_values=[], y_values=[]):
        plt.bar(x_values, y_values)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.show()

    def getCalculations(self, x_values=[], y_values=[]):
        mean = dml(0)
        for v, p in zip(x_values, y_values): mean += dml(v)*dml(p)
        varx = dml(0)
        for v, p in zip(x_values, y_values): varx += dml((v-mean)*(v-mean)*p)
        stdev = varx**dml(0.5)
        return mean, varx, stdev

    def showCalculations(self, title, x_label="Values", y_label="Probabilities", x_values=[], y_values=[]):
        mean, varx, stdev = self.getCalculations(x_values, y_values)
        x_label, y_label = x_label.strip(" ") or "Values", y_label.strip(" ") or "Probabilities"
        meanCalc = "E(X) = " + " + ".join([f"{v} × {p}" for v, p in zip(x_values, y_values)]) + f" = {round(mean, 4)}"
        varxCalc = "Var(X) = " + " + ".join([f"({v-mean})^2 × {p}" for v, p in zip(x_values, y_values)]) + f" = {round(varx, 4)}"
        stdevCalc = f"σ_X = √{round(varx, 4)} = {round(stdev, 4)}"
        print("Axes:")
        print(x_label, y_label)

        try:
            self.dataFrame.pack_forget()
            self.constructGraphButton.pack_forget()
        except:
            pass

        self.dataFrame = tk.Frame(master=self.master)

        npl = self.newPropertyLabel
        self.meanLabel = npl(f"Mean:\t\t{round(mean, 4)}", frame=self.dataFrame, anchor="w")
        self.meanLabel.pack(fill="both")

        self.varxLabel = npl(f"Variance:\t\t{round(varx, 4)}", frame=self.dataFrame, anchor="w")
        self.varxLabel.pack(fill="both")

        self.stdevLabel = npl(f"Standard Deviation:\t{round(stdev, 4)}", frame=self.dataFrame, anchor="w")
        self.stdevLabel.pack(fill="both")

        buttonFrame = tk.Frame(master=self.dataFrame)
        tk.Button(master=buttonFrame, text="Copy mean\ncalculation", width=18, height=3, command=lambda: pyc.copy(meanCalc)).grid(row=0, column=0, padx=4, pady=4)
        tk.Button(master=buttonFrame, text="Copy variance\ncalculation", width=18, height=3, command=lambda: pyc.copy(varxCalc)).grid(row=0, column=1, padx=4, pady=4)
        tk.Button(master=buttonFrame, text="Copy stdev\ncalculation", width=18, height=3, command=lambda: pyc.copy(stdevCalc)).grid(row=1, column=0, padx=4, pady=4)
        tk.Button(master=buttonFrame, text="Construct graph", width=18, height=3, command=lambda: self.constructGraph(title, x_label, y_label, x_values, y_values)).grid(row=1, column=1, padx=4, pady=4)

        buttonFrame.pack(fill="both")

        self.dataFrame.pack(padx=12, pady=(4, 8), fill="both")

        print("Finished showing calculations")

    def newPropertyLabel(self, text, width=None, height=None, frame=None, anchor=None):
        givenFrame = frame or self.master
        return tk.Label(master=givenFrame, text=text, width=width, height=height, anchor=anchor)

    def newClearButton(self, linkedEntry, width=8, height=1, frame=None):
        givenFrame = frame or self.master
        return tk.Button(master=givenFrame, text="Clear", width=width, height=height, command=lambda: linkedEntry.delete(0, "end"))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(master=root)
    app.mainloop()