# orto
Simple class for interfacing with i-DE (Iberdrola) power measurement equipment. This work is inspired on code from other people.

If you are interested in reading the power consumption of your electrical installation and you have i-DE (Iberdrola) as the distributor of the energy, you can use this in order to integrate into your own software the necessary calls.

Here are the available funcionalities:

- login(self, user, password): Creates session with your credentials. You will need a valid username and password from i-DE.
- watthourmeter: Returns your current power consumption in watt-hour.
- ipstatus: Returns the status of your ICP (the switch).
- contracts: getting the available contracts for your profile.
- contractselect: select one contract between the available for your profile.
- contract: get the details of the selected contract.
- getCsv: get in csv format the power measurements in a hourly basis for the specified day.
- getDailyData: get in JSON format the power measurements for the specified dat.
- getPowerDateLimits: returns the maximum and minimum dates of the interval with available data for query.
- getMaxPower: get the max power consumption from the period.
