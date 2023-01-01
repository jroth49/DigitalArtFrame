import os;


lFiles = os.listdir('art/Landscape');
lPath = '/home/jack/Documents/Art/art/Landscape/';
lRoll = [];

for l in lFiles:
	lRoll.append(lPath + l);


javascript = ''' var roll = ''' + str(lRoll) + '''


function displayInfo() {
	var img = document.getElementById('picture').src.split('/')[9];
	
	var pName = img.split('_')[0].replaceAll('-', ' ');
	var aName = img.split('_')[1].replaceAll('-', ' ') + ' - ' + img.split('_')[2].replaceAll('-', ' ');
	var price = img.split('_')[3].replaceAll('-', ' ');
	let dollarUS = Intl.NumberFormat('en-US');
	price = dollarUS.format(parseFloat(price));
	
	var p = document.getElementById('info').innerHTML = pName + ' - ' + aName + ' - $' + price;
	switchImage();
}

async function switchImage() {
	//check if roll is empty
	if(roll.length != 0) {
		console.log(roll[roll.length - 1]);
		await new Promise(resolve => setTimeout(resolve, 1800000));
		document.getElementById('picture').src = randomImage(roll);
	} else {
		console.log("Show's Over");
	}
}

function randomImage(array) {
	
  let curId = array.length;
  
  while (0 !== curId) {
    let randId = Math.floor(Math.random() * curId);
    curId -= 1;
    
    let tmp = array[curId];
    array[curId] = array[randId];
    array[randId] = tmp;
  }
  return array.pop();
}

'''

with open('script.js', 'w') as script:
	script.write(javascript);
	script.close();



