# IndexRangePredictor

This project is devlop to calculate range of below indices using stats of maththematics 

## Index 

1. Nifty 50
2. Bank Nifty
3. Sensex
4. Bankex
5. Nifty Financial Services


## Data prerequisite 

It need data in below format to calculate range 

Data Timeframe : Daily, Monthly, Yearly
Columns required :  Date, Open, High, Low, Close


## Results 

It Will calculate ranges given below 

<table>
<td>PredictType</td> <td>Quartile-90</td>  <td>ConfidenceInterval-80</td> <td> ConfidenceInterval-95</td>  <td>ConfidenceInterval-99</td>
 <tr><td>OPEN-HIGH_DAY </td>    <td> 646.217</td>             <td>340.214889</td>             <td>520.954049 </td>           <td> 684.682464</td></tr>
 <tr><td> OPEN-LOW_DAY   </td>    <td>   645.412    </td>    <td>         359.668473    </td>    <td>         550.742349    </td>    <td>         723.832802</td></tr>
<tr><td>CLOSE-HIGH_DAY   </td>    <td>   639.476    </td>    <td>         334.015215    </td>    <td>         511.460798   </td>    <td>          672.205621</td></tr>
 <tr><td>CLOSE-LOW_DAY   </td>    <td>   637.442    </td>    <td>         338.703979    </td>    <td>         518.640467   </td>    <td>          681.641757</td></tr>
 <tr><td> HIGH-LOW_DAY    </td>    <td> 1020.808     </td>    <td>        394.723658   </td>    <td>          604.420601   </td>    <td>          794.381361</td></tr>
<tr><td>OPEN-CLOSE_DAY   </td>    <td>   647.277     </td>    <td>        338.655725    </td>    <td>         518.566580   </td>    <td>          681.544647</td></tr>
</table>
