var ele1 = document.getElementsByClassName('count');
var sno = document.getElementsByClassName('sno');
var net = document.getElementsByClassName('net');
var gross = document.getElementsByClassName('gross');
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