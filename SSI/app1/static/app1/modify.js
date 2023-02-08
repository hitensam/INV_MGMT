var itemName = document.getElementsByClassName('itemName'); //ele1 name changed
var getitemName = document.getElementsByClassName('getitemName'); //ele1 name changed
var rollNo = document.getElementsByClassName('rollNo');
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

for (var i = 0; i < sno.length; i++ ) { //ele1 -->sno (no issues) both
    
    // setting value for the given name.
    if(getitemName[i] &&  itemName[i]){
    itemName[i].value = [getitemName[i].textContent.trim(), rollNo[i].textContent.trim(), widthSame[i].textContent.trim()]
    // itemName[i].checked = true 
    }

    // also adding Sno.
    sno[i].textContent = i+1;

    // if(document.getElementsByClassName('shortNarration'))
    // {
    //     document.getElementsByClassName('shortNarration')[i].placeholder = [getitemName[i].textContent.trim(), rollNo[i].textContent.trim(), document.getElementsByClassName('width')[i].textContent.trim()]
    //     console.log( document.getElementsByClassName('shortNarration')[i].pla)
    // }
    

    if(net.length>0 && net[i].textContent)
    {
    let netWt= parseFloat(net[i].textContent)
    let Gross= parseFloat(gross[i].textContent)

    netWeight = netWeight+netWt;
    grossWeight = grossWeight+Gross;
    }

}

if (document.getElementsByClassName('netWt')[0])
{
     // setting the total net weight
     netWeight = netWeight.toFixed(2)
     grossWeight = grossWeight.toFixed(2)
     // console.log('TOTAL NET WEIGHT : ', netWeight)
     // console.log('TOTAL GROSS WEIGHT : ', grossWeight)
 
     var netWt = document.getElementsByClassName('netWt')[0]
     var Gross = document.getElementsByClassName('Gross')[0]
 
     netWt.textContent = netWeight
     Gross.textContent = grossWeight 
}
   

var netWeight=0;
var grossWeight =0;
var netWsell = 0;
var netGsell = 0;

if (widthSame[0])
{


var temp=parseFloat(widthSame[0].textContent.trim())
for (var i = 0; i < sno.length; i++ )
 {
    if (temp === parseFloat(widthSame[i].textContent.trim()))
    {addsellStatus();}
    

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
        netWeight=0;
        grossWeight =0;
        netWsell = 0;
        netGsell = 0;
        temp = parseFloat(widthSame[i].textContent.trim());
        addsellStatus();
        let netWt= parseFloat(net[i].textContent.trim())
        let Gross= parseFloat(gross[i].textContent.trim())
    
        netWeight = netWeight+netWt;
        grossWeight = grossWeight+Gross;
    }
}
if(document.getElementsByClassName('contentSetting')[0])
{
    let row = document.createElement('tr')
row.innerHTML = `<td colspan="4" style="text-align: center;">Total SOLD ${temp} : </td>
        <td style="text-align: center;">${netWeight.toFixed(2)}</td>
        <td style="text-align: center;">${grossWeight.toFixed(2)}</td>
        `
document.getElementsByClassName('addElement')[0].insertBefore(row, document.getElementsByClassName('total')[0])    
}
else
{
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
}









function hideShow()
{
  x = document.getElementsByClassName('sellStatus')
  y = document.getElementById('soldRemove')
    for (var i = 0; i < sno.length; i++ )
    {
        if (x[i].style.display === "none") 
        {
            x[i].style.display = "block";
            y.style.display = "block";
        } 
        else 
        {
        x[i].style.display = "none";
        y.style.display = "none";
        }
    }
}



function addsellStatus()
{
    if (temp === parseFloat(widthSame[i].textContent.trim()))
    {
    
    // if(net.length>0){
        let netWt= parseFloat(net[i].textContent.trim())
        let Gross= parseFloat(gross[i].textContent.trim())

            if(document.getElementsByClassName('contentSetting')[0])
            {
                netWeight = netWeight+netWt;
                grossWeight = grossWeight+Gross;

            }
            else
            {
                if (parseInt(sellStatus[i].textContent.trim()) === 0)
                {;
                    netWeight = netWeight+netWt;
                    grossWeight = grossWeight+Gross;

                }
                else if(parseInt(sellStatus[i].textContent.trim()) !== 0)
                {
                    document.getElementsByClassName('insertBefore')[i].style="color:yellow";
                    document.getElementsByClassName('insertBefore')[i].style.backgroundColor = "red";
                    itemName[i].disabled = true;
                    netWsell = netWsell + netWt;
                    netGsell = netGsell + Gross;
                }
        // }
        
            }
    }
}



if(document.getElementById('autocomplete'))
{
    new Autocomplete('#autocomplete', {
        search : input=>
        {
          console.log(input)
          const url = `/search/?general=${input}`
          return new Promise(resolve =>
          {
            fetch(url)
            .then(response =>response.json())
            .then(data =>
            {
              console.log(data)
              
              const unique = (value, index, self) => {
              return self.indexOf(value) === index
              }
              data.data = data.data.filter(unique)
              resolve(data.data)
            }
            )
          })
        },
          onSubmit : result =>
          {
            console.log(result)
          }
          
      })
}


function makeChanges(element)
{
    // element.setAttribute('name', 'shortNarrations')
    // element.setAttribute('value', `${element.value}`)
    // element.value = [element.textContent, `${element.value}`]
    // element.innerHTML = `name = "shortNarrations" value="${element.textContent}"`
    alert(element.value)
}