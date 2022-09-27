var ele1 = document.getElementsByClassName('count');
var sno = document.getElementsByClassName('sno');
var net = document.getElementsByClassName('net');
var gross = document.getElementsByClassName('gross');
var widthSame = document.getElementsByClassName('width_same');
var sellStatus = document.getElementsByClassName('sellStatus');
// console.log('net : ', net)

var netWeight=0;
var grossWeight =0;
// console.log("length is : ", ele1.length)


function myFunction() {
    // alert(document.getElementById("myText").value)
    document.getElementById("spaceRemove").value = document.getElementById("spaceRemove").value.trim() ;      
  }

for (var i = 0; i < ele1.length; i++ ) {
    
    // also adding Sno.
    sno[i].textContent = i+1;
    if(net.length>0){
    let netWt= parseFloat(net[i].textContent)
    let Gross= parseFloat(gross[i].textContent)

    netWeight = netWeight+netWt;
    grossWeight = grossWeight+Gross;}
    // net[i].textContent.style.textAlign = 'center';
    // gross[i].textContent.style.textAlign = 'center';
}
if(net.length>0)
{
    netWeight = netWeight.toFixed(2)
    grossWeight = grossWeight.toFixed(2)
    console.log('TOTAL NET WEIGHT : ', netWeight)
    console.log('TOTAL GROSS WEIGHT : ', grossWeight)

    var netWt = document.getElementsByClassName('netWt')[0]
    var Gross = document.getElementsByClassName('Gross')[0]

    netWt.textContent = netWeight
    Gross.textContent = grossWeight
    // netWt.textContent.style.textAlign = 'center';
    // Gross.textContent.style.textAlign = 'center';
}

var netWeight=0;
var grossWeight =0;
var netWsell = 0;
var netGsell = 0;
var temp=parseFloat(widthSame[0].textContent)
for (var i = 0; i < ele1.length; i++ )
 {
    if (temp === parseFloat(widthSame[i].textContent)){
    
    if(net.length>0){
        let netWt= parseFloat(net[i].textContent)
        let Gross= parseFloat(gross[i].textContent)

        if(document.getElementsByClassName('contentSetting')[0])
        {
            netWeight = netWeight+netWt;
            grossWeight = grossWeight+Gross;

        }
        else{
        if (parseInt(sellStatus[i].textContent) === 0)
        {
            netWeight = netWeight+netWt;
        grossWeight = grossWeight+Gross;
        }
        else{
            // document.getElementsByClassName('insertBefore')[i].style.backgroundColor = "#FF3333"; 
            document.getElementsByClassName('insertBefore')[i].style="color:yellow";
            document.getElementsByClassName('insertBefore')[i].style.backgroundColor = "red"; 
            // console.log(document.getElementsByClassName('insertBefore')[i].innerHTML)
            netWsell = netWsell + netWt;
            netGsell = netGsell + Gross;
        }
    }
    
        }
    }

    else{
        if(document.getElementsByClassName('contentSetting')[0])
        {
            let row = document.createElement('tr')
        row.innerHTML = `<td colspan="4" style="text-align: center;">Total SOLD ${temp} : </td>
        <td style="text-align: center;">${netWeight.toFixed(2)}</td>
        <td style="text-align: center;">${grossWeight.toFixed(2)}</td>
        `
        document.getElementsByClassName('addElement')[0].insertBefore(row, document.getElementsByClassName('insertBefore')[i])
        }
        else{
        let row = document.createElement('tr')
        row.innerHTML = `<td colspan="4" style="text-align: center;">Total AVAILABLE ${temp} : </td>
        <td style="text-align: center;">${netWeight.toFixed(2)}</td>
        <td style="text-align: center;">${grossWeight.toFixed(2)}</td>
        `
        let row2 = document.createElement('tr');
        row2.innerHTML = `<td colspan="4" style="text-align: center;">Total Sold ${temp} : </td>
        <td style="text-align: center;">${netWsell.toFixed(2)}</td>
        <td style="text-align: center;">${netGsell.toFixed(2)}</td>
        `
        document.getElementsByClassName('addElement')[0].insertBefore(row2, document.getElementsByClassName('insertBefore')[i])
        document.getElementsByClassName('addElement')[0].insertBefore(row, document.getElementsByClassName('insertBefore')[i])
        }
        console.log(`${temp} : NETWEIGHT ${netWeight.toFixed(2)}`)
        netWeight=0;
        grossWeight =0;
        netWsell = 0;
        netGsell = 0;
        temp = parseFloat(widthSame[i].textContent)
        let netWt= parseFloat(net[i].textContent)
        let Gross= parseFloat(gross[i].textContent)
    
        netWeight = netWeight+netWt;
        grossWeight = grossWeight+Gross;

        
    }
}
if(document.getElementsByClassName('contentSetting')[0]){
    let row = document.createElement('tr')
row.innerHTML = `<td colspan="4" style="text-align: center;">Total SOLD ${temp} : </td>
        <td style="text-align: center;">${netWeight.toFixed(2)}</td>
        <td style="text-align: center;">${grossWeight.toFixed(2)}</td>
        `
document.getElementsByClassName('addElement')[0].insertBefore(row, document.getElementsByClassName('total')[0])
    
}
else{
let row = document.createElement('tr')
row.innerHTML = `<td colspan="4" style="text-align: center;">Total AVAILABLE ${temp} : </td>
        <td style="text-align: center;">${netWeight.toFixed(2)}</td>
        <td style="text-align: center;">${grossWeight.toFixed(2)}</td>
        `
let row2 = document.createElement('tr');
row2.innerHTML = `<td colspan="4" style="text-align: center;">Total Sold ${temp} : </td>
        <td style="text-align: center;">${netWsell.toFixed(2)}</td>
        <td style="text-align: center;">${netGsell.toFixed(2)}</td>
        `
document.getElementsByClassName('addElement')[0].insertBefore(row2, document.getElementsByClassName('total')[0])
document.getElementsByClassName('addElement')[0].insertBefore(row, document.getElementsByClassName('total')[0])
}